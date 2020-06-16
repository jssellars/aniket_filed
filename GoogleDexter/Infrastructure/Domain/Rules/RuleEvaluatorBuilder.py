import typing

from GoogleDexter.Infrastructure.Domain.DaysEnum import DaysEnum
from GoogleDexter.Infrastructure.Domain.Metrics.MetricCalculator import MetricCalculator
from GoogleDexter.Infrastructure.Domain.Rules.RuleBase import RuleBase


class RuleEvaluatorBuilder:
    def __init__(self):
        self._structure_id = None
        self._rule = None
        self._metric_calculator = None
        self._breakdown_metadata = None
        self._time_interval = None

    def set_id_and_rule(self, structure_id: typing.AnyStr = None, rule: RuleBase = None) -> typing.Any:
        self._structure_id = structure_id
        self._rule = rule
        return self

    def set_structure_id(self, structure_id: typing.AnyStr = None) -> typing.Any:
        self._structure_id = structure_id
        return self

    def set_rule(self, rule: RuleBase = None) -> typing.Any:
        self._rule = rule
        return self

    def set_metric_calculator(self, metric_calculator: MetricCalculator = None) -> typing.Any:
        self._metric_calculator = metric_calculator
        return self

    def set_time_interval(self, time_interval: DaysEnum = None) -> typing.Any:
        self._time_interval = time_interval
        return self
