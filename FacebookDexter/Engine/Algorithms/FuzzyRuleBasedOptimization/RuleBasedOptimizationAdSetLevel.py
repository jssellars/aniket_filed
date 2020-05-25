import typing

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
            recommendations += self.evaluate_general_rules(facebook_id=adset_id,
                                                           fuzzyfier_factory=self._fuzzyfier_factory)
            recommendations += self.evaluate_remove_rules(facebook_id=adset_id,
                                                          fuzzyfier_factory=self._fuzzyfier_factory)
            recommendations += self.evaluate_decrease_budget_rules(facebook_id=adset_id,
                                                                   fuzzyfier_factory=self._fuzzyfier_factory)
            recommendations += self.evaluate_increase_budget_rules(facebook_id=adset_id,
                                                                   fuzzyfier_factory=self._fuzzyfier_factory)
        return recommendations
