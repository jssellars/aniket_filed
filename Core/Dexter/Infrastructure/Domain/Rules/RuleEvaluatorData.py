import typing
from dataclasses import dataclass

from Core.Dexter.Infrastructure.Domain.Breakdowns import BreakdownMetadataBase


@dataclass
class RuleEvaluatorData:
    antecedent_id: int = None
    antecedent_truth_value: bool = None
    metric_value: typing.Any = None
    metric_value_confidence: float = None
    breakdown_metadata: BreakdownMetadataBase = None
