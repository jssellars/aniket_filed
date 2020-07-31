import typing

from Core.Dexter.Infrastructure.Domain.LevelEnums import LevelEnum
from GoogleDexter.Engine.Algorithms.FuzzyRuleBasedOptimization.GoogleRuleBasedOptimizationBase import \
    GoogleRuleBasedOptimizationBase


class GoogleRuleBasedOptimizationAdGroupLevel(GoogleRuleBasedOptimizationBase):

    def __init__(self):
        super().__init__()
        self.set_level(LevelEnum.ADGROUP)

    def run(self, adgroup_id: typing.AnyStr = None) -> typing.List[typing.Dict]:
        recommendations = []

        if self.is_available(adgroup_id):
            recommendations += self.evaluate_pause_rules(structure_id=adgroup_id,
                                                         fuzzyfier_factory=self._fuzzyfier_factory)
            recommendations += self.evaluate_general_rules(structure_id=adgroup_id,
                                                           fuzzyfier_factory=self._fuzzyfier_factory)
            recommendations += self.evaluate_remove_rules(structure_id=adgroup_id,
                                                          fuzzyfier_factory=self._fuzzyfier_factory)
            recommendations += self.evaluate_decrease_budget_rules(structure_id=adgroup_id,
                                                                   fuzzyfier_factory=self._fuzzyfier_factory)
            recommendations += self.evaluate_increase_budget_rules(structure_id=adgroup_id,
                                                                   fuzzyfier_factory=self._fuzzyfier_factory)
        return recommendations
