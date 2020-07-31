import typing
from dataclasses import dataclass

from Core.Dexter.Infrastructure.Domain.DaysEnum import DaysEnum
from Core.Dexter.Infrastructure.Domain.Metrics.Metric import Metric
from Core.Dexter.Infrastructure.Domain.Rules.AntecedentEnums import AntecedentTypeEnum
from GoogleDexter.Infrastructure.Domain.Metrics.GoogleMetricEnums import GoogleMetricTypeEnum
from GoogleDexter.Infrastructure.FuzzyEngine.GoogleFuzzySets import GoogleLinguisticVariableEnum


@dataclass
class GoogleRuleTemplateKeyword:
    id: int = None
    metric_name: Metric = None
    metric_type: GoogleMetricTypeEnum = None
    antecedent_type: AntecedentTypeEnum = None
    time_interval: DaysEnum = None
    linguistic_variable: GoogleLinguisticVariableEnum = None
    metric_count: int = 0
    value: typing.AnyStr = None
    breakdown_values: typing.List[typing.AnyStr] = None
