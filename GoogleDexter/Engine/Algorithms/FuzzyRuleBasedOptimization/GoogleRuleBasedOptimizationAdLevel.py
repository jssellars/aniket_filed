import typing

import numpy as np

from Core.Dexter.Infrastructure.Domain.Breakdowns import BreakdownMetadataBase
from Core.Dexter.Infrastructure.Domain.DaysEnum import DaysEnum
from Core.Dexter.Infrastructure.Domain.LevelEnums import LevelEnum
from Core.Dexter.Infrastructure.Domain.Rules.AntecedentEnums import AntecedentTypeEnum
from GoogleDexter.Engine.Algorithms.FuzzyRuleBasedOptimization.GoogleRuleBasedOptimizationBase import \
    GoogleRuleBasedOptimizationBase
from GoogleDexter.Engine.Algorithms.FuzzyRuleBasedOptimization.Metrics.GoogleAvailableMetricEnum import \
    GoogleAvailableMetricEnum
from GoogleDexter.Infrastructure.Domain.Breakdowns import GoogleActionBreakdownEnum, GoogleBreakdownEnum
from GoogleDexter.Infrastructure.Domain.Metrics.GoogleMetricCalculator import GoogleMetricCalculator


import logging

logger = logging.getLogger(__name__)


class GoogleRuleBasedOptimizationAdLevel(GoogleRuleBasedOptimizationBase):
    DEFAULT_AD_PERFORMANCE_TIME_RANGE = DaysEnum.SEVEN

    def __init__(self):
        super().__init__()
        self.__adgroup_id = None
        self.__ids = None
        self.set_level(LevelEnum.AD)

    def run(self, adgroup_id: typing.AnyStr = None) -> typing.List[typing.Dict]:
        self.__adgroup_id = adgroup_id
        self.__load_ids()
        if not self.__ids:
            return []

        lowest_25p_performing_ads = self.find_lowest_25p_performing_ads()

        recommendations = []
        for ad_id in lowest_25p_performing_ads:
            if self.is_available(ad_id):
                recommendations += self.evaluate_pause_rules(structure_id=ad_id,
                                                             fuzzyfier_factory=self._fuzzyfier_factory)

                recommendations += self.evaluate_pause_rules(structure_id=ad_id,
                                                             fuzzyfier_factory=self._fuzzyfier_factory)
                recommendations += self.evaluate_decrease_budget_rules(structure_id=ad_id,
                                                                       fuzzyfier_factory=self._fuzzyfier_factory)
                recommendations += self.evaluate_increase_budget_rules(structure_id=ad_id,
                                                                       fuzzyfier_factory=self._fuzzyfier_factory)
                recommendations += self.evaluate_general_rules(structure_id=ad_id,
                                                               fuzzyfier_factory=self._fuzzyfier_factory)

        return recommendations

    def __load_ids(self):
        self.__ids = self._mongo_repository.get_ads_by_adgroup_id(key_value=self.__adgroup_id)

    def find_lowest_25p_performing_ads(self, ad_performance_time_range: int = None) -> typing.List[typing.AnyStr]:
        if not ad_performance_time_range:
            ad_performance_time_range = self._time_interval

        calculator = GoogleMetricCalculator()
        calculator = (calculator.
                      set_level(LevelEnum.AD).
                      set_metric(GoogleAvailableMetricEnum.CLICKS.value).
                      set_repository(self._mongo_repository).
                      set_date_stop(self._date_stop).
                      set_time_interval(self._time_interval).
                      set_breakdown_metadata(BreakdownMetadataBase(breakdown=GoogleBreakdownEnum.NONE,
                                                                   action_breakdown=GoogleActionBreakdownEnum.NONE)))

        average_metric_values = [
            (ad_id, calculator.set_structure_id(ad_id).compute_value(atype=AntecedentTypeEnum.VALUE,
                                                                     time_interval=ad_performance_time_range))
            for ad_id in self.__ids]
        try:
            lowest_25p_slice = slice(0, int(np.ceil(len(average_metric_values) / 4)))
            sorted_values = sorted(average_metric_values, key=lambda x: x[1][0])
            lowest_25p_ad_ids = [value[0] for value in sorted_values][lowest_25p_slice]
        except TypeError as e:
            logger.exception(
                f"Cannot find lowest performing ads for {self.__adgroup_id} || {repr(e)}",
                extra={"structure_id": self.__adgroup_id, "config": self._dexter_config}
            )
            lowest_25p_ad_ids = []
        except Exception as e:
            logger.exception(
                f"Error finding lowest performing ads for {self.__adgroup_id} || {repr(e)}",
                extra={"structure_id": self.__adgroup_id, "config": self._dexter_config}
            )
            raise e

        return lowest_25p_ad_ids
