from Core.Dexter.Infrastructure.Domain.LevelEnums import LevelEnum
from Core.Web.FacebookGraphAPI.Models.FieldsMetadata import FieldsMetadata
from FacebookDexter.Infrastructure.DexterRules.OverTimeTrendBuckets.StrategyTimeBucket import (
    CauseMetricBase,
    MetricClause,
    StrategyTimeBucket,
    TrendEnum,
    TriggerMetric,
)
from FacebookDexter.Infrastructure.DexterRules.OverTimeTrendTemplates import OverTimeTrendTemplate

# THREE DAYS BUCKETS
THREE_DAYS_CONVERSION_RATE_DOWN = TriggerMetric(
    trigger=MetricClause(
        FieldsMetadata.conversion_rate,
        TrendEnum.DECREASING,
        variance_percentage=20,
    ),
    cause_metrics=[
        CauseMetricBase(
            metric_clauses=[
                MetricClause(FieldsMetadata.ctr_all, TrendEnum.DECREASING, variance_percentage=20),
                MetricClause(FieldsMetadata.cpc_all, TrendEnum.INCREASING, variance_percentage=20),
            ],
            output=OverTimeTrendTemplate.CR_DOWN_CTR_DOWN_CPC_UP,
        ),
        CauseMetricBase(
            metric_clauses=[
                MetricClause(FieldsMetadata.cpm, TrendEnum.INCREASING, variance_percentage=20),
            ],
            output=OverTimeTrendTemplate.CR_DOWN_CPM_UP,
        ),
    ],
)

THREE_DAYS_RESULTS_DOWN = TriggerMetric(
    trigger=MetricClause(FieldsMetadata.results, TrendEnum.DECREASING, variance_percentage=20),
    cause_metrics=[
        CauseMetricBase(
            metric_clauses=[
                MetricClause(FieldsMetadata.cpm, TrendEnum.INCREASING, variance_percentage=20),
                MetricClause(FieldsMetadata.conversion_rate, TrendEnum.DECREASING, variance_percentage=20),
            ],
            output=OverTimeTrendTemplate.RESULTS_DOWN_CPM_UP_CR_DOWN,
        ),
        CauseMetricBase(
            metric_clauses=[
                MetricClause(FieldsMetadata.cpc_all, TrendEnum.INCREASING, variance_percentage=20),
                MetricClause(FieldsMetadata.ctr_all, TrendEnum.INCREASING, variance_percentage=20),
            ],
            output=OverTimeTrendTemplate.RESULTS_DOWN_CPC_UP_CTR_UP,
        ),
        CauseMetricBase(
            metric_clauses=[
                MetricClause(FieldsMetadata.cpc_all, TrendEnum.INCREASING, variance_percentage=20),
                MetricClause(FieldsMetadata.ctr_all, TrendEnum.DECREASING, variance_percentage=20),
            ],
            output=OverTimeTrendTemplate.RESULTS_DOWN_CPC_UP_CTR_DOWN,
        ),
        CauseMetricBase(
            metric_clauses=[
                MetricClause(
                    FieldsMetadata.conversion_rate,
                    TrendEnum.DECREASING,
                    variance_percentage=20,
                ),
                MetricClause(
                    FieldsMetadata.cost_per_result,
                    TrendEnum.INCREASING,
                    variance_percentage=20,
                ),
            ],
            output=OverTimeTrendTemplate.RESULTS_DOWN_CR_DOWN_CPR_UP,
        ),
        CauseMetricBase(
            metric_clauses=[MetricClause(FieldsMetadata.unique_ctr_all, TrendEnum.INCREASING, variance_percentage=20)],
            output=OverTimeTrendTemplate.RESULTS_DOWN_UNIQUE_CTR_UP,
        ),
        CauseMetricBase(
            metric_clauses=[MetricClause(FieldsMetadata.unique_ctr_all, TrendEnum.DECREASING, variance_percentage=20)],
            output=OverTimeTrendTemplate.RESULTS_DOWN_UNIQUE_CTR_DOWN,
        ),
        CauseMetricBase(
            metric_clauses=[
                MetricClause(FieldsMetadata.amount_spent, TrendEnum.INCREASING, variance_percentage=20),
                MetricClause(FieldsMetadata.cpc_all, TrendEnum.INCREASING, variance_percentage=20),
            ],
            output=OverTimeTrendTemplate.RESULTS_DOWN_AMOUNT_SPENT_UP_CPC_UP,
        ),
        CauseMetricBase(
            metric_clauses=[
                MetricClause(FieldsMetadata.cost_per_result, TrendEnum.INCREASING, variance_percentage=20),
                MetricClause(FieldsMetadata.cpc_all, TrendEnum.INCREASING, variance_percentage=20),
            ],
            output=OverTimeTrendTemplate.RESULTS_DOWN_CPR_UP_CPC_UP,
        ),
    ],
)

THREE_DAYS_RESULTS_UP = TriggerMetric(
    trigger=MetricClause(FieldsMetadata.results, TrendEnum.INCREASING, variance_percentage=20),
    cause_metrics=[
        CauseMetricBase(
            metric_clauses=[MetricClause(FieldsMetadata.unique_ctr_all, TrendEnum.DECREASING, variance_percentage=20)],
            output=OverTimeTrendTemplate.RESULTS_UP_UNIQUE_CTR_DOWN,
        ),
        CauseMetricBase(
            metric_clauses=[
                MetricClause(FieldsMetadata.cpc_all, TrendEnum.DECREASING, variance_percentage=20),
                MetricClause(FieldsMetadata.ctr_all, TrendEnum.INCREASING, variance_percentage=20),
            ],
            output=OverTimeTrendTemplate.RESULTS_UP_CPC_DOWN_CTR_UP,
        ),
        CauseMetricBase(
            metric_clauses=[
                MetricClause(FieldsMetadata.cpc_all, TrendEnum.DECREASING, variance_percentage=20),
                MetricClause(FieldsMetadata.cpm, TrendEnum.DECREASING, variance_percentage=20),
            ],
            output=OverTimeTrendTemplate.RESULTS_UP_CPC_DOWN_CPM_DOWN,
        ),
        CauseMetricBase(
            metric_clauses=[
                MetricClause(FieldsMetadata.cpc_all, TrendEnum.DECREASING, variance_percentage=20),
                MetricClause(FieldsMetadata.ctr_all, TrendEnum.INCREASING, variance_percentage=20),
                MetricClause(FieldsMetadata.cpm, TrendEnum.DECREASING, variance_percentage=20),
            ],
            output=OverTimeTrendTemplate.RESULTS_UP_CPC_DOWN_CTR_UP_CPM_DOWN,
        ),
        CauseMetricBase(
            metric_clauses=[
                MetricClause(FieldsMetadata.amount_spent, TrendEnum.INCREASING, variance_percentage=20),
                MetricClause(FieldsMetadata.cpc_all, TrendEnum.DECREASING, variance_percentage=20),
                MetricClause(FieldsMetadata.cpm, TrendEnum.DECREASING, variance_percentage=20),
            ],
            output=OverTimeTrendTemplate.RESULTS_UP_AMOUNT_SPENT_UP_CPC_DOWN_CPM_DOWN,
        ),
        CauseMetricBase(
            metric_clauses=[
                MetricClause(FieldsMetadata.cost_per_result, TrendEnum.DECREASING, variance_percentage=20),
                MetricClause(FieldsMetadata.cpm, TrendEnum.DECREASING, variance_percentage=20),
            ],
            output=OverTimeTrendTemplate.RESULTS_UP_CPR_DOWN_CPM_DOWN,
        ),
    ],
)

THREE_DAYS_CTR_DOWN = TriggerMetric(
    trigger=MetricClause(FieldsMetadata.ctr_all, TrendEnum.DECREASING, variance_percentage=20),
    cause_metrics=[
        CauseMetricBase(
            metric_clauses=[
                MetricClause(FieldsMetadata.cpm, TrendEnum.INCREASING, variance_percentage=20),
                MetricClause(FieldsMetadata.cpc_all, TrendEnum.INCREASING, variance_percentage=20),
            ],
            output=OverTimeTrendTemplate.CTR_DOWN_CPM_UP_CPC_UP,
        ),
    ],
)

THREE_DAYS_CTR_UP = TriggerMetric(
    trigger=MetricClause(FieldsMetadata.ctr_all, TrendEnum.INCREASING, variance_percentage=20),
    cause_metrics=[
        CauseMetricBase(
            metric_clauses=[
                MetricClause(FieldsMetadata.cpm, TrendEnum.DECREASING, variance_percentage=20),
                MetricClause(FieldsMetadata.cpc_all, TrendEnum.DECREASING, variance_percentage=20),
            ],
            output=OverTimeTrendTemplate.CTR_UP_CPM_DOWN_CPC_DOWN,
        ),
    ],
)

THREE_DAYS_CPM_UP = TriggerMetric(
    trigger=MetricClause(FieldsMetadata.cpm, TrendEnum.INCREASING, variance_percentage=20),
    cause_metrics=[
        CauseMetricBase(
            metric_clauses=[
                MetricClause(FieldsMetadata.results, TrendEnum.DECREASING, variance_percentage=20),
                MetricClause(FieldsMetadata.ctr_all, TrendEnum.INCREASING, variance_percentage=20),
            ],
            output=OverTimeTrendTemplate.CPM_UP_RESULTS_DOWN_CTR_UP,
        ),
        CauseMetricBase(
            metric_clauses=[
                MetricClause(FieldsMetadata.results, TrendEnum.DECREASING, variance_percentage=20),
                MetricClause(FieldsMetadata.cost_per_result, TrendEnum.INCREASING, variance_percentage=20),
            ],
            output=OverTimeTrendTemplate.CPM_UP_RESULTS_DOWN_CPR_UP,
        ),
    ],
)

THREE_DAYS_CLICKS_DOWN = TriggerMetric(
    trigger=MetricClause(FieldsMetadata.clicks_all, TrendEnum.DECREASING, variance_percentage=20),
    cause_metrics=[
        CauseMetricBase(
            metric_clauses=[
                MetricClause(FieldsMetadata.cpc_all, TrendEnum.INCREASING, variance_percentage=20),
            ],
            output=OverTimeTrendTemplate.CLICKS_DOWN_CPC_UP,
        ),
        CauseMetricBase(
            metric_clauses=[
                MetricClause(FieldsMetadata.cpm, TrendEnum.INCREASING, variance_percentage=20),
            ],
            output=OverTimeTrendTemplate.CLICKS_DOWN_CPM_UP,
        ),
    ],
)

THREE_DAYS_CLICKS_UP = TriggerMetric(
    trigger=MetricClause(FieldsMetadata.clicks_all, TrendEnum.INCREASING, variance_percentage=20),
    cause_metrics=[
        CauseMetricBase(
            metric_clauses=[
                MetricClause(FieldsMetadata.ctr_all, TrendEnum.INCREASING, variance_percentage=20),
                MetricClause(FieldsMetadata.cpc_all, TrendEnum.DECREASING, variance_percentage=20),
                MetricClause(FieldsMetadata.cpm, TrendEnum.DECREASING, variance_percentage=20),
            ],
            output=OverTimeTrendTemplate.CLICK_UP_CTR_UP_CPC_DOWN_CPM_DOWN,
        ),
    ],
)

THREE_DAYS_AMOUNT_SPENT_DOWN = TriggerMetric(
    trigger=MetricClause(FieldsMetadata.amount_spent, TrendEnum.DECREASING, variance_percentage=20),
    cause_metrics=[
        CauseMetricBase(
            metric_clauses=[
                MetricClause(
                    FieldsMetadata.cost_per_result,
                    TrendEnum.INCREASING,
                    variance_percentage=20,
                )
            ],
            output=OverTimeTrendTemplate.AMOUNT_SPENT_DOWN_CPR_UP,
        ),
        CauseMetricBase(
            metric_clauses=[
                MetricClause(
                    FieldsMetadata.cost_per_result,
                    TrendEnum.DECREASING,
                    variance_percentage=20,
                )
            ],
            output=OverTimeTrendTemplate.AMOUNT_SPENT_DOWN_CPR_DOWN,
        ),
        CauseMetricBase(
            metric_clauses=[MetricClause(FieldsMetadata.results, TrendEnum.INCREASING, variance_percentage=20)],
            output=OverTimeTrendTemplate.AMOUNT_SPENT_DOWN_RESULTS_UP,
        ),
    ],
)

THREE_DAYS_AMOUNT_SPENT_UP = TriggerMetric(
    trigger=MetricClause(FieldsMetadata.amount_spent, TrendEnum.INCREASING, variance_percentage=20),
    cause_metrics=[
        CauseMetricBase(
            metric_clauses=[
                MetricClause(
                    FieldsMetadata.cost_per_result,
                    TrendEnum.INCREASING,
                    variance_percentage=20,
                )
            ],
            output=OverTimeTrendTemplate.AMOUNT_SPENT_UP_CPR_UP,
        ),
        CauseMetricBase(
            metric_clauses=[
                MetricClause(
                    FieldsMetadata.cost_per_result,
                    TrendEnum.DECREASING,
                    variance_percentage=20,
                )
            ],
            output=OverTimeTrendTemplate.AMOUNT_SPENT_UP_CPR_DOWN,
        ),
    ],
)

THREE_DAYS_COST_PER_RESULT_UP = TriggerMetric(
    trigger=MetricClause(
        FieldsMetadata.cost_per_result,
        TrendEnum.INCREASING,
        variance_percentage=20,
    ),
    cause_metrics=[
        CauseMetricBase(
            metric_clauses=[MetricClause(FieldsMetadata.impressions, TrendEnum.DECREASING, variance_percentage=20)],
            output=OverTimeTrendTemplate.CPR_UP_IMPRESSIONS_DOWN,
        )
    ],
)

THREE_DAYS_LANDING_PAGE_CONVERSION_RATE_DOWN = TriggerMetric(
    trigger=MetricClause(
        FieldsMetadata.landing_page_conversion_rate,
        TrendEnum.DECREASING,
        variance_percentage=20,
    ),
    cause_metrics=[
        CauseMetricBase(
            metric_clauses=[
                MetricClause(FieldsMetadata.unique_clicks_all, TrendEnum.INCREASING, variance_percentage=20)
            ],
            output=OverTimeTrendTemplate.LANDING_PAGE_CONVERSION_RATE_DOWN_UNIQUE_CLICKS_UP,
        )
    ],
)

THREE_DAYS_BUCKET = [
    THREE_DAYS_CONVERSION_RATE_DOWN,
    THREE_DAYS_RESULTS_DOWN,
    THREE_DAYS_RESULTS_UP,
    THREE_DAYS_CTR_DOWN,
    THREE_DAYS_CTR_UP,
    THREE_DAYS_CPM_UP,
    THREE_DAYS_AMOUNT_SPENT_UP,
    THREE_DAYS_AMOUNT_SPENT_DOWN,
    THREE_DAYS_COST_PER_RESULT_UP,
    THREE_DAYS_LANDING_PAGE_CONVERSION_RATE_DOWN,
    THREE_DAYS_CLICKS_DOWN,
    THREE_DAYS_CLICKS_UP,
]

# SEVEN DAYS BUCKETS
SEVEN_DAYS_CONVERSION_RATE_DOWN = TriggerMetric(
    trigger=MetricClause(
        FieldsMetadata.conversion_rate,
        TrendEnum.DECREASING,
        variance_percentage=20,
    ),
    cause_metrics=[
        CauseMetricBase(
            metric_clauses=[
                MetricClause(FieldsMetadata.ctr_all, TrendEnum.DECREASING, variance_percentage=20),
                MetricClause(FieldsMetadata.cpc_all, TrendEnum.INCREASING, variance_percentage=20),
            ],
            output=OverTimeTrendTemplate.CR_DOWN_CTR_DOWN_CPC_UP,
        ),
        CauseMetricBase(
            metric_clauses=[
                MetricClause(FieldsMetadata.cpm, TrendEnum.INCREASING, variance_percentage=20),
            ],
            output=OverTimeTrendTemplate.CR_DOWN_CPM_UP,
        ),
    ],
)

SEVEN_DAYS_RESULTS_DOWN = TriggerMetric(
    trigger=MetricClause(FieldsMetadata.results, TrendEnum.DECREASING, variance_percentage=20),
    cause_metrics=[
        CauseMetricBase(
            metric_clauses=[
                MetricClause(FieldsMetadata.cpm, TrendEnum.INCREASING, variance_percentage=20),
                MetricClause(FieldsMetadata.conversion_rate, TrendEnum.DECREASING, variance_percentage=20),
            ],
            output=OverTimeTrendTemplate.RESULTS_DOWN_CPM_UP_CR_DOWN,
        ),
        CauseMetricBase(
            metric_clauses=[
                MetricClause(FieldsMetadata.cpc_all, TrendEnum.INCREASING, variance_percentage=20),
                MetricClause(FieldsMetadata.ctr_all, TrendEnum.INCREASING, variance_percentage=20),
            ],
            output=OverTimeTrendTemplate.RESULTS_DOWN_CPC_UP_CTR_UP,
        ),
        CauseMetricBase(
            metric_clauses=[
                MetricClause(FieldsMetadata.cpc_all, TrendEnum.INCREASING, variance_percentage=20),
                MetricClause(FieldsMetadata.ctr_all, TrendEnum.DECREASING, variance_percentage=20),
            ],
            output=OverTimeTrendTemplate.RESULTS_DOWN_CPC_UP_CTR_DOWN,
        ),
        CauseMetricBase(
            metric_clauses=[
                MetricClause(
                    FieldsMetadata.conversion_rate,
                    TrendEnum.DECREASING,
                    variance_percentage=20,
                ),
                MetricClause(
                    FieldsMetadata.cost_per_result,
                    TrendEnum.INCREASING,
                    variance_percentage=20,
                ),
            ],
            output=OverTimeTrendTemplate.RESULTS_DOWN_CR_DOWN_CPR_UP,
        ),
        CauseMetricBase(
            metric_clauses=[MetricClause(FieldsMetadata.unique_ctr_all, TrendEnum.INCREASING, variance_percentage=20)],
            output=OverTimeTrendTemplate.RESULTS_DOWN_UNIQUE_CTR_UP,
        ),
        CauseMetricBase(
            metric_clauses=[MetricClause(FieldsMetadata.unique_ctr_all, TrendEnum.DECREASING, variance_percentage=20)],
            output=OverTimeTrendTemplate.RESULTS_DOWN_UNIQUE_CTR_DOWN,
        ),
        CauseMetricBase(
            metric_clauses=[
                MetricClause(FieldsMetadata.amount_spent, TrendEnum.INCREASING, variance_percentage=20),
                MetricClause(FieldsMetadata.cpc_all, TrendEnum.INCREASING, variance_percentage=20),
            ],
            output=OverTimeTrendTemplate.RESULTS_DOWN_AMOUNT_SPENT_UP_CPC_UP,
        ),
        CauseMetricBase(
            metric_clauses=[
                MetricClause(FieldsMetadata.cost_per_result, TrendEnum.INCREASING, variance_percentage=20),
                MetricClause(FieldsMetadata.cpc_all, TrendEnum.INCREASING, variance_percentage=20),
            ],
            output=OverTimeTrendTemplate.RESULTS_DOWN_CPR_UP_CPC_UP,
        ),
    ],
)

SEVEN_DAYS_RESULTS_UP = TriggerMetric(
    trigger=MetricClause(FieldsMetadata.results, TrendEnum.INCREASING, variance_percentage=20),
    cause_metrics=[
        CauseMetricBase(
            metric_clauses=[MetricClause(FieldsMetadata.unique_ctr_all, TrendEnum.DECREASING, variance_percentage=20)],
            output=OverTimeTrendTemplate.RESULTS_UP_UNIQUE_CTR_DOWN,
        ),
        CauseMetricBase(
            metric_clauses=[
                MetricClause(FieldsMetadata.cpc_all, TrendEnum.DECREASING, variance_percentage=20),
                MetricClause(FieldsMetadata.ctr_all, TrendEnum.INCREASING, variance_percentage=20),
            ],
            output=OverTimeTrendTemplate.RESULTS_UP_CPC_DOWN_CTR_UP,
        ),
        CauseMetricBase(
            metric_clauses=[
                MetricClause(FieldsMetadata.cpc_all, TrendEnum.DECREASING, variance_percentage=20),
                MetricClause(FieldsMetadata.cpm, TrendEnum.DECREASING, variance_percentage=20),
            ],
            output=OverTimeTrendTemplate.RESULTS_UP_CPC_DOWN_CPM_DOWN,
        ),
        CauseMetricBase(
            metric_clauses=[
                MetricClause(FieldsMetadata.cpc_all, TrendEnum.DECREASING, variance_percentage=20),
                MetricClause(FieldsMetadata.ctr_all, TrendEnum.INCREASING, variance_percentage=20),
                MetricClause(FieldsMetadata.cpm, TrendEnum.DECREASING, variance_percentage=20),
            ],
            output=OverTimeTrendTemplate.RESULTS_UP_CPC_DOWN_CTR_UP_CPM_DOWN,
        ),
        CauseMetricBase(
            metric_clauses=[
                MetricClause(FieldsMetadata.amount_spent, TrendEnum.INCREASING, variance_percentage=20),
                MetricClause(FieldsMetadata.cpc_all, TrendEnum.DECREASING, variance_percentage=20),
                MetricClause(FieldsMetadata.cpm, TrendEnum.DECREASING, variance_percentage=20),
            ],
            output=OverTimeTrendTemplate.RESULTS_UP_AMOUNT_SPENT_UP_CPC_DOWN_CPM_DOWN,
        ),
        CauseMetricBase(
            metric_clauses=[
                MetricClause(FieldsMetadata.cost_per_result, TrendEnum.DECREASING, variance_percentage=20),
                MetricClause(FieldsMetadata.cpm, TrendEnum.DECREASING, variance_percentage=20),
            ],
            output=OverTimeTrendTemplate.RESULTS_UP_CPR_DOWN_CPM_DOWN,
        ),
    ],
)

SEVEN_DAYS_CTR_DOWN = TriggerMetric(
    trigger=MetricClause(FieldsMetadata.ctr_all, TrendEnum.DECREASING, variance_percentage=20),
    cause_metrics=[
        CauseMetricBase(
            metric_clauses=[
                MetricClause(FieldsMetadata.cpm, TrendEnum.INCREASING, variance_percentage=20),
                MetricClause(FieldsMetadata.cpc_all, TrendEnum.INCREASING, variance_percentage=20),
            ],
            output=OverTimeTrendTemplate.CTR_DOWN_CPM_UP_CPC_UP,
        ),
    ],
)

SEVEN_DAYS_CTR_UP = TriggerMetric(
    trigger=MetricClause(FieldsMetadata.ctr_all, TrendEnum.INCREASING, variance_percentage=20),
    cause_metrics=[
        CauseMetricBase(
            metric_clauses=[
                MetricClause(FieldsMetadata.cpm, TrendEnum.DECREASING, variance_percentage=20),
                MetricClause(FieldsMetadata.cpc_all, TrendEnum.DECREASING, variance_percentage=20),
            ],
            output=OverTimeTrendTemplate.CTR_UP_CPM_DOWN_CPC_DOWN,
        ),
    ],
)

SEVEN_DAYS_CPM_UP = TriggerMetric(
    trigger=MetricClause(FieldsMetadata.cpm, TrendEnum.INCREASING, variance_percentage=20),
    cause_metrics=[
        CauseMetricBase(
            metric_clauses=[
                MetricClause(FieldsMetadata.results, TrendEnum.DECREASING, variance_percentage=20),
                MetricClause(FieldsMetadata.ctr_all, TrendEnum.INCREASING, variance_percentage=20),
            ],
            output=OverTimeTrendTemplate.CPM_UP_RESULTS_DOWN_CTR_UP,
        ),
        CauseMetricBase(
            metric_clauses=[
                MetricClause(FieldsMetadata.results, TrendEnum.DECREASING, variance_percentage=20),
                MetricClause(FieldsMetadata.cost_per_result, TrendEnum.INCREASING, variance_percentage=20),
            ],
            output=OverTimeTrendTemplate.CPM_UP_RESULTS_DOWN_CPR_UP,
        ),
    ],
)

SEVEN_DAYS_CLICKS_DOWN = TriggerMetric(
    trigger=MetricClause(FieldsMetadata.clicks_all, TrendEnum.DECREASING, variance_percentage=20),
    cause_metrics=[
        CauseMetricBase(
            metric_clauses=[
                MetricClause(FieldsMetadata.cpc_all, TrendEnum.INCREASING, variance_percentage=20),
            ],
            output=OverTimeTrendTemplate.CLICKS_DOWN_CPC_UP,
        ),
        CauseMetricBase(
            metric_clauses=[
                MetricClause(FieldsMetadata.cpm, TrendEnum.INCREASING, variance_percentage=20),
            ],
            output=OverTimeTrendTemplate.CLICKS_DOWN_CPM_UP,
        ),
    ],
)

SEVEN_DAYS_CLICKS_UP = TriggerMetric(
    trigger=MetricClause(FieldsMetadata.clicks_all, TrendEnum.INCREASING, variance_percentage=20),
    cause_metrics=[
        CauseMetricBase(
            metric_clauses=[
                MetricClause(FieldsMetadata.ctr_all, TrendEnum.INCREASING, variance_percentage=20),
                MetricClause(FieldsMetadata.cpc_all, TrendEnum.DECREASING, variance_percentage=20),
                MetricClause(FieldsMetadata.cpm, TrendEnum.DECREASING, variance_percentage=20),
            ],
            output=OverTimeTrendTemplate.CLICK_UP_CTR_UP_CPC_DOWN_CPM_DOWN,
        ),
    ],
)

SEVEN_DAYS_AMOUNT_SPENT_DOWN = TriggerMetric(
    trigger=MetricClause(FieldsMetadata.amount_spent, TrendEnum.DECREASING, variance_percentage=20),
    cause_metrics=[
        CauseMetricBase(
            metric_clauses=[
                MetricClause(
                    FieldsMetadata.cost_per_result,
                    TrendEnum.INCREASING,
                    variance_percentage=20,
                )
            ],
            output=OverTimeTrendTemplate.AMOUNT_SPENT_DOWN_CPR_UP,
        ),
        CauseMetricBase(
            metric_clauses=[
                MetricClause(
                    FieldsMetadata.cost_per_result,
                    TrendEnum.DECREASING,
                    variance_percentage=20,
                )
            ],
            output=OverTimeTrendTemplate.AMOUNT_SPENT_DOWN_CPR_DOWN,
        ),
        CauseMetricBase(
            metric_clauses=[MetricClause(FieldsMetadata.results, TrendEnum.INCREASING, variance_percentage=20)],
            output=OverTimeTrendTemplate.AMOUNT_SPENT_DOWN_RESULTS_UP,
        ),
    ],
)

SEVEN_DAYS_AMOUNT_SPENT_UP = TriggerMetric(
    trigger=MetricClause(FieldsMetadata.amount_spent, TrendEnum.INCREASING, variance_percentage=20),
    cause_metrics=[
        CauseMetricBase(
            metric_clauses=[
                MetricClause(
                    FieldsMetadata.cost_per_result,
                    TrendEnum.INCREASING,
                    variance_percentage=20,
                )
            ],
            output=OverTimeTrendTemplate.AMOUNT_SPENT_UP_CPR_UP,
        ),
        CauseMetricBase(
            metric_clauses=[
                MetricClause(
                    FieldsMetadata.cost_per_result,
                    TrendEnum.DECREASING,
                    variance_percentage=20,
                )
            ],
            output=OverTimeTrendTemplate.AMOUNT_SPENT_UP_CPR_DOWN,
        ),
    ],
)

SEVEN_DAYS_COST_PER_RESULT_UP = TriggerMetric(
    trigger=MetricClause(
        FieldsMetadata.cost_per_result,
        TrendEnum.INCREASING,
        variance_percentage=20,
    ),
    cause_metrics=[
        CauseMetricBase(
            metric_clauses=[MetricClause(FieldsMetadata.impressions, TrendEnum.DECREASING, variance_percentage=20)],
            output=OverTimeTrendTemplate.CPR_UP_IMPRESSIONS_DOWN,
        )
    ],
)

SEVEN_DAYS_LANDING_PAGE_CONVERSION_RATE_DOWN = TriggerMetric(
    trigger=MetricClause(
        FieldsMetadata.landing_page_conversion_rate,
        TrendEnum.DECREASING,
        variance_percentage=20,
    ),
    cause_metrics=[
        CauseMetricBase(
            metric_clauses=[
                MetricClause(FieldsMetadata.unique_clicks_all, TrendEnum.INCREASING, variance_percentage=20)
            ],
            output=OverTimeTrendTemplate.LANDING_PAGE_CONVERSION_RATE_DOWN_UNIQUE_CLICKS_UP,
        )
    ],
)

SEVEN_DAYS_BUCKET = [
    SEVEN_DAYS_CONVERSION_RATE_DOWN,
    SEVEN_DAYS_RESULTS_DOWN,
    SEVEN_DAYS_RESULTS_UP,
    SEVEN_DAYS_CTR_DOWN,
    SEVEN_DAYS_CTR_UP,
    SEVEN_DAYS_CPM_UP,
    SEVEN_DAYS_AMOUNT_SPENT_UP,
    SEVEN_DAYS_AMOUNT_SPENT_DOWN,
    SEVEN_DAYS_COST_PER_RESULT_UP,
    SEVEN_DAYS_LANDING_PAGE_CONVERSION_RATE_DOWN,
    SEVEN_DAYS_CLICKS_DOWN,
    SEVEN_DAYS_CLICKS_UP,
]

# FOURTEEN DAYS BUCKETS
FOURTEEN_DAYS_CONVERSION_RATE_DOWN = TriggerMetric(
    trigger=MetricClause(
        FieldsMetadata.conversion_rate,
        TrendEnum.DECREASING,
        variance_percentage=20,
    ),
    cause_metrics=[
        CauseMetricBase(
            metric_clauses=[
                MetricClause(FieldsMetadata.ctr_all, TrendEnum.DECREASING, variance_percentage=20),
                MetricClause(FieldsMetadata.cpc_all, TrendEnum.INCREASING, variance_percentage=20),
            ],
            output=OverTimeTrendTemplate.CR_DOWN_CTR_DOWN_CPC_UP,
        ),
        CauseMetricBase(
            metric_clauses=[
                MetricClause(FieldsMetadata.cpm, TrendEnum.INCREASING, variance_percentage=20),
            ],
            output=OverTimeTrendTemplate.CR_DOWN_CPM_UP,
        ),
    ],
)

FOURTEEN_DAYS_RESULTS_DOWN = TriggerMetric(
    trigger=MetricClause(FieldsMetadata.results, TrendEnum.DECREASING, variance_percentage=20),
    cause_metrics=[
        CauseMetricBase(
            metric_clauses=[
                MetricClause(FieldsMetadata.cpm, TrendEnum.INCREASING, variance_percentage=20),
                MetricClause(FieldsMetadata.conversion_rate, TrendEnum.DECREASING, variance_percentage=20),
            ],
            output=OverTimeTrendTemplate.RESULTS_DOWN_CPM_UP_CR_DOWN,
        ),
        CauseMetricBase(
            metric_clauses=[
                MetricClause(FieldsMetadata.cpc_all, TrendEnum.INCREASING, variance_percentage=20),
                MetricClause(FieldsMetadata.ctr_all, TrendEnum.INCREASING, variance_percentage=20),
            ],
            output=OverTimeTrendTemplate.RESULTS_DOWN_CPC_UP_CTR_UP,
        ),
        CauseMetricBase(
            metric_clauses=[
                MetricClause(FieldsMetadata.cpc_all, TrendEnum.INCREASING, variance_percentage=20),
                MetricClause(FieldsMetadata.ctr_all, TrendEnum.DECREASING, variance_percentage=20),
            ],
            output=OverTimeTrendTemplate.RESULTS_DOWN_CPC_UP_CTR_DOWN,
        ),
        CauseMetricBase(
            metric_clauses=[
                MetricClause(
                    FieldsMetadata.conversion_rate,
                    TrendEnum.DECREASING,
                    variance_percentage=20,
                ),
                MetricClause(
                    FieldsMetadata.cost_per_result,
                    TrendEnum.INCREASING,
                    variance_percentage=20,
                ),
            ],
            output=OverTimeTrendTemplate.RESULTS_DOWN_CR_DOWN_CPR_UP,
        ),
        CauseMetricBase(
            metric_clauses=[MetricClause(FieldsMetadata.unique_ctr_all, TrendEnum.INCREASING, variance_percentage=20)],
            output=OverTimeTrendTemplate.RESULTS_DOWN_UNIQUE_CTR_UP,
        ),
        CauseMetricBase(
            metric_clauses=[MetricClause(FieldsMetadata.unique_ctr_all, TrendEnum.DECREASING, variance_percentage=20)],
            output=OverTimeTrendTemplate.RESULTS_DOWN_UNIQUE_CTR_DOWN,
        ),
        CauseMetricBase(
            metric_clauses=[
                MetricClause(FieldsMetadata.amount_spent, TrendEnum.INCREASING, variance_percentage=20),
                MetricClause(FieldsMetadata.cpc_all, TrendEnum.INCREASING, variance_percentage=20),
            ],
            output=OverTimeTrendTemplate.RESULTS_DOWN_AMOUNT_SPENT_UP_CPC_UP,
        ),
        CauseMetricBase(
            metric_clauses=[
                MetricClause(FieldsMetadata.cost_per_result, TrendEnum.INCREASING, variance_percentage=20),
                MetricClause(FieldsMetadata.cpc_all, TrendEnum.INCREASING, variance_percentage=20),
            ],
            output=OverTimeTrendTemplate.RESULTS_DOWN_CPR_UP_CPC_UP,
        ),
    ],
)

FOURTEEN_DAYS_RESULTS_UP = TriggerMetric(
    trigger=MetricClause(FieldsMetadata.results, TrendEnum.INCREASING, variance_percentage=20),
    cause_metrics=[
        CauseMetricBase(
            metric_clauses=[
                MetricClause(FieldsMetadata.unique_clicks_all, TrendEnum.INCREASING, variance_percentage=20),
            ],
            output=OverTimeTrendTemplate.RESULTS_UP_UNIQUE_CLICKS_UP,
        ),
        CauseMetricBase(
            metric_clauses=[MetricClause(FieldsMetadata.unique_ctr_all, TrendEnum.DECREASING, variance_percentage=20)],
            output=OverTimeTrendTemplate.RESULTS_UP_UNIQUE_CTR_DOWN,
        ),
        CauseMetricBase(
            metric_clauses=[
                MetricClause(FieldsMetadata.cpc_all, TrendEnum.DECREASING, variance_percentage=20),
                MetricClause(FieldsMetadata.ctr_all, TrendEnum.INCREASING, variance_percentage=20),
            ],
            output=OverTimeTrendTemplate.RESULTS_UP_CPC_DOWN_CTR_UP,
        ),
        CauseMetricBase(
            metric_clauses=[
                MetricClause(FieldsMetadata.cpc_all, TrendEnum.DECREASING, variance_percentage=20),
                MetricClause(FieldsMetadata.cpm, TrendEnum.DECREASING, variance_percentage=20),
            ],
            output=OverTimeTrendTemplate.RESULTS_UP_CPC_DOWN_CPM_DOWN,
        ),
        CauseMetricBase(
            metric_clauses=[
                MetricClause(FieldsMetadata.cpc_all, TrendEnum.DECREASING, variance_percentage=20),
                MetricClause(FieldsMetadata.ctr_all, TrendEnum.INCREASING, variance_percentage=20),
                MetricClause(FieldsMetadata.cpm, TrendEnum.DECREASING, variance_percentage=20),
            ],
            output=OverTimeTrendTemplate.RESULTS_UP_CPC_DOWN_CTR_UP_CPM_DOWN,
        ),
        CauseMetricBase(
            metric_clauses=[
                MetricClause(FieldsMetadata.amount_spent, TrendEnum.INCREASING, variance_percentage=20),
                MetricClause(FieldsMetadata.cpc_all, TrendEnum.DECREASING, variance_percentage=20),
                MetricClause(FieldsMetadata.cpm, TrendEnum.DECREASING, variance_percentage=20),
            ],
            output=OverTimeTrendTemplate.RESULTS_UP_AMOUNT_SPENT_UP_CPC_DOWN_CPM_DOWN,
        ),
        CauseMetricBase(
            metric_clauses=[
                MetricClause(FieldsMetadata.cost_per_result, TrendEnum.DECREASING, variance_percentage=20),
                MetricClause(FieldsMetadata.cpm, TrendEnum.DECREASING, variance_percentage=20),
            ],
            output=OverTimeTrendTemplate.RESULTS_UP_CPR_DOWN_CPM_DOWN,
        ),
    ],
)

FOURTEEN_DAYS_CTR_DOWN = TriggerMetric(
    trigger=MetricClause(FieldsMetadata.ctr_all, TrendEnum.DECREASING, variance_percentage=20),
    cause_metrics=[
        CauseMetricBase(
            metric_clauses=[
                MetricClause(
                    FieldsMetadata.cost_per_result,
                    TrendEnum.INCREASING,
                    variance_percentage=20,
                ),
                MetricClause(
                    FieldsMetadata.cpm,
                    TrendEnum.INCREASING,
                    variance_percentage=20,
                ),
            ],
            output=OverTimeTrendTemplate.CTR_DOWN_CPR_UP_CPM_UP,
        ),
        CauseMetricBase(
            metric_clauses=[
                MetricClause(FieldsMetadata.cpm, TrendEnum.INCREASING, variance_percentage=20),
                MetricClause(FieldsMetadata.cpc_all, TrendEnum.INCREASING, variance_percentage=20),
            ],
            output=OverTimeTrendTemplate.CTR_DOWN_CPM_UP_CPC_UP,
        ),
    ],
)

FOURTEEN_DAYS_CTR_UP = TriggerMetric(
    trigger=MetricClause(FieldsMetadata.ctr_all, TrendEnum.INCREASING, variance_percentage=20),
    cause_metrics=[
        CauseMetricBase(
            metric_clauses=[
                MetricClause(FieldsMetadata.cpm, TrendEnum.DECREASING, variance_percentage=20),
                MetricClause(FieldsMetadata.cpc_all, TrendEnum.DECREASING, variance_percentage=20),
            ],
            output=OverTimeTrendTemplate.CTR_UP_CPM_DOWN_CPC_DOWN,
        ),
    ],
)

FOURTEEN_DAYS_CPM_UP = TriggerMetric(
    trigger=MetricClause(FieldsMetadata.cpm, TrendEnum.INCREASING, variance_percentage=20),
    cause_metrics=[
        CauseMetricBase(
            metric_clauses=[
                MetricClause(FieldsMetadata.results, TrendEnum.DECREASING, variance_percentage=20),
                MetricClause(FieldsMetadata.ctr_all, TrendEnum.INCREASING, variance_percentage=20),
            ],
            output=OverTimeTrendTemplate.CPM_UP_RESULTS_DOWN_CTR_UP,
        ),
        CauseMetricBase(
            metric_clauses=[
                MetricClause(FieldsMetadata.results, TrendEnum.DECREASING, variance_percentage=20),
                MetricClause(FieldsMetadata.cost_per_result, TrendEnum.INCREASING, variance_percentage=20),
            ],
            output=OverTimeTrendTemplate.CPM_UP_RESULTS_DOWN_CPR_UP,
        ),
    ],
)

FOURTEEN_DAYS_CLICKS_DOWN = TriggerMetric(
    trigger=MetricClause(FieldsMetadata.clicks_all, TrendEnum.DECREASING, variance_percentage=20),
    cause_metrics=[
        CauseMetricBase(
            metric_clauses=[
                MetricClause(FieldsMetadata.cpc_all, TrendEnum.INCREASING, variance_percentage=20),
            ],
            output=OverTimeTrendTemplate.CLICKS_DOWN_CPC_UP,
        ),
        CauseMetricBase(
            metric_clauses=[
                MetricClause(FieldsMetadata.cpm, TrendEnum.INCREASING, variance_percentage=20),
            ],
            output=OverTimeTrendTemplate.CLICKS_DOWN_CPM_UP,
        ),
    ],
)

FOURTEEN_DAYS_CLICKS_UP = TriggerMetric(
    trigger=MetricClause(FieldsMetadata.clicks_all, TrendEnum.INCREASING, variance_percentage=20),
    cause_metrics=[
        CauseMetricBase(
            metric_clauses=[
                MetricClause(FieldsMetadata.ctr_all, TrendEnum.INCREASING, variance_percentage=20),
                MetricClause(FieldsMetadata.cpc_all, TrendEnum.DECREASING, variance_percentage=20),
                MetricClause(FieldsMetadata.cpm, TrendEnum.DECREASING, variance_percentage=20),
            ],
            output=OverTimeTrendTemplate.CLICK_UP_CTR_UP_CPC_DOWN_CPM_DOWN,
        ),
    ],
)

FOURTEEN_DAYS_AMOUNT_SPENT_DOWN = TriggerMetric(
    trigger=MetricClause(FieldsMetadata.amount_spent, TrendEnum.DECREASING, variance_percentage=20),
    cause_metrics=[
        CauseMetricBase(
            metric_clauses=[
                MetricClause(
                    FieldsMetadata.cost_per_result,
                    TrendEnum.INCREASING,
                    variance_percentage=20,
                )
            ],
            output=OverTimeTrendTemplate.AMOUNT_SPENT_DOWN_CPR_UP,
        ),
        CauseMetricBase(
            metric_clauses=[
                MetricClause(
                    FieldsMetadata.cost_per_result,
                    TrendEnum.DECREASING,
                    variance_percentage=20,
                )
            ],
            output=OverTimeTrendTemplate.AMOUNT_SPENT_DOWN_CPR_DOWN,
        ),
        CauseMetricBase(
            metric_clauses=[MetricClause(FieldsMetadata.results, TrendEnum.INCREASING, variance_percentage=20)],
            output=OverTimeTrendTemplate.AMOUNT_SPENT_DOWN_RESULTS_UP,
        ),
    ],
)

FOURTEEN_DAYS_AMOUNT_SPENT_UP = TriggerMetric(
    trigger=MetricClause(FieldsMetadata.amount_spent, TrendEnum.INCREASING, variance_percentage=20),
    cause_metrics=[
        CauseMetricBase(
            metric_clauses=[
                MetricClause(
                    FieldsMetadata.cost_per_result,
                    TrendEnum.INCREASING,
                    variance_percentage=20,
                )
            ],
            output=OverTimeTrendTemplate.AMOUNT_SPENT_UP_CPR_UP,
        ),
        CauseMetricBase(
            metric_clauses=[
                MetricClause(
                    FieldsMetadata.cost_per_result,
                    TrendEnum.DECREASING,
                    variance_percentage=20,
                )
            ],
            output=OverTimeTrendTemplate.AMOUNT_SPENT_UP_CPR_DOWN,
        ),
    ],
)

FOURTEEN_DAYS_COST_PER_RESULT_UP = TriggerMetric(
    trigger=MetricClause(
        FieldsMetadata.cost_per_result,
        TrendEnum.INCREASING,
        variance_percentage=20,
    ),
    cause_metrics=[
        CauseMetricBase(
            metric_clauses=[MetricClause(FieldsMetadata.impressions, TrendEnum.DECREASING, variance_percentage=20)],
            output=OverTimeTrendTemplate.CPR_UP_IMPRESSIONS_DOWN,
        )
    ],
)

FOURTEEN_DAYS_LANDING_PAGE_CONVERSION_RATE_DOWN = TriggerMetric(
    trigger=MetricClause(
        FieldsMetadata.landing_page_conversion_rate,
        TrendEnum.DECREASING,
        variance_percentage=20,
    ),
    cause_metrics=[
        CauseMetricBase(
            metric_clauses=[
                MetricClause(FieldsMetadata.unique_clicks_all, TrendEnum.INCREASING, variance_percentage=20)
            ],
            output=OverTimeTrendTemplate.LANDING_PAGE_CONVERSION_RATE_DOWN_UNIQUE_CLICKS_UP,
        )
    ],
)

FOURTEEN_DAYS_BUCKET = [
    FOURTEEN_DAYS_CONVERSION_RATE_DOWN,
    FOURTEEN_DAYS_RESULTS_DOWN,
    FOURTEEN_DAYS_RESULTS_UP,
    FOURTEEN_DAYS_CTR_DOWN,
    FOURTEEN_DAYS_CTR_UP,
    FOURTEEN_DAYS_CPM_UP,
    FOURTEEN_DAYS_AMOUNT_SPENT_UP,
    FOURTEEN_DAYS_AMOUNT_SPENT_DOWN,
    FOURTEEN_DAYS_COST_PER_RESULT_UP,
    FOURTEEN_DAYS_LANDING_PAGE_CONVERSION_RATE_DOWN,
    FOURTEEN_DAYS_CLICKS_DOWN,
    FOURTEEN_DAYS_CLICKS_UP,
]

# THIRTY DAYS BUCKETS
THIRTY_DAYS_CONVERSION_RATE_DOWN = TriggerMetric(
    trigger=MetricClause(
        FieldsMetadata.conversion_rate,
        TrendEnum.DECREASING,
        variance_percentage=20,
    ),
    cause_metrics=[
        CauseMetricBase(
            metric_clauses=[
                MetricClause(FieldsMetadata.ctr_all, TrendEnum.DECREASING, variance_percentage=20),
                MetricClause(FieldsMetadata.cpc_all, TrendEnum.INCREASING, variance_percentage=20),
            ],
            output=OverTimeTrendTemplate.CR_DOWN_CTR_DOWN_CPC_UP,
        ),
        CauseMetricBase(
            metric_clauses=[
                MetricClause(FieldsMetadata.cpm, TrendEnum.INCREASING, variance_percentage=20),
            ],
            output=OverTimeTrendTemplate.CR_DOWN_CPM_UP,
        ),
    ],
)

THIRTY_DAYS_RESULTS_DOWN = TriggerMetric(
    trigger=MetricClause(FieldsMetadata.results, TrendEnum.DECREASING, variance_percentage=20),
    cause_metrics=[
        CauseMetricBase(
            metric_clauses=[
                MetricClause(FieldsMetadata.cpm, TrendEnum.INCREASING, variance_percentage=20),
                MetricClause(FieldsMetadata.conversion_rate, TrendEnum.DECREASING, variance_percentage=20),
            ],
            output=OverTimeTrendTemplate.RESULTS_DOWN_CPM_UP_CR_DOWN,
        ),
        CauseMetricBase(
            metric_clauses=[
                MetricClause(FieldsMetadata.cpc_all, TrendEnum.INCREASING, variance_percentage=20),
                MetricClause(FieldsMetadata.ctr_all, TrendEnum.INCREASING, variance_percentage=20),
            ],
            output=OverTimeTrendTemplate.RESULTS_DOWN_CPC_UP_CTR_UP,
        ),
        CauseMetricBase(
            metric_clauses=[
                MetricClause(FieldsMetadata.cpc_all, TrendEnum.INCREASING, variance_percentage=20),
                MetricClause(FieldsMetadata.ctr_all, TrendEnum.DECREASING, variance_percentage=20),
            ],
            output=OverTimeTrendTemplate.RESULTS_DOWN_CPC_UP_CTR_DOWN,
        ),
        CauseMetricBase(
            metric_clauses=[
                MetricClause(
                    FieldsMetadata.conversion_rate,
                    TrendEnum.DECREASING,
                    variance_percentage=20,
                ),
                MetricClause(
                    FieldsMetadata.cost_per_result,
                    TrendEnum.INCREASING,
                    variance_percentage=20,
                ),
            ],
            output=OverTimeTrendTemplate.RESULTS_DOWN_CR_DOWN_CPR_UP,
        ),
        CauseMetricBase(
            metric_clauses=[MetricClause(FieldsMetadata.unique_ctr_all, TrendEnum.INCREASING, variance_percentage=20)],
            output=OverTimeTrendTemplate.RESULTS_DOWN_UNIQUE_CTR_UP,
        ),
        CauseMetricBase(
            metric_clauses=[MetricClause(FieldsMetadata.unique_ctr_all, TrendEnum.DECREASING, variance_percentage=20)],
            output=OverTimeTrendTemplate.RESULTS_DOWN_UNIQUE_CTR_DOWN,
        ),
        CauseMetricBase(
            metric_clauses=[
                MetricClause(FieldsMetadata.amount_spent, TrendEnum.INCREASING, variance_percentage=20),
                MetricClause(FieldsMetadata.cpc_all, TrendEnum.INCREASING, variance_percentage=20),
            ],
            output=OverTimeTrendTemplate.RESULTS_DOWN_AMOUNT_SPENT_UP_CPC_UP,
        ),
        CauseMetricBase(
            metric_clauses=[
                MetricClause(FieldsMetadata.cost_per_result, TrendEnum.INCREASING, variance_percentage=20),
                MetricClause(FieldsMetadata.cpc_all, TrendEnum.INCREASING, variance_percentage=20),
            ],
            output=OverTimeTrendTemplate.RESULTS_DOWN_CPR_UP_CPC_UP,
        ),
    ],
)

THIRTY_DAYS_RESULTS_UP = TriggerMetric(
    trigger=MetricClause(FieldsMetadata.results, TrendEnum.INCREASING, variance_percentage=20),
    cause_metrics=[
        CauseMetricBase(
            metric_clauses=[
                MetricClause(FieldsMetadata.unique_clicks_all, TrendEnum.INCREASING, variance_percentage=20),
            ],
            output=OverTimeTrendTemplate.RESULTS_UP_UNIQUE_CLICKS_UP,
        ),
        CauseMetricBase(
            metric_clauses=[MetricClause(FieldsMetadata.unique_ctr_all, TrendEnum.DECREASING, variance_percentage=20)],
            output=OverTimeTrendTemplate.RESULTS_UP_UNIQUE_CTR_DOWN,
        ),
        CauseMetricBase(
            metric_clauses=[
                MetricClause(FieldsMetadata.cpc_all, TrendEnum.DECREASING, variance_percentage=20),
                MetricClause(FieldsMetadata.ctr_all, TrendEnum.INCREASING, variance_percentage=20),
            ],
            output=OverTimeTrendTemplate.RESULTS_UP_CPC_DOWN_CTR_UP,
        ),
        CauseMetricBase(
            metric_clauses=[
                MetricClause(FieldsMetadata.cpc_all, TrendEnum.DECREASING, variance_percentage=20),
                MetricClause(FieldsMetadata.cpm, TrendEnum.DECREASING, variance_percentage=20),
            ],
            output=OverTimeTrendTemplate.RESULTS_UP_CPC_DOWN_CPM_DOWN,
        ),
        CauseMetricBase(
            metric_clauses=[
                MetricClause(FieldsMetadata.cpc_all, TrendEnum.DECREASING, variance_percentage=20),
                MetricClause(FieldsMetadata.ctr_all, TrendEnum.INCREASING, variance_percentage=20),
                MetricClause(FieldsMetadata.cpm, TrendEnum.DECREASING, variance_percentage=20),
            ],
            output=OverTimeTrendTemplate.RESULTS_UP_CPC_DOWN_CTR_UP_CPM_DOWN,
        ),
        CauseMetricBase(
            metric_clauses=[
                MetricClause(FieldsMetadata.amount_spent, TrendEnum.INCREASING, variance_percentage=20),
                MetricClause(FieldsMetadata.cpc_all, TrendEnum.DECREASING, variance_percentage=20),
                MetricClause(FieldsMetadata.cpm, TrendEnum.DECREASING, variance_percentage=20),
            ],
            output=OverTimeTrendTemplate.RESULTS_UP_AMOUNT_SPENT_UP_CPC_DOWN_CPM_DOWN,
        ),
        CauseMetricBase(
            metric_clauses=[
                MetricClause(FieldsMetadata.cost_per_result, TrendEnum.DECREASING, variance_percentage=20),
                MetricClause(FieldsMetadata.cpm, TrendEnum.DECREASING, variance_percentage=20),
            ],
            output=OverTimeTrendTemplate.RESULTS_UP_CPR_DOWN_CPM_DOWN,
        ),
    ],
)

THIRTY_DAYS_CTR_DOWN = TriggerMetric(
    trigger=MetricClause(FieldsMetadata.ctr_all, TrendEnum.DECREASING, variance_percentage=20),
    cause_metrics=[
        CauseMetricBase(
            metric_clauses=[
                MetricClause(
                    FieldsMetadata.cost_per_result,
                    TrendEnum.INCREASING,
                    variance_percentage=20,
                ),
                MetricClause(
                    FieldsMetadata.cpm,
                    TrendEnum.INCREASING,
                    variance_percentage=20,
                ),
            ],
            output=OverTimeTrendTemplate.CTR_DOWN_CPR_UP_CPM_UP,
        ),
        CauseMetricBase(
            metric_clauses=[
                MetricClause(FieldsMetadata.cpm, TrendEnum.INCREASING, variance_percentage=20),
                MetricClause(FieldsMetadata.cpc_all, TrendEnum.INCREASING, variance_percentage=20),
            ],
            output=OverTimeTrendTemplate.CTR_DOWN_CPM_UP_CPC_UP,
        ),
    ],
)

THIRTY_DAYS_CTR_UP = TriggerMetric(
    trigger=MetricClause(FieldsMetadata.ctr_all, TrendEnum.INCREASING, variance_percentage=20),
    cause_metrics=[
        CauseMetricBase(
            metric_clauses=[
                MetricClause(FieldsMetadata.cpm, TrendEnum.DECREASING, variance_percentage=20),
                MetricClause(FieldsMetadata.cpc_all, TrendEnum.DECREASING, variance_percentage=20),
            ],
            output=OverTimeTrendTemplate.CTR_UP_CPM_DOWN_CPC_DOWN,
        ),
    ],
)

THIRTY_DAYS_CPM_UP = TriggerMetric(
    trigger=MetricClause(FieldsMetadata.cpm, TrendEnum.INCREASING, variance_percentage=20),
    cause_metrics=[
        CauseMetricBase(
            metric_clauses=[
                MetricClause(FieldsMetadata.results, TrendEnum.DECREASING, variance_percentage=20),
                MetricClause(FieldsMetadata.ctr_all, TrendEnum.INCREASING, variance_percentage=20),
            ],
            output=OverTimeTrendTemplate.CPM_UP_RESULTS_DOWN_CTR_UP,
        ),
        CauseMetricBase(
            metric_clauses=[
                MetricClause(FieldsMetadata.results, TrendEnum.DECREASING, variance_percentage=20),
                MetricClause(FieldsMetadata.cost_per_result, TrendEnum.INCREASING, variance_percentage=20),
            ],
            output=OverTimeTrendTemplate.CPM_UP_RESULTS_DOWN_CPR_UP,
        ),
    ],
)

THIRTY_DAYS_CLICKS_DOWN = TriggerMetric(
    trigger=MetricClause(FieldsMetadata.clicks_all, TrendEnum.DECREASING, variance_percentage=20),
    cause_metrics=[
        CauseMetricBase(
            metric_clauses=[
                MetricClause(FieldsMetadata.cpc_all, TrendEnum.INCREASING, variance_percentage=20),
            ],
            output=OverTimeTrendTemplate.CLICKS_DOWN_CPC_UP,
        ),
        CauseMetricBase(
            metric_clauses=[
                MetricClause(FieldsMetadata.cpm, TrendEnum.INCREASING, variance_percentage=20),
            ],
            output=OverTimeTrendTemplate.CLICKS_DOWN_CPM_UP,
        ),
    ],
)

THIRTY_DAYS_CLICKS_UP = TriggerMetric(
    trigger=MetricClause(FieldsMetadata.clicks_all, TrendEnum.INCREASING, variance_percentage=20),
    cause_metrics=[
        CauseMetricBase(
            metric_clauses=[
                MetricClause(FieldsMetadata.ctr_all, TrendEnum.INCREASING, variance_percentage=20),
                MetricClause(FieldsMetadata.cpc_all, TrendEnum.DECREASING, variance_percentage=20),
                MetricClause(FieldsMetadata.cpm, TrendEnum.DECREASING, variance_percentage=20),
            ],
            output=OverTimeTrendTemplate.CLICK_UP_CTR_UP_CPC_DOWN_CPM_DOWN,
        ),
    ],
)

THIRTY_DAYS_AMOUNT_SPENT_DOWN = TriggerMetric(
    trigger=MetricClause(FieldsMetadata.amount_spent, TrendEnum.DECREASING, variance_percentage=20),
    cause_metrics=[
        CauseMetricBase(
            metric_clauses=[
                MetricClause(
                    FieldsMetadata.cost_per_result,
                    TrendEnum.INCREASING,
                    variance_percentage=20,
                )
            ],
            output=OverTimeTrendTemplate.AMOUNT_SPENT_DOWN_CPR_UP,
        ),
        CauseMetricBase(
            metric_clauses=[
                MetricClause(
                    FieldsMetadata.cost_per_result,
                    TrendEnum.DECREASING,
                    variance_percentage=20,
                )
            ],
            output=OverTimeTrendTemplate.AMOUNT_SPENT_DOWN_CPR_DOWN,
        ),
        CauseMetricBase(
            metric_clauses=[MetricClause(FieldsMetadata.results, TrendEnum.INCREASING, variance_percentage=20)],
            output=OverTimeTrendTemplate.AMOUNT_SPENT_DOWN_RESULTS_UP,
        ),
    ],
)

THIRTY_DAYS_AMOUNT_SPENT_UP = TriggerMetric(
    trigger=MetricClause(FieldsMetadata.amount_spent, TrendEnum.INCREASING, variance_percentage=20),
    cause_metrics=[
        CauseMetricBase(
            metric_clauses=[
                MetricClause(
                    FieldsMetadata.cost_per_result,
                    TrendEnum.INCREASING,
                    variance_percentage=20,
                )
            ],
            output=OverTimeTrendTemplate.AMOUNT_SPENT_UP_CPR_UP,
        ),
        CauseMetricBase(
            metric_clauses=[
                MetricClause(
                    FieldsMetadata.cost_per_result,
                    TrendEnum.DECREASING,
                    variance_percentage=20,
                )
            ],
            output=OverTimeTrendTemplate.AMOUNT_SPENT_UP_CPR_DOWN,
        ),
    ],
)

THIRTY_DAYS_COST_PER_RESULT_UP = TriggerMetric(
    trigger=MetricClause(
        FieldsMetadata.cost_per_result,
        TrendEnum.INCREASING,
        variance_percentage=20,
    ),
    cause_metrics=[
        CauseMetricBase(
            metric_clauses=[MetricClause(FieldsMetadata.impressions, TrendEnum.DECREASING, variance_percentage=20)],
            output=OverTimeTrendTemplate.CPR_UP_IMPRESSIONS_DOWN,
        )
    ],
)

THIRTY_DAYS_LANDING_PAGE_CONVERSION_RATE_DOWN = TriggerMetric(
    trigger=MetricClause(
        FieldsMetadata.landing_page_conversion_rate,
        TrendEnum.DECREASING,
        variance_percentage=20,
    ),
    cause_metrics=[
        CauseMetricBase(
            metric_clauses=[
                MetricClause(FieldsMetadata.unique_clicks_all, TrendEnum.INCREASING, variance_percentage=20)
            ],
            output=OverTimeTrendTemplate.LANDING_PAGE_CONVERSION_RATE_DOWN_UNIQUE_CLICKS_UP,
        )
    ],
)

THIRTY_DAYS_BUCKET = [
    THIRTY_DAYS_CONVERSION_RATE_DOWN,
    THIRTY_DAYS_RESULTS_DOWN,
    THIRTY_DAYS_RESULTS_UP,
    THIRTY_DAYS_CTR_DOWN,
    THIRTY_DAYS_CTR_UP,
    THIRTY_DAYS_CPM_UP,
    THIRTY_DAYS_AMOUNT_SPENT_UP,
    THIRTY_DAYS_AMOUNT_SPENT_DOWN,
    THIRTY_DAYS_COST_PER_RESULT_UP,
    THIRTY_DAYS_LANDING_PAGE_CONVERSION_RATE_DOWN,
    THIRTY_DAYS_CLICKS_DOWN,
    THIRTY_DAYS_CLICKS_UP,
]

ADSET_TIME_BUCKETS = [
    StrategyTimeBucket(no_of_days=60, minimum_days_of_data=40, triggers=THIRTY_DAYS_BUCKET, level=LevelEnum.ADSET),
    StrategyTimeBucket(no_of_days=30, minimum_days_of_data=20, triggers=THIRTY_DAYS_BUCKET, level=LevelEnum.ADSET),
    StrategyTimeBucket(no_of_days=14, minimum_days_of_data=10, triggers=FOURTEEN_DAYS_BUCKET, level=LevelEnum.ADSET),
    StrategyTimeBucket(no_of_days=7, minimum_days_of_data=4, triggers=SEVEN_DAYS_BUCKET, level=LevelEnum.ADSET),
    StrategyTimeBucket(no_of_days=3, minimum_days_of_data=2, triggers=THREE_DAYS_BUCKET, level=LevelEnum.ADSET),
]
