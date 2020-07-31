import typing

from Core.Dexter.Infrastructure.Domain.FuzzyEngine.FuzzySets.FuzzySets import Fuzzyfier


class MetricFuzzyfierCollectionBase:

    @classmethod
    def get_fuzzyfier_by_metric_name(cls, metric_name: typing.AnyStr) -> Fuzzyfier:
        try:
            fuzzyfier = getattr(cls, metric_name)
        except ValueError as e:
            raise ValueError(f"Invalid metric name {metric_name}")

        return fuzzyfier
