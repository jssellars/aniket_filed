from FacebookDexter.Engine.Algorithms.FuzzyRuleBasedOptimization.Metrics.AvailableMetricEnum import AvailableMetricEnum
from FacebookDexter.Engine.Algorithms.FuzzyRuleBasedOptimization.Metrics.MetricValues import LOW_QUALITY_RANKING
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

RULES_AD_DECREASE_BUDGET = [
    RuleBase(rtype=RuleTypeEnum.BUDGET_AND_BID,
             channel=ChannelEnum.FACEBOOK,
             category=RuleCategoryEnum.IMPROVE_CPR,
             importance=RuleImportanceEnum.HIGH,
             source=RuleSourceEnum.DEXTER,
             level=LevelEnum.AD,
             action=ActionEnum.NONE,
             redirect=RuleRedirectEnum.EDIT_STRUCTURE,
             template="Dexter noticed your quality ranking and results are low. You should decrease "
                      "the budget by maximum 25%.",
             breakdown_metadata=BreakdownMetadata(breakdown=BreakdownEnum.NONE,
                                                  action_breakdown=ActionBreakdownEnum.NONE),
             time_interval=DaysEnum.THREE_MONTHS,
             connective=Connective(LogicOperatorEnum.AND),
             antecedents=[
                 Antecedent(aid=1,
                            atype=AntecedentTypeEnum.FUZZY_VALUE,
                            metric=AvailableMetricEnum.RESULTS.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=LinguisticVariableEnum.LOW),
                 Antecedent(aid=2,
                            atype=AntecedentTypeEnum.VALUE,
                            metric=AvailableMetricEnum.QUALITY_RANKING.value,
                            operator=LogicOperatorEnum.IN,
                            expected_value=LOW_QUALITY_RANKING)
             ]),
    RuleBase(rtype=RuleTypeEnum.BUDGET_AND_BID,
             channel=ChannelEnum.FACEBOOK,
             category=RuleCategoryEnum.IMPROVE_CPC,
             importance=RuleImportanceEnum.HIGH,
             source=RuleSourceEnum.DEXTER,
             level=LevelEnum.AD,
             action=ActionEnum.NONE,
             redirect=RuleRedirectEnum.EDIT_STRUCTURE,
             template="Dexter noticed your quality ranking is low while your CPC remains high. You should decrease "
                      "the budget by maximum 25%.",
             breakdown_metadata=BreakdownMetadata(breakdown=BreakdownEnum.NONE,
                                                  action_breakdown=ActionBreakdownEnum.NONE),
             time_interval=DaysEnum.THREE_MONTHS,
             connective=Connective(LogicOperatorEnum.AND),
             antecedents=[
                 Antecedent(aid=1,
                            atype=AntecedentTypeEnum.FUZZY_VALUE,
                            metric=AvailableMetricEnum.CPC.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=LinguisticVariableEnum.HIGH),
                 Antecedent(aid=2,
                            atype=AntecedentTypeEnum.VALUE,
                            metric=AvailableMetricEnum.QUALITY_RANKING.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=LOW_QUALITY_RANKING)
             ]),
    RuleBase(rtype=RuleTypeEnum.BUDGET_AND_BID,
             channel=ChannelEnum.FACEBOOK,
             category=RuleCategoryEnum.IMPROVE_CPC,
             importance=RuleImportanceEnum.HIGH,
             source=RuleSourceEnum.DEXTER,
             level=LevelEnum.AD,
             action=ActionEnum.NONE,
             redirect=RuleRedirectEnum.EDIT_STRUCTURE,
             template="Dexter noticed your ad has more that 20% text overlay and a high CPC. You should decrease "
                      "the budget by maximum 25%.",
             breakdown_metadata=BreakdownMetadata(breakdown=BreakdownEnum.NONE,
                                                  action_breakdown=ActionBreakdownEnum.NONE),
             time_interval=DaysEnum.THREE_MONTHS,
             connective=Connective(LogicOperatorEnum.AND),
             antecedents=[
                 Antecedent(aid=1,
                            atype=AntecedentTypeEnum.FUZZY_VALUE,
                            metric=AvailableMetricEnum.CPC.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=LinguisticVariableEnum.HIGH),
                 Antecedent(aid=2,
                            atype=AntecedentTypeEnum.VALUE,
                            metric=AvailableMetricEnum.TEXT_OVERLAY.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=True)
             ])
]
