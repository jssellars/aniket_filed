import typing

from Core.Dexter.Infrastructure.Domain.Metrics.MetricEnums import AggregatorEnum, MetricTypeBaseEnum


class MetricBase:
    def __init__(self, name: typing.AnyStr = None, display_name: typing.AnyStr = None):
        self.name = name
        self.display_name = display_name

    def __eq__(self, other):
        return self.name == other.name


class Metric(MetricBase):
    DEFAULT_MULTIPLIER = 1.0

    def __init__(self,
                 name: typing.AnyStr = None,
                 display_name: typing.AnyStr = None,
                 mtype: MetricTypeBaseEnum = None,
                 numerator: typing.List[MetricBase] = None,
                 numerator_aggregator: AggregatorEnum = None,
                 denominator: typing.List[MetricBase] = None,
                 denominator_aggregator: AggregatorEnum = None,
                 multiplier: float = None):

        super().__init__(name=name, display_name=display_name)

        if numerator is None:
            self.numerator = []
        elif isinstance(numerator, list):
            self.numerator = numerator
        else:
            self.numerator = [numerator]

        self.numerator_aggregator = numerator_aggregator if numerator_aggregator else AggregatorEnum.SUM

        if denominator is None:
            self.denominator = []
        elif isinstance(denominator, list):
            self.denominator = denominator
        else:
            self.denominator = [denominator]

        self.denominator_aggregator = denominator_aggregator if denominator_aggregator else AggregatorEnum.SUM

        self.multiplier = multiplier if multiplier else self.DEFAULT_MULTIPLIER
        self.type = mtype
