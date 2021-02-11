import logging
from collections import defaultdict
from copy import deepcopy
from dataclasses import asdict, dataclass
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple, Union

import requests
from bson import BSON
from Core.constants import DEFAULT_DATETIME_ISO
from Core.Dexter.Infrastructure.Domain.LevelEnums import LevelIdKeyEnum
from Core.Dexter.Infrastructure.Domain.Recommendations.RecommendationFields import (
    RecommendationField,
)
from Core.mongo_adapter import MongoOperator, MongoRepositoryStatus
from Core.Web.FacebookGraphAPI.GraphAPIDomain.FacebookMiscFields import (
    FacebookGender,
    FacebookMiscFields,
)
from Core.Web.FacebookGraphAPI.GraphAPIHandlers.GraphAPIBudgetValidationHandler import (
    GraphAPIBudgetValidationHandler,
)
from Core.Web.FacebookGraphAPI.GraphAPIMappings.LevelMapping import (
    LevelToGraphAPIStructure,
)
from Core.Web.FacebookGraphAPI.Models.FieldsMetadata import FieldsMetadata
from facebook_business.adobjects.ad import Ad
from facebook_business.adobjects.adset import AdSet
from facebook_business.adobjects.campaign import Campaign
from FacebookDexter.Infrastructure.DexterRules.OverTimeTrendBuckets.BreakdownGroupedData import (
    BreakdownGroupedData,
)
from FacebookDexter.Infrastructure.Domain.Actions.ActionEnums import (
    FacebookBudgetTypeEnum,
)
from FacebookDexter.Infrastructure.IntegrationEvents.DexterNewCreatedStructuresHandler import (
    DexterCreatedEventMapping,
    DexterNewCreatedStructureEvent,
    NewCreatedStructureKeys,
)
from FacebookDexter.Infrastructure.PersistanceLayer.StrategyDataMongoRepository import (
    StrategyDataMongoRepository,
)

TOTAL_KEY = "total"
UNKNOWN_KEY = "unknown"

logger = logging.getLogger(__name__)


@dataclass
class AdSetBreakdownSplit:
    min_age: int
    max_age: int
    metric_total: Optional[float] = None
    budget: Optional[int] = None
    budget_type: Optional[str] = None


@dataclass
class ApplyParameters:
    business_owner_id: str
    budget_increase: Optional[float] = None
    budget_decrease: Optional[float] = None
    existing_breakdowns: Optional[BreakdownGroupedData] = None
    underperforming_breakdowns: Optional[List[str]] = None


@dataclass
class RecommendationAction:
    config: Any
    fixtures: Any

    def process_action(self, recommendation: Dict, headers: str):
        raise NotImplementedError

    def get_action_parameters(self, apply_parameters: ApplyParameters, structure_details: Dict) -> Optional[Dict]:
        raise NotImplementedError

    @staticmethod
    def publish_response(response: Dict, fixtures: Any):
        rabbitmq_adapter = fixtures.rabbitmq_adapter
        rabbitmq_adapter.publish(response)


@dataclass
class BudgetAlterAction(RecommendationAction):

    def process_action(self, recommendation: Dict, headers: str):
        url = self.config.external_services.facebook_auto_apply.format(
            level=recommendation.get(RecommendationField.LEVEL.value),
            structureId=recommendation.get(RecommendationField.STRUCTURE_ID.value),
        )
        apply_request = requests.put(
            url,
            json=recommendation.get(RecommendationField.APPLY_PARAMETERS.value),
            headers=headers,
        )

        if apply_request.status_code != 200:
            raise Exception(f"Could not update structure {recommendation.get(RecommendationField.STRUCTURE_ID.value)}")

        return None

    def get_action_parameters(self, apply_parameters: ApplyParameters, structure_details: Dict) -> Optional[Dict]:
        raise NotImplementedError


@dataclass
class BudgetIncreaseAction(BudgetAlterAction):
    def get_action_parameters(self, apply_parameters: ApplyParameters, structure_details: Dict) -> Optional[Dict]:
        if not apply_parameters:
            return None

        if not _does_budget_exist(structure_details):
            return None

        budget, budget_type = _get_budget_value_and_type(structure_details)

        if not budget or not budget_type:
            return

        new_budget = budget + apply_parameters.budget_increase * budget
        action_details = {"details": {budget_type: new_budget}}

        return action_details


@dataclass
class BudgetDecreaseAction(BudgetAlterAction):
    def get_action_parameters(self, apply_parameters: ApplyParameters, structure_details: Dict) -> Optional[Dict]:
        if not apply_parameters:
            return None

        if not _does_budget_exist(structure_details):
            return None

        budget, budget_type = _get_budget_value_and_type(structure_details)

        if not budget or not budget_type:
            return

        new_budget = budget - apply_parameters.budget_decrease * budget
        action_details = {"details": {budget_type: new_budget}}

        return action_details


@dataclass
class AgeGenderBreakdownSplit(RecommendationAction):
    def process_action(self, recommendation: Dict, headers: str):

        facebook_id = recommendation.get(RecommendationField.STRUCTURE_ID.value)
        level = recommendation.get(RecommendationField.LEVEL.value)
        mongo_structure = self._get_db_structure(level, facebook_id)

        if not mongo_structure:
            raise Exception(
                f"Could not retrieve structure {recommendation.get(RecommendationField.STRUCTURE_ID.value)}"
            )

        structure = LevelToGraphAPIStructure.get(level, facebook_id)

        apply_parameters = recommendation[RecommendationField.APPLY_PARAMETERS.value][
            RecommendationField.ADSETS_SPLITS.value
        ]
        targeting = dict(BSON.decode(mongo_structure[0][FacebookMiscFields.details]))[FacebookMiscFields.targeting]

        new_created_structures = []
        for gender in apply_parameters:
            for split in apply_parameters[gender]:
                facebook_id = AgeGenderBreakdownSplit._create_and_update_split(
                    split, targeting, structure, gender, recommendation
                )
                new_created_structures.append(
                    NewCreatedStructureKeys(
                        level,
                        recommendation.get(RecommendationField.ACCOUNT_ID.value),
                        facebook_id,
                    )
                )

        self._publish_message_and_pause_structure(new_created_structures, recommendation, headers)

    def get_action_parameters(self, apply_parameters: ApplyParameters, structure_details: Dict) -> Optional[Dict]:
        existing_breakdowns = defaultdict(list)
        removed_amount_spent = 0

        total_amount_spent = apply_parameters.existing_breakdowns.get_breakdown_total(TOTAL_KEY)

        for breakdown in apply_parameters.existing_breakdowns.breakdown_data:
            if breakdown.breakdown_key == TOTAL_KEY:
                continue

            age, gender = breakdown.breakdown_key.split(", ")
            if age == UNKNOWN_KEY or gender == UNKNOWN_KEY:
                continue

            min_age, max_age = AgeGenderBreakdownSplit._get_min_max_age(age)
            existing_breakdowns[gender].append(AdSetBreakdownSplit(min_age, max_age, breakdown.total))

        for to_be_removed_breakdown in apply_parameters.underperforming_breakdowns:
            if to_be_removed_breakdown == TOTAL_KEY:
                continue

            age, gender = to_be_removed_breakdown.split(", ")
            min_age, max_age = AgeGenderBreakdownSplit._get_min_max_age(age)
            existing_breakdowns[gender].remove(
                AdSetBreakdownSplit(
                    min_age,
                    max_age,
                    apply_parameters.existing_breakdowns.get_breakdown_total(to_be_removed_breakdown),
                )
            )
            removed_amount_spent += apply_parameters.existing_breakdowns.get_breakdown_total(to_be_removed_breakdown)

        min_budget = 0
        if _does_budget_exist(structure_details):
            budget, budget_type = _get_budget_value_and_type(structure_details)
            AgeGenderBreakdownSplit._distribute_remaining_budget(
                existing_breakdowns,
                total_amount_spent,
                removed_amount_spent,
                budget,
                budget_type,
            )

            min_budget = self._get_minimum_budget(structure_details, apply_parameters, budget_type)

        adsets_splits = AgeGenderBreakdownSplit._merge_continuous_ages(existing_breakdowns, min_budget)

        return dict(adsets_splits=dict(adsets_splits))

    def _publish_message_and_pause_structure(
        self,
        new_created_structures: List[NewCreatedStructureKeys],
        recommendation: Dict,
        headers: str,
    ):

        new_created_structures_event = DexterNewCreatedStructureEvent(
            recommendation.get(RecommendationField.BUSINESS_OWNER_ID.value),
            new_created_structures,
        )
        mapper = DexterCreatedEventMapping(target=DexterNewCreatedStructureEvent)
        response = mapper.load(asdict(new_created_structures_event))
        RecommendationAction.publish_response(response, self.fixtures)

        url = self.config.external_services.facebook_auto_apply.format(
            level=recommendation.get(RecommendationField.LEVEL.value),
            structureId=recommendation.get(RecommendationField.STRUCTURE_ID.value),
        )
        apply_request = requests.put(url, json={"details": {"status": "PAUSED"}}, headers=headers)

        if apply_request.status_code != 200:
            raise Exception(f"Could not update structure {recommendation.get(RecommendationField.STRUCTURE_ID.value)}")

    def _get_db_structure(self, level: str, facebook_id: str) -> Optional[List]:

        structures_repo = StrategyDataMongoRepository(
            config=self.config.mongo,
            database_name=self.config.mongo.structures_database,
            collection_name=level,
        )
        structure_key = LevelIdKeyEnum[level.upper()].value
        query = {
            MongoOperator.AND.value: [
                {structure_key: {MongoOperator.EQUALS.value: facebook_id}},
                {FieldsMetadata.status.name: {MongoOperator.EQUALS.value: MongoRepositoryStatus.ACTIVE.value}},
            ]
        }

        return structures_repo.get(query=query)

    def _get_minimum_budget(
        self,
        structure_details: Dict,
        apply_parameters: ApplyParameters,
        budget_type: str,
    ):
        minimum_budget = GraphAPIBudgetValidationHandler.handle(
            f"act_{structure_details[LevelIdKeyEnum.ACCOUNT.value]}",
            self.fixtures.business_owner_repository.get_permanent_token(
                business_owner_facebook_id=apply_parameters.business_owner_id
            ),
            self.config,
        )

        # This might need to be changed based on the optimization goal of the structure
        daily_budget = int(minimum_budget["minimumAdAccountDailyBudget"]) * 100

        if budget_type == FacebookBudgetTypeEnum.LIFETIME:
            start_time = structure_details[FacebookMiscFields.created_time]
            end_time = structure_details[FacebookMiscFields.end_time]

            if start_time and end_time:
                start_time = datetime.strptime(start_time[:-5], DEFAULT_DATETIME_ISO)
                end_time = datetime.strptime(end_time[:-5], DEFAULT_DATETIME_ISO)

                # Minimum lifetime budget is minimum daily budget * no_of_days
                lifetime_budget = daily_budget * (end_time - start_time).days
                return lifetime_budget

        return daily_budget

    @staticmethod
    def _create_and_update_split(
        split: Dict,
        targeting: Dict,
        structure: Union[AdSet, Campaign, Ad],
        gender: str,
        recommendation: Dict,
    ):
        adset_split = AdSetBreakdownSplit(**split)
        current_targeting = deepcopy(targeting)

        current_targeting[FacebookMiscFields.age_min] = adset_split.min_age
        current_targeting[FacebookMiscFields.age_max] = adset_split.max_age
        current_targeting[FacebookMiscFields.genders] = [FacebookGender[gender.upper()].value]

        if adset_split.max_age == 65:
            adset_split.max_age = str(adset_split.max_age) + "+"

        copy_result = structure.create_copy(
            params={
                "campaign_id": recommendation.get(RecommendationField.CAMPAIGN_ID.value),
                "deep_copy": True,
                "status_option": AdSet.StatusOption.inherited_from_source,
                "rename_options": {"rename_suffix": f"{adset_split.min_age}-{adset_split.max_age} - {gender}"},
            }
        )

        new_adset = AdSet(copy_result[FacebookMiscFields.copied_adset_id])

        params = {AdSet.Field.targeting: current_targeting}

        if adset_split.budget_type and adset_split.budget:
            params.update({adset_split.budget_type: adset_split.budget})

        new_adset.api_update(params=params)

        return new_adset.get_id()

    @staticmethod
    def _merge_continuous_ages(
        existing_breakdowns: Dict[str, List[AdSetBreakdownSplit]], min_budget: int
    ) -> Dict[str, List[AdSetBreakdownSplit]]:
        adset_splits = defaultdict(list)

        for gender in existing_breakdowns:
            existing_breakdowns[gender].sort(key=lambda x: x.min_age)
            merged_ages = []
            for split in existing_breakdowns[gender]:

                if merged_ages and split.min_age == int(merged_ages[-1].max_age) + 1:
                    merged_ages[-1].max_age = split.max_age
                    if split.budget:
                        merged_ages[-1].budget += split.budget
                    continue

                merged_ages.append(
                    AdSetBreakdownSplit(
                        split.min_age,
                        split.max_age,
                        budget=split.budget,
                        budget_type=split.budget_type,
                    )
                )

            for adset_breakdown_split in merged_ages:
                if not adset_breakdown_split.budget:
                    continue

                if adset_breakdown_split.budget < min_budget:
                    adset_breakdown_split.budget = min_budget
                    continue

                adset_breakdown_split.budget = round(adset_breakdown_split.budget)

            adset_splits[gender] = merged_ages

        return adset_splits

    @staticmethod
    def _get_min_max_age(age: str) -> Tuple[int, int]:
        if "+" in age:
            # Facebook expects the 65-65+ targeting as min_age: 65, max_age: 65...
            max_age = age.replace("+", "")
            min_age = max_age
        else:
            min_age, max_age = age.split("-")

        return int(min_age), int(max_age)

    @staticmethod
    def _distribute_remaining_budget(
        existing_breakdowns: Dict[str, List[AdSetBreakdownSplit]],
        total_amount_spent: float,
        removed_amount_spent: float,
        budget: int,
        budget_type: str,
    ):
        for gender in existing_breakdowns:
            for split in existing_breakdowns[gender]:
                split.budget_type = budget_type
                split.budget = (budget * split.metric_total) / (total_amount_spent - removed_amount_spent)


class ApplyActionType(Enum):
    BUDGET_INCREASE = BudgetIncreaseAction
    BUDGET_DECREASE = BudgetDecreaseAction
    AGE_GENDER_BREAKDOWN_SPLIT = AgeGenderBreakdownSplit


def get_apply_action(action_type: ApplyActionType, config: Any, fixtures: Any):
    if not action_type:
        return None

    return ApplyActionType(action_type).value(config, fixtures)


def _does_budget_exist(structure_details: Dict) -> bool:
    lifetime_budget = structure_details.get(FacebookBudgetTypeEnum.LIFETIME.value)
    daily_budget = structure_details.get(FacebookBudgetTypeEnum.DAILY.value)

    if lifetime_budget or daily_budget:
        return True

    return False


def _get_budget_value_and_type(
    structure_details: Dict,
) -> Tuple[Optional[int], Optional[str]]:
    if not _does_budget_exist(structure_details):
        return None, None

    lifetime_budget = structure_details.get(FacebookBudgetTypeEnum.LIFETIME.value)
    daily_budget = structure_details.get(FacebookBudgetTypeEnum.DAILY.value)

    if daily_budget:
        budget = int(daily_budget)
        budget_type = FacebookBudgetTypeEnum.DAILY.value
    elif lifetime_budget:
        budget = int(lifetime_budget)
        budget_type = FacebookBudgetTypeEnum.LIFETIME.value
    else:
        return None, None

    return budget, budget_type
