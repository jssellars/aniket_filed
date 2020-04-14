import typing

from FacebookDexter.Engine.Algorithms.FuzzyRuleBasedOptimization.Fuzzifiers.RuleBasedOptimizationAdSetFuzzyfierFactory import \
    RuleBasedOptimizationAdSetFuzzyfierFactory
from FacebookDexter.Engine.Algorithms.FuzzyRuleBasedOptimization.RuleBasedOptimizationBase import RuleBasedOptimizationBase


class RuleBasedOptimizationAdSetLevel(RuleBasedOptimizationBase):

    def __init__(self, **kwargs):
        self.__fuzzyfier_factory = RuleBasedOptimizationAdSetFuzzyfierFactory

        super().__init__(**kwargs)

    def run(self, adset_id: typing.AnyStr = None) -> typing.List[typing.Dict]:
        recommendations = self.evaluate_general_rules(facebook_id=adset_id, fuzzyfier_factory=self.__fuzzyfier_factory)
        return recommendations
