import traceback
import typing
from queue import Queue
from threading import Thread

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
from FacebookDexter.Infrastructure.Domain.Rules.RuleEnums import RuleTypeSelectionEnum
from FacebookDexter.Infrastructure.PersistanceLayer.DexterMongoRepository import DexterMongoRepository


class RuleBasedOptimizationAdLevel(RuleBasedOptimizationBase):
    DEFAULT_AD_PERFORMANCE_TIME_RANGE = DaysEnum.SEVEN

    def __init__(self):
        super().__init__()
        self.__adset_id = None
        self.__ids = None
        self.set_level(LevelEnum.AD)

    def run(self, adset_id: typing.AnyStr = None, rule_selection_types: typing.List = None) -> typing.List[typing.Dict]:
        self.__adset_id = adset_id
        self.__load_ids()
        if not self.__ids:
            return []

        lowest_25p_performing_ads = self.find_lowest_25p_performing_ads()

        recommendations = []
        for ad_id in lowest_25p_performing_ads:
            if self.is_available(ad_id):
                que = Queue()
                t_list = []
                for rule_selection_type in rule_selection_types:
                    for evaluate_function in self.rules_selector(rule_selection_type):
                        t = Thread(target=lambda q, arg1, arg2: q.put(evaluate_function(arg1, arg2)),
                                args=(que, ad_id, self._fuzzyfier_factory))
                        t_list.append(t)

                # TODO: refactor this
                # t1 = Thread(target=lambda q, arg1, arg2: q.put(self.evaluate_general_rules(arg1, arg2)),
                #             args=(que, ad_id, self._fuzzyfier_factory))
                # t2 = Thread(target=lambda q, arg1, arg2: q.put(self.evaluate_pause_rules(arg1, arg2)),
                #             args=(que, ad_id, self._fuzzyfier_factory))
                # t3 = Thread(target=lambda q, arg1, arg2: q.put(self.evaluate_increase_budget_rules(arg1, arg2)),
                #             args=(que, ad_id, self._fuzzyfier_factory))
                # t4 = Thread(target=lambda q, arg1, arg2: q.put(self.evaluate_decrease_budget_rules(arg1, arg2)),
                #             args=(que, ad_id, self._fuzzyfier_factory))

                for t in t_list:
                    t.start()

                for t in t_list:
                    t.join()

                while not que.empty():
                    recommendations += que.get()

        return recommendations

    def __load_ids(self):
        self.__ids = self._mongo_repository.get_ads_by_adset_id(key_value=self.__adset_id)

    def find_lowest_25p_performing_ads(self, ad_performance_time_range: int = None) -> typing.List[typing.AnyStr]:
        if not ad_performance_time_range:
            ad_performance_time_range = self._time_interval

        calculator = (MetricCalculator().
                      set_level(LevelEnum.AD).
                      set_metric(AvailableMetricEnum.CLICKS.value).
                      set_repository(self._mongo_repository).
                      set_date_stop(self._date_stop).
                      set_time_interval(self._time_interval).
                      set_debug_mode(self._debug).
                      set_breakdown_metadata(BreakdownMetadata(breakdown=BreakdownEnum.NONE,
                                                               action_breakdown=ActionBreakdownEnum.NONE)))

        average_metric_values = [
            (ad_id, calculator.set_facebook_id(ad_id).compute_value(atype=AntecedentTypeEnum.VALUE,
                                                                    time_interval=ad_performance_time_range))
            for ad_id in self.__ids]
        try:
            lowest_25p_slice = slice(0, int(np.ceil(len(average_metric_values) / 4)))
            sorted_values = sorted(average_metric_values, key=lambda x: x[1][0])
            lowest_25p_ad_ids = [value[0] for value in sorted_values][lowest_25p_slice]
        except TypeError as type_error:
            if self._debug:
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
            if self._debug:
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
