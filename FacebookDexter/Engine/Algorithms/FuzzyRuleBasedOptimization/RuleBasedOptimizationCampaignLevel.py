import typing

from FacebookDexter.Engine.Algorithms.FuzzyRuleBasedOptimization.Fuzzifiers.RuleBasedOptimizationCampaignFuzzyfierFactory import \
    RuleBasedOptimizationCampaignFuzzyfierFactory
from FacebookDexter.Engine.Algorithms.FuzzyRuleBasedOptimization.RuleBasedOptimizationBase import RuleBasedOptimizationBase


class RuleBasedOptimizationCampaignLevel(RuleBasedOptimizationBase):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__fuzzyfier_factory = RuleBasedOptimizationCampaignFuzzyfierFactory

    def run(self, campaign_id: typing.AnyStr = None) -> typing.List[typing.Dict]:
        return self.evaluate_general_rules(campaign_id, self.__fuzzyfier_factory)
