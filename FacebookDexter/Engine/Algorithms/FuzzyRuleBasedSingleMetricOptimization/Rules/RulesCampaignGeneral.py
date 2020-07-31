from Core.Dexter.Infrastructure.Domain.Breakdowns import BreakdownMetadataBase
from Core.Dexter.Infrastructure.Domain.ChannelEnum import ChannelEnum
from Core.Dexter.Infrastructure.Domain.DaysEnum import DaysEnum
from Core.Dexter.Infrastructure.Domain.LevelEnums import LevelEnum
from Core.Dexter.Infrastructure.Domain.LogicalOperatorEnum import LogicOperatorEnum
from Core.Dexter.Infrastructure.Domain.Rules.Antecedent import Antecedent
from Core.Dexter.Infrastructure.Domain.Rules.AntecedentEnums import AntecedentTypeEnum
from Core.Dexter.Infrastructure.Domain.Rules.Connective import Connective
from Core.Dexter.Infrastructure.Domain.Rules.RuleBase import RuleBase
from FacebookDexter.Engine.Algorithms.FuzzyRuleBasedSingleMetricOptimization.Metrics.FacebookAvailableSingleMetricEnum import \
    FacebookAvailableSingleMetricEnum
from FacebookDexter.Infrastructure.Domain.Actions.ActionEnums import FacebookActionEnum
from FacebookDexter.Infrastructure.Domain.Breakdowns import FacebookActionBreakdownEnum, FacebookBreakdownEnum
from FacebookDexter.Infrastructure.Domain.FuzzyEngine.FacebookFuzzySets import FacebookLinguisticVariableEnum
from FacebookDexter.Infrastructure.Domain.Rules.FacebookRuleEnums import FacebookRuleTypeEnum, \
    FacebookRuleCategoryEnum, FacebookRuleSourceEnum, FacebookRuleImportanceEnum, FacebookRuleRedirectEnum

RULES_CAMPAIGN_GENERAL = [
    RuleBase(rtype=FacebookRuleTypeEnum.BUDGET_AND_BID,
             channel=ChannelEnum.FACEBOOK,
             category=FacebookRuleCategoryEnum.IMPROVE_CPR,
             importance=FacebookRuleImportanceEnum.HIGH,
             source=FacebookRuleSourceEnum.DEXTER,
             level=LevelEnum.CAMPAIGN,
             action=FacebookActionEnum.NONE,
             redirect=FacebookRuleRedirectEnum.EDIT_STRUCTURE,
             variance=20,
             template="Dexter noticed that your __id=1&metric_name=IMPRESSIONS&metric_type=1&antecedent_type=8__ "
                      "decreased by __id=1&value=null__%, "
                      "compared to the last __id=1&time_interval=3__ days average "
                      "of __id=2&value=null__ __id=2&metric_name=IMPRESSIONS&metric_type=1&antecedent_type=11__. "
                      "This means your competitors have better ad creative or your "
                      "audience saw the ads too many times. "
                      "Check your ads now to see which one is the less performing. ",
             breakdown_metadata=BreakdownMetadataBase(breakdown=FacebookBreakdownEnum.NONE,
                                                      action_breakdown=FacebookActionBreakdownEnum.NONE),
             time_interval=DaysEnum.THREE,
             connective=Connective(LogicOperatorEnum.AND),
             antecedents=[
                 Antecedent(aid=1,
                            atype=AntecedentTypeEnum.FUZZY_TREND,
                            metric=FacebookAvailableSingleMetricEnum.IMPRESSIONS.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=FacebookLinguisticVariableEnum.DECREASING)
             ]),
    RuleBase(rtype=FacebookRuleTypeEnum.BUDGET_AND_BID,
             channel=ChannelEnum.FACEBOOK,
             category=FacebookRuleCategoryEnum.IMPROVE_CPR,
             importance=FacebookRuleImportanceEnum.HIGH,
             source=FacebookRuleSourceEnum.DEXTER,
             level=LevelEnum.CAMPAIGN,
             action=FacebookActionEnum.NONE,
             redirect=FacebookRuleRedirectEnum.EDIT_STRUCTURE,
             variance=15,
             template="Dexter noticed that your __id=1&metric_name=IMPRESSIONS&metric_type=1&antecedent_type=8__ "
                      "decreased by __id=1&value=null__%, "
                      "compared to the last __id=1&time_interval=7__ days average "
                      "of __id=2&value=null__ __id=2&metric_name=IMPRESSIONS&metric_type=1&antecedent_type=11__. "
                      "This means your competitors have better ad creative or your "
                      "audience saw the ads too many times. "
                      "Check your ads now to see which one is the less performing. ",
             breakdown_metadata=BreakdownMetadataBase(breakdown=FacebookBreakdownEnum.NONE,
                                                      action_breakdown=FacebookActionBreakdownEnum.NONE),
             time_interval=DaysEnum.SEVEN,
             connective=Connective(LogicOperatorEnum.AND),
             antecedents=[
                 Antecedent(aid=1,
                            atype=AntecedentTypeEnum.FUZZY_TREND,
                            metric=FacebookAvailableSingleMetricEnum.IMPRESSIONS.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=FacebookLinguisticVariableEnum.DECREASING),
             ]),
    RuleBase(rtype=FacebookRuleTypeEnum.BUDGET_AND_BID,
             channel=ChannelEnum.FACEBOOK,
             category=FacebookRuleCategoryEnum.IMPROVE_CPR,
             importance=FacebookRuleImportanceEnum.HIGH,
             source=FacebookRuleSourceEnum.DEXTER,
             level=LevelEnum.CAMPAIGN,
             action=FacebookActionEnum.NONE,
             redirect=FacebookRuleRedirectEnum.EDIT_STRUCTURE,
             variance=10,
             template="Dexter noticed that your __id=1&metric_name=IMPRESSIONS&metric_type=1&antecedent_type=8__ "
                      "decreased by __id=1&value=null__%, "
                      "compared to the last __id=1&time_interval=14__ days average "
                      "of __id=2&value=null__ __id=2&metric_name=IMPRESSIONS&metric_type=1&antecedent_type=11__. "
                      "This means your competitors have better ad creative or your "
                      "audience saw the ads too many times. "
                      "Check your ads now to see which one is the less performing. ",
             breakdown_metadata=BreakdownMetadataBase(breakdown=FacebookBreakdownEnum.NONE,
                                                      action_breakdown=FacebookActionBreakdownEnum.NONE),
             time_interval=DaysEnum.FOURTEEN,
             connective=Connective(LogicOperatorEnum.AND),
             antecedents=[
                 Antecedent(aid=1,
                            atype=AntecedentTypeEnum.FUZZY_TREND,
                            metric=FacebookAvailableSingleMetricEnum.IMPRESSIONS.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=FacebookLinguisticVariableEnum.DECREASING),
             ]),
    RuleBase(rtype=FacebookRuleTypeEnum.BUDGET_AND_BID,
             channel=ChannelEnum.FACEBOOK,
             category=FacebookRuleCategoryEnum.IMPROVE_CPR,
             importance=FacebookRuleImportanceEnum.HIGH,
             source=FacebookRuleSourceEnum.DEXTER,
             level=LevelEnum.CAMPAIGN,
             action=FacebookActionEnum.NONE,
             redirect=FacebookRuleRedirectEnum.EDIT_STRUCTURE,
             variance=10,
             template="Dexter noticed that your __id=1&metric_name=IMPRESSIONS&metric_type=1&antecedent_type=8__ "
                      "decreased by __id=1&value=null__%, "
                      "compared to the last __id=1&time_interval=30__ days average "
                      "of __id=2&value=null__ __id=2&metric_name=IMPRESSIONS&metric_type=1&antecedent_type=11__. "
                      "This means your competitors have better ad creative or your "
                      "audience saw the ads too many times. "
                      "Check your ads now to see which one is the less performing. ",
             breakdown_metadata=BreakdownMetadataBase(breakdown=FacebookBreakdownEnum.NONE,
                                                      action_breakdown=FacebookActionBreakdownEnum.NONE),
             time_interval=DaysEnum.MONTH,
             connective=Connective(LogicOperatorEnum.AND),
             antecedents=[
                 Antecedent(aid=1,
                            atype=AntecedentTypeEnum.FUZZY_TREND,
                            metric=FacebookAvailableSingleMetricEnum.IMPRESSIONS.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=FacebookLinguisticVariableEnum.DECREASING),
             ]),
    # RuleBase(rtype=FacebookRuleTypeEnum.BUDGET_AND_BID,
    #          channel=ChannelEnum.FACEBOOK,
    #          category=FacebookRuleCategoryEnum.IMPROVE_CPR,
    #          importance=FacebookRuleImportanceEnum.HIGH,
    #          source=FacebookRuleSourceEnum.DEXTER,
    #          level=LevelEnum.CAMPAIGN,
    #          action=FacebookActionEnum.NONE,
    #          redirect=FacebookRuleRedirectEnum.EDIT_STRUCTURE,
    #          variance=10,
    #          template="Dexter noticed that your __id=1&metric_name=IMPRESSIONS&metric_type=1&antecedent_type=8__ "
    #                   "decreased by __id=1&value=null__%, "
    #                   "compared to the last __id=1&time_interval=30__ days average "
    #                   "of __id=2&value=null__ __id=2&metric_name=IMPRESSIONS&metric_type=1&antecedent_type=11__. "
    #                   "This means your competitors have better ad creative or your "
    #                   "audience saw the ads too many times. "
    #                   "Check your ads now to see which one is the less performing. ",
    #          breakdown_metadata=BreakdownMetadataBase(breakdown=FacebookBreakdownEnum.NONE,
    #                                                   action_breakdown=FacebookActionBreakdownEnum.NONE),
    #          time_interval=DaysEnum.MONTH,
    #          connective=Connective(LogicOperatorEnum.AND),
    #          antecedents=[
    #              Antecedent(aid=1,
    #                         atype=AntecedentTypeEnum.FUZZY_TREND,
    #                         metric=FacebookAvailableSingleMetricEnum.IMPRESSIONS.value,
    #                         operator=LogicOperatorEnum.EQUALS,
    #                         expected_value=FacebookLinguisticVariableEnum.DECREASING),
    #          ])

]