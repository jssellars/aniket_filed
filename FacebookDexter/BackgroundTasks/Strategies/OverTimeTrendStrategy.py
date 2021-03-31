import logging
from dataclasses import dataclass
from datetime import datetime
from statistics import mean
from typing import ClassVar, Dict, List, Optional

from Core.Dexter.Infrastructure.Domain.ChannelEnum import ChannelEnum
from Core.Dexter.Infrastructure.Domain.LevelEnums import LevelEnum
from Core.Dexter.Infrastructure.Domain.Recommendations.RecommendationEnums import RecommendationStatusEnum
from Core.mongo_adapter import MongoRepositoryBase
from Core.Web.FacebookGraphAPI.GraphAPIDomain.FacebookMiscFields import FacebookMiscFields
from Core.Web.FacebookGraphAPI.Models.FieldsMetadata import FieldsMetadata
from FacebookDexter.BackgroundTasks.startup import config, fixtures
from FacebookDexter.BackgroundTasks.Strategies.StrategyBase import DexterStrategyBase
from FacebookDexter.Infrastructure.DexterApplyActions.ApplyTypes import get_apply_action
from FacebookDexter.Infrastructure.DexterApplyActions.RecommendationApplyActions import ApplyParameters
from FacebookDexter.Infrastructure.DexterRules.OverTimeTrendBuckets.BreakdownGroupedData import (
    BreakdownGroupedData,
    get_group_data_from_list,
    get_max_number_of_days,
    get_max_number_of_days_from_bucket,
)
from FacebookDexter.Infrastructure.DexterRules.OverTimeTrendBuckets.StrategyTimeBucket import (
    CauseMetricBase,
    TrendEnum,
    recommendation_enums_union,
)
from FacebookDexter.Infrastructure.PersistanceLayer.StrategyJournalMongoRepository import RecommendationEntryModel

logger = logging.getLogger(__name__)

BUDGET_INCREASE_PERCENTAGE = 0.20
BUDGET_DECREASE_PERCENTAGE = 0.20


@dataclass
class OverTimeTrendStrategy(DexterStrategyBase):
    # This strategy has no breakdowns
    BREAKDOWN = FieldsMetadata.breakdown_none.name
    ALGORITHM: ClassVar[str] = "over_time_trend_strategy"

    def trend(self, reference_data: List[float], current_data: List[float]) -> Optional[TrendEnum]:
        try:
            if mean(current_data) > mean(reference_data):
                return TrendEnum.INCREASING

            return TrendEnum.DECREASING

        except Exception as e:
            logger.exception(f"Trend calculation error || {repr(e)}")

    def variance(
        self, reference_data: List[float], current_data: List[float], trend: Optional[TrendEnum] = None
    ) -> Optional[float]:
        try:
            variance = (mean(current_data) / mean(reference_data) - 1) * 100
            if trend == TrendEnum.DECREASING:
                variance *= -1

            return variance

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
    ) -> None:

        for time_bucket in self.time_buckets:
            if time_bucket.level != level or time_bucket.breakdown != breakdown:
                continue

            for trigger_metric in time_bucket.triggers:
                metric_name = trigger_metric.trigger.metric_field.name

                trend, variance = self.get_trend_and_variance(grouped_data, time_bucket.no_of_days, metric_name)

                if not trend or not variance:
                    continue

                reference_time = get_max_number_of_days_from_bucket(grouped_data, metric_name)
                if not reference_time:
                    continue

                if trend == trigger_metric.trigger.trend and variance >= trigger_metric.trigger.variance_percentage:
                    dexter_output = self.check_causes(
                        trigger_metric.cause_metrics,
                        grouped_data,
                        time_bucket.no_of_days,
                        variance,
                    )
                    if dexter_output:

                        structure_data, reports_data = DexterStrategyBase.get_structure_and_reports_data(
                            business_owner, account_id, structure, level, metric_name, breakdown
                        )

                        dexter_recommendation = dexter_output.value
                        apply_action = get_apply_action(dexter_recommendation.apply_action_type, config, fixtures)
                        apply_parameters = None

                        if apply_action:
                            apply_parameters = apply_action.get_action_parameters(
                                ApplyParameters(
                                    business_owner_id=business_owner,
                                    budget_increase=BUDGET_INCREASE_PERCENTAGE,
                                    budget_decrease=BUDGET_DECREASE_PERCENTAGE,
                                ),
                                structure.get(FacebookMiscFields.details),
                            )

                            # If something went wrong while processing the apply action then don't generate
                            # recommendation
                            if apply_parameters is None:
                                continue

                        entry = RecommendationEntryModel(
                            dexter_output.name,
                            RecommendationStatusEnum.ACTIVE.value,
                            variance,
                            datetime.now(),
                            get_max_number_of_days(grouped_data, metric_name),
                            ChannelEnum.FACEBOOK.value,
                            dexter_recommendation.priority.value,
                            structure_data,
                            reports_data,
                            algorithm_type=self.ALGORITHM,
                            apply_parameters=apply_parameters,
                        )
                        dexter_recommendation.process_output(
                            recommendations_repository, recommendation_entry_model=entry.get_extended_db_entry()
                        )
                        # TODO: This can be commented if we want to stop after the
                        #  first recommendation for the structure
                        return

        return

    def check_causes(
        self,
        cause_metrics: List[CauseMetricBase],
        grouped_data: List[BreakdownGroupedData],
        no_of_days: int,
        trigger_variance: float,
    ) -> Optional[recommendation_enums_union]:

        for cause_metric in cause_metrics:
            for metric_clause in cause_metric.metric_clauses:
                metric_name = metric_clause.metric_field.name

                trend, variance = self.get_trend_and_variance(grouped_data, no_of_days, metric_name)

                if trend is None or variance is None:
                    return None

                if trend == metric_clause.trend and variance >= metric_clause.variance_percentage:
                    continue

                # If one of the causes is not triggering, return
                return None

            cause_metric.output.value.no_of_days = no_of_days
            cause_metric.output.value.trigger_variance = trigger_variance

            return cause_metric.output

        return None

    def get_trend_and_variance(
        self, grouped_data: List[BreakdownGroupedData], current_time: int, metric_name: str
    ) -> (float, float):

        reference_time = get_max_number_of_days_from_bucket(grouped_data, metric_name)
        if not reference_time:
            return None, None

        if current_time == reference_time:
            return None, None

        reference_data = get_group_data_from_list(grouped_data, metric_name, reference_time)
        current_data = get_group_data_from_list(grouped_data, metric_name, current_time)

        if reference_data is None or current_data is None:
            return None, None

        trend = self.trend(
            reference_data.get_breakdown_datapoints(self.BREAKDOWN),
            current_data.get_breakdown_datapoints(self.BREAKDOWN),
        )
        variance = self.variance(
            reference_data.get_breakdown_datapoints(self.BREAKDOWN),
            current_data.get_breakdown_datapoints(self.BREAKDOWN),
            trend,
        )

        return trend, variance
