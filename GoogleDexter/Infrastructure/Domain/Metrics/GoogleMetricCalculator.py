import hashlib
import random
import typing
from datetime import datetime, timedelta

import numpy as np
from cachetools.func import lru_cache

from Core.Dexter.Engine.Algorithms.FuzzyRuleBasedOptimization.TimeBucketWeightingMethods.TimeBucketWeightingBySpend import \
    time_bucket_weighting_by_spend
from Core.Dexter.Infrastructure.Domain.DaysEnum import DaysEnum
from Core.Dexter.Infrastructure.Domain.Metrics.MetricCalculatorBase import MetricCalculatorBase
from Core.Dexter.Infrastructure.Domain.Metrics.MetricEnums import MetricTrendTimeBucketEnum
from Core.Dexter.Infrastructure.Domain.Rules.AntecedentEnums import AntecedentTypeEnum
from Core.logging_legacy import MongoLogger, log_message_as_dict
from Core.Tools.Misc.Constants import DEFAULT_DATETIME, DEFAULT_DATETIME_ISO
from GoogleDexter.Engine.Algorithms.FuzzyRuleBasedOptimization.Metrics.GoogleAvailableMetricEnum import \
    GoogleAvailableMetricEnum
from GoogleDexter.Infrastructure.Domain.Metrics.GoogleMetricEnums import GoogleMetricTypeEnum


import logging

logger_native = logging.getLogger(__name__)


class GoogleMetricCalculator(MetricCalculatorBase):

    def __init__(self):
        super().__init__()
        self._calculator = None
        value = str(random.randint(0, 1e20)) + self._date_stop.strftime(DEFAULT_DATETIME_ISO)
        self._calculator_id = hashlib.sha1(value.encode('utf-8')).hexdigest()

        if self._repository is not None:
            self.__logger = MongoLogger(repository=self._repository,
                                        database_name=self._repository.config.logs_database)
        else:
            self.__logger = None

    def __current_state(self):
        current_state = {
            "object_id": id(self),
            "calculator_id": self._calculator_id,
            "structure_id": self._structure_id,
            "metric": self._metric,
            "level": self._level,
            "breakdown_metadata": self._breakdown_metadata,
            "business_owner_id": self._business_owner_id,
        }
        return current_state

    @property
    def _logger(self):
        if self.__logger is None and self._repository is not None:
            self.__logger = MongoLogger(repository=self._repository,
                                        database_name=self._repository.config.logs_database)
        return self.__logger

    @property
    def calculator(self):
        if self._calculator is None:
            self._calculator = {
                (AntecedentTypeEnum.VALUE, GoogleMetricTypeEnum.STRUCTURE): self.structure_value,
                (AntecedentTypeEnum.FUZZY_VALUE, GoogleMetricTypeEnum.INSIGHT): self.fuzzy_value,
                (AntecedentTypeEnum.FUZZY_TREND, GoogleMetricTypeEnum.INSIGHT): self.fuzzy_trend,
                (AntecedentTypeEnum.WEIGHTED_FUZZY_TREND, GoogleMetricTypeEnum.INSIGHT): self.weighted_fuzzy_trend,
                (AntecedentTypeEnum.VALUE, GoogleMetricTypeEnum.INSIGHT): self.aggregated_value,
                (AntecedentTypeEnum.TREND, GoogleMetricTypeEnum.INSIGHT): self.trend,
                (AntecedentTypeEnum.WEIGHTED_TREND, GoogleMetricTypeEnum.INSIGHT): self.weighted_trend,
                (AntecedentTypeEnum.CURRENT_VALUE, GoogleMetricTypeEnum.INSIGHT): self.raw_value,
                (AntecedentTypeEnum.DIFFERENCE, GoogleMetricTypeEnum.INSIGHT): self.difference,
                (AntecedentTypeEnum.PERCENTAGE_DIFFERENCE, GoogleMetricTypeEnum.INSIGHT): self.percentage_difference,
                (AntecedentTypeEnum.VALUE, GoogleMetricTypeEnum.INSIGHT_CATEGORICAL): self.categorical_value,
                (AntecedentTypeEnum.VALUE, GoogleMetricTypeEnum.KEYWORDS): self.multiple_keywords_in_adgroup
            }

        return self._calculator

    def multiple_keywords_in_adgroup(self, *args, **kwargs) -> typing.Any:
        structure_details = self._repository.get_structure_details(key_value=self._structure_id, level=self._level)
        criteria = structure_details['criteria']

        truth_value = False
        if criteria:
            keyword_text = None
            for criterion in criteria:
                if criterion['criterion']['type'] == 'KEYWORD':
                    if not keyword_text:
                        keyword_text = criterion['criterion']['text']

                    if keyword_text != criterion['criterion']['text']:
                        truth_value = True
                        break

        return truth_value

    @lru_cache(maxsize=MetricCalculatorBase.MAX_CACHE_SIZE)
    def weighted_trend(self, date_start: typing.AnyStr = None, date_stop: typing.AnyStr = None) -> float:
        _date_start = datetime.strptime(date_start, DEFAULT_DATETIME)
        _date_stop = datetime.strptime(date_stop, DEFAULT_DATETIME)
        current_value = self.aggregated_value(date_start=date_stop, date_stop=date_stop)

        mc = GoogleMetricCalculator()
        mc = (mc.
              set_structure_id(self._structure_id).
              set_level(self._level).
              set_metric(GoogleAvailableMetricEnum.AVERAGE_SPEND.value).
              set_repository(self._repository).
              set_date_stop(self._date_stop).
              set_time_interval(self._time_interval).
              set_breakdown_metadata(self._breakdown_metadata))

        # todo: change to max_interval --> 3 months
        max_spend, _ = mc.compute_value(AntecedentTypeEnum.VALUE, self._time_interval)
        slopes = []
        for time_bucket in MetricTrendTimeBucketEnum:
            date_start = (_date_stop - timedelta(days=time_bucket.value))
            if time_bucket.value <= self._time_interval:
                if date_start >= _date_start:
                    date_start = date_start.strftime(DEFAULT_DATETIME)
                    bucket_value = self.aggregated_value(date_start=date_start, date_stop=date_stop)

                    if bucket_value:
                        dy = current_value - bucket_value
                        dt = time_bucket.value
                        spend, _ = mc.compute_value(AntecedentTypeEnum.VALUE, time_interval=time_bucket)
                        weighted_spend = float(spend) / float(max_spend)
                        weighted_time_bucket = float(time_bucket.value) / float(DaysEnum.MONTH.value)
                        w = time_bucket_weighting_by_spend(weighted_spend, weighted_time_bucket)
                        slope = w * np.arctan2(dy, dt)
                        slopes.append(slope)
                    else:
                        slopes.append(None)
                        self._logger.logger.info(log_message_as_dict(mtype=logging.WARNING,
                                                  name="MetricCalculator",
                                                  description=f"Time bucket for interval {time_bucket.value} is None.",
                                                  extra_data={
                                                    "state": self.__current_state()
                                                }))

        trend = self._compute_resultant_slope(slopes)

        return trend

    @lru_cache(maxsize=MetricCalculatorBase.MAX_CACHE_SIZE)
    def weighted_fuzzy_trend(self, date_start: typing.AnyStr = None, date_stop: typing.AnyStr = None):
        value = self.weighted_trend(date_start, date_stop)
        return self._fuzzy_value_base(value, AntecedentTypeEnum.WEIGHTED_FUZZY_TREND)
