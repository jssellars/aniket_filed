import typing
from dataclasses import dataclass

from GoogleDexter.Infrastructure.Domain.DaysEnum import DaysEnum
from GoogleDexter.Infrastructure.Domain.Metrics.Metric import Metric
from GoogleDexter.Infrastructure.Domain.Metrics.MetricEnums import MetricTypeEnum
from GoogleDexter.Infrastructure.Domain.Rules.AntecedentEnums import AntecedentTypeEnum
from GoogleDexter.Infrastructure.FuzzyEngine.FuzzySets.FuzzySets import LinguisticVariableEnum


@dataclass
class RuleTemplateKeyword:
    id: int = None
    metric_name: Metric = None
    metric_type: MetricTypeEnum = None
    antecedent_type: AntecedentTypeEnum = None
    time_interval: DaysEnum = None
    linguistic_variable: LinguisticVariableEnum = None
    metric_count: int = 0
    value: typing.AnyStr = None
    breakdown_values: typing.List[typing.AnyStr] = None
