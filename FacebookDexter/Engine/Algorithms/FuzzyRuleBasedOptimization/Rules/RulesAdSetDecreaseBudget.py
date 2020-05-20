from FacebookDexter.Engine.Algorithms.FuzzyRuleBasedOptimization.Metrics.AvailableMetricEnum import AvailableMetricEnum
from FacebookDexter.Engine.Algorithms.FuzzyRuleBasedOptimization.Metrics.MetricValues import NARROW_AUDIENCE_SIZE
from FacebookDexter.Infrastructure.Domain.Actions.ActionEnums import ActionEnum
from FacebookDexter.Infrastructure.Domain.Breakdowns import BreakdownMetadata, BreakdownEnum, ActionBreakdownEnum
from FacebookDexter.Infrastructure.Domain.ChannelEnum import ChannelEnum
from FacebookDexter.Infrastructure.Domain.DaysEnum import DaysEnum
from FacebookDexter.Infrastructure.Domain.LevelEnums import LevelEnum
from FacebookDexter.Infrastructure.Domain.LogicalOperatorEnum import LogicOperatorEnum
from FacebookDexter.Infrastructure.Domain.Rules.Antecedent import Antecedent
from FacebookDexter.Infrastructure.Domain.Rules.AntecedentEnums import AntecedentTypeEnum
from FacebookDexter.Infrastructure.Domain.Rules.Connective import Connective
from FacebookDexter.Infrastructure.Domain.Rules.RuleBase import RuleBase
from FacebookDexter.Infrastructure.Domain.Rules.RuleEnums import RuleTypeEnum, RuleCategoryEnum, RuleImportanceEnum, \
    RuleSourceEnum, RuleRedirectEnum
from FacebookDexter.Infrastructure.FuzzyEngine.FuzzySets.FuzzySets import LinguisticVariableEnum

RULES_ADSET_DECREASE_BUDGET = [
    RuleBase(rtype=RuleTypeEnum.BUDGET_AND_BID,
             channel=ChannelEnum.FACEBOOK,
             category=RuleCategoryEnum.IMPROVE_CPR,
             importance=RuleImportanceEnum.HIGH,
             source=RuleSourceEnum.DEXTER,
             level=LevelEnum.ADSET,
             action=ActionEnum.DECREASE_BUDGET,
             redirect=RuleRedirectEnum.EDIT_STRUCTURE,
             template="Dexter noticed your CPR increased while your CTR remains low. You should decrease "
                      "the budget by maximum 25%.",
             breakdown_metadata=BreakdownMetadata(breakdown=BreakdownEnum.NONE,
                                                  action_breakdown=ActionBreakdownEnum.NONE),
             time_interval=DaysEnum.THREE_MONTHS,
             connective=Connective(LogicOperatorEnum.AND),
             antecedents=[
                 Antecedent(aid=1,
                            atype=AntecedentTypeEnum.FUZZY_TREND,
                            metric=AvailableMetricEnum.COST_PER_RESULT.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=LinguisticVariableEnum.INCREASING),
                 Antecedent(aid=2,
                            atype=AntecedentTypeEnum.FUZZY_VALUE,
                            metric=AvailableMetricEnum.CTR.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=LinguisticVariableEnum.LOW)
             ]),
    RuleBase(rtype=RuleTypeEnum.BUDGET_AND_BID,
             channel=ChannelEnum.FACEBOOK,
             category=RuleCategoryEnum.IMPROVE_CPR,
             importance=RuleImportanceEnum.HIGH,
             source=RuleSourceEnum.DEXTER,
             level=LevelEnum.ADSET,
             action=ActionEnum.DECREASE_BUDGET,
             redirect=RuleRedirectEnum.EDIT_STRUCTURE,
             template="Dexter noticed your CPR is high while your audience is narrow. You should "
                      "decrease the budget by maximum 25%.",
             breakdown_metadata=BreakdownMetadata(breakdown=BreakdownEnum.NONE,
                                                  action_breakdown=ActionBreakdownEnum.NONE),
             time_interval=DaysEnum.THREE_MONTHS,
             connective=Connective(LogicOperatorEnum.AND),
             antecedents=[
                 Antecedent(aid=1,
                            atype=AntecedentTypeEnum.FUZZY_TREND,
                            metric=AvailableMetricEnum.COST_PER_RESULT.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=LinguisticVariableEnum.INCREASING),
                 Antecedent(aid=2,
                            atype=AntecedentTypeEnum.VALUE,
                            metric=AvailableMetricEnum.AUDIENCE_SIZE.value,
                            operator=LogicOperatorEnum.LESS_THAN,
                            expected_value=NARROW_AUDIENCE_SIZE)
             ]),
    RuleBase(rtype=RuleTypeEnum.BUDGET_AND_BID,
             channel=ChannelEnum.FACEBOOK,
             category=RuleCategoryEnum.IMPROVE_CPR,
             importance=RuleImportanceEnum.HIGH,
             source=RuleSourceEnum.DEXTER,
             level=LevelEnum.ADSET,
             action=ActionEnum.DECREASE_BUDGET,
             redirect=RuleRedirectEnum.EDIT_STRUCTURE,
             template="Dexter noticed your CPR increased while your conversions remains low. You should "
                      "decrease the budget by maximum 25%. ",
             breakdown_metadata=BreakdownMetadata(breakdown=BreakdownEnum.NONE,
                                                  action_breakdown=ActionBreakdownEnum.NONE),
             time_interval=DaysEnum.THREE_MONTHS,
             connective=Connective(LogicOperatorEnum.AND),
             antecedents=[
                 Antecedent(aid=1,
                            atype=AntecedentTypeEnum.FUZZY_TREND,
                            metric=AvailableMetricEnum.COST_PER_RESULT.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=LinguisticVariableEnum.INCREASING),
                 Antecedent(aid=2,
                            atype=AntecedentTypeEnum.FUZZY_VALUE,
                            metric=AvailableMetricEnum.CONVERSIONS.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=LinguisticVariableEnum.LOW)
             ])
]
