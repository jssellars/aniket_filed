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
    HIGH_QUALITY_RANKING, NARROW_AUDIENCE_SIZE
from FacebookDexter.Infrastructure.Domain.Actions.ActionEnums import FacebookActionEnum
from FacebookDexter.Infrastructure.Domain.Breakdowns import FacebookBreakdownEnum, FacebookActionBreakdownEnum
from FacebookDexter.Infrastructure.Domain.FuzzyEngine.FacebookFuzzySets import FacebookLinguisticVariableEnum
from FacebookDexter.Infrastructure.Domain.Rules.FacebookRuleEnums import FacebookRuleTypeEnum, \
    FacebookRuleImportanceEnum, FacebookRuleSourceEnum, FacebookRuleCategoryEnum, FacebookRuleRedirectEnum

RULES_AD_INCREASE_BUDGET = [
    RuleBase(rtype=FacebookRuleTypeEnum.BUDGET_AND_BID,
             channel=ChannelEnum.FACEBOOK,
             category=FacebookRuleCategoryEnum.IMPROVE_CPR,
             importance=FacebookRuleImportanceEnum.HIGH,
             source=FacebookRuleSourceEnum.DEXTER,
             level=LevelEnum.AD,
             action=FacebookActionEnum.NONE,
             redirect=FacebookRuleRedirectEnum.EDIT_STRUCTURE,
             template="Amazing job!! Dexter noticed your ads quality and results are high. You should increase "
                      "your budget by a maximum 25% "
                      "to reach as many people as possible.",
             breakdown_metadata=BreakdownMetadataBase(breakdown=FacebookBreakdownEnum.NONE,
                                                  action_breakdown=FacebookActionBreakdownEnum.NONE),
             time_interval=DaysEnum.THREE_MONTHS,
             connective=Connective(LogicOperatorEnum.AND),
             antecedents=[
                 Antecedent(aid=1,
                            atype=AntecedentTypeEnum.FUZZY_VALUE,
                            metric=FacebookAvailableMetricEnum.RESULTS.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=FacebookLinguisticVariableEnum.HIGH),
                 Antecedent(aid=2,
                            atype=AntecedentTypeEnum.VALUE,
                            metric=FacebookAvailableMetricEnum.QUALITY_RANKING.value,
                            operator=LogicOperatorEnum.IN,
                            expected_value=HIGH_QUALITY_RANKING)
             ]),
    RuleBase(rtype=FacebookRuleTypeEnum.BUDGET_AND_BID,
             channel=ChannelEnum.FACEBOOK,
             category=FacebookRuleCategoryEnum.IMPROVE_CTR,
             importance=FacebookRuleImportanceEnum.HIGH,
             source=FacebookRuleSourceEnum.DEXTER,
             level=LevelEnum.AD,
             action=FacebookActionEnum.NONE,
             redirect=FacebookRuleRedirectEnum.EDIT_STRUCTURE,
             template="Dexter noticed your ads quality and CTR are high, and you have a large audience. "
                      "Dexter suggests increasing your budget by a maximum 25% to reach as many people as possible.",
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
                 Antecedent(aid=2,
                            atype=AntecedentTypeEnum.VALUE,
                            metric=FacebookAvailableMetricEnum.QUALITY_RANKING.value,
                            operator=LogicOperatorEnum.IN,
                            expected_value=HIGH_QUALITY_RANKING),
                 Antecedent(aid=3,
                            atype=AntecedentTypeEnum.VALUE,
                            metric=FacebookAvailableMetricEnum.AUDIENCE_SIZE.value,
                            operator=LogicOperatorEnum.GREATER_THAN,
                            expected_value=NARROW_AUDIENCE_SIZE)
             ])

]
