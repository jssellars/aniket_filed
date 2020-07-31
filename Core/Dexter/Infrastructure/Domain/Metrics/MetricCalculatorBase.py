import traceback
import typing
from datetime import timedelta, datetime
from functools import lru_cache

import numpy as np

from Core.Dexter.Infrastructure.Domain.Breakdowns import BreakdownBaseEnum, ActionBreakdownBaseEnum, \
    BreakdownMetadataBase
from Core.Dexter.Infrastructure.Domain.DaysEnum import DaysEnum
from Core.Dexter.Infrastructure.Domain.Metrics.MetricCalculatorBuilder import MetricCalculatorBuilder
from Core.Dexter.Infrastructure.Domain.Metrics.MetricEnums import AggregatorEnum, MetricTrendTimeBucketEnum
from Core.Dexter.Infrastructure.Domain.Rules.AntecedentEnums import AntecedentTypeEnum
from Core.Tools.Logger.LoggerMessageBase import LoggerMessageTypeEnum, LoggerMessageBase
from Core.Tools.Logger.MongoLoggers.MongoLogger import MongoLogger
from Core.Tools.Misc.Constants import DEFAULT_DATETIME


class MetricCalculatorBase(MetricCalculatorBuilder):
    MAX_CACHE_SIZE = 2048

    def __init__(self):
        super().__init__()
        self._calculator_id = ''
        self._calculator = None
        self.__logger = None

    @property
    def _logger(self):
        if self.__logger is None or self._repository is not None:
            self.__logger = MongoLogger(repository=self._repository,
                                        database_name=self._repository.config.logs_database)
        return self.__logger

    @property
    def calculator(self):
        if self._calculator is None:
            raise NotImplementedError

        return self._calculator

    def _current_state(self):
        raise NotImplementedError

    def compute_value(self, atype: AntecedentTypeEnum = None,
                      time_interval: typing.Union[DaysEnum, int] = DaysEnum.ONE) -> \
            typing.Tuple[typing.Any, typing.Any]:
        date_stop = self._date_stop
        try:
            date_start = date_stop - timedelta(days=time_interval)
        except TypeError:
            date_start = date_stop - timedelta(days=time_interval.value)
        except Exception:
            if self._debug:
                log = LoggerMessageBase(mtype=LoggerMessageTypeEnum.ERROR,
                                        name="MetricCalculator",
                                        description=f"Failed to process date start and date stop for "
                                                    f"time interval {time_interval}.",
                                        extra_data={
                                            "state": self._current_state(),
                                            "error": traceback.format_exc()
                                        })
                self._logger.logger.info(log)
            date_start = date_stop

        calculator = self.calculator.get((atype, self._metric.type), None)

        if calculator is None:
            if self._debug:
                log = LoggerMessageBase(mtype=LoggerMessageTypeEnum.ERROR,
                                        name="MetricCalculator",
                                        description="Invalid antecedent and metric type combination.",
                                        extra_data={"state": self._current_state()})
                self._logger.logger.info(log)
            return None, None

        try:
            result = calculator(date_start.strftime(DEFAULT_DATETIME),
                                date_stop.strftime(DEFAULT_DATETIME),
                                metric=self._metric,
                                facebook_id=self._facebook_id)
        except Exception as e:
            if self._debug:
                log = LoggerMessageBase(mtype=LoggerMessageTypeEnum.ERROR,
                                        name="MetricCalculator",
                                        description="Other calculator exception.",
                                        extra_data={
                                            "state": self._current_state(),
                                            "error": traceback.format_exc()
                                        })
                self._logger.logger.info(log)
            return None, None

        if not isinstance(result, list) and not isinstance(result, tuple):
            return result, None
        else:
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
            if self._debug:
                log = LoggerMessageBase(mtype=LoggerMessageTypeEnum.ERROR,
                                        name="MetricCalculator",
                                        description="Failed to get breakdown values.",
                                        extra_data={
                                            "state": self._current_state(),
                                            "error": traceback.format_exc()
                                        })
                self._logger.logger.info(log)
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

    @lru_cache(maxsize=MAX_CACHE_SIZE)
    def structure_value(self, *args, **kwargs) -> typing.Any:
        structure_details = self._repository.get_structure_details(key_value=self._facebook_id, level=self._level)
        return structure_details.get(self._metric.name)

    def values(self, date_start: typing.AnyStr = None, date_stop: typing.AnyStr = None) -> typing.List[float]:
        data = self._get_metrics_values(date_start=date_start, date_stop=date_stop)

        numerator = self._compute_numerator_value(data=data)
        denominator = self._compute_denominator_values(data=data)

        if len(numerator) != len(denominator):
            if self._debug:
                log = LoggerMessageBase(mtype=LoggerMessageTypeEnum.ERROR,
                                        name="MetricCalculator",
                                        description="Numerator and denominator data mismatch.",
                                        extra_data={
                                            "state": self._current_state()
                                        })
                self._logger.logger.info(log)

            raise ValueError("Numerator and denominator data mismatch.")

        values = numerator
        for index in range(len(numerator)):
            if denominator[index]:
                values[index] /= denominator[index]

        return values

    def average(self, date_stop, date_start, *args, **kwargs):
        date_start = datetime.strptime(date_start, DEFAULT_DATETIME) - timedelta(days=1)
        date_start = datetime.strftime(date_start, DEFAULT_DATETIME)
        value = self.aggregated_value(date_start=date_stop, date_stop=date_start)
        date_stop = datetime.strptime(date_stop, DEFAULT_DATETIME)
        date_start = datetime.strptime(date_start, DEFAULT_DATETIME)
        days = (date_start - date_stop).days + 1

        return value / days

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
        except Exception:
            if self._debug:
                log = LoggerMessageBase(mtype=LoggerMessageTypeEnum.ERROR,
                                        name="MetricCalculator",
                                        description="Failed to compute aggregated metric value",
                                        extra_data={
                                            "state": self._current_state(),
                                            "error": traceback.format_exc()
                                        })
                self._logger.logger.info(log)

    @lru_cache(maxsize=MAX_CACHE_SIZE)
    def aggregated_value(self, date_start: typing.AnyStr = None, date_stop: typing.AnyStr = None, **kwargs) -> float:
        data = self._get_metrics_values(date_start=date_start, date_stop=date_stop)
        return self.__compute_aggregated_value(data)

    @lru_cache(maxsize=MAX_CACHE_SIZE)
    def categorical_value(self, *args, **kwargs) -> typing.AnyStr:
        date_stop = self._date_stop
        date_start = date_stop - timedelta(days=DaysEnum.THREE_MONTHS.value)

        data = self._get_metrics_values(date_start.strftime(DEFAULT_DATETIME), date_stop.strftime(DEFAULT_DATETIME))

        value = data[-1].get(self._metric.name, None) if data else None

        if value is None:
            if self._debug:
                log = LoggerMessageBase(mtype=LoggerMessageTypeEnum.WARNING,
                                        name="MetricCalculator",
                                        description="Categorical value is none",
                                        extra_data={
                                            "state": self._current_state(),
                                            "values": data
                                        })
                self._logger.logger.info(log)

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

    @lru_cache(maxsize=MAX_CACHE_SIZE)
    def trend(self, date_start: typing.AnyStr = None, date_stop: typing.AnyStr = None, **kwargs) -> typing.Union[
        typing.NoReturn, float]:
        _date_start = datetime.strptime(date_start, DEFAULT_DATETIME)
        _date_stop = datetime.strptime(date_stop, DEFAULT_DATETIME)
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
                    if self._debug:
                        log = LoggerMessageBase(mtype=LoggerMessageTypeEnum.WARNING,
                                                name="MetricCalculator",
                                                description=f"Time bucket for interval {time_bucket.value} is None.",
                                                extra_data={
                                                    "state": self._current_state()
                                                })
                        self._logger.logger.info(log)

        trend = self._compute_resultant_slope(slopes)

        return trend

    def _compute_resultant_slope(self, slopes: typing.List = None) -> float:
        unit_vectors = [(np.cos(slope), np.sin(slope)) for slope in slopes if slope is not None]
        mean_unit_vector = np.mean(unit_vectors, axis=0)

        resultant_slope = None

        if mean_unit_vector.size > 1:
            try:
                resultant_slope = np.arctan2(mean_unit_vector[1], mean_unit_vector[0])
            except Exception:
                if self._debug:
                    log = LoggerMessageBase(mtype=LoggerMessageTypeEnum.ERROR,
                                            name="MetricCalculator",
                                            description="Failed to compute resultant slope.",
                                            extra_data={
                                                "state": self._current_state(),
                                                "error": traceback.format_exc()
                                            })
                    self._logger.logger.info(log)

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
            if self._debug:
                log = LoggerMessageBase(mtype=LoggerMessageTypeEnum.WARNING,
                                        name="MetricCalculator",
                                        description=f"Couldn't compute the min-max normalized value "
                                                    f"for {value}, {min_value}, {max_value}.",
                                        extra_data={
                                            "state": self._current_state()
                                        })
                self._logger.logger.info(log)

        return scaled_value

    @lru_cache(maxsize=MAX_CACHE_SIZE)
    def fuzzy_value(self,
                    date_start: typing.AnyStr = None,
                    date_stop: typing.AnyStr = None,
                    **kwargs):
        value = self._min_max_normalized_value(date_start, date_stop)
        return self._fuzzy_value_base(value, AntecedentTypeEnum.FUZZY_VALUE)

    @lru_cache(maxsize=MAX_CACHE_SIZE)
    def fuzzy_trend(self,
                    date_start: typing.AnyStr = None,
                    date_stop: typing.AnyStr = None,
                    **kwargs):
        value = self.trend(date_start, date_stop)
        return self._fuzzy_value_base(value, AntecedentTypeEnum.FUZZY_TREND)

    @lru_cache(maxsize=MAX_CACHE_SIZE)
    def weighted_fuzzy_trend(self,
                             date_start: typing.AnyStr = None,
                             date_stop: typing.AnyStr = None,
                             **kwargs):
        raise NotImplementedError

    @lru_cache(maxsize=MAX_CACHE_SIZE)
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
        except Exception:
            if self._debug:
                log = LoggerMessageBase(mtype=LoggerMessageTypeEnum.ERROR,
                                        name="MetricCalculator",
                                        description=f"Couldn't compute fuzzy value for {value} and "
                                                    f"fuzzyfier {fuzzyfier_type.value}.",
                                        extra_data={
                                            "state": self._current_state(),
                                            "fuzzyfier": fuzzyfier,
                                            "error": traceback.format_exc()
                                        })
                self._logger.logger.info(log)

        return fuzzy_class, fuzzy_membership_value

    @lru_cache(maxsize=MAX_CACHE_SIZE)
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
            if self._debug:
                log = LoggerMessageBase(mtype=LoggerMessageTypeEnum.WARNING,
                                        name="MetricCalculator",
                                        description="Ill-defined difference. Initial metric value is none.",
                                        extra_data={
                                            "state": self._current_state()
                                        })
                self._logger.logger.info(log)
        elif initial_metric_value is not None and current_metric_value is None:
            difference = initial_metric_value
            if self._debug:
                log = LoggerMessageBase(mtype=LoggerMessageTypeEnum.WARNING,
                                        name="MetricCalculator",
                                        description="Ill-defined difference. Current metric value is none.",
                                        extra_data={
                                            "state": self._current_state()
                                        })
                self._logger.logger.info(log)
        else:
            difference = None
            if self._debug:
                log = LoggerMessageBase(mtype=LoggerMessageTypeEnum.WARNING,
                                        name="MetricCalculator",
                                        description="Ill-defined difference. Both initial and current metrics are none",
                                        extra_data={
                                            "state": self._current_state()
                                        })
                self._logger.logger.info(log)
        return difference

    @lru_cache(maxsize=MAX_CACHE_SIZE)
    def percentage_difference(self,
                              date_start: typing.AnyStr = None,
                              date_stop: typing.AnyStr = None,
                              **kwargs) -> typing.Union[int, float, typing.NoReturn]:

        date_start_ = datetime.strptime(date_start, DEFAULT_DATETIME) - timedelta(days=1)
        date_stop_ = datetime.strptime(date_stop, DEFAULT_DATETIME) - timedelta(days=1)
        days = abs((date_stop_ - date_start_).days)

        mean_on_time_interval = self.aggregated_value(date_start=date_start, date_stop=date_stop) / days
        current_metric_value = self.aggregated_value(date_start=date_stop, date_stop=date_stop)
        if mean_on_time_interval is not None and current_metric_value is not None:
            if mean_on_time_interval == 0.0 or current_metric_value == 0.0:
                return 100
            try:
                if mean_on_time_interval < current_metric_value:
                    difference = 100 * (current_metric_value - mean_on_time_interval) / current_metric_value
                else:
                    difference = 100 * (mean_on_time_interval - current_metric_value) / mean_on_time_interval
            except ZeroDivisionError:
                if current_metric_value == 0.0:
                    difference = None
                    if self._debug:
                        log = LoggerMessageBase(mtype=LoggerMessageTypeEnum.WARNING,
                                                name="MetricCalculator",
                                                description="Ill-defined percentage difference. Initial metric value and current metric value are none.",
                                                extra_data={
                                                    "state": self._current_state()
                                                })
                        self._logger.logger.info(log)
                else:
                    difference = 100 * current_metric_value
        elif mean_on_time_interval is None and current_metric_value is not None:
            difference = None
            if self._debug:
                log = LoggerMessageBase(mtype=LoggerMessageTypeEnum.WARNING,
                                        name="MetricCalculator",
                                        description="Ill-defined percentage difference. Initial metric value is none.",
                                        extra_data={
                                            "state": self._current_state()
                                        })
                self._logger.logger.info(log)
        elif mean_on_time_interval is not None and current_metric_value is None:
            difference = None
            if self._debug:
                log = LoggerMessageBase(mtype=LoggerMessageTypeEnum.WARNING,
                                        name="MetricCalculator",
                                        description="Ill-defined percentage difference. Current metric value is none.",
                                        extra_data={
                                            "state": self._current_state()
                                        })
                self._logger.logger.info(log)
        else:
            difference = None
            if self._debug:
                log = LoggerMessageBase(mtype=LoggerMessageTypeEnum.WARNING,
                                        name="MetricCalculator",
                                        description="Ill-defined percentage difference. Both initial and "
                                                    "current metrics are none",
                                        extra_data={
                                            "state": self._current_state()
                                        })
                self._logger.logger.info(log)
        return difference

    @lru_cache(maxsize=MAX_CACHE_SIZE)
    def raw_value(self, date_start: typing.AnyStr = None, *args, **kwargs) -> typing.Union[int, float]:
        result = self.aggregated_value(date_start=date_start, date_stop=date_start)

        if result is None:
            if self._debug:
                log = LoggerMessageBase(mtype=LoggerMessageTypeEnum.WARNING,
                                        name="MetricCalculator",
                                        description="Metric evaluated to none",
                                        extra_data={
                                            "state": self._current_state()
                                        })
                self._logger.logger.info(log)

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
            if self._debug:
                log = LoggerMessageBase(mtype=LoggerMessageTypeEnum.ERROR,
                                        name="MetricCalculator",
                                        description="Failed to get metric values.",
                                        extra_data={
                                            "state": self._current_state(),
                                            "error": traceback.format_exc()
                                        })
                self._logger.logger.info(log)
            raise e

        if not metrics_values:
            if self._debug:
                log = LoggerMessageBase(mtype=LoggerMessageTypeEnum.WARNING,
                                        name="MetricCalculator",
                                        description="No metric values returned from DB",
                                        extra_data={
                                            "state": self._current_state()
                                        })
                self._logger.logger.info(log)
        return metrics_values

    def __get_min_metrics_values(self):
        try:
            min_values = self._repository.get_min_value(key_value=self._facebook_id,
                                                        metrics=self._get_metrics(),
                                                        level=self._level,
                                                        breakdown_metadata=self._breakdown_metadata)
        except Exception as e:
            if self._debug:
                log = LoggerMessageBase(mtype=LoggerMessageTypeEnum.ERROR,
                                        name="MetricCalculator",
                                        description="Failed to get min metric values.",
                                        extra_data={
                                            "state": self._current_state(),
                                            "error": traceback.format_exc()
                                        })
                self._logger.logger.info(log)
            raise e

        if not min_values:
            if self._debug:
                log = LoggerMessageBase(mtype=LoggerMessageTypeEnum.WARNING,
                                        name="MetricCalculator",
                                        description="No min metric values returned from DB",
                                        extra_data={
                                            "state": self._current_state()
                                        })
                self._logger.logger.info(log)

        return min_values

    def __get_max_metrics_values(self):
        try:
            max_values = self._repository.get_max_value(key_value=self._facebook_id,
                                                        metrics=self._get_metrics(),
                                                        level=self._level,
                                                        breakdown_metadata=self._breakdown_metadata)
        except Exception as e:
            if self._debug:
                log = LoggerMessageBase(mtype=LoggerMessageTypeEnum.ERROR,
                                        name="MetricCalculator",
                                        description="Failed to get max metric values.",
                                        extra_data={
                                            "state": self._current_state(),
                                            "error": traceback.format_exc()
                                        })
                self._logger.logger.info(log)
            raise e

        if not max_values:
            if self._debug:
                log = LoggerMessageBase(mtype=LoggerMessageTypeEnum.WARNING,
                                        name="MetricCalculator",
                                        description="No max metric values returned from DB",
                                        extra_data={
                                            "state": self._current_state()
                                        })
                self._logger.logger.info(log)

        return max_values
