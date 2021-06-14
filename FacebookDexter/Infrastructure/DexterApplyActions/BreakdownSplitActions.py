import concurrent.futures
import logging
from collections import defaultdict
from copy import deepcopy
from dataclasses import asdict, dataclass
from datetime import datetime
from typing import ClassVar, Dict, List, Optional, Tuple, Union

import requests
from facebook_business.adobjects.ad import Ad
from facebook_business.adobjects.adset import AdSet
from facebook_business.adobjects.campaign import Campaign

from Core.constants import DEFAULT_DATETIME_ISO
from Core.Dexter.Infrastructure.Domain.LevelEnums import LevelEnum, LevelIdKeyEnum
from Core.Dexter.Infrastructure.Domain.Recommendations.RecommendationFields import RecommendationField
from Core.mongo_adapter import MongoOperator, MongoRepositoryStatus
from Core.Tools.QueryBuilder.QueryBuilderLogicalOperator import AgGridFacebookOperator
from Core.Web.FacebookGraphAPI.GraphAPI.SdkGetStructures import create_facebook_filter, get_and_map_structures
from Core.Web.FacebookGraphAPI.GraphAPIDomain.FacebookMiscFields import FacebookBreakdownGender, FacebookMiscFields
from Core.Web.FacebookGraphAPI.GraphAPIHandlers.GraphAPIBudgetValidationHandler import GraphAPIBudgetValidationHandler
from Core.Web.FacebookGraphAPI.GraphAPIMappings.LevelMapping import Level, LevelToGraphAPIStructure
from Core.Web.FacebookGraphAPI.Models.FieldsMetadata import FieldsMetadata
from Core.Web.FacebookGraphAPI.Tools import Tools
from FacebookDexter.Infrastructure.DexterApplyActions.ApplyActionsUtils import (
    INVALID_METRIC_VALUE,
    TOTAL_KEY,
    UNKNOWN_KEY,
    _does_budget_exist,
    _get_budget_value_and_type,
    make_ad_copies,
)
from FacebookDexter.Infrastructure.DexterApplyActions.RecommendationApplyActions import (
    ApplyButtonType,
    ApplyParameters,
    RecommendationAction,
)
from FacebookDexter.Infrastructure.DexterRules.OverTimeTrendBuckets.BreakdownGroupedData import get_group_data_from_list
from FacebookDexter.Infrastructure.Domain.Actions.ActionEnums import FacebookBudgetTypeEnum
from FacebookDexter.Infrastructure.IntegrationEvents.DexterNewCreatedStructuresHandler import (
    DexterCreatedEventMapping,
    DexterNewCreatedStructureEvent,
    NewCreatedStructureKeys,
)
from FacebookDexter.Infrastructure.PersistanceLayer.StrategyDataMongoRepository import StrategyDataMongoRepository

logger = logging.getLogger(__name__)


@dataclass
class AdSetBreakdownSplit:
    min_age: int
    max_age: int
    metric_total: Optional[float] = None
    budget: Optional[int] = None
    budget_type: Optional[str] = None


@dataclass
class AgeGenderBreakdownSplit(RecommendationAction):
    APPLY_TOOLTIP: ClassVar[str] = (
        "Selecting apply will create a custom number of new adsets with different targeting in such a way "
        "that the under-performing age/gender combinations will be avoided"
    )

    def process_action(self, recommendation: Dict, headers: str, apply_button_type: ApplyButtonType, command: Dict=None):

        facebook_id = recommendation.get(RecommendationField.STRUCTURE_ID.value)
        level = recommendation.get(RecommendationField.LEVEL.value)
        account_id = recommendation.get(RecommendationField.ACCOUNT_ID.value)

        structure_key = LevelIdKeyEnum[level.upper()].value

        filtering = create_facebook_filter(structure_key.replace("_", "."), AgGridFacebookOperator.EQUAL, facebook_id)

        structures_as_dict = get_and_map_structures(account_id, LevelEnum[level.upper()], filtering)

        if not structures_as_dict or len(structures_as_dict) > 1:
            raise Exception(
                f"Could not retrieve structure {recommendation.get(RecommendationField.STRUCTURE_ID.value)}"
            )

        structure_as_dict = structures_as_dict[0]

        apply_parameters = recommendation[RecommendationField.APPLY_PARAMETERS.value][
            RecommendationField.ADSETS_SPLITS.value
        ]
        targeting = structure_as_dict[FacebookMiscFields.details][FacebookMiscFields.targeting]

        fb_structure = LevelToGraphAPIStructure.get(level, facebook_id)

        # create all adsets with breakdowns and no ads of original adset
        new_adset_ids = []
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = []
            for gender in apply_parameters:
                for split in apply_parameters[gender]:
                    futures.append(
                        executor.submit(
                            AgeGenderBreakdownSplit._create_and_update_split,
                            split,
                            targeting,
                            fb_structure,
                            gender,
                            recommendation,
                        )
                    )
            for future in concurrent.futures.as_completed(futures):
                new_adset_ids.append(future.result())

        # get all the ads from the original adset
        orig_fb_adset = AdSet(fbid=facebook_id)
        ad_ids = [ad.get_id() for ad in (orig_fb_adset.get_ads(fields=["id"]))]

        # publish copies of ads to all new adsets
        new_ad_ids = make_ad_copies(ad_ids, new_adset_ids)

        new_created_structures = [
            NewCreatedStructureKeys(level, recommendation.get(RecommendationField.ACCOUNT_ID.value), new_adset_id)
            for new_adset_id in new_adset_ids
        ]

        self._publish_message_and_pause_structure(new_created_structures, recommendation, headers)

    def get_action_parameters(self, apply_parameters: ApplyParameters, structure_details: Dict) -> Optional[Dict]:
        existing_breakdowns = defaultdict(list)

        breakdown_grouped_data = get_group_data_from_list(
            apply_parameters.existing_breakdowns, apply_parameters.metric_name, apply_parameters.no_of_days
        )

        for breakdown in breakdown_grouped_data.breakdown_data:
            if breakdown.breakdown_key == TOTAL_KEY:
                continue

            age, gender = breakdown.breakdown_key.split(", ")
            if age == UNKNOWN_KEY or gender == UNKNOWN_KEY:
                continue

            min_age, max_age = AgeGenderBreakdownSplit._get_min_max_age(age)
            existing_breakdowns[gender].append(AdSetBreakdownSplit(min_age, max_age, 1 / breakdown.total))

        for to_be_removed_breakdown in apply_parameters.underperforming_breakdowns:
            if to_be_removed_breakdown == TOTAL_KEY:
                continue

            age, gender = to_be_removed_breakdown.split(", ")
            min_age, max_age = AgeGenderBreakdownSplit._get_min_max_age(age)
            existing_breakdowns[gender].remove(
                AdSetBreakdownSplit(
                    min_age,
                    max_age,
                    1 / breakdown_grouped_data.get_breakdown_total(to_be_removed_breakdown),
                )
            )

        min_budget = 0
        if _does_budget_exist(structure_details):
            budget, budget_type = _get_budget_value_and_type(structure_details)
            min_budget = self._get_minimum_budget(structure_details, apply_parameters, budget_type)
            AgeGenderBreakdownSplit._distribute_remaining_budget(
                existing_breakdowns,
                budget,
                budget_type,
            )

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
        apply_request = requests.put(url, json={"details": {FieldsMetadata.status.name: "PAUSED"}}, headers=headers)

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
    ) -> int:
        minimum_budget = GraphAPIBudgetValidationHandler.handle(
            f"act_{structure_details[LevelIdKeyEnum.ACCOUNT.value]}",
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
    ) -> str:
        adset_split = AdSetBreakdownSplit(**split)
        current_targeting = deepcopy(targeting)

        current_targeting[FacebookMiscFields.age_min] = adset_split.min_age
        current_targeting[FacebookMiscFields.age_max] = adset_split.max_age
        current_targeting[FacebookMiscFields.genders] = [FacebookBreakdownGender[gender.upper()].value]

        if adset_split.max_age == 65:
            adset_split.max_age = str(adset_split.max_age) + "+"

        copy_result = structure.create_copy(
            params={
                "campaign_id": recommendation.get(RecommendationField.CAMPAIGN_ID.value),
                "deep_copy": False,
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
                if adset_breakdown_split.budget is None:
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
        budget: int,
        budget_type: str,
    ) -> None:

        total_cpr = AgeGenderBreakdownSplit._calculate_total_cpr(existing_breakdowns)

        for gender in existing_breakdowns:
            for split in existing_breakdowns[gender]:
                split.budget_type = budget_type
                if split.metric_total == INVALID_METRIC_VALUE:
                    split.budget = 0
                    continue

                split.budget = budget * (split.metric_total / total_cpr)

    @staticmethod
    def _calculate_total_cpr(existing_breakdowns: Dict[str, List[AdSetBreakdownSplit]]) -> float:
        total_cpr = 0
        for gender in existing_breakdowns:
            for adset_split in existing_breakdowns[gender]:
                if adset_split.metric_total != INVALID_METRIC_VALUE:
                    total_cpr += adset_split.metric_total

        return total_cpr
