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
from GoogleDexter.Infrastructure.Domain.Rules.GoogleRuleEnums import GoogleRuleTypeEnum, GoogleRuleImportanceEnum, \
    GoogleRuleCategoryEnum, GoogleRuleSourceEnum, GoogleRuleRedirectEnum
from GoogleDexter.Infrastructure.FuzzyEngine.GoogleFuzzySets import GoogleLinguisticVariableEnum

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
    RuleBase(rtype=GoogleRuleTypeEnum.PERFORMANCE,
             channel=ChannelEnum.GOOGLE,
             category=GoogleRuleCategoryEnum.IMPROVE_CPR,
             importance=GoogleRuleImportanceEnum.HIGH,
             source=GoogleRuleSourceEnum.DEXTER,
             level=LevelEnum.AD,
             action=GoogleActionEnum.PAUSE,
             redirect=GoogleRuleRedirectEnum.EDIT_STRUCTURE,
             template="Dexter noticed your CTR is decreasing while your results remain low. You should pause this ad to improve performance.",
             breakdown_metadata=BreakdownMetadataBase(breakdown=GoogleBreakdownEnum.NONE,
                                                  action_breakdown=GoogleActionBreakdownEnum.NONE),
             time_interval=DaysEnum.THREE_MONTHS,
             connective=Connective(LogicOperatorEnum.AND),
             antecedents=[
                 Antecedent(aid=1,
                            atype=AntecedentTypeEnum.FUZZY_TREND,
                            metric=GoogleAvailableMetricEnum.CTR.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=GoogleLinguisticVariableEnum.DECREASING),
                 Antecedent(aid=2,
                            atype=AntecedentTypeEnum.FUZZY_VALUE,
                            metric=GoogleAvailableMetricEnum.RESULTS.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=GoogleLinguisticVariableEnum.LOW)
             ]),
]
