import typing
from operator import itemgetter

import numpy as np

from FacebookDexter.Engine.Algorithms.FuzzyRuleBasedOptimization.Fuzzifiers.RuleBasedOptimizationAdFuzzyfierFactory import RuleBasedOptimizationAdFuzzyfierFactory
from FacebookDexter.Engine.Algorithms.FuzzyRuleBasedOptimization.RuleBasedOptimizationBase import RuleBasedOptimizationBase
from FacebookDexter.Infrastructure.Domain.Breakdowns import BreakdownEnum, ActionBreakdownEnum, BreakdownMetadata
from FacebookDexter.Infrastructure.Domain.DaysEnum import DaysEnum
from FacebookDexter.Infrastructure.Domain.LevelEnums import LevelEnum
from FacebookDexter.Infrastructure.Domain.Metrics.MetricCalculator import MetricCalculator
from FacebookDexter.Infrastructure.Domain.Rules.AntecedentEnums import AntecedentTypeEnum


class RuleBasedOptimizationAdLevel(RuleBasedOptimizationBase):
    DEFAULT_AD_PERFORMANCE_TIME_RANGE = DaysEnum.SEVEN

    def __init__(self, **kwargs):
        self.__adset_id = None
        self.__ids = None
        self.__fuzzyfier_factory = RuleBasedOptimizationAdFuzzyfierFactory
        super().__init__(**kwargs)

    def run(self, adset_id: typing.AnyStr = None) -> typing.List[typing.Dict]:
        self.__adset_id = adset_id
        self.__load_ids()
        lowest_25p_performing_ads = self.find_lowest_25p_performing_ads()

        recommendations = []
        for ad_id in lowest_25p_performing_ads:
            recommendations += self.evaluate_remove_rules(facebook_id=ad_id, fuzzyfier_factory=self.__fuzzyfier_factory)
            recommendations += self.evaluate_create_rules(facebook_id=ad_id, fuzzyfier_factory=self.__fuzzyfier_factory)
            recommendations += self.evaluate_pause_rules(facebook_id=ad_id, fuzzyfier_factory=self.__fuzzyfier_factory)
            recommendations += self.evaluate_decrease_budget_rules(facebook_id=ad_id, fuzzyfier_factory=self.__fuzzyfier_factory)
            recommendations += self.evaluate_increase_budget_rules(facebook_id=ad_id, fuzzyfier_factory=self.__fuzzyfier_factory)

        return recommendations

    def __load_ids(self):
        self.__ids = self._mongo_repository.get_ads_by_adset_id(key_value=self.__adset_id, level=LevelEnum.AD.value)

    def find_lowest_25p_performing_ads(self, ad_performance_time_range: int = None) -> typing.List[typing.AnyStr]:
        if not ad_performance_time_range:
            ad_performance_time_range = self.DEFAULT_AD_PERFORMANCE_TIME_RANGE

        # todo: complete set_metric with results
        calculator = MetricCalculator()
        calculator = calculator. \
            set_level(LevelEnum.AD). \
            set_metric(). \
            set_repository(self._mongo_repository). \
            set_breakdown_metadata(BreakdownMetadata(breakdown=BreakdownEnum.NONE, action_breakdown=ActionBreakdownEnum.NONE))

        average_metric_values = [(ad_id, calculator.set_facebook_id(ad_id).compute_value(atype=AntecedentTypeEnum.VALUE,
                                                                                         time_interval=ad_performance_time_range))
                                 for ad_id in self.__ids]

        lowest_25p_slice = slice(0, np.ceil(len(average_metric_values) / 4))

        lowest_25p_ad_ids = [value[0] for value in sorted(average_metric_values, key=itemgetter(lambda x: x[1]))[lowest_25p_slice]]

        return lowest_25p_ad_ids
