from Core.Dexter.Infrastructure.Domain.Breakdowns import BreakdownMetadataBase
from Core.Dexter.Infrastructure.Domain.ChannelEnum import ChannelEnum
from Core.Dexter.Infrastructure.Domain.DaysEnum import DaysEnum
from Core.Dexter.Infrastructure.Domain.LevelEnums import LevelEnum
from Core.Dexter.Infrastructure.Domain.LogicalOperatorEnum import LogicOperatorEnum
from Core.Dexter.Infrastructure.Domain.Rules.Antecedent import Antecedent
from Core.Dexter.Infrastructure.Domain.Rules.AntecedentEnums import AntecedentTypeEnum
from Core.Dexter.Infrastructure.Domain.Rules.Connective import Connective
from Core.Dexter.Infrastructure.Domain.Rules.RuleBase import RuleBase
from GoogleDexter.Engine.Algorithms.FuzzyRuleBasedOptimization.Metrics.GoogleAvailableMetricEnum import GoogleAvailableMetricEnum
from GoogleDexter.Infrastructure.Domain.Actions.ActionEnums import GoogleActionEnum
from GoogleDexter.Infrastructure.Domain.Breakdowns import GoogleBreakdownEnum, GoogleActionBreakdownEnum
from GoogleDexter.Infrastructure.Domain.Rules.GoogleRuleEnums import GoogleRuleRedirectEnum, GoogleRuleSourceEnum, \
    GoogleRuleImportanceEnum, GoogleRuleCategoryEnum, GoogleRuleTypeEnum
from GoogleDexter.Infrastructure.FuzzyEngine.GoogleFuzzySets import GoogleLinguisticVariableEnum

RULES_ADSET_DECREASE_BUDGET = [
    RuleBase(rtype=GoogleRuleTypeEnum.BUDGET_AND_BID,
             channel=ChannelEnum.GOOGLE,
             category=GoogleRuleCategoryEnum.IMPROVE_CPR,
             importance=GoogleRuleImportanceEnum.HIGH,
             source=GoogleRuleSourceEnum.DEXTER,
             level=LevelEnum.ADGROUP,
             action=GoogleActionEnum.DECREASE_BUDGET,
             redirect=GoogleRuleRedirectEnum.EDIT_STRUCTURE,
             template="Dexter noticed your CPR increased while your CTR remains low. You should decrease the budget by maximum 25%.",
             breakdown_metadata=BreakdownMetadataBase(breakdown=GoogleBreakdownEnum.NONE,
                                                  action_breakdown=GoogleActionBreakdownEnum.NONE),
             time_interval=DaysEnum.THREE_MONTHS,
             connective=Connective(LogicOperatorEnum.AND),
             antecedents=[
                 Antecedent(aid=1,
                            atype=AntecedentTypeEnum.FUZZY_TREND,
                            metric=GoogleAvailableMetricEnum.COST_PER_RESULT.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=GoogleLinguisticVariableEnum.INCREASING),
                 Antecedent(aid=2,
                            atype=AntecedentTypeEnum.FUZZY_VALUE,
                            metric=GoogleAvailableMetricEnum.CTR.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=GoogleLinguisticVariableEnum.LOW)
             ]),
    # RuleBase(rtype=RuleTypeEnum.BUDGET_AND_BID,
    #          channel=ChannelEnum.FACEBOOK,
    #          category=RuleCategoryEnum.IMPROVE_CPR,
    #          importance=RuleImportanceEnum.HIGH,
    #          source=RuleSourceEnum.DEXTER,
    #          level=LevelEnum.ADSET,
    #          action=ActionEnum.DECREASE_BUDGET,
    #          redirect=RuleRedirectEnum.EDIT_STRUCTURE,
    #          template="Dexter noticed your CPR is high while your audience is narrow. You should decrease the budget by maximum 25%.",
    #          breakdown_metadata=BreakdownMetadata(breakdown=BreakdownEnum.NONE,
    #                                               action_breakdown=ActionBreakdownEnum.NONE),
    #          time_interval=DaysEnum.THREE_MONTHS,
    #          connective=Connective(LogicOperatorEnum.AND),
    #          antecedents=[
    #              Antecedent(aid=1,
    #                         atype=AntecedentTypeEnum.FUZZY_TREND,
    #                         metric=AvailableMetricEnum.COST_PER_RESULT.value,
    #                         operator=LogicOperatorEnum.EQUALS,
    #                         expected_value=LinguisticVariableEnum.INCREASING),
    #              Antecedent(aid=2,
    #                         atype=AntecedentTypeEnum.VALUE,
    #                         metric=AvailableMetricEnum.AUDIENCE_SIZE.value,
    #                         operator=LogicOperatorEnum.LESS_THAN,
    #                         expected_value=NARROW_AUDIENCE_SIZE)
    #          ]),
    RuleBase(rtype=GoogleRuleTypeEnum.BUDGET_AND_BID,
             channel=ChannelEnum.GOOGLE,
             category=GoogleRuleCategoryEnum.IMPROVE_CPR,
             importance=GoogleRuleImportanceEnum.HIGH,
             source=GoogleRuleSourceEnum.DEXTER,
             level=LevelEnum.ADGROUP,
             action=GoogleActionEnum.DECREASE_BUDGET,
             redirect=GoogleRuleRedirectEnum.EDIT_STRUCTURE,
             template="Dexter noticed your CPR increased while your conversions remains low. You should decrease the budget by maximum 25%. ",
             breakdown_metadata=BreakdownMetadataBase(breakdown=GoogleBreakdownEnum.NONE,
                                                  action_breakdown=GoogleActionBreakdownEnum.NONE),
             time_interval=DaysEnum.THREE_MONTHS,
             connective=Connective(LogicOperatorEnum.AND),
             antecedents=[
                 Antecedent(aid=1,
                            atype=AntecedentTypeEnum.FUZZY_TREND,
                            metric=GoogleAvailableMetricEnum.COST_PER_RESULT.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=GoogleLinguisticVariableEnum.INCREASING),
                 Antecedent(aid=2,
                            atype=AntecedentTypeEnum.FUZZY_VALUE,
                            metric=GoogleAvailableMetricEnum.CONVERSIONS.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=GoogleLinguisticVariableEnum.LOW)
             ])
]
