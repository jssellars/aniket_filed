import typing

from FacebookDexter.Infrastructure.Domain.DaysEnum import DaysEnum
from FacebookDexter.Infrastructure.Domain.Metrics.MetricCalculator import MetricCalculator
from FacebookDexter.Infrastructure.Domain.Rules.RuleBase import RuleBase


class RuleEvaluatorBuilder:
    def __init__(self):
        self._facebook_id = None
        self._rule = None
        self._metric_calculator = None
        self._breakdown_metadata = None
        self._time_interval = None

    def set_id_and_rule(self, facebook_id: typing.AnyStr = None, rule: RuleBase = None) -> typing.Any:
        self._facebook_id = facebook_id
        self._rule = rule
        return self

    def set_facebook_id(self, facebook_id: typing.AnyStr = None) -> typing.Any:
        self._facebook_id = facebook_id
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
