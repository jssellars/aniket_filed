from Core.Dexter.Infrastructure.Domain.LevelEnums import LevelEnum
from Core.Web.FacebookGraphAPI.Models.FieldsMetadata import FieldsMetadata
from FacebookDexter.Infrastructure.DexterRules.BreakdownAndAudiencesTemplates import (
    AudienceRecommendationTemplate,
    BreakdownRecommendationTemplate,
)
from FacebookDexter.Infrastructure.DexterRules.OverTimeTrendBuckets.StrategyTimeBucket import (
    CauseMetricBase,
    MetricClause,
    StrategyTimeBucket,
    TrendEnum,
    TriggerMetric,
)

AGE_GENDER_BREAKDOWN_RULE = [
    TriggerMetric(
        trigger=MetricClause(
            FieldsMetadata.amount_spent,
            TrendEnum.INCREASING,
            variance_percentage=-30,
            is_divided_by_no_breakdowns=True,
        ),
        cause_metrics=[
            CauseMetricBase(
                metric_clauses=[
                    MetricClause(FieldsMetadata.cost_per_result, TrendEnum.INCREASING, variance_percentage=30)
                ],
                output=BreakdownRecommendationTemplate.AGE_GENDER_BREAKDOWN,
            )
        ],
    )
]

PLACEMENT_BREAKDOWN_RULE = [
    TriggerMetric(
        trigger=MetricClause(
            FieldsMetadata.amount_spent,
            TrendEnum.INCREASING,
            variance_percentage=-30,
            is_divided_by_no_breakdowns=True,
        ),
        cause_metrics=[
            CauseMetricBase(
                metric_clauses=[
                    MetricClause(FieldsMetadata.cost_per_result, TrendEnum.INCREASING, variance_percentage=30)
                ],
                output=BreakdownRecommendationTemplate.PLACEMENT_BREAKDOWN,
            )
        ],
    )
]

AGE_GENDER_BREAKDOWN_BUCKET = [
    StrategyTimeBucket(
        no_of_days=60,
        minimum_days_of_data=3,
        triggers=AGE_GENDER_BREAKDOWN_RULE,
        level=LevelEnum.ADSET,
        breakdown=FieldsMetadata.age_gender,
    ),
]

PLACEMENT_BREAKDOWN_BUCKET = [
    StrategyTimeBucket(
        no_of_days=60,
        minimum_days_of_data=3,
        triggers=PLACEMENT_BREAKDOWN_RULE,
        level=LevelEnum.ADSET,
        breakdown=FieldsMetadata.placement,
    ),
]

REACH_AUDIENCE_SIZE_RULE = [
    TriggerMetric(
        trigger=MetricClause(
            FieldsMetadata.reach,
            TrendEnum.INCREASING,
            variance_percentage=65,
            is_divided_by_no_breakdowns=True,
        ),
        cause_metrics=[
            CauseMetricBase(
                metric_clauses=[],
                output=AudienceRecommendationTemplate.AUDIENCE_EXHAUSTED,
            )
        ],
    )
]

AUDIENCE_SIZE_BUCKET = [
    StrategyTimeBucket(
        no_of_days=60,
        minimum_days_of_data=1,
        triggers=REACH_AUDIENCE_SIZE_RULE,
        level=LevelEnum.ADSET,
        breakdown=FieldsMetadata.breakdown_none,
    ),
]
