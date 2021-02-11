from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Dict, List, Optional, Union

from Core.Dexter.Infrastructure.Domain.LevelEnums import LevelEnum
from Core.Web.FacebookGraphAPI.Models.Field import Field as FacebookField
from Core.Web.FacebookGraphAPI.Models.FieldsMetadata import FieldsMetadata
from FacebookDexter.Infrastructure.DexterRules.BreakdownAndAudiencesTemplates import (
    AudienceRecommendationTemplate,
    BreakdownRecommendationTemplate,
)
from FacebookDexter.Infrastructure.DexterRules.OverTimeTrendTemplates import OverTimeTrendTemplate


class TrendEnum(Enum):
    INCREASING = auto()
    DECREASING = auto()


@dataclass
class CostPerMetric:
    numerator: FacebookField
    denominator: FacebookField
    multiplier: int = 1

    def calculate_cost(self, data: Dict) -> Optional[float]:
        try:
            if self.numerator.name in data and self.denominator.name in data:
                return data[self.numerator.name] * self.multiplier / data[self.denominator.name]
        except Exception as e:
            # Can consider logging but too many divisions by zero occur
            return


# Custom dexter computed metrics
CUSTOM_DEXTER_METRICS = {
    FieldsMetadata.cost_per_result.name: CostPerMetric(
        numerator=FieldsMetadata.amount_spent, denominator=FieldsMetadata.results
    ),
    FieldsMetadata.landing_page_conversion_rate.name: CostPerMetric(
        numerator=FieldsMetadata.conversions, denominator=FieldsMetadata.unique_clicks_all, multiplier=100
    ),
    FieldsMetadata.conversion_rate.name: CostPerMetric(
        numerator=FieldsMetadata.purchases_total, denominator=FieldsMetadata.clicks_all, multiplier=100
    ),
}

recommendation_enums_union = Union[
    OverTimeTrendTemplate, BreakdownRecommendationTemplate, AudienceRecommendationTemplate
]


@dataclass
class MetricClause:
    metric_field: FacebookField
    trend: TrendEnum
    variance_percentage: float
    is_divided_by_no_breakdowns: Optional[bool] = False


@dataclass
class CauseMetricBase:
    metric_clauses: List[MetricClause]
    output: Optional[recommendation_enums_union] = None


@dataclass
class TriggerMetric:
    trigger: MetricClause
    cause_metrics: List[CauseMetricBase] = field(default_factory=list)
    breakdown: Optional[str] = None


@dataclass
class StrategyTimeBucket:
    no_of_days: int
    minimum_days_of_data: int
    triggers: List[TriggerMetric]
    level: LevelEnum = None
    breakdown: Optional[FacebookField] = FieldsMetadata.breakdown_none
