import typing
from dataclasses import dataclass

from Core.Dexter.Infrastructure.Domain.DaysEnum import DaysEnum
from Core.Dexter.Infrastructure.Domain.Metrics.Metric import Metric
from Core.Dexter.Infrastructure.Domain.Rules.AntecedentEnums import AntecedentTypeEnum
from FacebookDexter.Infrastructure.Domain.FuzzyEngine.FacebookFuzzySets import FacebookLinguisticVariableEnum
from FacebookDexter.Infrastructure.Domain.Metrics.FacebookMetricEnums import FacebookMetricTypeEnum


@dataclass
class RuleTemplateKeyword:
    id: int = None
    metric_name: Metric = None
    metric_type: FacebookMetricTypeEnum = None
    antecedent_type: AntecedentTypeEnum = None
    time_interval: DaysEnum = DaysEnum.THREE
    linguistic_variable: FacebookLinguisticVariableEnum = None
    metric_count: int = 0
    value: typing.AnyStr = None
    breakdown_values: typing.List[typing.AnyStr] = None
    display_metric_name: int = 1
