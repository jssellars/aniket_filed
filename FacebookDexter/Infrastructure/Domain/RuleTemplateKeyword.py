import typing
from dataclasses import dataclass

from FacebookDexter.Infrastructure.Domain.DaysEnum import DaysEnum
from FacebookDexter.Infrastructure.Domain.Metrics.Metric import Metric
from FacebookDexter.Infrastructure.Domain.Metrics.MetricEnums import MetricTypeEnum
from FacebookDexter.Infrastructure.Domain.Rules.AntecedentEnums import AntecedentTypeEnum
from FacebookDexter.Infrastructure.FuzzyEngine.FuzzySets.FuzzySets import LinguisticVariableEnum


@dataclass
class RuleTemplateKeyword:
    id: int = None
    metric_name: Metric = None
    metric_type: MetricTypeEnum = None
    antecedent_type: AntecedentTypeEnum = None
    time_interval: DaysEnum = DaysEnum.THREE
    linguistic_variable: LinguisticVariableEnum = None
    metric_count: int = 0
    value: typing.AnyStr = None
    breakdown_values: typing.List[typing.AnyStr] = None
    display_metric_name: int = 1
