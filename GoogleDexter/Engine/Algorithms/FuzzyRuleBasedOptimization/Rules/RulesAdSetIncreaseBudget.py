from GoogleDexter.Engine.Algorithms.FuzzyRuleBasedOptimization.Metrics.AvailableMetricEnum import AvailableMetricEnum
from GoogleDexter.Infrastructure.Domain.Actions.ActionEnums import ActionEnum
from GoogleDexter.Infrastructure.Domain.Breakdowns import BreakdownMetadata, BreakdownEnum, ActionBreakdownEnum
from GoogleDexter.Infrastructure.Domain.ChannelEnum import ChannelEnum
from GoogleDexter.Infrastructure.Domain.DaysEnum import DaysEnum
from GoogleDexter.Infrastructure.Domain.LevelEnums import LevelEnum
from GoogleDexter.Infrastructure.Domain.LogicalOperatorEnum import LogicOperatorEnum
from GoogleDexter.Infrastructure.Domain.Rules.Antecedent import Antecedent
from GoogleDexter.Infrastructure.Domain.Rules.AntecedentEnums import AntecedentTypeEnum
from GoogleDexter.Infrastructure.Domain.Rules.Connective import Connective
from GoogleDexter.Infrastructure.Domain.Rules.RuleBase import RuleBase
from GoogleDexter.Infrastructure.Domain.Rules.RuleEnums import RuleTypeEnum, RuleCategoryEnum, RuleImportanceEnum, \
    RuleSourceEnum, RuleRedirectEnum
from GoogleDexter.Infrastructure.FuzzyEngine.FuzzySets.FuzzySets import LinguisticVariableEnum

RULES_ADSET_INCREASE_BUDGET = [
    RuleBase(rtype=RuleTypeEnum.BUDGET_AND_BID,
             channel=ChannelEnum.GOOGLE,
             category=RuleCategoryEnum.IMPROVE_CPR,
             importance=RuleImportanceEnum.HIGH,
             source=RuleSourceEnum.DEXTER,
             level=LevelEnum.ADGROUP,
             action=ActionEnum.INCREASE_BUDGET,
             redirect=RuleRedirectEnum.EDIT_STRUCTURE,
             template="Dexter noticed your cost per result is low while getting good conversions. You should increase the budget by maximum 25%.",
             breakdown_metadata=BreakdownMetadata(breakdown=BreakdownEnum.NONE,
                                                  action_breakdown=ActionBreakdownEnum.NONE),
             time_interval=DaysEnum.THREE_MONTHS,
             connective=Connective(LogicOperatorEnum.AND),
             antecedents=[
                 Antecedent(aid=1,
                            atype=AntecedentTypeEnum.FUZZY_VALUE,
                            metric=AvailableMetricEnum.COST_PER_RESULT.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=LinguisticVariableEnum.LOW),
                 Antecedent(aid=2,
                            atype=AntecedentTypeEnum.FUZZY_VALUE,
                            metric=AvailableMetricEnum.CONVERSIONS.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=LinguisticVariableEnum.HIGH)
             ]),
    # RuleBase(rtype=RuleTypeEnum.BUDGET_AND_BID,
    #          channel=ChannelEnum.FACEBOOK,
    #          category=RuleCategoryEnum.IMPROVE_CPR,
    #          importance=RuleImportanceEnum.HIGH,
    #          source=RuleSourceEnum.DEXTER,
    #          level=LevelEnum.ADSET,
    #          action=ActionEnum.INCREASE_BUDGET,
    #          redirect=RuleRedirectEnum.EDIT_STRUCTURE,
    #          template="Dexter noticed your CTR is high and you are targeting a large audience. You should increase the budget by maximum 25%.",
    #          breakdown_metadata=BreakdownMetadata(breakdown=BreakdownEnum.NONE,
    #                                               action_breakdown=ActionBreakdownEnum.NONE),
    #          time_interval=DaysEnum.THREE_MONTHS,
    #          connective=Connective(LogicOperatorEnum.AND),
    #          antecedents=[
    #              Antecedent(aid=1,
    #                         atype=AntecedentTypeEnum.FUZZY_VALUE,
    #                         metric=AvailableMetricEnum.CTR.value,
    #                         operator=LogicOperatorEnum.EQUALS,
    #                         expected_value=LinguisticVariableEnum.HIGH),
    #              Antecedent(aid=2,
    #                         atype=AntecedentTypeEnum.VALUE,
    #                         metric=AvailableMetricEnum.AUDIENCE_SIZE.value,
    #                         operator=LogicOperatorEnum.GREATER_THAN,
    #                         expected_value=NARROW_AUDIENCE_SIZE)
    #          ]),
    RuleBase(rtype=RuleTypeEnum.BUDGET_AND_BID,
             channel=ChannelEnum.GOOGLE,
             category=RuleCategoryEnum.IMPROVE_CPR,
             importance=RuleImportanceEnum.HIGH,
             source=RuleSourceEnum.DEXTER,
             level=LevelEnum.ADGROUP,
             action=ActionEnum.INCREASE_BUDGET,
             redirect=RuleRedirectEnum.EDIT_STRUCTURE,
             template="Dexter noticed your CTR and conversion rate are both increasing. You should increase the budget by maximum 25%.",
             breakdown_metadata=BreakdownMetadata(breakdown=BreakdownEnum.NONE,
                                                  action_breakdown=ActionBreakdownEnum.NONE),
             time_interval=DaysEnum.THREE_MONTHS,
             connective=Connective(LogicOperatorEnum.AND),
             antecedents=[
                 Antecedent(aid=1,
                            atype=AntecedentTypeEnum.FUZZY_TREND,
                            metric=AvailableMetricEnum.CTR.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=LinguisticVariableEnum.INCREASING),
                 Antecedent(aid=2,
                            atype=AntecedentTypeEnum.FUZZY_TREND,
                            metric=AvailableMetricEnum.CR.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=LinguisticVariableEnum.INCREASING)
             ]),
    # RuleBase(rtype=RuleTypeEnum.BUDGET_AND_BID,
    #          channel=ChannelEnum.FACEBOOK,
    #          category=RuleCategoryEnum.IMPROVE_CPC,
    #          importance=RuleImportanceEnum.HIGH,
    #          source=RuleSourceEnum.DEXTER,
    #          level=LevelEnum.ADSET,
    #          action=ActionEnum.INCREASE_BUDGET,
    #          redirect=RuleRedirectEnum.EDIT_STRUCTURE,
    #          template="Dexter noticed your text overlay is above 20% while your CPC remains high. You should decrease the budget by maximum 25%.",
    #          breakdown_metadata=BreakdownMetadata(breakdown=BreakdownEnum.NONE,
    #                                               action_breakdown=ActionBreakdownEnum.NONE),
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
    #                         expected_value=LinguisticVariableEnum.HIGH)
    #          ]),
    # RuleBase(rtype=RuleTypeEnum.BUDGET_AND_BID,
    #          channel=ChannelEnum.FACEBOOK,
    #          category=RuleCategoryEnum.IMPROVE_CPR,
    #          importance=RuleImportanceEnum.HIGH,
    #          source=RuleSourceEnum.DEXTER,
    #          level=LevelEnum.ADSET,
    #          action=ActionEnum.INCREASE_BUDGET,
    #          redirect=RuleRedirectEnum.EDIT_STRUCTURE,
    #          template="Dexter noticed your cost per results is low while your conversions are increasing. Your audience is large, so you should increase the "
    #                   "budget by maximum 25% to reach as many people as possible.",
    #          breakdown_metadata=BreakdownMetadata(breakdown=BreakdownEnum.NONE,
    #                                               action_breakdown=ActionBreakdownEnum.NONE),
    #          time_interval=DaysEnum.THREE_MONTHS,
    #          connective=Connective(LogicOperatorEnum.AND),
    #          antecedents=[
    #              Antecedent(aid=1,
    #                         atype=AntecedentTypeEnum.FUZZY_VALUE,
    #                         metric=AvailableMetricEnum.COST_PER_RESULT.value,
    #                         operator=LogicOperatorEnum.EQUALS,
    #                         expected_value=LinguisticVariableEnum.LOW),
    #              Antecedent(aid=2,
    #                         atype=AntecedentTypeEnum.FUZZY_TREND,
    #                         metric=AvailableMetricEnum.CONVERSIONS.value,
    #                         operator=LogicOperatorEnum.EQUALS,
    #                         expected_value=LinguisticVariableEnum.INCREASING),
    #              Antecedent(aid=2,
    #                         atype=AntecedentTypeEnum.VALUE,
    #                         metric=AvailableMetricEnum.AUDIENCE_SIZE.value,
    #                         operator=LogicOperatorEnum.GREATER_THAN,
    #                         expected_value=NARROW_AUDIENCE_SIZE)
    #          ])
]
