import hashlib
import random
import traceback
import typing
from datetime import timedelta, datetime

import numpy as np
from facebook_business.adobjects.ad import Ad
from facebook_business.adobjects.adaccount import AdAccount

from Core.Dexter.Engine.Algorithms.FuzzyRuleBasedOptimization.TimeBucketWeightingMethods.TimeBucketWeightingBySpend import \
    time_bucket_weighting_by_spend
from Core.Dexter.Infrastructure.Domain.Breakdowns import BreakdownMetadataBase, BreakdownBaseEnum, \
    ActionBreakdownBaseEnum
from Core.Dexter.Infrastructure.Domain.DaysEnum import DaysEnum
from Core.Dexter.Infrastructure.Domain.LevelEnums import LevelEnum
from Core.Dexter.Infrastructure.Domain.Metrics.MetricCalculatorBase import MetricCalculatorBase
from Core.Dexter.Infrastructure.Domain.Metrics.MetricEnums import MetricTrendTimeBucketEnum
from Core.Dexter.Infrastructure.Domain.Rules.AntecedentEnums import AntecedentTypeEnum
from Core.Tools.Logger.LoggerMessageBase import LoggerMessageBase, LoggerMessageTypeEnum
from Core.Tools.Logger.MongoLoggers.MongoLogger import MongoLogger
from Core.Tools.Misc.Constants import DEFAULT_DATETIME_ISO, DEFAULT_DATETIME
from Core.Web.BusinessOwnerRepository.BusinessOwnerRepository import BusinessOwnerRepository
from Core.Web.FacebookGraphAPI.GraphAPI.GraphAPISdkBase import GraphAPISdkBase
from Core.Web.FacebookGraphAPI.Tools import Tools
from FacebookDexter.Engine.Algorithms.FuzzyRuleBasedOptimization.Metrics.FacebookAvailableMetricEnum import \
    FacebookAvailableMetricEnum
from FacebookDexter.Infrastructure.Domain.Metrics.FacebookMetricEnums import FacebookMetricTypeEnum


class FacebookMetricCalculator(MetricCalculatorBase):

    def __init__(self):
        super().__init__()
        self.minimum_number_of_data_points = None
        self._calculator = None
        value = str(random.randint(0, 1e20)) + self._date_stop.strftime(DEFAULT_DATETIME_ISO)
        self._calculator_id = hashlib.sha1(value.encode('utf-8')).hexdigest()

        if self._repository is not None:
            self.__logger = MongoLogger(repository=self._repository,
                                        database_name=self._repository.config.logs_database)
        else:
            self.__logger = None

    def set_minimum_number_of_data_points(self, minimum_number_of_data_points: int = None):
        self.minimum_number_of_data_points = minimum_number_of_data_points
        return self

    def _current_state(self):
        current_state = {
            "object_id": id(self),
            "calculator_id": self._calculator_id,
            "facebook_id": self._facebook_id,
            "metric": self._metric,
            "level": self._level,
            "breakdown_metadata": self._breakdown_metadata,
            "business_owner_id": self._business_owner_id,
        }
        return current_state

    @property
    def calculator(self):
        if self._calculator is None:
            self._calculator = {
                (AntecedentTypeEnum.VALUE, FacebookMetricTypeEnum.STRUCTURE): self.structure_value,
                (AntecedentTypeEnum.FUZZY_VALUE, FacebookMetricTypeEnum.INSIGHT): self.fuzzy_value,
                (AntecedentTypeEnum.FUZZY_TREND, FacebookMetricTypeEnum.INSIGHT): self.fuzzy_trend,
                (AntecedentTypeEnum.WEIGHTED_FUZZY_TREND, FacebookMetricTypeEnum.INSIGHT): self.weighted_fuzzy_trend,
                (AntecedentTypeEnum.VALUE, FacebookMetricTypeEnum.INSIGHT): self.aggregated_value,
                (AntecedentTypeEnum.TREND, FacebookMetricTypeEnum.INSIGHT): self.trend,
                (AntecedentTypeEnum.WEIGHTED_TREND, FacebookMetricTypeEnum.INSIGHT): self.weighted_trend,
                (AntecedentTypeEnum.CURRENT_VALUE, FacebookMetricTypeEnum.INSIGHT): self.raw_value,
                (AntecedentTypeEnum.DIFFERENCE, FacebookMetricTypeEnum.INSIGHT): self.difference,
                (AntecedentTypeEnum.PERCENTAGE_DIFFERENCE, FacebookMetricTypeEnum.INSIGHT): self.percentage_difference,
                (AntecedentTypeEnum.VALUE, FacebookMetricTypeEnum.AUDIENCE): self.audience_size,
                (AntecedentTypeEnum.VALUE, FacebookMetricTypeEnum.PIXEL): self.has_pixel,
                (AntecedentTypeEnum.VALUE, FacebookMetricTypeEnum.CREATIVE): self.has_over_20p_text,
                (AntecedentTypeEnum.VALUE, FacebookMetricTypeEnum.PROSPECTING): self.is_prospecting_campaign,
                (AntecedentTypeEnum.VALUE, FacebookMetricTypeEnum.INSIGHT_CATEGORICAL): self.categorical_value,
                (AntecedentTypeEnum.VALUE, FacebookMetricTypeEnum.NUMBER_OF_ADS): self.number_of_ads_per_adset,
                (AntecedentTypeEnum.VALUE, FacebookMetricTypeEnum.DUPLICATE_AD): self.duplicate_best_performing_ad,
                (AntecedentTypeEnum.AVERAGE, FacebookMetricTypeEnum.INSIGHT): self.average,
                (AntecedentTypeEnum.VARIANCE, FacebookMetricTypeEnum.INSIGHT): self.variance
            }

        return self._calculator

    def audience_size(self, *args, **kwargs) -> typing.Any:
        structure_details = self._repository.get_structure_details(self._facebook_id, self._level)

        permanent_token = BusinessOwnerRepository(self._business_owner_repo_session).get_permanent_token(
            self._business_owner_id)
        _ = GraphAPISdkBase(self._facebook_config, permanent_token)

        ad_account_id = self._repository.get_ad_account_id(self._facebook_id, self._level)

        try:
            ad_account = AdAccount(fbid=ad_account_id)
            targeting_spec = structure_details.get('targeting', None)
            optimization_goal = structure_details.get('optimization_goal', None)
            if targeting_spec is not None and optimization_goal is not None:
                response = ad_account.get_delivery_estimate(fields=['estimate_mau'],
                                                            params={'targeting_spec': targeting_spec,
                                                                    'optimization_goal': optimization_goal})
                response = Tools.convert_to_json(response)
                audience_size_estimate = response.get('estimate_mau', None)
            else:
                audience_size_estimate = None
        except Exception as e:
            audience_size_estimate = None
            if self._debug:
                log = LoggerMessageBase(mtype=LoggerMessageTypeEnum.WARNING,
                                        name="MetricCalculator",
                                        description="Failed to get audience size.",
                                        extra_data={
                                            "state": self._current_state(),
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
            if self._debug:
                log = LoggerMessageBase(mtype=LoggerMessageTypeEnum.WARNING,
                                        name="MetricCalculator",
                                        description="Failed to get pixels.",
                                        extra_data={
                                            "state": self._current_state(),
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
            if structure_id is None:
                return False
            structure_details = self._repository.get_structure_details(key_value=structure_id, level=LevelEnum.ADSET)
        elif self._level == LevelEnum.ADSET:
            structure_details = self._repository.get_structure_details(key_value=self._facebook_id, level=self._level)
        elif self._level == LevelEnum.AD:
            structure_id = self._repository.get_adset_id_by_ad_id(key_value=self._facebook_id)
            if structure_id is None:
                return False
            structure_details = self._repository.get_structure_details(key_value=structure_id, level=LevelEnum.ADSET)
        else:
            raise ValueError(f"Cannot extract ad set targeting for level {self._level}")

        try:
            if 'flexible_spec' in structure_details['targeting']:
                interests = [interest_dict['name']
                             for entry in structure_details['targeting']['flexible_spec']
                             for interest_lists in entry.values()
                             for interest_dict in interest_lists
                             if self.__is_interest(entry)]
                if not interests:
                    return False
            else:
                return False
        except Exception as e:
            if self._debug:
                log = LoggerMessageBase(mtype=LoggerMessageTypeEnum.ERROR,
                                        name="MetricCalculator",
                                        description="Failed to get interests from structure targeting.",
                                        extra_data={
                                            "state": self._current_state(),
                                            "error": traceback.format_exc()
                                        })
                self._logger.logger.info(log)
            return False

    def number_of_ads_per_adset(self, *args, **kwargs):
        ads = self._repository.get_all_ads_by_adset_id(key_value=self._facebook_id)
        return len(ads)

    def duplicate_best_performing_ad(self, *args, **kwargs):
        ad_ids = self._repository.get_ads_by_adset_id(key_value=self._facebook_id)

        calculator = (FacebookMetricCalculator().
                      set_level(LevelEnum.AD).
                      set_metric(FacebookAvailableMetricEnum.CLICKS.value).
                      set_repository(self._repository).
                      set_date_stop(self._date_stop).
                      set_time_interval(self._time_interval).
                      set_debug_mode(self._debug).
                      set_breakdown_metadata(BreakdownMetadataBase(breakdown=BreakdownBaseEnum.NONE,
                                                                   action_breakdown=ActionBreakdownBaseEnum.NONE)))

        average_metric_values = [
            (ad_id, calculator.
             set_facebook_id(ad_id).
             compute_value(atype=AntecedentTypeEnum.VALUE,
                           time_interval=self._time_interval)) for ad_id in ad_ids]
        try:
            sorted_values = sorted(average_metric_values, key=lambda x: x[1][0], reverse=True)
            if sorted_values[0][1][0]:
                best_performing_ad_id = sorted_values[0][0]
            else:
                return None, None
        except TypeError:
            import traceback
            traceback.print_exc()
            return None

        best_performing_ad_name = self._repository.get_ad_name_by_ad_id(best_performing_ad_id)
        return best_performing_ad_id, best_performing_ad_name

    def weighted_trend(self, date_start: typing.AnyStr = None, date_stop: typing.AnyStr = None, **kwargs) -> float:
        _date_start = datetime.strptime(date_start, DEFAULT_DATETIME)
        _date_stop = datetime.strptime(date_stop, DEFAULT_DATETIME)
        current_value = self.aggregated_value(date_start=date_stop, date_stop=date_stop)

        mc = (FacebookMetricCalculator().
              set_facebook_id(self._facebook_id).
              set_level(self._level).
              set_metric(FacebookAvailableMetricEnum.AVERAGE_SPEND.value).
              set_repository(self._repository).
              set_date_stop(self._date_stop).
              set_time_interval(self._time_interval).
              set_debug_mode(self._debug).
              set_breakdown_metadata(self._breakdown_metadata))

        max_spend, _ = mc.compute_value(AntecedentTypeEnum.VALUE, self._time_interval)
        slopes = []
        for time_bucket in MetricTrendTimeBucketEnum:
            if time_bucket.value <= self._time_interval:
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

    def weighted_fuzzy_trend(self,
                             date_start: typing.AnyStr = None,
                             date_stop: typing.AnyStr = None,
                             **kwargs):
        value = self.weighted_trend(date_start, date_stop)
        return self._fuzzy_value_base(value, AntecedentTypeEnum.WEIGHTED_FUZZY_TREND)
