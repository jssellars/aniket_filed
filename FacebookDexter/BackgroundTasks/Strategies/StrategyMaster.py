import concurrent.futures
import logging
from dataclasses import asdict, dataclass
from datetime import datetime, timedelta
from enum import Enum
from typing import Dict, List, Set, Union

from bson import BSON

from Core.constants import DEFAULT_DATETIME
from Core.Dexter.Infrastructure.Domain.ChannelEnum import ChannelEnum
from Core.Dexter.Infrastructure.Domain.DexterJournalEnums import RunStatusDexterEngineJournal
from Core.Dexter.Infrastructure.Domain.LevelEnums import LevelEnum, LevelIdKeyEnum
from Core.mongo_adapter import MongoRepositoryBase
from Core.Tools.QueryBuilder.QueryBuilderLogicalOperator import AgGridFacebookOperator
from Core.Web.FacebookGraphAPI.GraphAPI.SdkGetStructures import (
    create_facebook_filter,
    get_dexter_insights,
    get_sdk_structures,
)
from Core.Web.FacebookGraphAPI.GraphAPIDomain.FacebookMiscFields import FacebookMiscFields
from Core.Web.FacebookGraphAPI.GraphAPIMappings.DexterCustomMetricMapper import CUSTOM_DEXTER_METRICS
from Core.Web.FacebookGraphAPI.GraphAPIMappings.FacebookToTuringStatusMapping import EffectiveStatusEnum
from Core.Web.FacebookGraphAPI.GraphAPIMappings.LevelMapping import Level
from Core.Web.FacebookGraphAPI.GraphAPIMappings.ObjectiveToResultsMapper import (
    AdSetOptimizationToResult,
    PixelCustomEventTypeToResult,
)
from Core.Web.FacebookGraphAPI.GraphAPIMappings.StructureMapping import StructureFields, StructureMapping
from Core.Web.FacebookGraphAPI.Models.Field import Field
from Core.Web.FacebookGraphAPI.Models.Field import Field as FacebookField
from Core.Web.FacebookGraphAPI.Models.FieldsMetadata import FieldsMetadata
from Core.Web.FacebookGraphAPI.Models.FieldsMetricStructureMetadata import FieldsMetricStructureMetadata
from FacebookDexter.BackgroundTasks.startup import config, fixtures
from FacebookDexter.BackgroundTasks.Strategies.AudienceSizeStrategy import AudienceSizeStrategy
from FacebookDexter.BackgroundTasks.Strategies.BreakdownStrategy import BreakdownAverageStrategy
from FacebookDexter.BackgroundTasks.Strategies.OverTimeTrendStrategy import OverTimeTrendStrategy
from FacebookDexter.BackgroundTasks.Strategies.StrategyBase import DexterStrategyBase
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

                    self.data_repository.set_structures_collection(level, config)

                    filtering = create_facebook_filter(
                        FieldsMetadata.effective_status.name,
                        AgGridFacebookOperator.IN,
                        [EffectiveStatusEnum.ACTIVE.value],
                    )

                    sdk_structures = get_sdk_structures(
                        f"act_{account_id}",
                        Level[level.value.upper()],
                        fields=StructureFields.get(level.value).get_structure_fields(),
                        params={"filtering": [filtering]},
                    )

                    structures = []

                    for structure in sdk_structures:
                        mapping = StructureMapping.get(level.value)
                        updated_structure = mapping.load(structure.export_all_data())
                        updated_structure = asdict(updated_structure)
                        updated_structure[FacebookMiscFields.details] = BSON.decode(
                            updated_structure.get(FacebookMiscFields.details)
                        )
                        structures.append(updated_structure)

                    self.data_repository.set_insights_collection(level, breakdown, action_breakdown, config)

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
            on_metrics = required_metrics + [
                FieldsMetadata.result_type.name,
                FieldsMetadata.date_start.name,
                FieldsMetadata.date_stop.name,
                LevelIdKeyEnum[level.value.upper()].value,
            ]
            if breakdown != FieldsMetadata.breakdown_none:
                on_metrics.append(breakdown.name)

            results = get_dexter_insights(
                f"act_{account_id}",
                Level[level.value.upper()],
                breakdown,
                action_breakdown,
                config.days_to_sync,
                on_metrics,
                structure,
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
