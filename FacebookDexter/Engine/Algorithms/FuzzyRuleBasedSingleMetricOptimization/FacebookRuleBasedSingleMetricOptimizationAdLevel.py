import typing
from queue import Queue
from threading import Thread

from Core.Dexter.Infrastructure.Domain.LevelEnums import LevelEnum
from FacebookDexter.Engine.Algorithms.FuzzyRuleBasedSingleMetricOptimization.FacebookRuleBasedSingleMetricOptimizationBase \
    import FacebookRuleBasedSingleMetricOptimizationBase


class FacebookRuleBasedSingleMetricOptimizationAdLevel(FacebookRuleBasedSingleMetricOptimizationBase):

    def __init__(self):
        super().__init__()
        self.__adset_id = None
        self.set_level(LevelEnum.AD)

    def run(self, adset_id: typing.AnyStr = None, rule_selection_types: typing.List = None) -> typing.List[
        typing.Dict]:
        self.__adset_id = adset_id

        ad_ids = self._mongo_repository.get_ads_by_adset_id(key_value=self.__adset_id)

        recommendations = []
        for ad_id in ad_ids:
            if self.is_available(ad_id):
                que = Queue()
                thread_list = []
                for rule_selection_type in rule_selection_types:
                    for evaluate_function in self.rules_selector(rule_selection_type):
                        thread = Thread(target=lambda q, arg1, arg2: q.put(evaluate_function(arg1, arg2)),
                                   args=(que, ad_id, self._fuzzyfier_factory))
                        thread_list.append(thread)

                for thread in thread_list:
                    thread.start()

                for thread in thread_list:
                    thread.join()

                while not que.empty():
                    recommendations += que.get()

        return recommendations
