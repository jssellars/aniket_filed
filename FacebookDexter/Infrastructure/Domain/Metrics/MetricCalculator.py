import typing
from datetime import datetime, timedelta

import numpy as np

from FacebookDexter.Infrastructure.Constants import DEFAULT_DATETIME
from FacebookDexter.Infrastructure.Domain.Breakdowns import BreakdownMetadata
from FacebookDexter.Infrastructure.Domain.DaysEnum import DaysEnum
from FacebookDexter.Infrastructure.Domain.Metrics.MetricCalculatorBuilder import MetricCalculatorBuilder
from FacebookDexter.Infrastructure.Domain.Metrics.MetricEnums import AggregatorEnum, MetricTrendTimeBucketEnum, MetricTypeEnum
from FacebookDexter.Infrastructure.Domain.Rules.AntecedentEnums import AntecedentTypeEnum
from FacebookDexter.Infrastructure.FuzzyEngine.FuzzySets.FuzzySets import LinguisticVariableEnum


class MetricCalculator(MetricCalculatorBuilder):

    def compute_value(self, atype: AntecedentTypeEnum = None, time_interval: DaysEnum = None) -> typing.Sequence[typing.Any, typing.Any]:
        # todo: turn this into a dictionary
        date_stop = datetime.now()
        date_start = date_stop - timedelta(days=time_interval.value)

        if self.__metric.type == MetricTypeEnum.STRUCTURE:
            return self.structure_value(), None

        if self.__metric.type == MetricTypeEnum.INSIGHT:
            if atype == AntecedentTypeEnum.FUZZY_VALUE:
                return self.fuzzy_value(date_start.strftime(DEFAULT_DATETIME), date_stop.strftime(DEFAULT_DATETIME))

            if atype == AntecedentTypeEnum.FUZZY_TREND:
                return self.fuzzy_trend(date_start.strftime(DEFAULT_DATETIME), date_stop.strftime(DEFAULT_DATETIME))

            if atype == AntecedentTypeEnum.VALUE:
                return self.aggregated_value(date_start.strftime(DEFAULT_DATETIME), date_stop.strftime(DEFAULT_DATETIME)), None

            if atype == AntecedentTypeEnum.TREND:
                return self.trend(date_start.strftime(DEFAULT_DATETIME), date_stop.strftime(DEFAULT_DATETIME)), None

            if atype == AntecedentTypeEnum.LIST:
                return self.values(date_start.strftime(DEFAULT_DATETIME), date_stop.strftime(DEFAULT_DATETIME)), None

    def get_breakdown_metadata(self, time_interval: DaysEnum = None) -> typing.List[BreakdownMetadata]:
        date_stop = datetime.now()
        date_start = date_stop - timedelta(days=time_interval.value)

        breakdown_values = self.__repository.get_breakdown_values(key_value=self.__facebook_id,
                                                                  level=self.__level,
                                                                  date_start=date_start.strftime(DEFAULT_DATETIME),
                                                                  date_stop=date_stop.strftime(DEFAULT_DATETIME))
        breakdown_metadata = [BreakdownMetadata(breakdown=self.__breakdown_metadata.breakdown, breakdown_value=breakdown_value[0],
                                                action_breakdown=self.__breakdown_metadata.action_breakdown, action_breakdown_value=breakdown_value[1])
                              for breakdown_value in breakdown_values]

        return breakdown_metadata

    def __compute_numerator_value(self, data: typing.List[typing.Dict]) -> typing.List[float]:
        return [AggregatorEnum.SUM.value([entry[metric.name] for metric in self.__metric.numerator]) for entry in data]

    def __compute_denominator_values(self, data: typing.List[typing.Dict]) -> typing.List[float]:
        return [AggregatorEnum.SUM.value([entry[metric.name] for metric in self.__metric.denominator]) for entry in data]

    def structure_value(self) -> typing.Any:
        structure_details = self.__repository.get_structure_details(key_value=self.__facebook_id, level=self.__level)
        return structure_details.get(self.__metric.name)

    def values(self, date_start: typing.AnyStr = None, date_stop: typing.AnyStr = None) -> typing.List[float]:
        data = self.__get_metrics_values(date_start=date_start, date_stop=date_stop)

        numerator = self.__compute_numerator_value(data=data)
        denominator = self.__compute_denominator_values(data=data)
        if len(numerator) != len(denominator):
            raise ValueError("Numerator and denominator data mismatch.")

        values = [numerator[index] / denominator[index] for index in range(len(numerator))]
        return values

    def aggregated_value(self, date_start: typing.AnyStr = None, date_stop: typing.AnyStr = None) -> float:
        data = self.__get_metrics_values(date_start=date_start, date_stop=date_stop)
        aggregated_numerator = self.__metric.numerator_aggregator.value(self.__compute_numerator_value(data))
        if isinstance(self.__metric.denominator, list):
            aggregated_denominator = self.__metric.denominator_aggregator.value(self.__compute_denominator_values(data))
            return self.__metric.multiplier * aggregated_numerator / aggregated_denominator if aggregated_denominator else None
        else:
            return self.__metric.multiplier * aggregated_numerator

    def trend(self, date_start: typing.AnyStr = None, date_stop: typing.AnyStr = None) -> float:
        _date_start = datetime.strptime(date_start, DEFAULT_DATETIME)
        _date_stop = datetime.strptime(date_stop, DEFAULT_DATETIME)
        current_value = self.aggregated_value(date_start=date_start, date_stop=date_start)

        slopes = []
        for time_bucket in MetricTrendTimeBucketEnum:
            date_stop = (_date_start - timedelta(days=time_bucket.value))

            if date_stop >= _date_stop:
                date_stop = date_stop.strftime(DEFAULT_DATETIME)
                bucket_value = self.aggregated_value(date_start=date_start, date_stop=date_stop)

                dy = current_value - bucket_value
                dt = time_bucket.value

                slopes.append(np.arctan2(dy, dt))

        trend = self.__compute_resultant_slope(slopes)

        return trend

    @staticmethod
    def __compute_resultant_slope(slopes: typing.List = None) -> float:
        unit_vectors = [(np.cos(slope), np.sin(slope)) for slope in slopes]
        mean_unit_vector = np.mean(unit_vectors, axis=0)
        resultant_slope = np.arctan2(mean_unit_vector[1], mean_unit_vector[0])
        return resultant_slope

    def fuzzy_value(self, date_start: typing.AnyStr = None, date_stop: typing.AnyStr = None) -> typing.Tuple[LinguisticVariableEnum, float]:
        value = self.aggregated_value(date_start, date_stop)
        return self.__fuzzy_value_base(value)

    def fuzzy_trend(self, date_start: typing.AnyStr = None, date_stop: typing.AnyStr = None) -> typing.Tuple[LinguisticVariableEnum, float]:
        value = self.trend(date_start, date_stop)
        return self.__fuzzy_value_base(value)

    def __fuzzy_value_base(self, value: float = None) -> typing.Tuple[LinguisticVariableEnum, float]:
        fuzzyfier_collection = self.__fuzzyfier_factory.get_fuzzyfier_collection_by_metric_type(self.__metric.type)
        fuzzyfier = fuzzyfier_collection.get_fuzzyfier_by_metric_name(self.__metric.name)
        fuzzy_class = None
        fuzzy_membership_value = 0.0
        for linguistic_level in fuzzyfier.levels:
            current_fuzzy_class, current_fuzzy_membership_value = fuzzyfier.fuzzyfy(value, linguistic_level)
            if current_fuzzy_membership_value > fuzzy_membership_value:
                fuzzy_class = current_fuzzy_class
                fuzzy_membership_value = current_fuzzy_membership_value
        return fuzzy_class, fuzzy_membership_value

    @property
    def metrics(self):
        if self.__metrics is None:
            metrics = [value.name for value in self.__metric.numerator]
            if self.__metric.denominator:
                metrics += [value.name for value in self.__metric.denominator]

        return self.__metrics

    def __get_metrics_values(self, date_start: typing.AnyStr = None, date_stop: typing.AnyStr = None) -> typing.List[typing.Dict]:
        metrics_values = self.__repository.get_metrics_values(key_value=self.__facebook_id,
                                                              date_start=date_start,
                                                              date_stop=date_stop,
                                                              metrics=self.metrics,
                                                              level=self.__level,
                                                              breakdown_metadata=self.__breakdown_metadata)
        return metrics_values
