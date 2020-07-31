from Core.Dexter.Infrastructure.Domain.Breakdowns import BreakdownMetadataBase
from Core.Dexter.Infrastructure.Domain.ChannelEnum import ChannelEnum
from Core.Dexter.Infrastructure.Domain.DaysEnum import DaysEnum
from Core.Dexter.Infrastructure.Domain.LevelEnums import LevelEnum
from Core.Dexter.Infrastructure.Domain.LogicalOperatorEnum import LogicOperatorEnum
from Core.Dexter.Infrastructure.Domain.Rules.Antecedent import Antecedent
from Core.Dexter.Infrastructure.Domain.Rules.AntecedentEnums import AntecedentTypeEnum
from Core.Dexter.Infrastructure.Domain.Rules.Connective import Connective
from Core.Dexter.Infrastructure.Domain.Rules.RuleBase import RuleBase
from GoogleDexter.Engine.Algorithms.FuzzyRuleBasedOptimization.Metrics.GoogleAvailableMetricEnum import \
    GoogleAvailableMetricEnum
from GoogleDexter.Infrastructure.Domain.Actions.ActionEnums import GoogleActionEnum
from GoogleDexter.Infrastructure.Domain.Breakdowns import GoogleActionBreakdownEnum, GoogleBreakdownEnum
from GoogleDexter.Infrastructure.Domain.Rules.GoogleRuleEnums import GoogleRuleTypeEnum, GoogleRuleCategoryEnum, \
    GoogleRuleSourceEnum, GoogleRuleImportanceEnum, GoogleRuleRedirectEnum
from GoogleDexter.Infrastructure.FuzzyEngine.GoogleFuzzySets import GoogleLinguisticVariableEnum

RULES_ADSET_INCREASE_BUDGET = [
    RuleBase(rtype=GoogleRuleTypeEnum.BUDGET_AND_BID,
             channel=ChannelEnum.GOOGLE,
             category=GoogleRuleCategoryEnum.IMPROVE_CPR,
             importance=GoogleRuleImportanceEnum.HIGH,
             source=GoogleRuleSourceEnum.DEXTER,
             level=LevelEnum.ADGROUP,
             action=GoogleActionEnum.INCREASE_BUDGET,
             redirect=GoogleRuleRedirectEnum.EDIT_STRUCTURE,
             template="Dexter noticed your cost per result is low while getting good conversions. You should increase the budget by maximum 25%.",
             breakdown_metadata=BreakdownMetadataBase(breakdown=GoogleBreakdownEnum.NONE,
                                                  action_breakdown=GoogleActionBreakdownEnum.NONE),
             time_interval=DaysEnum.THREE_MONTHS,
             connective=Connective(LogicOperatorEnum.AND),
             antecedents=[
                 Antecedent(aid=1,
                            atype=AntecedentTypeEnum.FUZZY_VALUE,
                            metric=GoogleAvailableMetricEnum.COST_PER_RESULT.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=GoogleLinguisticVariableEnum.LOW),
                 Antecedent(aid=2,
                            atype=AntecedentTypeEnum.FUZZY_VALUE,
                            metric=GoogleAvailableMetricEnum.CONVERSIONS.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=GoogleLinguisticVariableEnum.HIGH)
             ]),
    # RuleBase(rtype=GoogleRuleTypeEnum.BUDGET_AND_BID,
    #          channel=ChannelEnum.FACEBOOK,
    #          category=GoogleRuleCategoryEnum.IMPROVE_CPR,
    #          importance=GoogleRuleImportanceEnum.HIGH,
    #          source=GoogleRuleSourceEnum.DEXTER,
    #          level=LevelEnum.ADSET,
    #          action=GoogleActionEnum.INCREASE_BUDGET,
    #          redirect=GoogleRuleRedirectEnum.EDIT_STRUCTURE,
    #          template="Dexter noticed your CTR is high and you are targeting a large audience. You should increase the budget by maximum 25%.",
    #          breakdown_metadata=BreakdownMetadataBase(breakdown=GoogleBreakdownEnum.NONE,
    #                                               action_breakdown=GoogleActionBreakdownEnum.NONE),
    #          time_interval=DaysEnum.THREE_MONTHS,
    #          connective=Connective(LogicOperatorEnum.AND),
    #          antecedents=[
    #              Antecedent(aid=1,
    #                         atype=AntecedentTypeEnum.FUZZY_VALUE,
    #                         metric=AvailableMetricEnum.CTR.value,
    #                         operator=LogicOperatorEnum.EQUALS,
    #                         expected_value=GoogleLinguisticVariableEnum.HIGH),
    #              Antecedent(aid=2,
    #                         atype=AntecedentTypeEnum.VALUE,
    #                         metric=AvailableMetricEnum.AUDIENCE_SIZE.value,
    #                         operator=LogicOperatorEnum.GREATER_THAN,
    #                         expected_value=NARROW_AUDIENCE_SIZE)
    #          ]),
    RuleBase(rtype=GoogleRuleTypeEnum.BUDGET_AND_BID,
             channel=ChannelEnum.GOOGLE,
             category=GoogleRuleCategoryEnum.IMPROVE_CPR,
             importance=GoogleRuleImportanceEnum.HIGH,
             source=GoogleRuleSourceEnum.DEXTER,
             level=LevelEnum.ADGROUP,
             action=GoogleActionEnum.INCREASE_BUDGET,
             redirect=GoogleRuleRedirectEnum.EDIT_STRUCTURE,
             template="Dexter noticed your CTR and conversion rate are both increasing. You should increase the budget by maximum 25%.",
             breakdown_metadata=BreakdownMetadataBase(breakdown=GoogleBreakdownEnum.NONE,
                                                  action_breakdown=GoogleActionBreakdownEnum.NONE),
             time_interval=DaysEnum.THREE_MONTHS,
             connective=Connective(LogicOperatorEnum.AND),
             antecedents=[
                 Antecedent(aid=1,
                            atype=AntecedentTypeEnum.FUZZY_TREND,
                            metric=GoogleAvailableMetricEnum.CTR.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=GoogleLinguisticVariableEnum.INCREASING),
                 Antecedent(aid=2,
                            atype=AntecedentTypeEnum.FUZZY_TREND,
                            metric=GoogleAvailableMetricEnum.CR.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=GoogleLinguisticVariableEnum.INCREASING)
             ]),
    # RuleBase(rtype=GoogleRuleTypeEnum.BUDGET_AND_BID,
    #          channel=ChannelEnum.FACEBOOK,
    #          category=GoogleRuleCategoryEnum.IMPROVE_CPC,
    #          importance=GoogleRuleImportanceEnum.HIGH,
    #          source=GoogleRuleSourceEnum.DEXTER,
    #          level=LevelEnum.ADSET,
    #          action=GoogleActionEnum.INCREASE_BUDGET,
    #          redirect=GoogleRuleRedirectEnum.EDIT_STRUCTURE,
    #          template="Dexter noticed your text overlay is above 20% while your CPC remains high. You should decrease the budget by maximum 25%.",
    #          breakdown_metadata=BreakdownMetadataBase(breakdown=GoogleBreakdownEnum.NONE,
    #                                               action_breakdown=GoogleActionBreakdownEnum.NONE),
    #          time_interval=DaysEnum.THREE_MONTHS,
    #          connective=Connective(LogicOperatorEnum.AND),
    #          antecedents=[
    #              Antecedent(aid=1,
    #                         atype=AntecedentTypeEnum.VALUE,
    #                         metric=AvailableMetricEnum.TEXT_OVERLAY.value,
    #                         operator=LogicOperatorEnum.EQUALS,
    #                         expected_value=True),
    #              Antecedent(aid=2,
    #                         atype=AntecedentTypeEnum.FUZZY_VALUE,
    #                         metric=AvailableMetricEnum.CPC.value,
    #                         operator=LogicOperatorEnum.EQUALS,
    #                         expected_value=GoogleLinguisticVariableEnum.HIGH)
    #          ]),
    # RuleBase(rtype=GoogleRuleTypeEnum.BUDGET_AND_BID,
    #          channel=ChannelEnum.FACEBOOK,
    #          category=GoogleRuleCategoryEnum.IMPROVE_CPR,
    #          importance=GoogleRuleImportanceEnum.HIGH,
    #          source=GoogleRuleSourceEnum.DEXTER,
    #          level=LevelEnum.ADSET,
    #          action=GoogleActionEnum.INCREASE_BUDGET,
    #          redirect=GoogleRuleRedirectEnum.EDIT_STRUCTURE,
    #          template="Dexter noticed your cost per results is low while your conversions are increasing. Your audience is large, so you should increase the "
    #                   "budget by maximum 25% to reach as many people as possible.",
    #          breakdown_metadata=BreakdownMetadataBase(breakdown=GoogleBreakdownEnum.NONE,
    #                                               action_breakdown=GoogleActionBreakdownEnum.NONE),
    #          time_interval=DaysEnum.THREE_MONTHS,
    #          connective=Connective(LogicOperatorEnum.AND),
    #          antecedents=[
    #              Antecedent(aid=1,
    #                         atype=AntecedentTypeEnum.FUZZY_VALUE,
    #                         metric=AvailableMetricEnum.COST_PER_RESULT.value,
    #                         operator=LogicOperatorEnum.EQUALS,
    #                         expected_value=GoogleLinguisticVariableEnum.LOW),
    #              Antecedent(aid=2,
    #                         atype=AntecedentTypeEnum.FUZZY_TREND,
    #                         metric=AvailableMetricEnum.CONVERSIONS.value,
    #                         operator=LogicOperatorEnum.EQUALS,
    #                         expected_value=GoogleLinguisticVariableEnum.INCREASING),
    #              Antecedent(aid=2,
    #                         atype=AntecedentTypeEnum.VALUE,
    #                         metric=AvailableMetricEnum.AUDIENCE_SIZE.value,
    #                         operator=LogicOperatorEnum.GREATER_THAN,
    #                         expected_value=NARROW_AUDIENCE_SIZE)
    #          ])
]
