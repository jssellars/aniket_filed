import traceback
import typing

import numpy as np

from Core.Tools.Logger.LoggerMessageBase import LoggerMessageBase, LoggerMessageTypeEnum
from FacebookDexter.Engine.Algorithms.FuzzyRuleBasedOptimization.Metrics.AvailableMetricEnum import AvailableMetricEnum
from FacebookDexter.Engine.Algorithms.FuzzyRuleBasedOptimization.RuleBasedOptimizationBase import \
    RuleBasedOptimizationBase
from FacebookDexter.Infrastructure.Domain.Breakdowns import BreakdownEnum, ActionBreakdownEnum, BreakdownMetadata
from FacebookDexter.Infrastructure.Domain.DaysEnum import DaysEnum
from FacebookDexter.Infrastructure.Domain.LevelEnums import LevelEnum
from FacebookDexter.Infrastructure.Domain.Metrics.MetricCalculator import MetricCalculator
from FacebookDexter.Infrastructure.Domain.Rules.AntecedentEnums import AntecedentTypeEnum


class RuleBasedOptimizationAdLevel(RuleBasedOptimizationBase):
    DEFAULT_AD_PERFORMANCE_TIME_RANGE = DaysEnum.SEVEN

    def __init__(self):
        super().__init__()
        self.__adset_id = None
        self.__ids = None
        self.set_level(LevelEnum.AD)

    def run(self, adset_id: typing.AnyStr = None) -> typing.List[typing.Dict]:
        self.__adset_id = adset_id
        self.__load_ids()
        if not self.__ids:
            return []

        lowest_25p_performing_ads = self.find_lowest_25p_performing_ads()

        recommendations = []
        for ad_id in lowest_25p_performing_ads:
            if self.is_available(ad_id):
                recommendations += self.evaluate_pause_rules(facebook_id=ad_id,
                                                             fuzzyfier_factory=self._fuzzyfier_factory)
                recommendations += self.evaluate_decrease_budget_rules(facebook_id=ad_id,
                                                                       fuzzyfier_factory=self._fuzzyfier_factory)
                recommendations += self.evaluate_increase_budget_rules(facebook_id=ad_id,
                                                                       fuzzyfier_factory=self._fuzzyfier_factory)
                recommendations += self.evaluate_general_rules(facebook_id=ad_id,
                                                               fuzzyfier_factory=self._fuzzyfier_factory)
        return recommendations

    def __load_ids(self):
        self.__ids = self._mongo_repository.get_ads_by_adset_id(key_value=self.__adset_id)

    def find_lowest_25p_performing_ads(self, ad_performance_time_range: int = None) -> typing.List[typing.AnyStr]:
        if not ad_performance_time_range:
            ad_performance_time_range = self.DEFAULT_AD_PERFORMANCE_TIME_RANGE

        calculator = MetricCalculator()
        calculator = calculator. \
            set_level(LevelEnum.AD). \
            set_metric(AvailableMetricEnum.CLICKS.value). \
            set_repository(self._mongo_repository). \
            set_breakdown_metadata(
            BreakdownMetadata(breakdown=BreakdownEnum.NONE, action_breakdown=ActionBreakdownEnum.NONE))

        average_metric_values = [
            (ad_id, calculator.set_facebook_id(ad_id).compute_value(atype=AntecedentTypeEnum.VALUE,
                                                                    time_interval=ad_performance_time_range))
            for ad_id in self.__ids]
        try:
            lowest_25p_slice = slice(0, int(np.ceil(len(average_metric_values) / 4)))
            sorted_values = sorted(average_metric_values, key=lambda x: x[1][0])
            lowest_25p_ad_ids = [value[0] for value in sorted_values][lowest_25p_slice]
        except TypeError as type_error:
            log = LoggerMessageBase(mtype=LoggerMessageTypeEnum.WARNING,
                                    name="RuleBasedOptimizationCampaignLevel",
                                    description=f"Cannot find lowest performing ads for {self.__adset_id}",
                                    extra_data={
                                        "facebook_id": self.__adset_id,
                                        "config": self._dexter_config,
                                        "error": traceback.format_exc()
                                    })
            self.get_logger().logger.info(log)
            lowest_25p_ad_ids = []
        except Exception as e:
            log = LoggerMessageBase(mtype=LoggerMessageTypeEnum.ERROR,
                                    name="RuleBasedOptimizationCampaignLevel",
                                    description=f"Error finding lowest performing ads for {self.__adset_id}",
                                    extra_data={
                                        "facebook_id": self.__adset_id,
                                        "config": self._dexter_config,
                                        "error": traceback.format_exc()
                                    })
            self.get_logger().logger.info(log)
            raise e

        return lowest_25p_ad_ids
