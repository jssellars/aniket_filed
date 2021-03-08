import logging
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import ClassVar, Dict, List, Optional

from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.adobjects.adset import AdSet
from facebook_business.adobjects.targeting import Targeting
from facebook_business.adobjects.targetingsearch import TargetingSearch

from Core.Dexter.Infrastructure.Domain.ChannelEnum import ChannelEnum
from Core.Dexter.Infrastructure.Domain.LevelEnums import LevelEnum, LevelIdKeyEnum
from Core.Dexter.Infrastructure.Domain.Recommendations.RecommendationEnums import RecommendationStatusEnum
from Core.Web.FacebookGraphAPI.GraphAPI.GraphAPISdkBase import GraphAPISdkBase
from Core.Web.FacebookGraphAPI.GraphAPIDomain.FacebookMiscFields import FacebookMiscFields
from Core.Web.FacebookGraphAPI.Models.FieldsMetadata import FieldsMetadata
from Core.Web.FacebookGraphAPI.Tools import Tools
from Core.constants import DEFAULT_DATETIME
from Core.mongo_adapter import MongoRepositoryBase
from FacebookDexter.BackgroundTasks.Strategies.StrategyBase import DexterStrategyBase
from FacebookDexter.BackgroundTasks.startup import config, fixtures
from FacebookDexter.Infrastructure.DexterRules.OverTimeTrendBuckets.BreakdownGroupedData import (
    BreakdownGroupedData,
    get_max_number_of_days,
    get_max_number_of_days_from_bucket,
)
from FacebookDexter.Infrastructure.DexterRules.OverTimeTrendBuckets.StrategyTimeBucket import TrendEnum
from FacebookDexter.Infrastructure.DexterRules.OverTimeTrendTemplates import RecommendationPriority
from FacebookDexter.Infrastructure.PersistanceLayer.StrategyJournalMongoRepository import RecommendationEntryModel

logger = logging.getLogger(__name__)

INVALID_AUDIENCE_SIZE = -1
HIDDEN_INTERESTS_LIMIT = 500


def get_audience_size_priority(variance: float) -> int:
    if variance is None:
        return RecommendationPriority.HIGH.value

    if variance < 85:
        return RecommendationPriority.LOW.value
    elif variance < 95:
        return RecommendationPriority.MEDIUM.value

    return RecommendationPriority.HIGH.value


@dataclass
class AudienceSizeStrategy(DexterStrategyBase):
    BREAKDOWN = FieldsMetadata.breakdown_none.name
    ALGORITHM: ClassVar[str] = "audience_size_strategy"
    INVALID_METRIC = -1

    def trend(self, reference_data: List[float], current_data: List[float]) -> Optional[TrendEnum]:
        raise NotImplementedError

    def variance(
        self, reference_data: float, current_data: float, trend: Optional[TrendEnum] = None
    ) -> Optional[float]:
        try:
            return current_data / reference_data * 100

        except ArithmeticError as e:
            logger.exception(f"Arithmetic Error at variance calculation || {repr(e)}")
            return None

    def generate_recommendation(
        self,
        grouped_data: List[BreakdownGroupedData],
        level: LevelEnum,
        breakdown: FieldsMetadata,
        business_owner: str,
        account_id: str,
        structure: Dict,
        recommendations_repository: MongoRepositoryBase,
    ):
        structure_key = LevelIdKeyEnum[level.value.upper()].value

        permanent_token = fixtures.business_owner_repository.get_permanent_token(business_owner)

        # initialize GraphAPI SDK
        _ = GraphAPISdkBase(config.facebook, permanent_token)

        reach_cursor = AdSet(structure[structure_key]).get_insights(
            fields=[FieldsMetadata.reach.name],
            params={
                "time_range": {
                    "since": (datetime.now() - timedelta(days=90)).strftime(DEFAULT_DATETIME),
                    "until": datetime.now().strftime(DEFAULT_DATETIME),
                },
            },
        )

        reach = int(reach_cursor.get_one()[FieldsMetadata.reach.name])

        for time_bucket in self.time_buckets:
            if time_bucket.level != level or time_bucket.breakdown != breakdown:
                continue

            for trigger_metric in time_bucket.triggers:
                metric_name = trigger_metric.trigger.metric_field.name

                structure_details = structure.get(FacebookMiscFields.details)

                if not structure_details:
                    continue

                targeting = structure_details["targeting"]
                optimization_goal = structure_details["optimization_goal"]
                promoted_object = structure_details["promoted_object"]

                audience_size = get_audience_size(
                    account_id,
                    targeting,
                    optimization_goal,
                    promoted_object,
                )

                if audience_size is None:
                    return

                variance = self.variance(audience_size, reach, None)
                if variance >= trigger_metric.trigger.variance_percentage:

                    hidden_interests = ", ".join(get_hidden_interests(targeting))

                    dexter_output = trigger_metric.cause_metrics[0].output
                    template_key = dexter_output.name
                    dexter_recommendation = dexter_output.value

                    if dexter_recommendation:
                        structure_data, reports_data = DexterStrategyBase.get_structure_and_reports_data(
                            business_owner, account_id, structure, level, metric_name, breakdown
                        )

                        reference_time = get_max_number_of_days_from_bucket(grouped_data, metric_name)
                        if not reference_time:
                            continue

                        entry = RecommendationEntryModel(
                            template_key,
                            RecommendationStatusEnum.ACTIVE.value,
                            variance,
                            datetime.now(),
                            get_max_number_of_days(grouped_data, metric_name),
                            ChannelEnum.FACEBOOK.value,
                            get_audience_size_priority(variance),
                            structure_data,
                            reports_data,
                            algorithm_type=self.ALGORITHM,
                            debug_msg=f"Audience size - {audience_size} and total reach {reach}",
                            hidden_interests=hidden_interests if hidden_interests else None,
                        )

                        dexter_recommendation.process_output(
                            recommendations_repository,
                            recommendation_entry_model=entry.get_extended_db_entry(),
                        )


def get_audience_size(
    ad_account_id: str, targeting_spec: Dict, optimization_goal: str, promoted_object: str
) -> Optional[int]:
    ad_account = AdAccount(fbid=f"act_{ad_account_id}")
    targeting = Targeting()
    targeting.set_data(targeting_spec)
    if targeting_spec is not None and optimization_goal is not None:
        response = ad_account.get_delivery_estimate(
            fields=["estimate_mau"],
            params={
                "targeting_spec": targeting,
                "optimization_goal": optimization_goal,
                "promoted_object": promoted_object,
            },
        )
        response = Tools.convert_to_json(response[0])
        response = response.get("estimate_mau", None)
        return response if response != INVALID_AUDIENCE_SIZE else None


def get_hidden_interests(targeting: Dict) -> List[str]:
    if not targeting:
        return []

    flexible_spec = targeting.get("flexible_spec", [])
    targeting_interests = []

    targeting_interests.extend([interest["name"] for spec in flexible_spec for interest in spec.get("interests", [])])
    targeting_interests.extend([interest["name"] for interest in targeting.get("interests", [])])

    params = {
        "interest_list": targeting_interests,
        "type": TargetingSearch.TargetingSearchTypes.interest_suggestion,
        "limit": HIDDEN_INTERESTS_LIMIT,
    }

    results = TargetingSearch.search(params=params)
    results = [Tools.convert_to_json(result) for result in results]

    results = sorted(results, key=lambda i: i["audience_size"], reverse=True)[:3]

    return [entry["name"] for entry in results if entry["name"] not in targeting_interests]
