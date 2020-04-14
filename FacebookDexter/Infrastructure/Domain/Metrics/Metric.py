import typing

from FacebookDexter.Infrastructure.Domain.Metrics.MetricEnums import AggregatorEnum, MetricTypeEnum


class MetricBase:
    def __init__(self, name: typing.AnyStr = None, display_name: typing.AnyStr = None):
        self.name = name
        self.display_name = display_name


class Metric(MetricBase):
    DEFAULT_MULTIPLIER = 1.0

    def __init__(self,
                 name: typing.AnyStr = None,
                 display_name: typing.AnyStr = None,
                 mtype: MetricTypeEnum = None,
                 numerator: typing.List[MetricBase] = None,
                 numerator_aggregator: AggregatorEnum = None,
                 denominator: typing.List[MetricBase] = None,
                 denominator_aggregator: AggregatorEnum = None,
                 multiplier: float = None):

        super().__init__(name=name, display_name=display_name)

        self.numerator = numerator if isinstance(numerator, list) else [numerator]
        self.numerator_aggregator = numerator_aggregator if numerator_aggregator else AggregatorEnum.SUM
        self.denominator = denominator if isinstance(denominator, list) else [denominator]
        self.denominator_aggregator = denominator_aggregator if denominator_aggregator else AggregatorEnum.SUM
        self.multiplier = multiplier if multiplier else self.DEFAULT_MULTIPLIER
        self.type = mtype



