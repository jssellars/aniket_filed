import typing
from queue import Queue
from threading import Thread

from Core.Dexter.Infrastructure.Domain.LevelEnums import LevelEnum
from FacebookDexter.Engine.Algorithms.FuzzyRuleBasedSingleMetricOptimization.FacebookRuleBasedSingleMetricOptimizationBase \
    import FacebookRuleBasedSingleMetricOptimizationBase


class FacebookRuleBasedSingleMetricOptimizationAdSetLevel(FacebookRuleBasedSingleMetricOptimizationBase):

    def __init__(self):
        super().__init__()
        self.set_level(LevelEnum.ADSET)

    def run(self, adset_id: typing.AnyStr = None, rule_selection_types: typing.List = None) -> typing.List[typing.Dict]:
        recommendations = []
        if self.is_available(adset_id):
            que = Queue()
            thread_list = []
            for rule_selection_type in rule_selection_types:
                for evaluate_function in self.rules_selector(rule_selection_type):
                    thread = Thread(target=lambda q, arg1, arg2: q.put(evaluate_function(arg1, arg2)),
                               args=(que, adset_id, self._fuzzyfier_factory))
                    thread_list.append(thread)

            for thread in thread_list:
                thread.start()

            for thread in thread_list:
                thread.join()

            while not que.empty():
                recommendations += que.get()

        return recommendations
