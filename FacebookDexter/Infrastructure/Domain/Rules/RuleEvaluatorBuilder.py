import typing

from FacebookDexter.Infrastructure.Domain.DaysEnum import DaysEnum


class RuleEvaluatorBuilder:
    def __init__(self):
        self._breakdown_metadata = None
        self._time_interval = None

    def set_time_interval(self, time_interval: DaysEnum = None) -> typing.Any:
        self._time_interval = time_interval
        return self
