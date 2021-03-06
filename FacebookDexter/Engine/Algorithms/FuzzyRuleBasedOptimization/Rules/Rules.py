import typing

from Core.Dexter.Infrastructure.Domain.LevelEnums import LevelEnum
from Core.Dexter.Infrastructure.Domain.Rules.RuleBase import RuleBase
from FacebookDexter.Engine.Algorithms.FuzzyRuleBasedOptimization.Rules.RulesAdDecreaseBudget import \
    RULES_AD_DECREASE_BUDGET
from FacebookDexter.Engine.Algorithms.FuzzyRuleBasedOptimization.Rules.RulesAdGeneral import RULES_AD_GENERAL
from FacebookDexter.Engine.Algorithms.FuzzyRuleBasedOptimization.Rules.RulesAdIncreaseBudget import \
    RULES_AD_INCREASE_BUDGET
from FacebookDexter.Engine.Algorithms.FuzzyRuleBasedOptimization.Rules.RulesAdPause import RULES_AD_PAUSE
from FacebookDexter.Engine.Algorithms.FuzzyRuleBasedOptimization.Rules.RulesAdSetCreateAds import \
    RULES_ADSET_CREATE_ADS
from FacebookDexter.Engine.Algorithms.FuzzyRuleBasedOptimization.Rules.RulesAdSetDecreaseBudget import \
    RULES_ADSET_DECREASE_BUDGET
from FacebookDexter.Engine.Algorithms.FuzzyRuleBasedOptimization.Rules.RulesAdSetGeneral import RULES_ADSET_GENERAL
from FacebookDexter.Engine.Algorithms.FuzzyRuleBasedOptimization.Rules.RulesAdSetIncreaseBudget import \
    RULES_ADSET_INCREASE_BUDGET
from FacebookDexter.Engine.Algorithms.FuzzyRuleBasedOptimization.Rules.RulesAdSetRemoveAgeGroups import \
    RULES_ADSET_REMOVE_AGE_GROUPS
from FacebookDexter.Engine.Algorithms.FuzzyRuleBasedOptimization.Rules.RulesAdSetRemoveDevice import \
    RULES_ADSET_REMOVE_DEVICE
from FacebookDexter.Engine.Algorithms.FuzzyRuleBasedOptimization.Rules.RulesAdSetRemoveGender import \
    RULES_ADSET_REMOVE_GENDER
from FacebookDexter.Engine.Algorithms.FuzzyRuleBasedOptimization.Rules.RulesAdSetRemovePlacement import \
    RULES_ADSET_REMOVE_PLACEMENT
from FacebookDexter.Engine.Algorithms.FuzzyRuleBasedOptimization.Rules.RulesAdSetRemovePlatform import \
    RULES_ADSET_REMOVE_PLATFORM
from FacebookDexter.Engine.Algorithms.FuzzyRuleBasedOptimization.Rules.RulesCampaignCreateAudience import \
    RULES_CAMPAIGN_CREATE_AUDIENCE
from FacebookDexter.Engine.Algorithms.FuzzyRuleBasedOptimization.Rules.RulesCampaignDecreaseBudget import \
    RULES_CAMPAIGN_DECREASE_BUDGET
from FacebookDexter.Engine.Algorithms.FuzzyRuleBasedOptimization.Rules.RulesCampaignGeneral import \
    RULES_CAMPAIGN_GENERAL
from FacebookDexter.Engine.Algorithms.FuzzyRuleBasedOptimization.Rules.RulesCampaignIncreaseBudget import \
    RULES_CAMPAIGN_INCREASE_BUDGET
from FacebookDexter.Infrastructure.Domain.Actions.ActionEnums import FacebookActionEnum


class Rules:
    remove = [*RULES_ADSET_REMOVE_AGE_GROUPS,
              *RULES_ADSET_REMOVE_GENDER,
              *RULES_ADSET_REMOVE_PLACEMENT,
              *RULES_ADSET_REMOVE_DEVICE,
              *RULES_ADSET_REMOVE_PLATFORM]
    create = [*RULES_CAMPAIGN_CREATE_AUDIENCE,
              *RULES_ADSET_CREATE_ADS]
    pause = [*RULES_AD_PAUSE]
    decrease_budget = [*RULES_CAMPAIGN_DECREASE_BUDGET,
                       *RULES_ADSET_DECREASE_BUDGET,
                       *RULES_AD_DECREASE_BUDGET]
    increase_budget = [*RULES_CAMPAIGN_INCREASE_BUDGET,
                       *RULES_ADSET_INCREASE_BUDGET,
                       *RULES_AD_INCREASE_BUDGET]
    general = [*RULES_CAMPAIGN_GENERAL,
               *RULES_ADSET_GENERAL,
               *RULES_AD_GENERAL]

    def get_rules_by_action_and_metric(self,
                                       action: FacebookActionEnum = None,
                                       metric: typing.AnyStr = None) -> typing.List[RuleBase]:
        rules = getattr(self, action.value)
        available_rules = [rule for rule in rules if metric in self.__get_rule_metrics_metadata(rule)]
        return available_rules

    def get_rules_by_action(self, action: FacebookActionEnum = None, level: LevelEnum = None) -> typing.List[RuleBase]:
        available_rules = getattr(self, action.value)
        return [rule for rule in available_rules if rule.level == level]

    @staticmethod
    def __get_rule_metrics_metadata(rule):
        return [metric_metadata.name for metric_metadata in rule.metrics]
