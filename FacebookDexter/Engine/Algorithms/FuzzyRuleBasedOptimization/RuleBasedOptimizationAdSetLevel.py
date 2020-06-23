import typing
from queue import Queue
from threading import Thread

from FacebookDexter.Engine.Algorithms.FuzzyRuleBasedOptimization.RuleBasedOptimizationBase import \
    RuleBasedOptimizationBase
from FacebookDexter.Infrastructure.Domain.LevelEnums import LevelEnum


class RuleBasedOptimizationAdSetLevel(RuleBasedOptimizationBase):

    def __init__(self):
        super().__init__()
        self.set_level(LevelEnum.ADSET)

    def run(self, adset_id: typing.AnyStr = None) -> typing.List[typing.Dict]:
        recommendations = []
        if self.is_available(adset_id):
            que = Queue()

            # TODO: refactor this
            t1 = Thread(target=lambda q, arg1, arg2: q.put(self.evaluate_general_rules(arg1, arg2)),
                        args=(que, adset_id, self._fuzzyfier_factory))
            t2 = Thread(target=lambda q, arg1, arg2: q.put(self.evaluate_remove_rules(arg1, arg2)),
                        args=(que, adset_id, self._fuzzyfier_factory))
            t3 = Thread(target=lambda q, arg1, arg2: q.put(self.evaluate_increase_budget_rules(arg1, arg2)),
                        args=(que, adset_id, self._fuzzyfier_factory))
            t4 = Thread(target=lambda q, arg1, arg2: q.put(self.evaluate_decrease_budget_rules(arg1, arg2)),
                        args=(que, adset_id, self._fuzzyfier_factory))
            t5 = Thread(target=lambda q, arg1, arg2: q.put(self.evaluate_create_rules(arg1, arg2)),
                        args=(que, adset_id, self._fuzzyfier_factory))

            t_list = [t1, t2, t3, t4, t5]

            for t in t_list:
                t.start()

            for t in t_list:
                t.join()

            while not que.empty():
                recommendations += que.get()

        return recommendations