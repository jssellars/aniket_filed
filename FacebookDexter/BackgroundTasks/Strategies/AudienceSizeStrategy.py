import logging
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import ClassVar, Dict, List, Optional

from bson import BSON
from Core.constants import DEFAULT_DATETIME
from Core.Dexter.Infrastructure.Domain.ChannelEnum import ChannelEnum
from Core.Dexter.Infrastructure.Domain.LevelEnums import LevelEnum, LevelIdKeyEnum
from Core.Dexter.Infrastructure.Domain.Recommendations.RecommendationEnums import RecommendationStatusEnum
from Core.mongo_adapter import MongoRepositoryBase
from Core.Web.FacebookGraphAPI.GraphAPI.GraphAPISdkBase import GraphAPISdkBase
from Core.Web.FacebookGraphAPI.Models.FieldsMetadata import FieldsMetadata
from Core.Web.FacebookGraphAPI.Tools import Tools
from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.adobjects.adset import AdSet
from facebook_business.adobjects.targeting import Targeting
from FacebookDexter.BackgroundTasks.startup import config, fixtures
from FacebookDexter.BackgroundTasks.Strategies.StrategyBase import (
    DexterGroupedData,
    DexterStrategyBase,
    get_group_data_from_list,
)
from FacebookDexter.BackgroundTasks.Strategies.StrategyTimeBucket import TrendEnum
from FacebookDexter.Infrastructure.DexterRules.OverTimeTrendTemplates import RecommendationPriority
from FacebookDexter.Infrastructure.PersistanceLayer.StrategyJournalMongoRepository import RecommendationEntryModel

logger = logging.getLogger(__name__)

INVALID_AUDIENCE_SIZE = -1


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
            grouped_data: List[DexterGroupedData],
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

                structure_details = dict(BSON.decode(structure["details"]))

                audience_size = get_audience_size(
                    account_id,
                    structure_details["targeting"],
                    structure_details["optimization_goal"],
                    structure_details["promoted_object"],
                )

                if audience_size is None:
                    return

                variance = self.variance(audience_size, reach, None)
                if variance >= trigger_metric.trigger.variance_percentage:
                    dexter_recommendation = trigger_metric.cause_metrics[0].output

                    if dexter_recommendation:
                        entry = RecommendationEntryModel(
                            dexter_recommendation.recommendation_template_key,
                            RecommendationStatusEnum.ACTIVE.value,
                            variance,
                            business_owner,
                            f"act_{str(account_id)}",
                            structure[structure_key],
                            structure[f"{level.value}_name"],
                            structure[FieldsMetadata.campaign_id.name],
                            structure[FieldsMetadata.campaign_name.name],
                            level.value,
                            datetime.now(),
                            time_bucket.no_of_days,
                            ChannelEnum.FACEBOOK.value,
                            get_audience_size_priority(variance),
                            [{"display_name": metric_name.replace("_", " ").title(), "name": metric_name}],
                            {"display_name": breakdown.name.replace("_", " ").title(), "name": breakdown.name},
                            algorithm_type=self.ALGORITHM,
                            debug_msg=f"Audience size - {audience_size} and total reach {reach}",
                        )

                        dexter_recommendation.process_output(
                            recommendations_repository,
                            recommendation_entry_model=entry,
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
