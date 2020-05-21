import hashlib
import random
import traceback
import typing
from datetime import datetime, timedelta

import numpy as np
from facebook_business.adobjects.ad import Ad
from facebook_business.adobjects.adaccount import AdAccount

from Core.Tools.Logger.LoggerMessageBase import LoggerMessageBase, LoggerMessageTypeEnum
from Core.Tools.Logger.MongoLoggers.MongoLogger import MongoLogger
from Core.Web.BusinessOwnerRepository.BusinessOwnerRepository import BusinessOwnerRepository
from Core.Web.FacebookGraphAPI.GraphAPI.GraphAPISdkBase import GraphAPISdkBase
from FacebookDexter.Engine.Algorithms.FuzzyRuleBasedOptimization.Metrics.AvailableMetricEnum import AvailableMetricEnum
from FacebookDexter.Engine.Algorithms.FuzzyRuleBasedOptimization.TimeBucketWeightingMethods.TimeBucketWeightingBySpend import \
    time_bucket_weighting_by_spend
from FacebookDexter.Infrastructure.Constants import DEFAULT_DATETIME, DEFAULT_DATETIME_ISO
from FacebookDexter.Infrastructure.Domain.Breakdowns import BreakdownMetadata, BreakdownEnum, ActionBreakdownEnum
from FacebookDexter.Infrastructure.Domain.DaysEnum import DaysEnum
from FacebookDexter.Infrastructure.Domain.LevelEnums import LevelEnum
from FacebookDexter.Infrastructure.Domain.Metrics.MetricCalculatorBuilder import MetricCalculatorBuilder
from FacebookDexter.Infrastructure.Domain.Metrics.MetricEnums import AggregatorEnum, MetricTrendTimeBucketEnum, \
    MetricTypeEnum
from FacebookDexter.Infrastructure.Domain.Rules.AntecedentEnums import AntecedentTypeEnum
from FacebookDexter.Infrastructure.FuzzyEngine.FuzzySets.FuzzySets import LinguisticVariableEnum


class MetricCalculator(MetricCalculatorBuilder):

    def __init__(self):
        super().__init__()
        self.__calculator = None
        value = str(random.randint(0, 1e20)) + datetime.now().strftime(DEFAULT_DATETIME_ISO)
        self.__calculator_id = hashlib.sha1(value.encode('utf-8')).hexdigest()

        if self._repository is not None:
            self.__logger = MongoLogger(repository=self._repository,
                                        database_name=self._repository.config.logs_database)
        else:
            self.__logger = None

    def __current_state(self):
        current_state = {
            "object_id": id(self),
            "calculator_id": self.__calculator_id,
            "facebook_id": self._facebook_id,
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
                                        database_name=self._repository.config.logs_database, )
        return self.__logger

    @property
    def calculator(self):
        if self.__calculator is None:
            self.__calculator = {
                (AntecedentTypeEnum.VALUE, MetricTypeEnum.STRUCTURE): self.structure_value,
                (AntecedentTypeEnum.FUZZY_VALUE, MetricTypeEnum.INSIGHT): self.fuzzy_value,
                (AntecedentTypeEnum.FUZZY_TREND, MetricTypeEnum.INSIGHT): self.fuzzy_trend,
                (AntecedentTypeEnum.WEIGHTED_FUZZY_TREND, MetricTypeEnum.INSIGHT): self.weighted_fuzzy_trend,
                (AntecedentTypeEnum.VALUE, MetricTypeEnum.INSIGHT): self.aggregated_value,
                (AntecedentTypeEnum.TREND, MetricTypeEnum.INSIGHT): self.trend,
                (AntecedentTypeEnum.WEIGHTED_TREND, MetricTypeEnum.INSIGHT): self.weighted_trend,
                (AntecedentTypeEnum.CURRENT_VALUE, MetricTypeEnum.INSIGHT): self.raw_value,
                (AntecedentTypeEnum.DIFFERENCE, MetricTypeEnum.INSIGHT): self.difference,
                (AntecedentTypeEnum.PERCENTAGE_DIFFERENCE, MetricTypeEnum.INSIGHT): self.percentage_difference,
                (AntecedentTypeEnum.VALUE, MetricTypeEnum.AUDIENCE): self.audience_size,
                (AntecedentTypeEnum.VALUE, MetricTypeEnum.PIXEL): self.has_pixel,
                (AntecedentTypeEnum.VALUE, MetricTypeEnum.CREATIVE): self.has_over_20p_text,
                (AntecedentTypeEnum.VALUE, MetricTypeEnum.PROSPECTING): self.is_prospecting_campaign,
                (AntecedentTypeEnum.VALUE, MetricTypeEnum.INSIGHT_CATEGORICAL): self.categorical_value
            }

        return self.__calculator

    def compute_value(self, atype: AntecedentTypeEnum = None,
                      time_interval: typing.Union[DaysEnum, int] = DaysEnum.ONE) -> \
            typing.Tuple[typing.Any, typing.Any]:
        date_stop = datetime.now()
        try:
            date_start = date_stop - timedelta(days=time_interval)
        except TypeError:
            date_start = date_stop - timedelta(days=time_interval.value)
        except Exception:
            log = LoggerMessageBase(mtype=LoggerMessageTypeEnum.ERROR,
                                    name="MetricCalculator",
                                    description=f"Failed to process date start and date stop for "
                                                f"time interval {time_interval}.",
                                    extra_data={
                                        "state": self.__current_state(),
                                        "error": traceback.format_exc()
                                    })
            self._logger.logger.info(log)
            date_start = date_stop

        calculator = self.calculator.get((atype, self._metric.type), None)

        if calculator is None:
            log = LoggerMessageBase(mtype=LoggerMessageTypeEnum.ERROR,
                                    name="MetricCalculator",
                                    description="Invalid antecedent and metric type combination.",
                                    extra_data={"state": self.__current_state()})
            self._logger.logger.info(log)
            return None, None

        try:
            result = calculator(date_start.strftime(DEFAULT_DATETIME), date_stop.strftime(DEFAULT_DATETIME))
        except Exception:
            log = LoggerMessageBase(mtype=LoggerMessageTypeEnum.ERROR,
                                    name="MetricCalculator",
                                    description="Other calculator exception.",
                                    extra_data={
                                        "state": self.__current_state(),
                                        "error": traceback.format_exc()
                                    })
            self._logger.logger.info(log)
            return None, None

        if not isinstance(result, list) and not isinstance(result, tuple):
            return result, None
        else:
            return result

    def get_breakdown_metadata(self,
                               breakdown: BreakdownEnum = None,
                               action_breakdown: ActionBreakdownEnum = None,
                               time_interval: DaysEnum = None) -> typing.List[BreakdownMetadata]:
        date_stop = datetime.now()
        date_start = date_stop - timedelta(days=time_interval.value)

        try:
            breakdown_values = self._repository.get_breakdown_values(key_value=self._facebook_id,
                                                                     level=self._level,
                                                                     date_start=date_start.strftime(DEFAULT_DATETIME),
                                                                     date_stop=date_stop.strftime(DEFAULT_DATETIME),
                                                                     breakdown=breakdown,
                                                                     action_breakdown=action_breakdown)
        except Exception as e:
            log = LoggerMessageBase(mtype=LoggerMessageTypeEnum.ERROR,
                                    name="MetricCalculator",
                                    description="Failed to get breakdown values.",
                                    extra_data={
                                        "state": self.__current_state(),
                                        "error": traceback.format_exc()
                                    })
            self._logger.logger.info(log)
            raise e

        if breakdown_values:
            breakdown_metadata = [BreakdownMetadata(breakdown=breakdown, breakdown_value=breakdown_value[0],
                                                    action_breakdown=action_breakdown,
                                                    action_breakdown_value=breakdown_value[1])
                                  for breakdown_value in breakdown_values]
        else:
            breakdown_metadata = [BreakdownMetadata(breakdown=breakdown,
                                                    action_breakdown=action_breakdown)]
        return breakdown_metadata

    def __compute_numerator_value(self, data: typing.List[typing.Dict]) -> typing.List[float]:
        return [AggregatorEnum.SUM.value([entry[metric.name] for metric in self._metric.numerator]) for entry in data]

    def __compute_denominator_values(self, data: typing.List[typing.Dict]) -> typing.List[float]:
        return [AggregatorEnum.SUM.value([entry[metric.name] for metric in self._metric.denominator]) for entry in
                data]

    def audience_size(self, *args, **kwargs) -> typing.Any:
        audience_details = self.structure_value()

        permanent_token = BusinessOwnerRepository(self._business_owner_repo_session).get_permanent_token(
            self._business_owner_id)
        _ = GraphAPISdkBase(self._facebook_config, permanent_token)

        ad_account_id = self._repository.get_ad_account_id(self._facebook_id, self._level)

        try:
            ad_account = AdAccount(fbid=ad_account_id)
            audience_size_estimate = ad_account.get_reach_estimate(params={'targeting_spec': audience_details})
        except Exception as e:
            audience_size_estimate = None

            log = LoggerMessageBase(mtype=LoggerMessageTypeEnum.WARNING,
                                    name="MetricCalculator",
                                    description="Failed to get audience size.",
                                    extra_data={
                                        "state": self.__current_state(),
                                        "error": traceback.format_exc()
                                    })
            self._logger.logger.info(log)

        return audience_size_estimate

    def has_pixel(self, *args, **kwargs) -> typing.Any:
        permanent_token = BusinessOwnerRepository(self._business_owner_repo_session).get_permanent_token(
            self._business_owner_id)
        _ = GraphAPISdkBase(self._facebook_config, permanent_token)

        ad_account_id = self._repository.get_ad_account_id(self._facebook_id, self._level)

        try:
            ad_account = AdAccount(fbid=ad_account_id)
            pixels = ad_account.get_ads_pixels()
        except Exception as e:
            pixels = []

            log = LoggerMessageBase(mtype=LoggerMessageTypeEnum.WARNING,
                                    name="MetricCalculator",
                                    description="Failed to get pixels.",
                                    extra_data={
                                        "state": self.__current_state(),
                                        "error": traceback.format_exc()
                                    })
            self._logger.logger.info(log)

        return len(pixels) > 0

    def has_over_20p_text(self, *args, **kwargs):
        structure_details = self._repository.get_structure_details(key_value=self._facebook_id, level=self._level)
        text_overlay_rec_codes = [1942017, 1942018, 1942019]
        if Ad.Field.recommendations in structure_details:
            for recommendation in structure_details[Ad.Field.recommendations]:
                if recommendation['code'] in text_overlay_rec_codes:
                    return True
        return False

    def structure_value(self, *args, **kwargs) -> typing.Any:
        structure_details = self._repository.get_structure_details(key_value=self._facebook_id, level=self._level)
        return structure_details.get(self._metric.name)

    @staticmethod
    def __is_interest(entry: typing.Dict) -> bool:
        interest_keys = ['interests', 'behaviors', 'life_events', 'industries', 'income', 'family_statuses',
                         'education_schools',
                         'work_employers', 'education_majors', 'work_positions']
        if not isinstance(entry, dict):
            return False

        for key in entry.keys():
            if key not in interest_keys:
                return False

        return True

    def is_prospecting_campaign(self, *args, **kwargs) -> bool:
        if self._level == LevelEnum.CAMPAIGN:
            structure_id = self._repository.get_adset_id_by_campaign_id(key_value=self._facebook_id)
            structure_details = self._repository.get_structure_details(key_value=structure_id, level=LevelEnum.ADSET)
        elif self._level == LevelEnum.ADSET:
            structure_details = self._repository.get_structure_details(key_value=self._facebook_id, level=self._level)
        elif self._level == LevelEnum.AD:
            structure_id = self._repository.get_adset_id_by_campaign_id(key_value=self._facebook_id)
            structure_details = self._repository.get_structure_details(key_value=structure_id, level=LevelEnum.ADSET)
        else:
            raise ValueError(f"Cannot extract ad set targeting for level {self._level}")

        try:
            interests = [interest_dict['name']
                         for entry in structure_details['targeting']['flexible_spec']
                         for interest_lists in entry.values()
                         for interest_dict in interest_lists
                         if self.__is_interest(entry)]
            if not interests:
                return False
        except Exception as e:
            log = LoggerMessageBase(mtype=LoggerMessageTypeEnum.ERROR,
                                    name="MetricCalculator",
                                    description="Failed to get interests from structure targeting.",
                                    extra_data={
                                        "state": self.__current_state(),
                                        "error": traceback.format_exc()
                                    })
            self._logger.logger.info(log)
            return False

    def values(self, date_start: typing.AnyStr = None, date_stop: typing.AnyStr = None) -> typing.List[float]:
        data = self.__get_metrics_values(date_start=date_start, date_stop=date_stop)

        numerator = self.__compute_numerator_value(data=data)
        denominator = self.__compute_denominator_values(data=data)

        if len(numerator) != len(denominator):
            log = LoggerMessageBase(mtype=LoggerMessageTypeEnum.ERROR,
                                    name="MetricCalculator",
                                    description="Numerator and denominator data mismatch.",
                                    extra_data={
                                        "state": self.__current_state()
                                    })
            self._logger.logger.info(log)

            raise ValueError("Numerator and denominator data mismatch.")

        values = [numerator[index] / denominator[index] for index in range(len(numerator)) if denominator[index]]
        return values

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

            aggregated_numerator = numerator_aggregator_function(self.__compute_numerator_value(data))
            if isinstance(self._metric.denominator, list) and self._metric.denominator:
                aggregated_denominator = denominator_aggregator_function(self.__compute_denominator_values(data))
                return self._metric.multiplier * aggregated_numerator / aggregated_denominator \
                    if aggregated_denominator else None
            else:
                return self._metric.multiplier * aggregated_numerator
        except Exception:
            log = LoggerMessageBase(mtype=LoggerMessageTypeEnum.ERROR,
                                    name="MetricCalculator",
                                    description="Failed to compute aggregated metric value",
                                    extra_data={
                                        "state": self.__current_state(),
                                        "error": traceback.format_exc()
                                    })
            self._logger.logger.info(log)

    def aggregated_value(self, date_start: typing.AnyStr = None, date_stop: typing.AnyStr = None) -> float:
        data = self.__get_metrics_values(date_start=date_start, date_stop=date_stop)
        return self.__compute_aggregated_value(data)

    def categorical_value(self, *args, **kwargs) -> typing.AnyStr:
        date_stop = datetime.now()
        date_start = date_stop - timedelta(days=DaysEnum.THREE_MONTHS.value)

        data = self.__get_metrics_values(date_start.strftime(DEFAULT_DATETIME), date_stop.strftime(DEFAULT_DATETIME))

        value = data[-1].get(self._metric.name, None)

        if value is None:
            log = LoggerMessageBase(mtype=LoggerMessageTypeEnum.WARNING,
                                    name="MetricCalculator",
                                    description="Categorical value is none",
                                    extra_data={
                                        "state": self.__current_state(),
                                        "values": data
                                    })
            self._logger.logger.info(log)

        return value

    def min_max_value(self):
        date_stop = datetime.now()
        date_start = date_stop - timedelta(days=DaysEnum.THREE_MONTHS.value)
        data = self.values(date_start.strftime(DEFAULT_DATETIME), date_stop.strftime(DEFAULT_DATETIME))
        min_data = min(data) if data else None
        max_data = max(data) if data else None
        return min_data, max_data

    def min_value(self):
        date_stop = datetime.now()
        date_start = date_stop - timedelta(days=DaysEnum.THREE_MONTHS.value)
        data = self.values(date_start.strftime(DEFAULT_DATETIME), date_stop.strftime(DEFAULT_DATETIME))
        return min(data) if data else None

    def max_value(self):
        date_stop = datetime.now()
        date_start = date_stop - timedelta(days=DaysEnum.THREE_MONTHS.value)
        data = self.values(date_start.strftime(DEFAULT_DATETIME), date_stop.strftime(DEFAULT_DATETIME))
        return max(data) if data else None

    def trend(self, date_start: typing.AnyStr = None, date_stop: typing.AnyStr = None) -> typing.Union[typing.NoReturn, float]:
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
                    log = LoggerMessageBase(mtype=LoggerMessageTypeEnum.WARNING,
                                            name="MetricCalculator",
                                            description=f"Time bucket for interval {time_bucket.value} is None.",
                                            extra_data={
                                                "state": self.__current_state()
                                            })
                    self._logger.logger.info(log)

        trend = self.__compute_resultant_slope(slopes)

        return trend

    def weighted_trend(self, date_start: typing.AnyStr = None, date_stop: typing.AnyStr = None) -> float:
        _date_start = datetime.strptime(date_start, DEFAULT_DATETIME)
        _date_stop = datetime.strptime(date_stop, DEFAULT_DATETIME)
        current_value = self.aggregated_value(date_start=date_stop, date_stop=date_stop)

        mc = MetricCalculator()
        mc = mc. \
            set_facebook_id(self._facebook_id). \
            set_level(self._level). \
            set_metric(AvailableMetricEnum.AVERAGE_SPEND.value). \
            set_repository(self._repository). \
            set_breakdown_metadata(self._breakdown_metadata)

        # todo: change to max_interval --> 3 months
        max_spend, _ = mc.compute_value(AntecedentTypeEnum.VALUE, time_interval=DaysEnum.MONTH)
        slopes = []
        for time_bucket in MetricTrendTimeBucketEnum:
            date_start = (_date_stop - timedelta(days=time_bucket.value))

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
                    log = LoggerMessageBase(mtype=LoggerMessageTypeEnum.WARNING,
                                            name="MetricCalculator",
                                            description=f"Time bucket for interval {time_bucket.value} is None.",
                                            extra_data={
                                                "state": self.__current_state()
                                            })
                    self._logger.logger.info(log)

        trend = self.__compute_resultant_slope(slopes)

        return trend

    def __compute_resultant_slope(self, slopes: typing.List = None) -> float:
        unit_vectors = [(np.cos(slope), np.sin(slope)) for slope in slopes if slope is not None]
        mean_unit_vector = np.mean(unit_vectors, axis=0)

        resultant_slope = None

        if mean_unit_vector.size > 1:
            try:
                resultant_slope = np.arctan2(mean_unit_vector[1], mean_unit_vector[0])
            except Exception:
                log = LoggerMessageBase(mtype=LoggerMessageTypeEnum.ERROR,
                                        name="MetricCalculator",
                                        description="Failed to compute resultant slope.",
                                        extra_data={
                                            "state": self.__current_state(),
                                            "error": traceback.format_exc()
                                        })
                self._logger.logger.info(log)

        return resultant_slope

    def __min_max_normalized_value(self,
                                   date_start: typing.AnyStr = None,
                                   date_stop: typing.AnyStr = None) -> typing.Union[int, float]:
        value = self.aggregated_value(date_start, date_stop)
        min_value, max_value = self.min_max_value()
        if min_value is None:
            min_value = 0.0
        if value and min_value is not None and max_value is not None:
            scaled_value = (value - min_value) / (max_value - min_value)
        else:
            scaled_value = None
            log = LoggerMessageBase(mtype=LoggerMessageTypeEnum.WARNING,
                                    name="MetricCalculator",
                                    description=f"Couldn't compute the min-max normalized value "
                                                f"for {value}, {min_value}, {max_value}.",
                                    extra_data={
                                        "state": self.__current_state()
                                    })
            self._logger.logger.info(log)

        return scaled_value

    def fuzzy_value(self,
                    date_start: typing.AnyStr = None,
                    date_stop: typing.AnyStr = None) -> typing.Tuple[LinguisticVariableEnum, float]:
        value = self.__min_max_normalized_value(date_start, date_stop)
        return self.__fuzzy_value_base(value, AntecedentTypeEnum.FUZZY_VALUE)

    def fuzzy_trend(self,
                    date_start: typing.AnyStr = None,
                    date_stop: typing.AnyStr = None) -> typing.Tuple[LinguisticVariableEnum, float]:
        value = self.trend(date_start, date_stop)
        return self.__fuzzy_value_base(value, AntecedentTypeEnum.FUZZY_TREND)

    def weighted_fuzzy_trend(self,
                             date_start: typing.AnyStr = None,
                             date_stop: typing.AnyStr = None) -> typing.Tuple[LinguisticVariableEnum, float]:
        value = self.weighted_trend(date_start, date_stop)
        return self.__fuzzy_value_base(value, AntecedentTypeEnum.WEIGHTED_FUZZY_TREND)

    def __fuzzy_value_base(self,
                           value: float = None,
                           fuzzyfier_type: AntecedentTypeEnum = None) -> typing.Tuple[LinguisticVariableEnum, float]:
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
            log = LoggerMessageBase(mtype=LoggerMessageTypeEnum.ERROR,
                                    name="MetricCalculator",
                                    description=f"Couldn't compute fuzzy value for {value} and "
                                                f"fuzzyfier {fuzzyfier_type.value}.",
                                    extra_data={
                                        "state": self.__current_state(),
                                        "fuzzyfier": fuzzyfier,
                                        "error": traceback.format_exc()
                                    })
            self._logger.logger.info(log)

        return fuzzy_class, fuzzy_membership_value

    def difference(self,
                   date_start: typing.AnyStr = None,
                   date_stop: typing.AnyStr = None) -> typing.Union[int, float]:
        initial_metric_value = self.aggregated_value(date_start=date_start, date_stop=date_start)
        current_metric_value = self.aggregated_value(date_start=date_stop, date_stop=date_stop)
        if initial_metric_value is not None and current_metric_value is not None:
            difference = current_metric_value - initial_metric_value
        elif initial_metric_value is None and current_metric_value is not None:
            difference = current_metric_value

            log = LoggerMessageBase(mtype=LoggerMessageTypeEnum.WARNING,
                                    name="MetricCalculator",
                                    description="Ill-defined difference. Initial metric value is none.",
                                    extra_data={
                                        "state": self.__current_state()
                                    })
            self._logger.logger.info(log)
        elif initial_metric_value is not None and current_metric_value is None:
            difference = initial_metric_value

            log = LoggerMessageBase(mtype=LoggerMessageTypeEnum.WARNING,
                                    name="MetricCalculator",
                                    description="Ill-defined difference. Current metric value is none.",
                                    extra_data={
                                        "state": self.__current_state()
                                    })
            self._logger.logger.info(log)
        else:
            difference = None

            log = LoggerMessageBase(mtype=LoggerMessageTypeEnum.WARNING,
                                    name="MetricCalculator",
                                    description="Ill-defined difference. Both initial and current metrics are none",
                                    extra_data={
                                        "state": self.__current_state()
                                    })
            self._logger.logger.info(log)
        return difference

    def percentage_difference(self,
                              date_start: typing.AnyStr = None,
                              date_stop: typing.AnyStr = None) -> typing.Union[int, float]:
        initial_metric_value = self.aggregated_value(date_start=date_start, date_stop=date_start)
        current_metric_value = self.aggregated_value(date_start=date_stop, date_stop=date_stop)
        if initial_metric_value is not None and current_metric_value is not None:
            try:
                difference = 100 * (current_metric_value - initial_metric_value) / initial_metric_value
            except ZeroDivisionError:
                difference = 100 * current_metric_value
        elif initial_metric_value is None and current_metric_value is not None:
            difference = 100

            log = LoggerMessageBase(mtype=LoggerMessageTypeEnum.WARNING,
                                    name="MetricCalculator",
                                    description="Ill-defined percentage difference. Initial metric value is none.",
                                    extra_data={
                                        "state": self.__current_state()
                                    })
            self._logger.logger.info(log)
        elif initial_metric_value is not None and current_metric_value is None:
            difference = -100

            log = LoggerMessageBase(mtype=LoggerMessageTypeEnum.WARNING,
                                    name="MetricCalculator",
                                    description="Ill-defined percentage difference. Current metric value is none.",
                                    extra_data={
                                        "state": self.__current_state()
                                    })
            self._logger.logger.info(log)
        else:
            difference = None

            log = LoggerMessageBase(mtype=LoggerMessageTypeEnum.WARNING,
                                    name="MetricCalculator",
                                    description="Ill-defined percentage difference. Both initial and "
                                                "current metrics are none",
                                    extra_data={
                                        "state": self.__current_state()
                                    })
            self._logger.logger.info(log)
        return difference

    def raw_value(self, date_start: typing.AnyStr = None, *args, **kwargs) -> typing.Union[int, float]:
        result = self.aggregated_value(date_start=date_start, date_stop=date_start)

        if result is None:
            log = LoggerMessageBase(mtype=LoggerMessageTypeEnum.WARNING,
                                    name="MetricCalculator",
                                    description="Metric evaluated to none",
                                    extra_data={
                                        "state": self.__current_state()
                                    })
            self._logger.logger.info(log)

        return result

    def __get_metrics(self):
        metrics = [value.name for value in self._metric.numerator if value]
        if self._metric.denominator:
            metrics += [value.name for value in self._metric.denominator if value]
        return metrics

    def __get_metrics_values(self,
                             date_start: typing.AnyStr = None,
                             date_stop: typing.AnyStr = None) -> typing.List[typing.Dict]:
        try:
            metrics_values = self._repository.get_metrics_values(key_value=self._facebook_id,
                                                                 date_start=date_start,
                                                                 date_stop=date_stop,
                                                                 metrics=self.__get_metrics(),
                                                                 level=self._level,
                                                                 breakdown_metadata=self._breakdown_metadata)
        except Exception as e:
            log = LoggerMessageBase(mtype=LoggerMessageTypeEnum.ERROR,
                                    name="MetricCalculator",
                                    description="Failed to get metric values.",
                                    extra_data={
                                        "state": self.__current_state(),
                                        "error": traceback.format_exc()
                                    })
            self._logger.logger.info(log)
            raise e

        if not metrics_values:
            log = LoggerMessageBase(mtype=LoggerMessageTypeEnum.WARNING,
                                    name="MetricCalculator",
                                    description="No metric values returned from DB",
                                    extra_data={
                                        "state": self.__current_state()
                                    })
            self._logger.logger.info(log)
        return metrics_values

    def __get_min_metrics_values(self):
        try:
            min_values = self._repository.get_min_value(key_value=self._facebook_id,
                                                        metrics=self.__get_metrics(),
                                                        level=self._level,
                                                        breakdown_metadata=self._breakdown_metadata)
        except Exception as e:
            log = LoggerMessageBase(mtype=LoggerMessageTypeEnum.ERROR,
                                    name="MetricCalculator",
                                    description="Failed to get min metric values.",
                                    extra_data={
                                        "state": self.__current_state(),
                                        "error": traceback.format_exc()
                                    })
            self._logger.logger.info(log)
            raise e

        if not min_values:
            log = LoggerMessageBase(mtype=LoggerMessageTypeEnum.WARNING,
                                    name="MetricCalculator",
                                    description="No min metric values returned from DB",
                                    extra_data={
                                        "state": self.__current_state()
                                    })
            self._logger.logger.info(log)

        return min_values

    def __get_max_metrics_values(self):
        try:
            max_values = self._repository.get_max_value(key_value=self._facebook_id,
                                                        metrics=self.__get_metrics(),
                                                        level=self._level,
                                                        breakdown_metadata=self._breakdown_metadata)
        except Exception as e:
            log = LoggerMessageBase(mtype=LoggerMessageTypeEnum.ERROR,
                                    name="MetricCalculator",
                                    description="Failed to get max metric values.",
                                    extra_data={
                                        "state": self.__current_state(),
                                        "error": traceback.format_exc()
                                    })
            self._logger.logger.info(log)
            raise e

        if not max_values:
            log = LoggerMessageBase(mtype=LoggerMessageTypeEnum.WARNING,
                                    name="MetricCalculator",
                                    description="No max metric values returned from DB",
                                    extra_data={
                                        "state": self.__current_state()
                                    })
            self._logger.logger.info(log)

        return max_values
