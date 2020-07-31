import typing

from Core.Dexter.Infrastructure.Domain.DaysEnum import DaysEnum
from Core.Dexter.Infrastructure.Domain.LevelEnums import LevelEnum
from Core.Dexter.Infrastructure.Domain.Rules.RuleBase import RuleBase
from FacebookDexter.Engine.Algorithms.FuzzyRuleBasedSingleMetricOptimization.Rules.RulesAdGeneral import \
    RULES_AD_GENERAL
from FacebookDexter.Engine.Algorithms.FuzzyRuleBasedSingleMetricOptimization.Rules.RulesAdsetGeneral import \
    RULES_ADSET_GENERAL
from FacebookDexter.Engine.Algorithms.FuzzyRuleBasedSingleMetricOptimization.Rules.RulesCampaignGeneral import \
    RULES_CAMPAIGN_GENERAL
from FacebookDexter.Infrastructure.Domain.Actions.ActionEnums import FacebookActionEnum


class Rules:
    remove = []
    create = []
    pause = []
    decrease_budget = []
    increase_budget = []
    general = [*RULES_CAMPAIGN_GENERAL,
               *RULES_ADSET_GENERAL,
               *RULES_AD_GENERAL]

    def get_rules_by_action_and_metric(self,
                                       action: FacebookActionEnum = None,
                                       metric: typing.AnyStr = None) -> typing.List[RuleBase]:
        rules = getattr(self, action.value)
        available_rules = [rule for rule in rules if metric in self.__get_rule_metrics_metadata(rule)]
        return available_rules

    def get_rules_by_action_and_time_interval(self, action: FacebookActionEnum = None, level: LevelEnum = None,
                                              time_interval: DaysEnum = None) -> typing.List[RuleBase]:
        available_rules = getattr(self, action.value)
        return [rule for rule in available_rules if rule.level == level and time_interval == self.__get_time_interval(rule)]

    @staticmethod
    def __get_rule_metrics_metadata(rule):
        return [metric_metadata.name for metric_metadata in rule.metrics]

    def __get_time_interval(self, rule):
        return rule.time_interval
