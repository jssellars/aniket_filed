import logging
from dataclasses import dataclass
from datetime import datetime
from statistics import mean
from typing import ClassVar, Dict, List, Optional, Tuple

from Core.Dexter.Infrastructure.Domain.ChannelEnum import ChannelEnum
from Core.Dexter.Infrastructure.Domain.LevelEnums import LevelEnum, LevelIdKeyEnum
from Core.Dexter.Infrastructure.Domain.Recommendations.RecommendationEnums import RecommendationStatusEnum
from Core.mongo_adapter import MongoRepositoryBase
from Core.Web.FacebookGraphAPI.Models.FieldsMetadata import FieldsMetadata
from FacebookDexter.BackgroundTasks.Strategies.StrategyBase import (
    DexterGroupedData,
    DexterStrategyBase,
    get_group_data_from_list,
    get_number_of_days,
)
from FacebookDexter.BackgroundTasks.Strategies.StrategyTimeBucket import CauseMetricBase, TrendEnum
from FacebookDexter.Infrastructure.DexterRules.DexterOutput import DexterOutput, get_formatted_message
from FacebookDexter.Infrastructure.PersistanceLayer.StrategyJournalMongoRepository import RecommendationEntryModel

logger = logging.getLogger(__name__)


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
        grouped_data: List[DexterGroupedData],
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

                if not trend and not variance:
                    continue

                time_frames_with_data = get_number_of_days(grouped_data, metric_name)
                if not time_frames_with_data:
                    continue

                reference_time = max(time_frames_with_data)

                if trend == trigger_metric.trigger.trend and variance >= trigger_metric.trigger.variance_percentage:
                    (dexter_recommendation, cause_benchmark, cause_current,) = self.check_causes(
                        trigger_metric.cause_metrics,
                        grouped_data,
                        time_bucket.no_of_days,
                        reference_time,
                        variance,
                    )
                    if dexter_recommendation:
                        debug_msg = create_debug_message(
                            dexter_recommendation.recommendation_template_key,
                            variance,
                            time_bucket.no_of_days,
                            reference_time,
                            get_group_data_from_list(
                                grouped_data, metric_name, reference_time
                            ).get_breakdown_datapoints(self.BREAKDOWN),
                            get_group_data_from_list(
                                grouped_data, metric_name, time_bucket.no_of_days
                            ).get_breakdown_datapoints(self.BREAKDOWN),
                            cause_benchmark,
                            cause_current,
                        )

                        structure_key = LevelIdKeyEnum[level.value.upper()].value

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
                            dexter_recommendation.priority.value,
                            [{"display_name": metric_name.replace("_", " ").title(), "name": metric_name}],
                            {"display_name": breakdown.name.replace("_", " ").title(), "name": breakdown.name},
                            algorithm_type=self.ALGORITHM,
                            debug_msg=debug_msg,
                        )
                        dexter_recommendation.process_output(
                            recommendations_repository, recommendation_entry_model=entry
                        )
                        # For testing purposes we let the algorithm keep generating
                        # return None

        return None

    def check_causes(
        self,
        cause_metrics: List[CauseMetricBase],
        grouped_data: List[DexterGroupedData],
        no_of_days: int,
        reference_time: int,
        trigger_variance: float,
    ) -> Tuple[Optional[DexterOutput], Optional[List[List[float]]], Optional[List[List[float]]]]:

        testing_benchmark_cause_values = []
        testing_recent_cause_values = []

        for cause_metric in cause_metrics:
            for metric_clause in cause_metric.metric_clauses:
                metric_name = metric_clause.metric_field.name

                trend, variance = self.get_trend_and_variance(grouped_data, no_of_days, metric_name)

                if trend is None and variance is None:
                    return None, None, None

                if trend == metric_clause.trend and variance >= metric_clause.variance_percentage:
                    benchmark_data = get_group_data_from_list(grouped_data, metric_name, reference_time)
                    if benchmark_data:
                        testing_benchmark_cause_values.append(benchmark_data.get_breakdown_datapoints(self.BREAKDOWN))
                    current_data = get_group_data_from_list(grouped_data, metric_name, no_of_days)
                    if current_data:
                        testing_recent_cause_values.append(current_data.get_breakdown_datapoints(self.BREAKDOWN))
                    continue

                # If one of the causes is not triggering, return
                return None, None, None

            cause_metric.output.no_of_days = no_of_days
            cause_metric.output.trigger_variance = trigger_variance

            return (
                cause_metric.output,
                testing_benchmark_cause_values,
                testing_recent_cause_values,
            )

        return None, None, None

    def get_trend_and_variance(
        self, grouped_data: List[DexterGroupedData], current_time: int, metric_name: str
    ) -> (float, float):

        time_frames_with_data = get_number_of_days(grouped_data, metric_name)
        if not time_frames_with_data:
            return None, None

        reference_time = max(time_frames_with_data)
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


def create_debug_message(
    recommendation_template_key: str,
    trigger_variance: float,
    no_of_days: int,
    reference_time: int,
    reference_data: List[float],
    current_data: List[float],
    cause_reference_data: List[List[float]],
    cause_current_data: List[List[float]],
) -> str:
    recommendation_str = get_formatted_message(
        recommendation_template_key,
        trigger_variance=trigger_variance,
        no_of_days=no_of_days,
    )
    reference_data = [f"{elem:.2f}" for elem in reference_data]
    current_data = [f"{elem:.2f}" for elem in current_data]
    output_reference_cause = []
    output_current_cause = []
    for cause in cause_reference_data:
        output_reference_cause.append([f"{elem:.2f}" for elem in cause])
    for cause in cause_current_data:
        output_current_cause.append([f"{elem:.2f}" for elem in cause])

    return "\n".join(
        (
            f"Recommendation: {recommendation_str}",
            f"Reference_time_bucket: {reference_time}",
            f"Reference_data: {reference_data}",
            f"Current_time_bucket: {no_of_days}",
            f"Current_data: {current_data}",
            f"Reference_cause_data: {output_reference_cause}",
            f"Current_cause_data: {output_current_cause}",
        )
    )
