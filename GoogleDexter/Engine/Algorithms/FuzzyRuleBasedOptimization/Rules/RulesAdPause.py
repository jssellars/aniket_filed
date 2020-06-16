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

RULES_AD_PAUSE = [
    # RuleBase(rtype=RuleTypeEnum.PERFORMANCE,
    #          channel=ChannelEnum.FACEBOOK,
    #          category=RuleCategoryEnum.IMPROVE_CPC,
    #          importance=RuleImportanceEnum.HIGH,
    #          source=RuleSourceEnum.DEXTER,
    #          level=LevelEnum.AD,
    #          action=ActionEnum.PAUSE,
    #          redirect=RuleRedirectEnum.EDIT_STRUCTURE,
    #          template="Dexter noticed your CPC increased while your results remain low. You should pause this ad to improve performance.",
    #          breakdown_metadata=BreakdownMetadata(breakdown=BreakdownEnum.NONE,
    #                                               action_breakdown=ActionBreakdownEnum.NONE),
    #          time_interval=DaysEnum.THREE_MONTHS,
    #          connective=Connective(LogicOperatorEnum.AND),
    #          antecedents=[
    #              Antecedent(aid=1,
    #                         atype=AntecedentTypeEnum.VALUE,
    #                         metric=AvailableMetricEnum.OBJECTIVE.value,
    #                         operator=LogicOperatorEnum.NOT_EQUAL,
    #                         expected_value=ObjectiveEnum.REACH.value),
    #              Antecedent(aid=2,
    #                         atype=AntecedentTypeEnum.FUZZY_TREND,
    #                         metric=AvailableMetricEnum.CPC.value,
    #                         operator=LogicOperatorEnum.EQUALS,
    #                         expected_value=LinguisticVariableEnum.INCREASING),
    #              Antecedent(aid=3,
    #                         atype=AntecedentTypeEnum.FUZZY_VALUE,
    #                         metric=AvailableMetricEnum.RESULTS.value,
    #                         operator=LogicOperatorEnum.EQUALS,
    #                         expected_value=LinguisticVariableEnum.LOW)
    #          ]),
    # RuleBase(rtype=RuleTypeEnum.PERFORMANCE,
    #          channel=ChannelEnum.FACEBOOK,
    #          category=RuleCategoryEnum.IMPROVE_CPR,
    #          importance=RuleImportanceEnum.HIGH,
    #          source=RuleSourceEnum.DEXTER,
    #          level=LevelEnum.AD,
    #          action=ActionEnum.PAUSE,
    #          redirect=RuleRedirectEnum.EDIT_STRUCTURE,
    #          template="Dexter noticed your impressions increased while your results remain low. You should pause this ad to improve performance.",
    #          breakdown_metadata=BreakdownMetadata(breakdown=BreakdownEnum.NONE,
    #                                               action_breakdown=ActionBreakdownEnum.NONE),
    #          time_interval=DaysEnum.THREE_MONTHS,
    #          connective=Connective(LogicOperatorEnum.AND),
    #          antecedents=[
    #              Antecedent(aid=1,
    #                         atype=AntecedentTypeEnum.VALUE,
    #                         metric=AvailableMetricEnum.OBJECTIVE.value,
    #                         operator=LogicOperatorEnum.NOT_EQUAL,
    #                         expected_value=ObjectiveEnum.REACH.value),
    #              Antecedent(aid=2,
    #                         atype=AntecedentTypeEnum.FUZZY_TREND,
    #                         metric=AvailableMetricEnum.IMPRESSIONS.value,
    #                         operator=LogicOperatorEnum.EQUALS,
    #                         expected_value=LinguisticVariableEnum.INCREASING),
    #              Antecedent(aid=3,
    #                         atype=AntecedentTypeEnum.FUZZY_VALUE,
    #                         metric=AvailableMetricEnum.RESULTS.value,
    #                         operator=LogicOperatorEnum.EQUALS,
    #                         expected_value=LinguisticVariableEnum.LOW)
    #          ]),
    # RuleBase(rtype=RuleTypeEnum.PERFORMANCE,
    #          channel=ChannelEnum.FACEBOOK,
    #          category=RuleCategoryEnum.IMPROVE_CPR,
    #          importance=RuleImportanceEnum.HIGH,
    #          source=RuleSourceEnum.DEXTER,
    #          level=LevelEnum.AD,
    #          action=ActionEnum.PAUSE,
    #          redirect=RuleRedirectEnum.EDIT_STRUCTURE,
    #          template="Dexter noticed your cost per result is at historical high levels. You should pause this ad to improve performance.",
    #          breakdown_metadata=BreakdownMetadata(breakdown=BreakdownEnum.NONE,
    #                                               action_breakdown=ActionBreakdownEnum.NONE),
    #          time_interval=DaysEnum.THREE_MONTHS,
    #          connective=Connective(LogicOperatorEnum.AND),
    #          antecedents=[
    #              Antecedent(aid=1,
    #                         atype=AntecedentTypeEnum.VALUE,
    #                         metric=AvailableMetricEnum.OBJECTIVE.value,
    #                         operator=LogicOperatorEnum.NOT_EQUAL,
    #                         expected_value=ObjectiveEnum.REACH.value),
    #              Antecedent(aid=2,
    #                         atype=AntecedentTypeEnum.FUZZY_TREND,
    #                         metric=AvailableMetricEnum.COST_PER_RESULT.value,
    #                         operator=LogicOperatorEnum.EQUALS,
    #                         expected_value=LinguisticVariableEnum.HIGH)
    #          ]),
    RuleBase(rtype=RuleTypeEnum.PERFORMANCE,
             channel=ChannelEnum.GOOGLE,
             category=RuleCategoryEnum.IMPROVE_CPR,
             importance=RuleImportanceEnum.HIGH,
             source=RuleSourceEnum.DEXTER,
             level=LevelEnum.AD,
             action=ActionEnum.PAUSE,
             redirect=RuleRedirectEnum.EDIT_STRUCTURE,
             template="Dexter noticed your CTR is decreasing while your results remain low. You should pause this ad to improve performance.",
             breakdown_metadata=BreakdownMetadata(breakdown=BreakdownEnum.NONE,
                                                  action_breakdown=ActionBreakdownEnum.NONE),
             time_interval=DaysEnum.THREE_MONTHS,
             connective=Connective(LogicOperatorEnum.AND),
             antecedents=[
                 Antecedent(aid=1,
                            atype=AntecedentTypeEnum.FUZZY_TREND,
                            metric=AvailableMetricEnum.CTR.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=LinguisticVariableEnum.DECREASING),
                 Antecedent(aid=2,
                            atype=AntecedentTypeEnum.FUZZY_VALUE,
                            metric=AvailableMetricEnum.RESULTS.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=LinguisticVariableEnum.LOW)
             ]),
]
