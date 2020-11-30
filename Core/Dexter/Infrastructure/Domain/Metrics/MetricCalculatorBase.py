import typing
from datetime import timedelta, datetime

import numpy as np

from Core.Dexter.Infrastructure.Domain.Breakdowns import BreakdownBaseEnum, ActionBreakdownBaseEnum, \
    BreakdownMetadataBase
from Core.Dexter.Infrastructure.Domain.DaysEnum import DaysEnum
from Core.Dexter.Infrastructure.Domain.Metrics.MetricCalculatorBuilder import MetricCalculatorBuilder
from Core.Dexter.Infrastructure.Domain.Metrics.MetricEnums import AggregatorEnum, MetricTrendTimeBucketEnum
from Core.Dexter.Infrastructure.Domain.Rules.AntecedentEnums import AntecedentTypeEnum
from Core.Tools.Misc.Constants import DEFAULT_DATETIME

import logging

logger = logging.getLogger(__name__)


class MetricCalculatorBase(MetricCalculatorBuilder):
    MAX_CACHE_SIZE = 2048
    HUNDRED_MULTIPLIER = 100

    def __init__(self):
        super().__init__()
        self._calculator_id = ''
        self._calculator = None

    @property
    def calculator(self):
        if self._calculator is None:
            raise NotImplementedError

        return self._calculator

    def _current_state(self):
        raise NotImplementedError

    def compute_value(self, atype: AntecedentTypeEnum = None,
                      time_interval: typing.Union[DaysEnum, int] = DaysEnum.ONE,
                      metric_cache: typing.Dict = None) -> typing.Tuple[typing.Any, typing.Any]:

        metric_cached_key = ""
        if metric_cache is not None:
            metric_cached_key = self._metric.name + "_" + atype.name + "_" + time_interval.name + "_" + "breakdown" + "_" + \
                                self._breakdown_metadata.breakdown.name + "_" + self._breakdown_metadata.action_breakdown.name
            if metric_cached_key in metric_cache:
                return metric_cache[metric_cached_key]

        date_stop = self._date_stop
        try:
            date_start = date_stop - timedelta(days=time_interval)
        except TypeError:
            date_start = date_stop - timedelta(days=time_interval.value)
        except Exception as e:
            logger.debug(
                f"Failed to process date start and date stop for time interval {time_interval} || {repr(e)}",
                extra={"state": self._current_state()},
                exc_info=True,
            )
            date_start = date_stop

        date_start += timedelta(days=1)
        calculator = self.calculator.get((atype, self._metric.type), None)

        if calculator is None:
            logger.debug("Invalid antecedent and metric type combination.", extra={"state": self._current_state()})
            return None, None

        try:
            result = calculator(date_start.strftime(DEFAULT_DATETIME),
                                date_stop.strftime(DEFAULT_DATETIME),
                                metric=self._metric,
                                facebook_id=self._facebook_id)
        except Exception as e:
            logger.debug(
                f"Other calculator exception || {repr(e)}",
                extra={"state": self._current_state()},
                exc_info=True,
            )
            return None, None

        if not isinstance(result, list) and not isinstance(result, tuple):
            if metric_cache is not None:
                metric_cache[metric_cached_key] = result, None
            return result, None
        else:
            if metric_cache is not None:
                metric_cache[metric_cached_key] = result
            return result

    def get_breakdown_metadata(self,
                               breakdown: BreakdownBaseEnum = None,
                               action_breakdown: ActionBreakdownBaseEnum = None,
                               time_interval: DaysEnum = None) -> typing.List[BreakdownMetadataBase]:
        date_stop = self._date_stop
        date_start = date_stop - timedelta(days=time_interval.value)

        try:
            breakdown_values = self._repository.get_breakdown_values(key_value=self._facebook_id,
                                                                     level=self._level,
                                                                     date_start=date_start.strftime(DEFAULT_DATETIME),
                                                                     date_stop=date_stop.strftime(DEFAULT_DATETIME),
                                                                     breakdown=breakdown,
                                                                     action_breakdown=action_breakdown)
        except Exception as e:
            logger.debug(
                f"Failed to get breakdown values || {repr(e)}",
                extra={"state": self._current_state()},
                exc_info=True,
            )
            raise e

        if breakdown_values:
            breakdown_metadata = [BreakdownMetadataBase(breakdown=breakdown, breakdown_value=breakdown_value[0],
                                                        action_breakdown=action_breakdown,
                                                        action_breakdown_value=breakdown_value[1])
                                  for breakdown_value in breakdown_values]
        else:
            breakdown_metadata = [BreakdownMetadataBase(breakdown=breakdown,
                                                        action_breakdown=action_breakdown)]
        return breakdown_metadata

    def _compute_numerator_value(self, data: typing.List[typing.Dict]) -> typing.List[float]:
        return [AggregatorEnum.SUM.value([entry[metric.name] for metric in self._metric.numerator]) for entry in data]

    def _compute_denominator_values(self, data: typing.List[typing.Dict]) -> typing.List[float]:
        return [AggregatorEnum.SUM.value([entry[metric.name] for metric in self._metric.denominator]) for entry in
                data]

    def structure_value(self, *args, **kwargs) -> typing.Any:
        structure_details = self._repository.get_structure_details(key_value=self._facebook_id, level=self._level)
        return structure_details.get(self._metric.name)

    def values(self, date_start: typing.AnyStr = None, date_stop: typing.AnyStr = None) -> typing.List[float]:
        data = self._get_metrics_values(date_start=date_start, date_stop=date_stop)

        numerator = self._compute_numerator_value(data=data)
        denominator = self._compute_denominator_values(data=data)

        if len(numerator) != len(denominator):
            logger.debug("Numerator and denominator data mismatch.", extra={"state": self._current_state()})

            raise ValueError("Numerator and denominator data mismatch.")

        values = numerator
        for index in range(len(numerator)):
            if denominator[index]:
                values[index] /= denominator[index]

        return values

    def average(self, date_start, date_stop, *args, **kwargs):
        self._metric.numerator_aggregator = AggregatorEnum.AVERAGE
        self._metric.denominator_aggregator = AggregatorEnum.AVERAGE
        value = self.aggregated_value(date_start=date_start, date_stop=date_stop)

        return value

    def __compute_aggregated_value(self, data: typing.List[typing.Dict]) -> float:
        try:
            if callable(self._metric.numerator_aggregator):
                numerator_aggregator_function = self._metric.numerator_aggregator
            else:
                numerator_aggregator_function = self._metric.numerator_aggregator.value

            if callable(self._metric.denominator_aggregator):
                denominator_aggregator_function = self._metric.denominator_aggregator
            else:
                denominator_aggregator_function = self._metric.denominator_aggregator.value

            aggregated_numerator = numerator_aggregator_function(self._compute_numerator_value(data))
            if isinstance(self._metric.denominator, list) and self._metric.denominator:
                aggregated_denominator = denominator_aggregator_function(self._compute_denominator_values(data))
                return self._metric.multiplier * aggregated_numerator / aggregated_denominator \
                    if aggregated_denominator else None
            else:
                return self._metric.multiplier * aggregated_numerator
        except Exception as e:
            logger.debug(
                f"Failed to compute aggregated metric value || repr{e}",
                extra={"state": self._current_state()},
            )

    def aggregated_value(self, date_start: typing.AnyStr = None, date_stop: typing.AnyStr = None, **kwargs) -> float:
        data = self._get_metrics_values(date_start=date_start, date_stop=date_stop)
        return self.__compute_aggregated_value(data)

    def categorical_value(self, *args, **kwargs) -> typing.AnyStr:
        date_stop = self._date_stop
        date_start = date_stop - timedelta(days=DaysEnum.THREE_MONTHS.value)

        data = self._get_metrics_values(date_start.strftime(DEFAULT_DATETIME), date_stop.strftime(DEFAULT_DATETIME))

        value = data[-1].get(self._metric.name, None) if data else None

        if value is None:
            logger.debug("Categorical value is none", extra={"state": self._current_state(), "values": data})

        return value

    def min_max_value(self):
        date_stop = self._date_stop
        date_start = date_stop - timedelta(days=DaysEnum.THREE_MONTHS.value)
        data = self.values(date_start.strftime(DEFAULT_DATETIME), date_stop.strftime(DEFAULT_DATETIME))
        min_data = min(data) if data else None
        max_data = max(data) if data else None
        return min_data, max_data

    def min_value(self):
        date_stop = self._date_stop
        date_start = date_stop - timedelta(days=DaysEnum.THREE_MONTHS.value)
        data = self.values(date_start.strftime(DEFAULT_DATETIME), date_stop.strftime(DEFAULT_DATETIME))
        return min(data) if data else None

    def max_value(self):
        date_stop = self._date_stop
        date_start = date_stop - timedelta(days=DaysEnum.THREE_MONTHS.value)
        data = self.values(date_start.strftime(DEFAULT_DATETIME), date_stop.strftime(DEFAULT_DATETIME))
        return max(data) if data else None

    def trend(self, date_stop: typing.AnyStr = None, **kwargs) -> typing.Union[
        typing.NoReturn, float]:

        _date_stop = datetime.strptime(date_stop, DEFAULT_DATETIME)
        _date_start = _date_stop - timedelta(days=30)
        current_value = self.aggregated_value(date_start=date_stop, date_stop=date_stop)

        if current_value is None:
            return None

        slopes = []
        for time_bucket in MetricTrendTimeBucketEnum:
            date_start = (_date_stop - timedelta(days=time_bucket.value))

            if date_start >= _date_start:
                date_start = date_start.strftime(DEFAULT_DATETIME)
                bucket_value = self.aggregated_value(date_start=date_start, date_stop=date_stop)

                if bucket_value is not None:
                    dy = current_value - bucket_value
                    dt = time_bucket.value
                    slopes.append(np.arctan2(dy, dt))
                else:
                    slopes.append(None)
                    logger.debug(
                        f"Time bucket for interval {time_bucket.value} is None.",
                        extra={"state": self._current_state()},
                    )

        trend = self._compute_resultant_slope(slopes)

        return trend

    def _compute_resultant_slope(self, slopes: typing.List = None) -> float:
        unit_vectors = [(np.cos(slope), np.sin(slope)) for slope in slopes if slope is not None]
        mean_unit_vector = np.mean(unit_vectors, axis=0)

        resultant_slope = None

        if mean_unit_vector.size > 1:
            try:
                resultant_slope = np.arctan2(mean_unit_vector[1], mean_unit_vector[0])
            except Exception as e:
                logger.debug(
                    f"Failed to compute resultant slope || {repr(e)}",
                    extra={"state": self._current_state()},
                    exc_info=True,
                )

        return resultant_slope

    def _min_max_normalized_value(self,
                                  date_start: typing.AnyStr = None,
                                  date_stop: typing.AnyStr = None) -> typing.Union[int, float, typing.NoReturn]:
        value = self.aggregated_value(date_start, date_stop)
        min_value, max_value = self.min_max_value()
        if min_value is None:
            min_value = 0.0
        if value and min_value is not None and max_value is not None:
            if max_value - min_value != 0:
                scaled_value = (value - min_value) / (max_value - min_value)
            else:
                return None
        else:
            scaled_value = None
            logger.debug(
                f"Couldn't compute the min-max normalized value for {value}, {min_value}, {max_value}.",
                extra={"state": self._current_state()},
            )

        return scaled_value

    def fuzzy_value(self,
                    date_start: typing.AnyStr = None,
                    date_stop: typing.AnyStr = None,
                    **kwargs):
        value = self._min_max_normalized_value(date_start, date_stop)
        return self._fuzzy_value_base(value, AntecedentTypeEnum.FUZZY_VALUE)

    def fuzzy_trend(self,
                    date_start: typing.AnyStr = None,
                    date_stop: typing.AnyStr = None,
                    **kwargs):
        value = self.trend(date_stop)
        return self._fuzzy_value_base(value, AntecedentTypeEnum.FUZZY_TREND)

    def weighted_fuzzy_trend(self,
                             date_start: typing.AnyStr = None,
                             date_stop: typing.AnyStr = None,
                             **kwargs):
        raise NotImplementedError

    def weighted_trend(self, date_start: typing.AnyStr = None, date_stop: typing.AnyStr = None, **kwargs) -> float:
        raise NotImplementedError

    def _fuzzy_value_base(self,
                          value: float = None,
                          fuzzyfier_type: AntecedentTypeEnum = None):
        fuzzyfier = self._fuzzyfier_factory.get_fuzzyfier(fuzzyfier_type, self._metric.name)
        fuzzy_class = None
        fuzzy_membership_value = 0.0
        try:
            for linguistic_level in fuzzyfier.levels:
                current_fuzzy_class, current_fuzzy_membership_value = fuzzyfier.fuzzyfy(value, linguistic_level)
                if current_fuzzy_membership_value is not None and \
                        current_fuzzy_membership_value > fuzzy_membership_value:
                    fuzzy_class = current_fuzzy_class
                    fuzzy_membership_value = current_fuzzy_membership_value
        except Exception as e:
            logger.debug(
                f"Couldn't compute fuzzy value for {value} and fuzzyfier {fuzzyfier_type.value} || {repr(e)}",
                extra={"state": self._current_state(), "fuzzyfier": fuzzyfier},
                exc_info=True,
            )

        return fuzzy_class, fuzzy_membership_value

    def difference(self,
                   date_start: typing.AnyStr = None,
                   date_stop: typing.AnyStr = None,
                   **kwargs) -> typing.Union[int, float, typing.NoReturn]:
        initial_metric_value = self.aggregated_value(date_start=date_start, date_stop=date_start)
        current_metric_value = self.aggregated_value(date_start=date_stop, date_stop=date_stop)
        if initial_metric_value is not None and current_metric_value is not None:
            difference = current_metric_value - initial_metric_value
        elif initial_metric_value is None and current_metric_value is not None:
            difference = current_metric_value
            logger.debug(
                "Ill-defined difference. Initial metric value is none.",
                extra={"state": self._current_state()},
            )
        elif initial_metric_value is not None and current_metric_value is None:
            difference = initial_metric_value
            logger.debug(
                "Ill-defined difference. Current metric value is none.",
                extra={"state": self._current_state()},
            )
        else:
            difference = None
            logger.debug(
                "Ill-defined difference. Both initial and current metrics are none",
                extra={"state": self._current_state()},
            )
        return difference

    def variance(self,
                 date_start: typing.AnyStr = None,
                 date_stop: typing.AnyStr = None,
                 **kwargs) -> typing.Union[int, float, typing.NoReturn]:

        variance = None
        _date_stop = datetime.strptime(date_stop, DEFAULT_DATETIME)
        _mean_date_start = _date_stop - timedelta(days=30)
        _date_stop = datetime.strftime(_date_stop, DEFAULT_DATETIME)
        _mean_date_start = datetime.strftime(_mean_date_start, DEFAULT_DATETIME)

        mean_on_thirty_days_interval = self.average(date_start=_mean_date_start, date_stop=_date_stop)

        self._metric.numerator_aggregator = AggregatorEnum.STANDARD_DEVIATION
        self._metric.denominator_aggregator = AggregatorEnum.STANDARD_DEVIATION
        standard_deviation_on_time_interval = self.aggregated_value(date_start=date_start,
                                                                    date_stop=_date_stop)

        if mean_on_thirty_days_interval and standard_deviation_on_time_interval is not None:
            variance = self.HUNDRED_MULTIPLIER * (standard_deviation_on_time_interval / mean_on_thirty_days_interval)

        return variance

    def percentage_difference(self,
                              date_start: typing.AnyStr = None,
                              date_stop: typing.AnyStr = None,
                              **kwargs) -> typing.Union[int, float, typing.NoReturn]:

        mean_on_time_interval = self.average(date_start=date_start, date_stop=date_stop)
        current_metric_value = self.aggregated_value(date_start=date_stop, date_stop=date_stop)
        if mean_on_time_interval is not None and current_metric_value is not None:
            if mean_on_time_interval == 0.0 or current_metric_value == 0.0:
                return 1 * self.HUNDRED_MULTIPLIER
            try:
                difference = self.HUNDRED_MULTIPLIER * float(
                    (current_metric_value - mean_on_time_interval) / mean_on_time_interval)
            except ZeroDivisionError:
                if current_metric_value == 0.0:
                    difference = None
                    logger.debug(
                        "Ill-defined percentage difference. Initial metric value and current metric value are none.",
                        extra={"state": self._current_state()},
                    )
                else:
                    difference = self.HUNDRED_MULTIPLIER * current_metric_value
        elif mean_on_time_interval is None and current_metric_value is not None:
            difference = None
            logger.debug(
                "Ill-defined percentage difference. Initial metric value is none.",
                extra={"state": self._current_state()},
            )
        elif mean_on_time_interval is not None and current_metric_value is None:
            difference = None
            logger.debug(
                "Ill-defined percentage difference. Current metric value is none.",
                extra={"state": self._current_state()},
            )
        else:
            difference = None
            logger.debug(
                "Ill-defined percentage difference. Both initial and current metrics are none",
                extra={"state": self._current_state()},
            )
        return difference

    def raw_value(self, date_start: typing.AnyStr = None, *args, **kwargs) -> typing.Union[int, float]:
        result = self.aggregated_value(date_start=date_start, date_stop=date_start)

        if result is None:
            logger.debug("Metric evaluated to none", extra={"state": self._current_state()})

        return result

    def _get_metrics(self):
        metrics = [value.name for value in self._metric.numerator if value]
        if self._metric.denominator:
            metrics += [value.name for value in self._metric.denominator if value]
        return metrics

    def _get_metrics_values(self,
                            date_start: typing.AnyStr = None,
                            date_stop: typing.AnyStr = None) -> typing.List[typing.Dict]:
        try:
            metrics_values = self._repository.get_metrics_values(key_value=self._facebook_id,
                                                                 date_start=date_start,
                                                                 date_stop=date_stop,
                                                                 metrics=self._get_metrics(),
                                                                 level=self._level,
                                                                 breakdown_metadata=self._breakdown_metadata)
        except Exception as e:
            logger.debug(
                f"Failed to get metric values || {repr(e)}",
                extra={"state": self._current_state()},
                exc_info=True,
            )
            raise e

        if not metrics_values:
            logger.debug("No metric values returned from DB", extra={"state": self._current_state()})

        if hasattr(self, "minimum_number_of_data_points") \
                and getattr(self, "minimum_number_of_data_points") is not None \
                and date_stop != date_start:
            return metrics_values if len(metrics_values) >= getattr(self, "minimum_number_of_data_points") else []

        return metrics_values

    def __get_min_metrics_values(self):
        try:
            min_values = self._repository.get_min_value(key_value=self._facebook_id,
                                                        metrics=self._get_metrics(),
                                                        level=self._level,
                                                        breakdown_metadata=self._breakdown_metadata)
        except Exception as e:
            logger.debug(
                f"Failed to get min metric values || {repr(e)}",
                extra={"state": self._current_state()},
                exc_info=True,
            )
            raise e

        if not min_values:
            logger.debug("No min metric values returned from DB", extra={"state": self._current_state()})

        return min_values

    def __get_max_metrics_values(self):
        try:
            max_values = self._repository.get_max_value(key_value=self._facebook_id,
                                                        metrics=self._get_metrics(),
                                                        level=self._level,
                                                        breakdown_metadata=self._breakdown_metadata)
        except Exception as e:
            logger.debug(
                f"Failed to get max metric values || {repr(e)}",
                extra={"state": self._current_state()},
                exc_info=True,
            )
            raise e

        if not max_values:
            logger.debug("No max metric values returned from DB", extra={"state": self._current_state()})

        return max_values
