import json
import logging
from dataclasses import asdict, dataclass
from datetime import datetime
from typing import ClassVar, Dict, List, Optional, Tuple

from Core.Dexter.Infrastructure.Domain.ChannelEnum import ChannelEnum
from Core.Dexter.Infrastructure.Domain.LevelEnums import LevelEnum
from Core.Dexter.Infrastructure.Domain.Recommendations.RecommendationEnums import RecommendationStatusEnum
from Core.mongo_adapter import MongoRepositoryBase
from Core.Web.FacebookGraphAPI.GraphAPIDomain.FacebookMiscFields import FacebookMiscFields
from Core.Web.FacebookGraphAPI.GraphAPIMappings.DexterCustomMetricMapper import CUSTOM_DEXTER_METRICS
from Core.Web.FacebookGraphAPI.Models.FieldsMetadata import FieldsMetadata
from FacebookDexter.BackgroundTasks.startup import config, fixtures
from FacebookDexter.BackgroundTasks.Strategies.StrategyBase import DexterStrategyBase
from FacebookDexter.Infrastructure.DexterApplyActions.ApplyActionsUtils import INVALID_METRIC_VALUE, TOTAL_KEY
from FacebookDexter.Infrastructure.DexterApplyActions.ApplyTypes import get_apply_action
from FacebookDexter.Infrastructure.DexterApplyActions.RecommendationApplyActions import ApplyParameters
from FacebookDexter.Infrastructure.DexterRules.OverTimeTrendBuckets.BreakdownGroupedData import (
    BreakdownData,
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
        grouped_data: List[BreakdownGroupedData],
        level: LevelEnum,
        breakdown: FieldsMetadata,
        business_owner: str,
        account_id: str,
        structure: Dict,
        recommendations_repository: MongoRepositoryBase,
    ):

        self.aggregate_grouped_data(grouped_data)

        for time_bucket in self.time_buckets:

            underperforming_breakdowns = []
            dexter_breakdown_recommendation = None
            variance = None
            cause_variance = None
            cause_metric_name = None

            if time_bucket.level != level or time_bucket.breakdown != breakdown:
                continue

            # There is a single trigger in these buckets
            if not time_bucket.triggers:
                return

            trigger_metric = time_bucket.triggers[0]
            trigger = trigger_metric.trigger
            metric_name = trigger.metric_field.name
            grouped_metric_data = get_group_data_from_list(grouped_data, metric_name, time_bucket.no_of_days)
            if grouped_metric_data is None:
                continue

            no_of_breakdowns = 1
            if trigger.is_divided_by_no_breakdowns:
                # Remove the total key
                no_of_breakdowns = len({s for s in grouped_metric_data.get_breakdowns()}) - 1

            if grouped_metric_data.get_breakdown_datapoints(TOTAL_KEY) is None:
                continue

            reference_data = grouped_metric_data.get_breakdown_total(TOTAL_KEY) / no_of_breakdowns

            for breakdown_data in grouped_metric_data.breakdown_data:

                if breakdown_data.breakdown_key == TOTAL_KEY:
                    continue

                trend = self.trend(reference_data, breakdown_data.total)
                variance = self.variance(reference_data, breakdown_data.total, trend)

                if variance >= trigger.variance_percentage:
                    dexter_output, cause_variance, cause_metric = self.check_causes(
                        trigger_metric.cause_metrics,
                        grouped_data,
                        time_bucket.no_of_days,
                        breakdown_data.breakdown_key,
                    )
                    if dexter_output:
                        underperforming_breakdowns.append(breakdown_data.breakdown_key)
                        dexter_breakdown_recommendation = dexter_output

            if not dexter_breakdown_recommendation:
                continue

            apply_action = get_apply_action(dexter_breakdown_recommendation.value.apply_action_type, config, fixtures)
            apply_parameters = None

            if apply_action:
                cause_metric_name = trigger_metric.cause_metrics[0].metric_clauses[0].metric_field.name
                apply_parameters = apply_action.get_action_parameters(
                    ApplyParameters(
                        business_owner_id=business_owner,
                        existing_breakdowns=grouped_data,
                        underperforming_breakdowns=underperforming_breakdowns,
                        metric_name=cause_metric_name,
                        no_of_days=time_bucket.no_of_days,
                    ),
                    structure.get(FacebookMiscFields.details),
                )

                # If something went wrong while processing the apply action then don't generate
                # recommendation
                if apply_parameters is None:
                    continue

            structure_data, reports_data = DexterStrategyBase.get_structure_and_reports_data(
                business_owner, account_id, structure, level, cause_metric_name, breakdown
            )

            reference_time = get_max_number_of_days_from_bucket(grouped_data, cause_metric_name)
            if not reference_time:
                continue

            entry = RecommendationEntryModel(
                dexter_breakdown_recommendation.name,
                RecommendationStatusEnum.ACTIVE.value,
                variance,
                datetime.now().isoformat(),
                # The number of days with CPR is equal to the number of days with results
                get_max_number_of_days(grouped_data, FieldsMetadata.results.name),
                ChannelEnum.FACEBOOK.value,
                get_breakdown_priority(cause_variance),
                structure_data,
                reports_data,
                algorithm_type=self.ALGORITHM,
                debug_msg=json.dumps([asdict(x) for x in grouped_data]),
                underperforming_breakdowns=underperforming_breakdowns,
                apply_parameters=apply_parameters,
            )
            dexter_breakdown_recommendation.value.process_output(
                recommendations_repository,
                recommendation_entry_model=entry.get_extended_db_entry(),
            )

    def check_causes(
        self,
        cause_metrics: List[CauseMetricBase],
        grouped_data: List[BreakdownGroupedData],
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

                if metric_data.get_breakdown_datapoints(TOTAL_KEY) is None:
                    continue

                reference_data = metric_data.get_breakdown_total(TOTAL_KEY) / no_of_breakdowns

                current_data = metric_data.get_breakdown_total(breakdown)
                if current_data == INVALID_METRIC_VALUE:
                    return cause_metric.output, None, metric_name

                trend = self.trend(reference_data, current_data)
                variance = self.variance(reference_data, current_data, trend)

                if variance >= metric_clause.variance_percentage:
                    return cause_metric.output, variance, metric_name

        return None, None, None

    def aggregate_grouped_data(self, grouped_data: List[BreakdownGroupedData]):

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
        grouped_data: List[BreakdownGroupedData],
        metric,
        no_of_days: int,
    ):

        # If there is a custom metric, we need to aggregate data first and then do the math for the total value
        if metric.is_dexter_custom_metric:
            self.aggregate_custom_metric(grouped_data, metric, no_of_days)
        else:
            metric_data = get_group_data_from_list(grouped_data, metric.name, no_of_days)
            total_data = metric_data.get_breakdown_datapoints(TOTAL_KEY)
            if total_data is not None:
                return

            metric_data.breakdown_data.append(
                BreakdownData(TOTAL_KEY, [], sum([sum(x.data_points) for x in metric_data.breakdown_data]))
            )

            for breakdown_data in metric_data.breakdown_data:

                if breakdown_data.breakdown_key == TOTAL_KEY:
                    continue

                breakdown_data.total = sum(breakdown_data.data_points)

    def aggregate_custom_metric(
        self, grouped_data: List[BreakdownGroupedData], metric: FieldsMetadata, no_of_days: int
    ):
        custom_metric = CUSTOM_DEXTER_METRICS[metric.name]
        denominator_name = custom_metric.denominator
        numerator_name = custom_metric.numerator

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

        total_breakpoint = BreakdownData(TOTAL_KEY, [], custom_metric.calculate_metric(data))
        metric_data = BreakdownGroupedData(no_of_days, metric.name, [total_breakpoint])
        grouped_data.append(metric_data)

        for breakdown in all_keys:

            if breakdown == TOTAL_KEY:
                continue

            numerator_breakpoint_data = numerator_data.get_breakdown_datapoints(breakdown)
            denominator_breakpoint_data = denominator_data.get_breakdown_datapoints(breakdown)
            if numerator_breakpoint_data is None or denominator_breakpoint_data is None:
                metric_data.breakdown_data.append(BreakdownData(breakdown, [], total=INVALID_METRIC_VALUE))
                continue

            data[numerator_name] = sum(numerator_breakpoint_data)
            data[denominator_name] = sum(denominator_breakpoint_data)

            metric_data.breakdown_data.append(BreakdownData(breakdown, [], custom_metric.calculate_metric(data)))
