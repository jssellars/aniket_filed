from Core.Dexter.Infrastructure.Domain.Breakdowns import BreakdownMetadataBase
from Core.Dexter.Infrastructure.Domain.ChannelEnum import ChannelEnum
from Core.Dexter.Infrastructure.Domain.DaysEnum import DaysEnum
from Core.Dexter.Infrastructure.Domain.LevelEnums import LevelEnum
from Core.Dexter.Infrastructure.Domain.LogicalOperatorEnum import LogicOperatorEnum
from Core.Dexter.Infrastructure.Domain.Rules.Antecedent import Antecedent
from Core.Dexter.Infrastructure.Domain.Rules.AntecedentEnums import AntecedentTypeEnum
from Core.Dexter.Infrastructure.Domain.Rules.Connective import Connective
from Core.Dexter.Infrastructure.Domain.Rules.RuleBase import RuleBase
from FacebookDexter.Engine.Algorithms.FuzzyRuleBasedOptimization.Metrics.FacebookAvailableMetricEnum import \
    FacebookAvailableMetricEnum
from FacebookDexter.Engine.Algorithms.FuzzyRuleBasedOptimization.Metrics.FacebookMetricValues import \
    NARROW_AUDIENCE_SIZE, LOW_QUALITY_RANKING
from FacebookDexter.Infrastructure.Domain.Actions.ActionEnums import FacebookActionEnum
from FacebookDexter.Infrastructure.Domain.Breakdowns import FacebookBreakdownEnum, FacebookActionBreakdownEnum
from FacebookDexter.Infrastructure.Domain.FuzzyEngine.FacebookFuzzySets import FacebookLinguisticVariableEnum
from FacebookDexter.Infrastructure.Domain.Rules.FacebookRuleEnums import FacebookRuleImportanceEnum, \
    FacebookRuleCategoryEnum, FacebookRuleSourceEnum, FacebookRuleRedirectEnum, FacebookRuleTypeEnum

RULES_CAMPAIGN_DECREASE_BUDGET = [
    RuleBase(rtype=FacebookRuleTypeEnum.BUDGET_AND_BID,
             channel=ChannelEnum.FACEBOOK,
             category=FacebookRuleCategoryEnum.OPTIMIZE_BUDGET,
             importance=FacebookRuleImportanceEnum.HIGH,
             source=FacebookRuleSourceEnum.DEXTER,
             level=LevelEnum.CAMPAIGN,
             action=FacebookActionEnum.NONE,
             redirect=FacebookRuleRedirectEnum.EDIT_STRUCTURE,
             template="Dexter noticed your cost per result is high while your CTR remains low. "
                      "Dexter suggests decreasing your budget by maximum 25%.",
             breakdown_metadata=BreakdownMetadataBase(breakdown=FacebookBreakdownEnum.NONE,
                                                      action_breakdown=FacebookActionBreakdownEnum.NONE),
             time_interval=DaysEnum.THREE_MONTHS,
             connective=Connective(LogicOperatorEnum.AND),
             antecedents=[
                 Antecedent(aid=1,
                            atype=AntecedentTypeEnum.FUZZY_VALUE,
                            metric=FacebookAvailableMetricEnum.CTR.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=FacebookLinguisticVariableEnum.HIGH),
                 Antecedent(aid=1,
                            atype=AntecedentTypeEnum.FUZZY_VALUE,
                            metric=FacebookAvailableMetricEnum.COST_PER_RESULT.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=FacebookLinguisticVariableEnum.HIGH)
             ]),
    RuleBase(rtype=FacebookRuleTypeEnum.BUDGET_AND_BID,
             channel=ChannelEnum.FACEBOOK,
             category=FacebookRuleCategoryEnum.IMPROVE_CPR,
             importance=FacebookRuleImportanceEnum.HIGH,
             source=FacebookRuleSourceEnum.DEXTER,
             level=LevelEnum.CAMPAIGN,
             action=FacebookActionEnum.DECREASE_BUDGET,
             redirect=FacebookRuleRedirectEnum.EDIT_STRUCTURE,
             template="Dexter noticed your cost per result is high while your audience is narrow. Dexter suggests you "
                      "decrease the budget by maximum 25%.",
             breakdown_metadata=BreakdownMetadataBase(breakdown=FacebookBreakdownEnum.NONE,
                                                      action_breakdown=FacebookActionBreakdownEnum.NONE),
             time_interval=DaysEnum.THREE_MONTHS,
             connective=Connective(LogicOperatorEnum.AND),
             antecedents=[
                 Antecedent(aid=1,
                            atype=AntecedentTypeEnum.FUZZY_TREND,
                            metric=FacebookAvailableMetricEnum.COST_PER_RESULT.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=FacebookLinguisticVariableEnum.INCREASING),
                 Antecedent(aid=2,
                            atype=AntecedentTypeEnum.VALUE,
                            metric=FacebookAvailableMetricEnum.AUDIENCE_SIZE.value,
                            operator=LogicOperatorEnum.LESS_THAN,
                            expected_value=NARROW_AUDIENCE_SIZE)
             ]),
    RuleBase(rtype=FacebookRuleTypeEnum.BUDGET_AND_BID,
             channel=ChannelEnum.FACEBOOK,
             category=FacebookRuleCategoryEnum.IMPROVE_CPR,
             importance=FacebookRuleImportanceEnum.HIGH,
             source=FacebookRuleSourceEnum.DEXTER,
             level=LevelEnum.CAMPAIGN,
             action=FacebookActionEnum.DECREASE_BUDGET,
             redirect=FacebookRuleRedirectEnum.EDIT_STRUCTURE,
             template="Dexter noticed your cost per result increased while your conversions remain low. Dexter "
                      "suggests you decrease the budget by maximum 25%.",
             breakdown_metadata=BreakdownMetadataBase(breakdown=FacebookBreakdownEnum.NONE,
                                                      action_breakdown=FacebookActionBreakdownEnum.NONE),
             time_interval=DaysEnum.THREE_MONTHS,
             connective=Connective(LogicOperatorEnum.AND),
             antecedents=[
                 Antecedent(aid=1,
                            atype=AntecedentTypeEnum.FUZZY_TREND,
                            metric=FacebookAvailableMetricEnum.COST_PER_RESULT.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=FacebookLinguisticVariableEnum.INCREASING),
                 Antecedent(aid=2,
                            atype=AntecedentTypeEnum.FUZZY_VALUE,
                            metric=FacebookAvailableMetricEnum.CONVERSIONS.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=FacebookLinguisticVariableEnum.LOW)
             ]),
    RuleBase(rtype=FacebookRuleTypeEnum.BUDGET_AND_BID,
             channel=ChannelEnum.FACEBOOK,
             category=FacebookRuleCategoryEnum.IMPROVE_CPR,
             importance=FacebookRuleImportanceEnum.HIGH,
             source=FacebookRuleSourceEnum.DEXTER,
             level=LevelEnum.CAMPAIGN,
             action=FacebookActionEnum.DECREASE_BUDGET,
             redirect=FacebookRuleRedirectEnum.EDIT_STRUCTURE,
             template="Dexter noticed your ads quality is low and your results are also low. "
                      "Dexter suggests decreasing the budget by 25%.",
             breakdown_metadata=BreakdownMetadataBase(breakdown=FacebookBreakdownEnum.NONE,
                                                      action_breakdown=FacebookActionBreakdownEnum.NONE),
             time_interval=DaysEnum.THREE_MONTHS,
             connective=Connective(LogicOperatorEnum.AND),
             antecedents=[
                 Antecedent(aid=1,
                            atype=AntecedentTypeEnum.FUZZY_VALUE,
                            metric=FacebookAvailableMetricEnum.RESULTS.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=FacebookLinguisticVariableEnum.LOW),
                 Antecedent(aid=2,
                            atype=AntecedentTypeEnum.VALUE,
                            metric=FacebookAvailableMetricEnum.QUALITY_RANKING.value,
                            operator=LogicOperatorEnum.IN,
                            expected_value=LOW_QUALITY_RANKING)
             ]),
    RuleBase(rtype=FacebookRuleTypeEnum.BUDGET_AND_BID,
             channel=ChannelEnum.FACEBOOK,
             category=FacebookRuleCategoryEnum.IMPROVE_CPC,
             importance=FacebookRuleImportanceEnum.HIGH,
             source=FacebookRuleSourceEnum.DEXTER,
             level=LevelEnum.CAMPAIGN,
             action=FacebookActionEnum.DECREASE_BUDGET,
             redirect=FacebookRuleRedirectEnum.EDIT_STRUCTURE,
             template="Dexter noticed your ads quality is low while your CPC is high. "
                      "Dexter suggests decreasing the budget by 25%.",
             breakdown_metadata=BreakdownMetadataBase(breakdown=FacebookBreakdownEnum.NONE,
                                                      action_breakdown=FacebookActionBreakdownEnum.NONE),
             time_interval=DaysEnum.THREE_MONTHS,
             connective=Connective(LogicOperatorEnum.AND),
             antecedents=[
                 Antecedent(aid=1,
                            atype=AntecedentTypeEnum.FUZZY_VALUE,
                            metric=FacebookAvailableMetricEnum.CPC.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=FacebookLinguisticVariableEnum.HIGH),
                 Antecedent(aid=2,
                            atype=AntecedentTypeEnum.VALUE,
                            metric=FacebookAvailableMetricEnum.QUALITY_RANKING.value,
                            operator=LogicOperatorEnum.IN,
                            expected_value=LOW_QUALITY_RANKING)
             ])
]
