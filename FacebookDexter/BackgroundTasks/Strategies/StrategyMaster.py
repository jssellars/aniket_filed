import concurrent.futures
import functools
import logging
from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum
from typing import Dict, List, Set, Union

from Core.constants import DEFAULT_DATETIME
from Core.Dexter.Infrastructure.Domain.ChannelEnum import ChannelEnum
from Core.Dexter.Infrastructure.Domain.DexterJournalEnums import RunStatusDexterEngineJournal
from Core.Dexter.Infrastructure.Domain.LevelEnums import LevelEnum, LevelIdKeyEnum
from Core.mongo_adapter import MongoRepositoryBase
from Core.Tools.QueryBuilder.QueryBuilderLogicalOperator import AgGridFacebookOperator
from Core.Web.FacebookGraphAPI.GraphAPI.SdkGetStructures import (
    create_facebook_filter,
    get_and_map_structures,
    get_dexter_insights,
)
from Core.Web.FacebookGraphAPI.GraphAPIDomain.FacebookMiscFields import FacebookMiscFields, FacebookParametersStrings
from Core.Web.FacebookGraphAPI.GraphAPIMappings.DexterCustomMetricMapper import CUSTOM_DEXTER_METRICS
from Core.Web.FacebookGraphAPI.GraphAPIMappings.FacebookToTuringStatusMapping import EffectiveStatusEnum
from Core.Web.FacebookGraphAPI.GraphAPIMappings.LevelMapping import Level, LevelToFacebookIdKeyMapping
from Core.Web.FacebookGraphAPI.GraphAPIMappings.ObjectiveToResultsMapper import (
    AdSetOptimizationToResult,
    PixelCustomEventTypeToResult,
)
from Core.Web.FacebookGraphAPI.Models.Field import Field
from Core.Web.FacebookGraphAPI.Models.Field import Field as FacebookField
from Core.Web.FacebookGraphAPI.Models.FieldsMetadata import FieldsMetadata
from Core.Web.FacebookGraphAPI.Models.FieldsMetricStructureMetadata import FieldsMetricStructureMetadata
from FacebookDexter.BackgroundTasks.startup import config
from FacebookDexter.BackgroundTasks.Strategies.AudienceSizeStrategy import AudienceSizeStrategy
from FacebookDexter.BackgroundTasks.Strategies.BreakdownStrategy import BreakdownAverageStrategy
from FacebookDexter.BackgroundTasks.Strategies.OverTimeTrendStrategy import OverTimeTrendStrategy
from FacebookDexter.BackgroundTasks.Strategies.StrategyBase import DexterStrategyBase
from FacebookDexter.Infrastructure.DexterApplyActions.ApplyTypes import ApplyActionType
from FacebookDexter.Infrastructure.DexterRules.BreakdownAndAudiencesRules import (
    AGE_GENDER_BREAKDOWN_BUCKET,
    AUDIENCE_SIZE_BUCKET,
    PLACEMENT_BREAKDOWN_BUCKET,
)
from FacebookDexter.Infrastructure.DexterRules.OverTimeTrendBuckets.AdSetTimeBuckets import ADSET_TIME_BUCKETS
from FacebookDexter.Infrastructure.DexterRules.OverTimeTrendBuckets.AdTimeBuckets import AD_TIME_BUCKETS
from FacebookDexter.Infrastructure.DexterRules.OverTimeTrendBuckets.BreakdownGroupedData import (
    BreakdownData,
    BreakdownGroupedData,
)
from FacebookDexter.Infrastructure.DexterRules.OverTimeTrendBuckets.CampaignTimeBuckets import CAMPAIGN_TIME_BUCKETS
from FacebookDexter.Infrastructure.DexterRules.OverTimeTrendBuckets.StrategyTimeBucket import (
    CauseMetricBase,
    MetricClause,
    StrategyTimeBucket,
    TriggerMetric,
)
from FacebookDexter.Infrastructure.PersistanceLayer.StrategyDataMongoRepository import StrategyDataMongoRepository
from FacebookDexter.Infrastructure.PersistanceLayer.StrategyJournalMongoRepository import StrategyJournalMongoRepository

logger = logging.getLogger(__name__)


class DexterStrategiesEnum(Enum):
    AVERAGE_STRATEGY = OverTimeTrendStrategy(
        levels=[LevelEnum.CAMPAIGN, LevelEnum.ADSET, LevelEnum.AD],
        breakdowns=[FieldsMetadata.breakdown_none],
        action_breakdowns=[FieldsMetadata.action_none],
        time_buckets=CAMPAIGN_TIME_BUCKETS + ADSET_TIME_BUCKETS + AD_TIME_BUCKETS,
    )

    BREAKDOWN_STRATEGY = BreakdownAverageStrategy(
        levels=[LevelEnum.ADSET],
        breakdowns=[FieldsMetadata.age_gender, FieldsMetadata.placement],
        action_breakdowns=[FieldsMetadata.action_none],
        time_buckets=AGE_GENDER_BREAKDOWN_BUCKET + PLACEMENT_BREAKDOWN_BUCKET,
    )

    AUDIENCE_SIZE_STRATEGY = AudienceSizeStrategy(
        levels=[LevelEnum.ADSET],
        breakdowns=[FieldsMetadata.breakdown_none],
        action_breakdowns=[FieldsMetadata.action_none],
        time_buckets=AUDIENCE_SIZE_BUCKET,
    )


@dataclass
class DexterStrategyMaster:
    dexter_strategy: DexterStrategyBase
    data_repository: StrategyDataMongoRepository
    recommendations_repository: MongoRepositoryBase
    journal_repository: StrategyJournalMongoRepository

    def analyze_data_for_business_owner(self, business_owner: str, account_ids: List):

        sort_dexter_triggers(self.dexter_strategy.time_buckets)
        required_fields = self.get_required_fields()

        for account_id in account_ids:
            self.analyze_account(business_owner, account_id, required_fields)

    def get_required_fields(self) -> List[str]:
        required_fields = set()
        try:
            for time_bucket in self.dexter_strategy.time_buckets:
                for trigger_metric in time_bucket.triggers:
                    add_metrics_to_set(required_fields, trigger_metric.trigger)
                    for cause in trigger_metric.cause_metrics:
                        for metric_clause in cause.metric_clauses:
                            add_metrics_to_set(required_fields, metric_clause)

        except Exception as e:
            logger.exception(f"Could not get the required fields || {repr(e)}")

        return list(required_fields)

    def analyze_account(self, business_owner: str, account_id: str, required_metrics: List[str]) -> None:

        self.journal_repository.update_journal_entry(
            business_owner,
            account_id,
            RunStatusDexterEngineJournal.IN_PROGRESS,
            ChannelEnum.FACEBOOK,
            self.dexter_strategy.ALGORITHM,
            start_time=datetime.now(),
        )

        has_errors = False

        for level in self.dexter_strategy.levels:
            for breakdown in self.dexter_strategy.breakdowns:
                for action_breakdown in self.dexter_strategy.action_breakdowns:

                    # Filter that have active status only.
                    filtering = create_facebook_filter(
                        FieldsMetadata.effective_status.name,
                        AgGridFacebookOperator.IN,
                        [EffectiveStatusEnum.ACTIVE.value],
                    )

                    # Structure is each campaign, each adset and each ad related to the ad_account.
                    structures = get_and_map_structures(f"act_{account_id}", level, filtering)

                    with concurrent.futures.ThreadPoolExecutor() as executor:
                        for structure in structures:
                            executor.submit(
                                self.get_recommendation_for_structure,
                                required_metrics,
                                level,
                                breakdown,
                                action_breakdown,
                                account_id,
                                structure,
                                business_owner,
                            )

        status = RunStatusDexterEngineJournal.FAILED if has_errors else RunStatusDexterEngineJournal.COMPLETED

        self.journal_repository.update_journal_entry(
            business_owner,
            account_id,
            status,
            ChannelEnum.FACEBOOK,
            self.dexter_strategy.ALGORITHM,
            end_time=datetime.now(),
        )

    def get_recommendation_for_structure(
        self,
        required_metrics: List,
        level: LevelEnum,
        breakdown: Field,
        action_breakdown: Field,
        account_id: str,
        structure: Dict,
        business_owner: str,
    ):
        try:

            results = get_dexter_insights(
                f"act_{account_id}",
                Level[level.value.upper()],
                breakdown,
                add_missing_fields(required_metrics, level, breakdown),
                get_fb_request_parameters(level, breakdown, action_breakdown, structure),
            )
            if not results:
                return

            grouped_data = self.get_grouped_data(results, level, breakdown)
            if not grouped_data:
                return

            self.dexter_strategy.generate_recommendation(
                grouped_data,
                level,
                breakdown,
                business_owner,
                account_id,
                structure,
                self.recommendations_repository,
            )

        except Exception as e:
            logger.exception(f"Dexter could not run for structure id || {repr(e)}")
            has_errors = True

    def get_grouped_data(
        self, metrics_data: List[Dict], level: LevelEnum, breakdown: Field
    ) -> List[BreakdownGroupedData]:

        result = []

        for daily_data in metrics_data:
            if FieldsMetadata.result_type.name not in daily_data:
                return []
            if daily_data[FieldsMetadata.result_type.name] not in [
                PixelCustomEventTypeToResult.PURCHASE.value.name,
                AdSetOptimizationToResult.OFFSITE_CONVERSIONS.value.name,
            ]:
                return []

        for time_bucket in self.dexter_strategy.time_buckets:
            if time_bucket.level != level or time_bucket.breakdown != breakdown:
                continue

            for trigger_metric in time_bucket.triggers:
                get_metric_group_data(time_bucket, trigger_metric.trigger, metrics_data, breakdown, result)

                for cause in trigger_metric.cause_metrics:
                    for metric_clause in cause.metric_clauses:
                        get_metric_group_data(time_bucket, metric_clause, metrics_data, breakdown, result)

        return result


def get_data_after_end_date(end_date: datetime, metric: FacebookField, metrics_data: List[Dict]) -> List[Dict]:
    result = []
    for metric_day in metrics_data:
        metric_end_date = datetime.strptime(metric_day[FieldsMetricStructureMetadata.date_stop.name], DEFAULT_DATETIME)
        if metric.is_dexter_custom_metric:
            metric_day.update({metric.name: CUSTOM_DEXTER_METRICS[metric.name].calculate_metric(metric_day)})

        if metric_end_date >= end_date and metric_day.get(metric.name, None) is not None:
            result.append(metric_day)

    return result


def add_metrics_to_set(required_fields: Set, metric: Union[MetricClause, CauseMetricBase]) -> None:
    required_fields.add(metric.metric_field.name)
    if not metric.metric_field.is_dexter_custom_metric:
        return

    required_fields.add(CUSTOM_DEXTER_METRICS[metric.metric_field.name].denominator)
    required_fields.add(CUSTOM_DEXTER_METRICS[metric.metric_field.name].numerator)


def get_metric_group_data(
    time_bucket: StrategyTimeBucket,
    metric: Union[MetricClause, CauseMetricBase],
    metrics_data: List[Dict],
    breakdown: Field,
    all_grouped_data: List[BreakdownGroupedData],
) -> None:
    end_date = datetime.now() - timedelta(time_bucket.no_of_days + 1)
    is_none_breakdown = breakdown == FieldsMetadata.breakdown_none

    if is_none_breakdown or not metric.metric_field.is_dexter_custom_metric:
        required_metrics = [metric.metric_field]
    else:
        required_metrics = metric.metric_field.composing_fields

    for metric in required_metrics:
        add_missing_metric_to_group(time_bucket, metric, metrics_data, breakdown, all_grouped_data, end_date)


def add_missing_metric_to_group(
    time_bucket: StrategyTimeBucket,
    metric_field: FacebookField,
    metrics_data: List[Dict],
    breakdown: Field,
    all_grouped_data: List[BreakdownGroupedData],
    end_date: datetime,
):
    existing_metric = False
    for grouped_data in all_grouped_data:
        if grouped_data.metric_name == metric_field.name and grouped_data.no_of_days == time_bucket.no_of_days:
            existing_metric = True

    if existing_metric:
        return

    bucket_data = get_data_after_end_date(end_date, metric_field, metrics_data)

    if len(bucket_data) < time_bucket.minimum_days_of_data:
        return

    breakdown_name = breakdown.name if breakdown != FieldsMetadata.breakdown_none else "breakdown"

    grouped_data = None

    for entry in bucket_data:
        if metric_field.name in entry and breakdown_name in entry:
            if not grouped_data:
                grouped_data = BreakdownGroupedData(
                    time_bucket.no_of_days,
                    metric_field.name,
                    [BreakdownData(entry[breakdown_name], [entry[metric_field.name]])],
                )
            elif grouped_data.get_breakdown_datapoints(entry[breakdown_name]):
                grouped_data.get_breakdown_datapoints(entry[breakdown_name]).append(entry[metric_field.name])
            else:
                grouped_data.breakdown_data.append(BreakdownData(entry[breakdown_name], [entry[metric_field.name]]))

    # If there is a breakdown, make sure that at least one breakdown has the minimum days of data
    if breakdown != FieldsMetadata.breakdown_none:
        if max([len(x.data_points) for x in grouped_data.breakdown_data]) < time_bucket.minimum_days_of_data:
            return

    all_grouped_data.append(grouped_data)


def add_missing_fields(required_metrics: List, level: LevelEnum, breakdown: Field) -> List[str]:
    dexter_insights_metrics = required_metrics + [
        FieldsMetadata.result_type.name,
        FieldsMetadata.date_start.name,
        FieldsMetadata.date_stop.name,
        LevelIdKeyEnum[level.value.upper()].value,
    ]

    if FieldsMetadata.results.name not in dexter_insights_metrics:
        dexter_insights_metrics.append(FieldsMetadata.results.name)

    if breakdown != FieldsMetadata.breakdown_none:
        dexter_insights_metrics.append(breakdown.name)

    return dexter_insights_metrics


def get_fb_request_parameters(level: LevelEnum, breakdown: Field, action_breakdown: Field, structure: Dict) -> Dict:
    structure_key = LevelToFacebookIdKeyMapping[level.value.upper()].value

    return {
        FacebookParametersStrings.level: level.value,
        FacebookParametersStrings.breakdowns: breakdown.facebook_fields,
        # For now this will be default on action_type
        FacebookParametersStrings.action_breakdowns: "action_type",
        FacebookParametersStrings.time_increment: FieldsMetadata.day.facebook_value,
        FacebookParametersStrings.time_range: {
            FacebookParametersStrings.since: (datetime.now() - timedelta(days=config.days_to_sync)).strftime(
                DEFAULT_DATETIME
            ),
            FacebookParametersStrings.until: datetime.now().strftime(DEFAULT_DATETIME),
        },
        FacebookParametersStrings.limit: 50,
        FacebookParametersStrings.filtering: [
            create_facebook_filter(
                structure_key.replace("_", "."), AgGridFacebookOperator.EQUAL, structure[structure_key]
            )
        ],
        FacebookParametersStrings.sort: "date_start",
    }


def sort_dexter_triggers(time_buckets: List[StrategyTimeBucket]):

    for time_bucket in time_buckets:
        sorted_triggers = []
        for trigger_metric in time_bucket.triggers:
            for cause_metric in trigger_metric.cause_metrics:
                sorted_triggers.append(TriggerMetric(trigger_metric.trigger, [cause_metric], trigger_metric.breakdown))

        sorted_triggers.sort(key=functools.cmp_to_key(trigger_compare))
        time_bucket.triggers = sorted_triggers


# Highest should be budget_increase, then any other action, then no action, then budget_decrease
ACTION_TYPE_PRIORITY = {
    ApplyActionType.BUDGET_INCREASE.name: 0,
    ApplyActionType.AGE_GENDER_BREAKDOWN_SPLIT.name: 2,
    ApplyActionType.DUPLICATE_AND_PAUSE_STRUCTURE.name: 2,
    ApplyActionType.CREATE_LOOKALIKE.name: 2,
    "NONE": 3,
    ApplyActionType.BUDGET_DECREASE.name: 4,
}


def trigger_compare(trigger1: TriggerMetric, trigger2: TriggerMetric):
    dexter_output1 = trigger1.cause_metrics[0].output.value
    dexter_output2 = trigger2.cause_metrics[0].output.value
    if dexter_output1.priority.value != dexter_output2.priority.value:
        return dexter_output1.priority.value < dexter_output2.priority.value

    dexter_apply_action1 = dexter_output1.apply_action_type.name if dexter_output1.apply_action_type else "NONE"
    dexter_apply_action2 = dexter_output2.apply_action_type.name if dexter_output2.apply_action_type else "NONE"

    return ACTION_TYPE_PRIORITY[dexter_apply_action1] < ACTION_TYPE_PRIORITY[dexter_apply_action2]
