from dataclasses import dataclass, field
from enum import Enum, auto
from typing import List, Optional, Union

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
