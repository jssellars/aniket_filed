import json
import logging
from dataclasses import asdict, dataclass
from datetime import datetime
from typing import ClassVar, Dict, List, Optional, Tuple

from Core.Dexter.Infrastructure.Domain.ChannelEnum import ChannelEnum
from Core.Dexter.Infrastructure.Domain.LevelEnums import LevelEnum
from Core.Dexter.Infrastructure.Domain.Recommendations.RecommendationEnums import RecommendationStatusEnum
from Core.mongo_adapter import MongoRepositoryBase
from Core.Web.FacebookGraphAPI.Models.FieldsMetadata import FieldsMetadata
from FacebookDexter.BackgroundTasks.Strategies.StrategyBase import (
    BreakdownData,
    DexterGroupedData,
    DexterStrategyBase,
    get_group_data_from_list,
)
from FacebookDexter.BackgroundTasks.Strategies.StrategyTimeBucket import (
    CUSTOM_DEXTER_METRICS,
    CauseMetricBase,
    TrendEnum,
    recommendation_enums_union,
)
from FacebookDexter.Infrastructure.DexterRules.OverTimeTrendTemplates import RecommendationPriority
from FacebookDexter.Infrastructure.PersistanceLayer.StrategyJournalMongoRepository import RecommendationEntryModel

logger = logging.getLogger(__name__)


def get_breakdown_priority(variance: float) -> int:
    if variance is None:
        return RecommendationPriority.HIGH.value

    if variance < 50:
        return RecommendationPriority.LOW.value
    elif variance < 70:
        return RecommendationPriority.MEDIUM.value

    return RecommendationPriority.HIGH.value


@dataclass
class BreakdownAverageStrategy(DexterStrategyBase):
    ALGORITHM: ClassVar[str] = "breakdown_average_algorithm"
    INVALID_METRIC = -1

    def trend(self, reference_data: float, current_data: float) -> Optional[TrendEnum]:
        try:
            if current_data > reference_data:
                return TrendEnum.INCREASING

            return TrendEnum.DECREASING

        except Exception as e:
            logger.exception(f"Trend calculation error || {repr(e)}")

    def variance(
        self, reference_data: float, current_data: float, trend: Optional[TrendEnum] = None
    ) -> Optional[float]:
        try:
            variance = ((current_data / reference_data) - 1) * 100

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
    ):

        self.aggregate_grouped_data(grouped_data)

        for time_bucket in self.time_buckets:
            if time_bucket.level != level or time_bucket.breakdown != breakdown:
                continue

            for trigger_metric in time_bucket.triggers:
                trigger = trigger_metric.trigger
                metric_name = trigger.metric_field.name
                metric_data = get_group_data_from_list(grouped_data, metric_name, time_bucket.no_of_days)
                if metric_data is None:
                    continue

                no_of_breakdowns = 1
                if trigger.is_divided_by_no_breakdowns:
                    # Remove the total key
                    no_of_breakdowns = len({s for s in metric_data.get_breakdowns()}) - 1

                if metric_data.get_breakdown_datapoints("total") is None:
                    continue

                reference_data = metric_data.get_breakdown_total("total") / no_of_breakdowns
                for breakdown_data in metric_data.breakdown_data:

                    if breakdown_data.breakdown_group == "total":
                        continue

                    trend = self.trend(reference_data, breakdown_data.total)
                    variance = self.variance(reference_data, breakdown_data.total, trend)

                    if variance >= trigger.variance_percentage:
                        dexter_output, cause_variance, cause_metric = self.check_causes(
                            trigger_metric.cause_metrics,
                            grouped_data,
                            time_bucket.no_of_days,
                            breakdown_data.breakdown_group,
                        )
                        if dexter_output:
                            structure_data, reports_data = DexterStrategyBase.get_structure_and_reports_data(
                                business_owner, account_id, structure, level, metric_name, breakdown
                            )

                            entry = RecommendationEntryModel(
                                dexter_output.name,
                                RecommendationStatusEnum.ACTIVE.value,
                                variance,
                                datetime.now(),
                                time_bucket.no_of_days,
                                ChannelEnum.FACEBOOK.value,
                                get_breakdown_priority(cause_variance),
                                structure_data,
                                reports_data,
                                algorithm_type=self.ALGORITHM,
                                debug_msg=json.dumps([asdict(x) for x in grouped_data]),
                                breakdown_group=breakdown_data.breakdown_group,
                            )
                            dexter_output.value.process_output(
                                recommendations_repository,
                                recommendation_entry_model=entry.get_extended_db_entry(),
                            )

    def check_causes(
        self,
        cause_metrics: List[CauseMetricBase],
        grouped_data: List[DexterGroupedData],
        no_of_days: int,
        breakdown: str,
    ) -> Tuple[Optional[recommendation_enums_union], Optional[float], Optional[str]]:

        # TODO extract this logic to a method and use twice
        for cause_metric in cause_metrics:
            for metric_clause in cause_metric.metric_clauses:
                metric_name = metric_clause.metric_field.name

                metric_data = get_group_data_from_list(grouped_data, metric_name, no_of_days)

                if metric_data is None:
                    return None, None, None

                no_of_breakdowns = 1
                if metric_clause.is_divided_by_no_breakdowns:
                    # Remove the total key
                    no_of_breakdowns = len({s for s in metric_data.get_breakdowns()}) - 1

                if metric_data.get_breakdown_datapoints("total") is None:
                    continue

                reference_data = metric_data.get_breakdown_total("total") / no_of_breakdowns

                current_data = metric_data.get_breakdown_total(breakdown)
                if current_data == self.INVALID_METRIC:
                    return cause_metric.output, None, metric_name

                trend = self.trend(reference_data, current_data)
                variance = self.variance(reference_data, current_data, trend)

                if variance >= metric_clause.variance_percentage:
                    return cause_metric.output, variance, metric_name

        return None, None, None

    def aggregate_grouped_data(self, grouped_data: List[DexterGroupedData]):

        for time_bucket in self.time_buckets:
            for trigger_metric in time_bucket.triggers:
                self.add_totals_to_breakdowns(
                    grouped_data,
                    trigger_metric.trigger.metric_field,
                    time_bucket.no_of_days,
                )

                for cause in trigger_metric.cause_metrics:
                    for metric_clause in cause.metric_clauses:
                        self.add_totals_to_breakdowns(
                            grouped_data,
                            metric_clause.metric_field,
                            time_bucket.no_of_days,
                        )

        return

    def add_totals_to_breakdowns(
        self,
        grouped_data: List[DexterGroupedData],
        metric,
        no_of_days: int,
    ):

        # If there is a custom metric, we need to aggregate data first and then do the math for the total value
        if metric.is_dexter_custom_metric:
            self.aggregate_custom_metric(grouped_data, metric, no_of_days)
        else:
            metric_data = get_group_data_from_list(grouped_data, metric.name, no_of_days)
            total_data = metric_data.get_breakdown_datapoints("total")
            if total_data is not None:
                return

            metric_data.breakdown_data.append(
                BreakdownData("total", [], sum([sum(x.data_points) for x in metric_data.breakdown_data]))
            )

            for breakdown_data in metric_data.breakdown_data:

                if breakdown_data.breakdown_group == "total":
                    continue

                breakdown_data.total = sum(breakdown_data.data_points)

    def aggregate_custom_metric(self, grouped_data: List[DexterGroupedData], metric: FieldsMetadata, no_of_days: int):
        custom_metric = CUSTOM_DEXTER_METRICS[metric.name]
        denominator_name = custom_metric.denominator.name
        numerator_name = custom_metric.numerator.name

        denominator_data = get_group_data_from_list(grouped_data, denominator_name, no_of_days)
        numerator_data = get_group_data_from_list(grouped_data, numerator_name, no_of_days)

        if denominator_data is None or numerator_data is None:
            return

        all_keys = list(set(denominator_data.get_breakdowns()) | set(numerator_data.get_breakdowns()))
        data = {
            denominator_name: sum([sum(x.data_points) for x in denominator_data.breakdown_data]),
            numerator_name: sum([sum(x.data_points) for x in numerator_data.breakdown_data]),
        }

        metric_data = get_group_data_from_list(grouped_data, metric.name, no_of_days)
        if metric_data is not None:
            return

        total_breakpoint = BreakdownData("total", [], custom_metric.calculate_cost(data))
        metric_data = DexterGroupedData(no_of_days, metric.name, [total_breakpoint])
        grouped_data.append(metric_data)

        for breakdown in all_keys:

            if breakdown == "total":
                continue

            numerator_breakpoint_data = numerator_data.get_breakdown_datapoints(breakdown)
            denominator_breakpoint_data = denominator_data.get_breakdown_datapoints(breakdown)
            if numerator_breakpoint_data is None or denominator_breakpoint_data is None:
                metric_data.breakdown_data.append(BreakdownData(breakdown, [], total=self.INVALID_METRIC))
                continue

            data[numerator_name] = sum(numerator_breakpoint_data)
            data[denominator_name] = sum(denominator_breakpoint_data)

            metric_data.breakdown_data.append(BreakdownData(breakdown, [], custom_metric.calculate_cost(data)))
