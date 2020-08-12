from Core.Dexter.Infrastructure.Domain.Breakdowns import BreakdownMetadataBase
from Core.Dexter.Infrastructure.Domain.ChannelEnum import ChannelEnum
from Core.Dexter.Infrastructure.Domain.DaysEnum import DaysEnum
from Core.Dexter.Infrastructure.Domain.LevelEnums import LevelEnum
from Core.Dexter.Infrastructure.Domain.LogicalOperatorEnum import LogicOperatorEnum
from Core.Dexter.Infrastructure.Domain.Rules.Antecedent import Antecedent
from Core.Dexter.Infrastructure.Domain.Rules.AntecedentEnums import AntecedentTypeEnum
from Core.Dexter.Infrastructure.Domain.Rules.Connective import Connective
from Core.Dexter.Infrastructure.Domain.Rules.RuleBase import RuleBase
from FacebookDexter.Engine.Algorithms.FuzzyRuleBasedSingleMetricOptimization.Metrics.FacebookAvailableSingleMetricEnum import FacebookAvailableSingleMetricEnum
from FacebookDexter.Infrastructure.Domain.Actions.ActionEnums import FacebookActionEnum
from FacebookDexter.Infrastructure.Domain.Breakdowns import FacebookBreakdownEnum, FacebookActionBreakdownEnum
from FacebookDexter.Infrastructure.Domain.FuzzyEngine.FacebookFuzzySets import FacebookLinguisticVariableEnum
from FacebookDexter.Infrastructure.Domain.Rules.FacebookRuleEnums import FacebookRuleTypeEnum, FacebookRuleCategoryEnum, \
    FacebookRuleImportanceEnum, FacebookRuleSourceEnum, \
    FacebookRuleRedirectEnum

RULES_AD_GENERAL = [
    RuleBase(rtype=FacebookRuleTypeEnum.BUDGET_AND_BID,
             channel=ChannelEnum.FACEBOOK,
             category=FacebookRuleCategoryEnum.IMPROVE_CPR,
             importance=FacebookRuleImportanceEnum.MEDIUM,
             source=FacebookRuleSourceEnum.DEXTER,
             level=LevelEnum.AD,
             action=FacebookActionEnum.NONE,
             redirect=FacebookRuleRedirectEnum.EDIT_STRUCTURE,
             template="Dexter noticed that your __id=1&metric_name=IMPRESSIONS&metric_type=1&antecedent_type=8__ "
                      "decreased by __id=1&value=null__%, "
                      "compared to the last __id=1&time_interval=3__ days average "
                      "of __id=2&value=null__ __id=2&metric_name=IMPRESSIONS&metric_type=1&antecedent_type=11__. "
                      "This means your competitors have better ad creative or your audience saw the ads too many times. "
                      "Dexter recommends you to change the ad creative now.",
             breakdown_metadata=BreakdownMetadataBase(breakdown=FacebookBreakdownEnum.NONE,
                                                      action_breakdown=FacebookActionBreakdownEnum.NONE),
             time_interval=DaysEnum.THREE,
             connective=Connective(LogicOperatorEnum.AND),
             antecedents=[
                 Antecedent(aid=1,
                            atype=AntecedentTypeEnum.FUZZY_TREND,
                            metric=FacebookAvailableSingleMetricEnum.IMPRESSIONS.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=FacebookLinguisticVariableEnum.DECREASING),
                 Antecedent(aid=2,
                            atype=AntecedentTypeEnum.VARIANCE,
                            metric=FacebookAvailableSingleMetricEnum.IMPRESSIONS.value,
                            operator=LogicOperatorEnum.EQUAL_OR_GREATER_THAN,
                            expected_value=25)
             ]),
    RuleBase(rtype=FacebookRuleTypeEnum.BUDGET_AND_BID,
             channel=ChannelEnum.FACEBOOK,
             category=FacebookRuleCategoryEnum.IMPROVE_CPR,
             importance=FacebookRuleImportanceEnum.MEDIUM,
             source=FacebookRuleSourceEnum.DEXTER,
             level=LevelEnum.AD,
             action=FacebookActionEnum.NONE,
             redirect=FacebookRuleRedirectEnum.EDIT_STRUCTURE,
             template="Dexter noticed that your __id=1&metric_name=IMPRESSIONS&metric_type=1&antecedent_type=8__ "
                      "decreased by __id=1&value=null__%, "
                      "compared to the last __id=1&time_interval=7__ days average "
                      "of __id=2&value=null__ __id=2&metric_name=IMPRESSIONS&metric_type=1&antecedent_type=11__. "
                      "This means your competitors have better ad creative or your audience saw the ads too many times. "
                      "Dexter recommends you to change the ad creative now.",
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
                 Antecedent(aid=2,
                            atype=AntecedentTypeEnum.VARIANCE,
                            metric=FacebookAvailableSingleMetricEnum.IMPRESSIONS.value,
                            operator=LogicOperatorEnum.EQUAL_OR_GREATER_THAN,
                            expected_value=20)
             ]),
    RuleBase(rtype=FacebookRuleTypeEnum.BUDGET_AND_BID,
             channel=ChannelEnum.FACEBOOK,
             category=FacebookRuleCategoryEnum.IMPROVE_CPR,
             importance=FacebookRuleImportanceEnum.MEDIUM,
             source=FacebookRuleSourceEnum.DEXTER,
             level=LevelEnum.AD,
             action=FacebookActionEnum.NONE,
             redirect=FacebookRuleRedirectEnum.EDIT_STRUCTURE,
             template="Dexter noticed that your __id=1&metric_name=IMPRESSIONS&metric_type=1&antecedent_type=8__ "
                      "decreased by __id=1&value=null__%, "
                      "compared to the last __id=1&time_interval=14__ days average "
                      "of __id=2&value=null__ __id=2&metric_name=IMPRESSIONS&metric_type=1&antecedent_type=11__. "
                      "This means your competitors have better ad creative or your audience saw the ads too many times. "
                      "Dexter recommends you to change the ad creative now.",
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
                 Antecedent(aid=2,
                            atype=AntecedentTypeEnum.VARIANCE,
                            metric=FacebookAvailableSingleMetricEnum.IMPRESSIONS.value,
                            operator=LogicOperatorEnum.EQUAL_OR_GREATER_THAN,
                            expected_value=15)
             ]),
    RuleBase(rtype=FacebookRuleTypeEnum.BUDGET_AND_BID,
             channel=ChannelEnum.FACEBOOK,
             category=FacebookRuleCategoryEnum.IMPROVE_CPR,
             importance=FacebookRuleImportanceEnum.MEDIUM,
             source=FacebookRuleSourceEnum.DEXTER,
             level=LevelEnum.AD,
             action=FacebookActionEnum.NONE,
             redirect=FacebookRuleRedirectEnum.EDIT_STRUCTURE,
             template="Dexter noticed that your __id=1&metric_name=IMPRESSIONS&metric_type=1&antecedent_type=8__ "
                      "decreased by __id=1&value=null__%, "
                      "compared to the last __id=1&time_interval=30__ days average "
                      "of __id=2&value=null__ __id=2&metric_name=IMPRESSIONS&metric_type=1&antecedent_type=11__. "
                      "This means your competitors have better ad creative or your audience saw the ads too many times. "
                      "Dexter recommends you to change the ad creative now.",
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
                 Antecedent(aid=2,
                            atype=AntecedentTypeEnum.VARIANCE,
                            metric=FacebookAvailableSingleMetricEnum.IMPRESSIONS.value,
                            operator=LogicOperatorEnum.EQUAL_OR_GREATER_THAN,
                            expected_value=10)
             ]),
    RuleBase(rtype=FacebookRuleTypeEnum.BUDGET_AND_BID,
             channel=ChannelEnum.FACEBOOK,
             category=FacebookRuleCategoryEnum.IMPROVE_CPR,
             importance=FacebookRuleImportanceEnum.MEDIUM,
             source=FacebookRuleSourceEnum.DEXTER,
             level=LevelEnum.AD,
             action=FacebookActionEnum.NONE,
             redirect=FacebookRuleRedirectEnum.EDIT_STRUCTURE,
             template="Dexter noticed that your __id=1&metric_name=CPM&metric_type=1&antecedent_type=8__ "
                      "increased by __id=1&value=null__%, "
                      "compared to the last __id=1&time_interval=3__ days average "
                      "of __id=2&value=null__ __id=2&metric_name=CPM&metric_type=1&antecedent_type=11__. "
                      " This means your audience saw the ads too many times and they are not as engaged as before. "
                      "Dexter recommends you to change the ad creative now.",
             breakdown_metadata=BreakdownMetadataBase(breakdown=FacebookBreakdownEnum.NONE,
                                                      action_breakdown=FacebookActionBreakdownEnum.NONE),
             time_interval=DaysEnum.THREE,
             connective=Connective(LogicOperatorEnum.AND),
             antecedents=[
                 Antecedent(aid=1,
                            atype=AntecedentTypeEnum.FUZZY_TREND,
                            metric=FacebookAvailableSingleMetricEnum.CPM.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=FacebookLinguisticVariableEnum.INCREASING),
                 Antecedent(aid=2,
                            atype=AntecedentTypeEnum.VARIANCE,
                            metric=FacebookAvailableSingleMetricEnum.CPM.value,
                            operator=LogicOperatorEnum.EQUAL_OR_GREATER_THAN,
                            expected_value=20)
             ]),
    RuleBase(rtype=FacebookRuleTypeEnum.BUDGET_AND_BID,
             channel=ChannelEnum.FACEBOOK,
             category=FacebookRuleCategoryEnum.IMPROVE_CPR,
             importance=FacebookRuleImportanceEnum.MEDIUM,
             source=FacebookRuleSourceEnum.DEXTER,
             level=LevelEnum.AD,
             action=FacebookActionEnum.NONE,
             redirect=FacebookRuleRedirectEnum.EDIT_STRUCTURE,
             template="Dexter noticed that your __id=1&metric_name=CPM&metric_type=1&antecedent_type=8__ "
                      "increased by __id=1&value=null__%, "
                      "compared to the last __id=1&time_interval=7__ days average "
                      "of __id=2&value=null__ __id=2&metric_name=CPM&metric_type=1&antecedent_type=11__. "
                      " This means your audience saw the ads too many times and they are not as engaged as before. "
                      "Dexter recommends you to change the ad creative now.",
             breakdown_metadata=BreakdownMetadataBase(breakdown=FacebookBreakdownEnum.NONE,
                                                      action_breakdown=FacebookActionBreakdownEnum.NONE),
             time_interval=DaysEnum.SEVEN,
             connective=Connective(LogicOperatorEnum.AND),
             antecedents=[
                 Antecedent(aid=1,
                            atype=AntecedentTypeEnum.FUZZY_TREND,
                            metric=FacebookAvailableSingleMetricEnum.CPM.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=FacebookLinguisticVariableEnum.INCREASING),
                 Antecedent(aid=2,
                            atype=AntecedentTypeEnum.VARIANCE,
                            metric=FacebookAvailableSingleMetricEnum.CPM.value,
                            operator=LogicOperatorEnum.EQUAL_OR_GREATER_THAN,
                            expected_value=15)
             ]),
    RuleBase(rtype=FacebookRuleTypeEnum.BUDGET_AND_BID,
             channel=ChannelEnum.FACEBOOK,
             category=FacebookRuleCategoryEnum.IMPROVE_CPR,
             importance=FacebookRuleImportanceEnum.MEDIUM,
             source=FacebookRuleSourceEnum.DEXTER,
             level=LevelEnum.AD,
             action=FacebookActionEnum.NONE,
             redirect=FacebookRuleRedirectEnum.EDIT_STRUCTURE,
             template="Dexter noticed that your __id=1&metric_name=CPM&metric_type=1&antecedent_type=8__ "
                      "increased by __id=1&value=null__%, "
                      "compared to the last __id=1&time_interval=14__ days average "
                      "of __id=2&value=null__ __id=2&metric_name=CPM&metric_type=1&antecedent_type=11__. "
                      " This means your audience saw the ads too many times and they are not as engaged as before. "
                      "Dexter recommends you to change the ad creative now.",
             breakdown_metadata=BreakdownMetadataBase(breakdown=FacebookBreakdownEnum.NONE,
                                                      action_breakdown=FacebookActionBreakdownEnum.NONE),
             time_interval=DaysEnum.FOURTEEN,
             connective=Connective(LogicOperatorEnum.AND),
             antecedents=[
                 Antecedent(aid=1,
                            atype=AntecedentTypeEnum.FUZZY_TREND,
                            metric=FacebookAvailableSingleMetricEnum.CPM.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=FacebookLinguisticVariableEnum.INCREASING),
                 Antecedent(aid=2,
                            atype=AntecedentTypeEnum.VARIANCE,
                            metric=FacebookAvailableSingleMetricEnum.CPM.value,
                            operator=LogicOperatorEnum.EQUAL_OR_GREATER_THAN,
                            expected_value=10)
             ]),
    RuleBase(rtype=FacebookRuleTypeEnum.BUDGET_AND_BID,
             channel=ChannelEnum.FACEBOOK,
             category=FacebookRuleCategoryEnum.IMPROVE_CPR,
             importance=FacebookRuleImportanceEnum.MEDIUM,
             source=FacebookRuleSourceEnum.DEXTER,
             level=LevelEnum.AD,
             action=FacebookActionEnum.NONE,
             redirect=FacebookRuleRedirectEnum.EDIT_STRUCTURE,
             template="Dexter noticed that your __id=1&metric_name=CPM&metric_type=1&antecedent_type=8__ "
                      "increased by __id=1&value=null__%, "
                      "compared to the last __id=1&time_interval=30__ days average "
                      "of __id=2&value=null__ __id=2&metric_name=CPM&metric_type=1&antecedent_type=11__. "
                      " This means your audience saw the ads too many times and they are not as engaged as before. "
                      "Dexter recommends you to change the ad creative now.",
             breakdown_metadata=BreakdownMetadataBase(breakdown=FacebookBreakdownEnum.NONE,
                                                      action_breakdown=FacebookActionBreakdownEnum.NONE),
             time_interval=DaysEnum.MONTH,
             connective=Connective(LogicOperatorEnum.AND),
             antecedents=[
                 Antecedent(aid=1,
                            atype=AntecedentTypeEnum.FUZZY_TREND,
                            metric=FacebookAvailableSingleMetricEnum.CPM.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=FacebookLinguisticVariableEnum.INCREASING),
                 Antecedent(aid=2,
                            atype=AntecedentTypeEnum.VARIANCE,
                            metric=FacebookAvailableSingleMetricEnum.CPM.value,
                            operator=LogicOperatorEnum.EQUAL_OR_GREATER_THAN,
                            expected_value=10)
             ]),
    RuleBase(rtype=FacebookRuleTypeEnum.BUDGET_AND_BID,
             channel=ChannelEnum.FACEBOOK,
             category=FacebookRuleCategoryEnum.IMPROVE_CPR,
             importance=FacebookRuleImportanceEnum.MEDIUM,
             source=FacebookRuleSourceEnum.DEXTER,
             level=LevelEnum.AD,
             action=FacebookActionEnum.NONE,
             redirect=FacebookRuleRedirectEnum.EDIT_STRUCTURE,
             template="Dexter noticed that your __id=1&metric_name=CTR&metric_type=1&antecedent_type=8__ "
                      "decreased by __id=1&value=null__%, "
                      "compared to the last __id=1&time_interval=3__ days average "
                      "of __id=2&value=null__ __id=2&metric_name=CTR&metric_type=1&antecedent_type=11__. "
                      "This means your audience saw the ads too many times or your ad creative doesn't "
                      "resonate with current selected audience. Dexter recommends you to change the ad creative now.",
             breakdown_metadata=BreakdownMetadataBase(breakdown=FacebookBreakdownEnum.NONE,
                                                      action_breakdown=FacebookActionBreakdownEnum.NONE),
             time_interval=DaysEnum.THREE,
             connective=Connective(LogicOperatorEnum.AND),
             antecedents=[
                 Antecedent(aid=1,
                            atype=AntecedentTypeEnum.FUZZY_TREND,
                            metric=FacebookAvailableSingleMetricEnum.CTR.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=FacebookLinguisticVariableEnum.DECREASING),
                 Antecedent(aid=2,
                            atype=AntecedentTypeEnum.VARIANCE,
                            metric=FacebookAvailableSingleMetricEnum.CTR.value,
                            operator=LogicOperatorEnum.EQUAL_OR_GREATER_THAN,
                            expected_value=20)
             ]),
    RuleBase(rtype=FacebookRuleTypeEnum.BUDGET_AND_BID,
             channel=ChannelEnum.FACEBOOK,
             category=FacebookRuleCategoryEnum.IMPROVE_CPR,
             importance=FacebookRuleImportanceEnum.MEDIUM,
             source=FacebookRuleSourceEnum.DEXTER,
             level=LevelEnum.AD,
             action=FacebookActionEnum.NONE,
             redirect=FacebookRuleRedirectEnum.EDIT_STRUCTURE,
             template="Dexter noticed that your __id=1&metric_name=CTR&metric_type=1&antecedent_type=8__ "
                      "decreased by __id=1&value=null__%, "
                      "compared to the last __id=1&time_interval=7__ days average "
                      "of __id=2&value=null__ __id=2&metric_name=CTR&metric_type=1&antecedent_type=11__. "
                      "This means your audience saw the ads too many times or your ad creative doesn't "
                      "resonate with current selected audience. Dexter recommends you to change the ad creative now.",
             breakdown_metadata=BreakdownMetadataBase(breakdown=FacebookBreakdownEnum.NONE,
                                                      action_breakdown=FacebookActionBreakdownEnum.NONE),
             time_interval=DaysEnum.SEVEN,
             connective=Connective(LogicOperatorEnum.AND),
             antecedents=[
                 Antecedent(aid=1,
                            atype=AntecedentTypeEnum.FUZZY_TREND,
                            metric=FacebookAvailableSingleMetricEnum.CTR.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=FacebookLinguisticVariableEnum.DECREASING),
                 Antecedent(aid=2,
                            atype=AntecedentTypeEnum.VARIANCE,
                            metric=FacebookAvailableSingleMetricEnum.CTR.value,
                            operator=LogicOperatorEnum.EQUAL_OR_GREATER_THAN,
                            expected_value=15)
             ]),
    RuleBase(rtype=FacebookRuleTypeEnum.BUDGET_AND_BID,
             channel=ChannelEnum.FACEBOOK,
             category=FacebookRuleCategoryEnum.IMPROVE_CPR,
             importance=FacebookRuleImportanceEnum.MEDIUM,
             source=FacebookRuleSourceEnum.DEXTER,
             level=LevelEnum.AD,
             action=FacebookActionEnum.NONE,
             redirect=FacebookRuleRedirectEnum.EDIT_STRUCTURE,
             template="Dexter noticed that your __id=1&metric_name=CTR&metric_type=1&antecedent_type=8__ "
                      "decreased by __id=1&value=null__%, "
                      "compared to the last __id=1&time_interval=14__ days average "
                      "of __id=2&value=null__ __id=2&metric_name=CTR&metric_type=1&antecedent_type=11__. "
                      "This means your audience saw the ads too many times or your ad creative doesn't "
                      "resonate with current selected audience. Dexter recommends you to change the ad creative now.",
             breakdown_metadata=BreakdownMetadataBase(breakdown=FacebookBreakdownEnum.NONE,
                                                      action_breakdown=FacebookActionBreakdownEnum.NONE),
             time_interval=DaysEnum.FOURTEEN,
             connective=Connective(LogicOperatorEnum.AND),
             antecedents=[
                 Antecedent(aid=1,
                            atype=AntecedentTypeEnum.FUZZY_TREND,
                            metric=FacebookAvailableSingleMetricEnum.CTR.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=FacebookLinguisticVariableEnum.DECREASING),
                 Antecedent(aid=2,
                            atype=AntecedentTypeEnum.VARIANCE,
                            metric=FacebookAvailableSingleMetricEnum.CTR.value,
                            operator=LogicOperatorEnum.EQUAL_OR_GREATER_THAN,
                            expected_value=10)
             ]),
    RuleBase(rtype=FacebookRuleTypeEnum.BUDGET_AND_BID,
             channel=ChannelEnum.FACEBOOK,
             category=FacebookRuleCategoryEnum.IMPROVE_CPR,
             importance=FacebookRuleImportanceEnum.MEDIUM,
             source=FacebookRuleSourceEnum.DEXTER,
             level=LevelEnum.AD,
             action=FacebookActionEnum.NONE,
             redirect=FacebookRuleRedirectEnum.EDIT_STRUCTURE,
             template="Dexter noticed that your __id=1&metric_name=CTR&metric_type=1&antecedent_type=8__ "
                      "decreased by __id=1&value=null__%, "
                      "compared to the last __id=1&time_interval=30__ days average "
                      "of __id=2&value=null__ __id=2&metric_name=CTR&metric_type=1&antecedent_type=11__. "
                      "This means your audience saw the ads too many times or your ad creative doesn't "
                      "resonate with current selected audience. Dexter recommends you to change the ad creative now.",
             breakdown_metadata=BreakdownMetadataBase(breakdown=FacebookBreakdownEnum.NONE,
                                                      action_breakdown=FacebookActionBreakdownEnum.NONE),
             time_interval=DaysEnum.MONTH,
             connective=Connective(LogicOperatorEnum.AND),
             antecedents=[
                 Antecedent(aid=1,
                            atype=AntecedentTypeEnum.FUZZY_TREND,
                            metric=FacebookAvailableSingleMetricEnum.CTR.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=FacebookLinguisticVariableEnum.DECREASING),
                 Antecedent(aid=2,
                            atype=AntecedentTypeEnum.VARIANCE,
                            metric=FacebookAvailableSingleMetricEnum.CTR.value,
                            operator=LogicOperatorEnum.EQUAL_OR_GREATER_THAN,
                            expected_value=10)
             ]),
    RuleBase(rtype=FacebookRuleTypeEnum.BUDGET_AND_BID,
             channel=ChannelEnum.FACEBOOK,
             category=FacebookRuleCategoryEnum.IMPROVE_CPR,
             importance=FacebookRuleImportanceEnum.HIGH,
             source=FacebookRuleSourceEnum.DEXTER,
             level=LevelEnum.AD,
             action=FacebookActionEnum.NONE,
             redirect=FacebookRuleRedirectEnum.EDIT_STRUCTURE,
             template="Dexter noticed that your __id=1&metric_name=UNIQUE_CLICKS&metric_type=1&antecedent_type=8__ "
                      "decreased by __id=1&value=null__%, "
                      "compared to the last __id=1&time_interval=3__ days average "
                      "of __id=2&value=null__ __id=2&metric_name=UNIQUE_CLICKS&metric_type=1&antecedent_type=11__. "
                      "This means your audience saw the ads too many times or your ad creative doesn't resonate "
                      "with current selected audience. Dexter recommends you to change the ad creative now.",
             breakdown_metadata=BreakdownMetadataBase(breakdown=FacebookBreakdownEnum.NONE,
                                                      action_breakdown=FacebookActionBreakdownEnum.NONE),
             time_interval=DaysEnum.THREE,
             connective=Connective(LogicOperatorEnum.AND),
             antecedents=[
                 Antecedent(aid=1,
                            atype=AntecedentTypeEnum.FUZZY_TREND,
                            metric=FacebookAvailableSingleMetricEnum.UNIQUE_CLICKS.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=FacebookLinguisticVariableEnum.DECREASING),
                 Antecedent(aid=2,
                            atype=AntecedentTypeEnum.VARIANCE,
                            metric=FacebookAvailableSingleMetricEnum.UNIQUE_CLICKS.value,
                            operator=LogicOperatorEnum.EQUAL_OR_GREATER_THAN,
                            expected_value=25)
             ]),
    RuleBase(rtype=FacebookRuleTypeEnum.BUDGET_AND_BID,
             channel=ChannelEnum.FACEBOOK,
             category=FacebookRuleCategoryEnum.IMPROVE_CPR,
             importance=FacebookRuleImportanceEnum.HIGH,
             source=FacebookRuleSourceEnum.DEXTER,
             level=LevelEnum.AD,
             action=FacebookActionEnum.NONE,
             redirect=FacebookRuleRedirectEnum.EDIT_STRUCTURE,
             template="Dexter noticed that your __id=1&metric_name=UNIQUE_CLICKS&metric_type=1&antecedent_type=8__ "
                      "decreased by __id=1&value=null__%, "
                      "compared to the last __id=1&time_interval=7__ days average "
                      "of __id=2&value=null__ __id=2&metric_name=UNIQUE_CLICKS&metric_type=1&antecedent_type=11__. "
                      "This means your audience saw the ads too many times or your ad creative doesn't resonate "
                      "with current selected audience. Dexter recommends you to change the ad creative now.",
             breakdown_metadata=BreakdownMetadataBase(breakdown=FacebookBreakdownEnum.NONE,
                                                      action_breakdown=FacebookActionBreakdownEnum.NONE),
             time_interval=DaysEnum.SEVEN,
             connective=Connective(LogicOperatorEnum.AND),
             antecedents=[
                 Antecedent(aid=1,
                            atype=AntecedentTypeEnum.FUZZY_TREND,
                            metric=FacebookAvailableSingleMetricEnum.UNIQUE_CLICKS.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=FacebookLinguisticVariableEnum.DECREASING),
                 Antecedent(aid=2,
                            atype=AntecedentTypeEnum.VARIANCE,
                            metric=FacebookAvailableSingleMetricEnum.UNIQUE_CLICKS.value,
                            operator=LogicOperatorEnum.EQUAL_OR_GREATER_THAN,
                            expected_value=20)
             ]),
    RuleBase(rtype=FacebookRuleTypeEnum.BUDGET_AND_BID,
             channel=ChannelEnum.FACEBOOK,
             category=FacebookRuleCategoryEnum.IMPROVE_CPR,
             importance=FacebookRuleImportanceEnum.HIGH,
             source=FacebookRuleSourceEnum.DEXTER,
             level=LevelEnum.AD,
             action=FacebookActionEnum.NONE,
             redirect=FacebookRuleRedirectEnum.EDIT_STRUCTURE,
             template="Dexter noticed that your __id=1&metric_name=UNIQUE_CLICKS&metric_type=1&antecedent_type=8__ "
                      "decreased by __id=1&value=null__%, "
                      "compared to the last __id=1&time_interval=14__ days average "
                      "of __id=2&value=null__ __id=2&metric_name=UNIQUE_CLICKS&metric_type=1&antecedent_type=11__. "
                      "This means your audience saw the ads too many times or your ad creative doesn't resonate "
                      "with current selected audience. Dexter recommends you to change the ad creative now.",
             breakdown_metadata=BreakdownMetadataBase(breakdown=FacebookBreakdownEnum.NONE,
                                                      action_breakdown=FacebookActionBreakdownEnum.NONE),
             time_interval=DaysEnum.FOURTEEN,
             connective=Connective(LogicOperatorEnum.AND),
             antecedents=[
                 Antecedent(aid=1,
                            atype=AntecedentTypeEnum.FUZZY_TREND,
                            metric=FacebookAvailableSingleMetricEnum.UNIQUE_CLICKS.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=FacebookLinguisticVariableEnum.DECREASING),
                 Antecedent(aid=2,
                            atype=AntecedentTypeEnum.VARIANCE,
                            metric=FacebookAvailableSingleMetricEnum.UNIQUE_CLICKS.value,
                            operator=LogicOperatorEnum.EQUAL_OR_GREATER_THAN,
                            expected_value=15)
             ]),
    RuleBase(rtype=FacebookRuleTypeEnum.BUDGET_AND_BID,
             channel=ChannelEnum.FACEBOOK,
             category=FacebookRuleCategoryEnum.IMPROVE_CPR,
             importance=FacebookRuleImportanceEnum.HIGH,
             source=FacebookRuleSourceEnum.DEXTER,
             level=LevelEnum.AD,
             action=FacebookActionEnum.NONE,
             redirect=FacebookRuleRedirectEnum.EDIT_STRUCTURE,
             template="Dexter noticed that your __id=1&metric_name=UNIQUE_CLICKS&metric_type=1&antecedent_type=8__ "
                      "decreased by __id=1&value=null__%, "
                      "compared to the last __id=1&time_interval=30__ days average "
                      "of __id=2&value=null__ __id=2&metric_name=UNIQUE_CLICKS&metric_type=1&antecedent_type=11__. "
                      "This means your audience saw the ads too many times or your ad creative doesn't resonate "
                      "with current selected audience. Dexter recommends you to change the ad creative now.",
             breakdown_metadata=BreakdownMetadataBase(breakdown=FacebookBreakdownEnum.NONE,
                                                      action_breakdown=FacebookActionBreakdownEnum.NONE),
             time_interval=DaysEnum.MONTH,
             connective=Connective(LogicOperatorEnum.AND),
             antecedents=[
                 Antecedent(aid=1,
                            atype=AntecedentTypeEnum.FUZZY_TREND,
                            metric=FacebookAvailableSingleMetricEnum.UNIQUE_CLICKS.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=FacebookLinguisticVariableEnum.DECREASING),
                 Antecedent(aid=2,
                            atype=AntecedentTypeEnum.VARIANCE,
                            metric=FacebookAvailableSingleMetricEnum.UNIQUE_CLICKS.value,
                            operator=LogicOperatorEnum.EQUAL_OR_GREATER_THAN,
                            expected_value=10)
             ]),
    RuleBase(rtype=FacebookRuleTypeEnum.BUDGET_AND_BID,
             channel=ChannelEnum.FACEBOOK,
             category=FacebookRuleCategoryEnum.IMPROVE_CPR,
             importance=FacebookRuleImportanceEnum.HIGH,
             source=FacebookRuleSourceEnum.DEXTER,
             level=LevelEnum.AD,
             action=FacebookActionEnum.NONE,
             redirect=FacebookRuleRedirectEnum.EDIT_STRUCTURE,
             template="Dexter noticed that your __id=1&metric_name=CPC&metric_type=1&antecedent_type=8__ "
                      "increased by __id=1&value=null__%, "
                      "compared to the last __id=1&time_interval=3__ days average "
                      "of __id=2&value=null__ __id=2&metric_name=CPC&metric_type=1&antecedent_type=11__. "
                      "This means either you have a low relevance score or you have an audience overlap, "
                      "so you're bidding against yourself. Let's first improve the ad creative to rise the "
                      "relevance score. Try to match your ad message and landing page with current selected audence.",
             breakdown_metadata=BreakdownMetadataBase(breakdown=FacebookBreakdownEnum.NONE,
                                                      action_breakdown=FacebookActionBreakdownEnum.NONE),
             time_interval=DaysEnum.THREE,
             connective=Connective(LogicOperatorEnum.AND),
             antecedents=[
                 Antecedent(aid=1,
                            atype=AntecedentTypeEnum.FUZZY_TREND,
                            metric=FacebookAvailableSingleMetricEnum.CPC.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=FacebookLinguisticVariableEnum.INCREASING),
                 Antecedent(aid=2,
                            atype=AntecedentTypeEnum.VARIANCE,
                            metric=FacebookAvailableSingleMetricEnum.CPC.value,
                            operator=LogicOperatorEnum.EQUAL_OR_GREATER_THAN,
                            expected_value=20)
             ]),
    RuleBase(rtype=FacebookRuleTypeEnum.BUDGET_AND_BID,
             channel=ChannelEnum.FACEBOOK,
             category=FacebookRuleCategoryEnum.IMPROVE_CPR,
             importance=FacebookRuleImportanceEnum.HIGH,
             source=FacebookRuleSourceEnum.DEXTER,
             level=LevelEnum.AD,
             action=FacebookActionEnum.NONE,
             redirect=FacebookRuleRedirectEnum.EDIT_STRUCTURE,
             template="Dexter noticed that your __id=1&metric_name=CPC&metric_type=1&antecedent_type=8__ "
                      "increased by __id=1&value=null__%, "
                      "compared to the last __id=1&time_interval=7__ days average "
                      "of __id=2&value=null__ __id=2&metric_name=CPC&metric_type=1&antecedent_type=11__. "
                      "This means either you have a low relevance score or you have an audience overlap, "
                      "so you're bidding against yourself. Let's first improve the ad creative to rise the "
                      "relevance score. Try to match your ad message and landing page with current selected audence.",
             breakdown_metadata=BreakdownMetadataBase(breakdown=FacebookBreakdownEnum.NONE,
                                                      action_breakdown=FacebookActionBreakdownEnum.NONE),
             time_interval=DaysEnum.SEVEN,
             connective=Connective(LogicOperatorEnum.AND),
             antecedents=[
                 Antecedent(aid=1,
                            atype=AntecedentTypeEnum.FUZZY_TREND,
                            metric=FacebookAvailableSingleMetricEnum.CPC.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=FacebookLinguisticVariableEnum.INCREASING),
                 Antecedent(aid=2,
                            atype=AntecedentTypeEnum.VARIANCE,
                            metric=FacebookAvailableSingleMetricEnum.CPC.value,
                            operator=LogicOperatorEnum.EQUAL_OR_GREATER_THAN,
                            expected_value=15)
             ]),
    RuleBase(rtype=FacebookRuleTypeEnum.BUDGET_AND_BID,
             channel=ChannelEnum.FACEBOOK,
             category=FacebookRuleCategoryEnum.IMPROVE_CPR,
             importance=FacebookRuleImportanceEnum.HIGH,
             source=FacebookRuleSourceEnum.DEXTER,
             level=LevelEnum.AD,
             action=FacebookActionEnum.NONE,
             redirect=FacebookRuleRedirectEnum.EDIT_STRUCTURE,
             template="Dexter noticed that your __id=1&metric_name=CPC&metric_type=1&antecedent_type=8__ "
                      "increased by __id=1&value=null__%, "
                      "compared to the last __id=1&time_interval=14__ days average "
                      "of __id=2&value=null__ __id=2&metric_name=CPC&metric_type=1&antecedent_type=11__. "
                      "This means either you have a low relevance score or you have an audience overlap, "
                      "so you're bidding against yourself. Let's first improve the ad creative to rise the "
                      "relevance score. Try to match your ad message and landing page with current selected audence.",
             breakdown_metadata=BreakdownMetadataBase(breakdown=FacebookBreakdownEnum.NONE,
                                                      action_breakdown=FacebookActionBreakdownEnum.NONE),
             time_interval=DaysEnum.FOURTEEN,
             connective=Connective(LogicOperatorEnum.AND),
             antecedents=[
                 Antecedent(aid=1,
                            atype=AntecedentTypeEnum.FUZZY_TREND,
                            metric=FacebookAvailableSingleMetricEnum.CPC.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=FacebookLinguisticVariableEnum.INCREASING),
                 Antecedent(aid=2,
                            atype=AntecedentTypeEnum.VARIANCE,
                            metric=FacebookAvailableSingleMetricEnum.CPC.value,
                            operator=LogicOperatorEnum.EQUAL_OR_GREATER_THAN,
                            expected_value=10)
             ]),
    RuleBase(rtype=FacebookRuleTypeEnum.BUDGET_AND_BID,
             channel=ChannelEnum.FACEBOOK,
             category=FacebookRuleCategoryEnum.IMPROVE_CPR,
             importance=FacebookRuleImportanceEnum.HIGH,
             source=FacebookRuleSourceEnum.DEXTER,
             level=LevelEnum.AD,
             action=FacebookActionEnum.NONE,
             redirect=FacebookRuleRedirectEnum.EDIT_STRUCTURE,
             template="Dexter noticed that your __id=1&metric_name=CPC&metric_type=1&antecedent_type=8__ "
                      "increased by __id=1&value=null__%, "
                      "compared to the last __id=1&time_interval=30__ days average "
                      "of __id=2&value=null__ __id=2&metric_name=CPC&metric_type=1&antecedent_type=11__. "
                      "This means either you have a low relevance score or you have an audience overlap, "
                      "so you're bidding against yourself. Let's first improve the ad creative to rise the "
                      "relevance score. Try to match your ad message and landing page with current selected audence.",
             breakdown_metadata=BreakdownMetadataBase(breakdown=FacebookBreakdownEnum.NONE,
                                                      action_breakdown=FacebookActionBreakdownEnum.NONE),
             time_interval=DaysEnum.MONTH,
             connective=Connective(LogicOperatorEnum.AND),
             antecedents=[
                 Antecedent(aid=1,
                            atype=AntecedentTypeEnum.FUZZY_TREND,
                            metric=FacebookAvailableSingleMetricEnum.CPC.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=FacebookLinguisticVariableEnum.INCREASING),
                 Antecedent(aid=2,
                            atype=AntecedentTypeEnum.VARIANCE,
                            metric=FacebookAvailableSingleMetricEnum.CPC.value,
                            operator=LogicOperatorEnum.EQUAL_OR_GREATER_THAN,
                            expected_value=10)
             ]),
    RuleBase(rtype=FacebookRuleTypeEnum.BUDGET_AND_BID,
             channel=ChannelEnum.FACEBOOK,
             category=FacebookRuleCategoryEnum.IMPROVE_CPR,
             importance=FacebookRuleImportanceEnum.HIGH,
             source=FacebookRuleSourceEnum.DEXTER,
             level=LevelEnum.AD,
             action=FacebookActionEnum.NONE,
             redirect=FacebookRuleRedirectEnum.EDIT_STRUCTURE,
             template="Dexter noticed that your __id=1&metric_name=FREQUENCY&metric_type=1&antecedent_type=8__ "
                      "increased by __id=1&value=null__%, "
                      "compared to the last __id=1&time_interval=3__ days average "
                      "of __id=2&value=null__ __id=2&metric_name=FREQUENCY&metric_type=1&antecedent_type=11__. "
                      "A high frequency will decrease the CTR and increase the CPC. "
                      "Consider increasing your audience or change the Ad creative now.",
             breakdown_metadata=BreakdownMetadataBase(breakdown=FacebookBreakdownEnum.NONE,
                                                      action_breakdown=FacebookActionBreakdownEnum.NONE),
             time_interval=DaysEnum.THREE,
             connective=Connective(LogicOperatorEnum.AND),
             antecedents=[
                 Antecedent(aid=1,
                            atype=AntecedentTypeEnum.FUZZY_TREND,
                            metric=FacebookAvailableSingleMetricEnum.FREQUENCY.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=FacebookLinguisticVariableEnum.INCREASING),
                 Antecedent(aid=2,
                            atype=AntecedentTypeEnum.VARIANCE,
                            metric=FacebookAvailableSingleMetricEnum.FREQUENCY.value,
                            operator=LogicOperatorEnum.EQUAL_OR_GREATER_THAN,
                            expected_value=20)
             ]),
    RuleBase(rtype=FacebookRuleTypeEnum.BUDGET_AND_BID,
             channel=ChannelEnum.FACEBOOK,
             category=FacebookRuleCategoryEnum.IMPROVE_CPR,
             importance=FacebookRuleImportanceEnum.HIGH,
             source=FacebookRuleSourceEnum.DEXTER,
             level=LevelEnum.AD,
             action=FacebookActionEnum.NONE,
             redirect=FacebookRuleRedirectEnum.EDIT_STRUCTURE,
             template="Dexter noticed that your __id=1&metric_name=FREQUENCY&metric_type=1&antecedent_type=8__ "
                      "increased by __id=1&value=null__%, "
                      "compared to the last __id=1&time_interval=7__ days average "
                      "of __id=2&value=null__ __id=2&metric_name=FREQUENCY&metric_type=1&antecedent_type=11__. "
                      "A high frequency will decrease the CTR and increase the CPC. "
                      "Consider increasing your audience or change the Ad creative now.",
             breakdown_metadata=BreakdownMetadataBase(breakdown=FacebookBreakdownEnum.NONE,
                                                      action_breakdown=FacebookActionBreakdownEnum.NONE),
             time_interval=DaysEnum.SEVEN,
             connective=Connective(LogicOperatorEnum.AND),
             antecedents=[
                 Antecedent(aid=1,
                            atype=AntecedentTypeEnum.FUZZY_TREND,
                            metric=FacebookAvailableSingleMetricEnum.FREQUENCY.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=FacebookLinguisticVariableEnum.INCREASING),
                 Antecedent(aid=2,
                            atype=AntecedentTypeEnum.VARIANCE,
                            metric=FacebookAvailableSingleMetricEnum.FREQUENCY.value,
                            operator=LogicOperatorEnum.EQUAL_OR_GREATER_THAN,
                            expected_value=15)
             ]),
    RuleBase(rtype=FacebookRuleTypeEnum.BUDGET_AND_BID,
             channel=ChannelEnum.FACEBOOK,
             category=FacebookRuleCategoryEnum.IMPROVE_CPR,
             importance=FacebookRuleImportanceEnum.HIGH,
             source=FacebookRuleSourceEnum.DEXTER,
             level=LevelEnum.AD,
             action=FacebookActionEnum.NONE,
             redirect=FacebookRuleRedirectEnum.EDIT_STRUCTURE,
             template="Dexter noticed that your __id=1&metric_name=FREQUENCY&metric_type=1&antecedent_type=8__ "
                      "increased by __id=1&value=null__%, "
                      "compared to the last __id=1&time_interval=14__ days average "
                      "of __id=2&value=null__ __id=2&metric_name=FREQUENCY&metric_type=1&antecedent_type=11__. "
                      "A high frequency will decrease the CTR and increase the CPC. "
                      "Consider increasing your audience or change the Ad creative now.",
             breakdown_metadata=BreakdownMetadataBase(breakdown=FacebookBreakdownEnum.NONE,
                                                      action_breakdown=FacebookActionBreakdownEnum.NONE),
             time_interval=DaysEnum.FOURTEEN,
             connective=Connective(LogicOperatorEnum.AND),
             antecedents=[
                 Antecedent(aid=1,
                            atype=AntecedentTypeEnum.FUZZY_TREND,
                            metric=FacebookAvailableSingleMetricEnum.FREQUENCY.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=FacebookLinguisticVariableEnum.INCREASING),
                 Antecedent(aid=2,
                            atype=AntecedentTypeEnum.VARIANCE,
                            metric=FacebookAvailableSingleMetricEnum.FREQUENCY.value,
                            operator=LogicOperatorEnum.EQUAL_OR_GREATER_THAN,
                            expected_value=10)
             ]),
    RuleBase(rtype=FacebookRuleTypeEnum.BUDGET_AND_BID,
             channel=ChannelEnum.FACEBOOK,
             category=FacebookRuleCategoryEnum.IMPROVE_CPR,
             importance=FacebookRuleImportanceEnum.HIGH,
             source=FacebookRuleSourceEnum.DEXTER,
             level=LevelEnum.AD,
             action=FacebookActionEnum.NONE,
             redirect=FacebookRuleRedirectEnum.EDIT_STRUCTURE,
             template="Dexter noticed that your __id=1&metric_name=FREQUENCY&metric_type=1&antecedent_type=8__ "
                      "increased by __id=1&value=null__%, "
                      "compared to the last __id=1&time_interval=30__ days average "
                      "of __id=2&value=null__ __id=2&metric_name=FREQUENCY&metric_type=1&antecedent_type=11__. "
                      "A high frequency will decrease the CTR and increase the CPC. "
                      "Consider increasing your audience or change the Ad creative now.",
             breakdown_metadata=BreakdownMetadataBase(breakdown=FacebookBreakdownEnum.NONE,
                                                      action_breakdown=FacebookActionBreakdownEnum.NONE),
             time_interval=DaysEnum.MONTH,
             connective=Connective(LogicOperatorEnum.AND),
             antecedents=[
                 Antecedent(aid=1,
                            atype=AntecedentTypeEnum.FUZZY_TREND,
                            metric=FacebookAvailableSingleMetricEnum.FREQUENCY.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=FacebookLinguisticVariableEnum.INCREASING),
                 Antecedent(aid=2,
                            atype=AntecedentTypeEnum.VARIANCE,
                            metric=FacebookAvailableSingleMetricEnum.FREQUENCY.value,
                            operator=LogicOperatorEnum.EQUAL_OR_GREATER_THAN,
                            expected_value=10)
             ]),
    RuleBase(rtype=FacebookRuleTypeEnum.BUDGET_AND_BID,
             channel=ChannelEnum.FACEBOOK,
             category=FacebookRuleCategoryEnum.IMPROVE_CPR,
             importance=FacebookRuleImportanceEnum.LOW,
             source=FacebookRuleSourceEnum.DEXTER,
             level=LevelEnum.AD,
             action=FacebookActionEnum.NONE,
             redirect=FacebookRuleRedirectEnum.EDIT_STRUCTURE,
             template="Dexter noticed that your __id=1&metric_name=SPEND&metric_type=1&antecedent_type=8__ "
                      "increased by __id=1&value=null__%, "
                      "compared to the last __id=1&time_interval=3__ days average "
                      "of __id=2&value=null__ __id=2&metric_name=SPEND&metric_type=1&antecedent_type=11__. "
                      "There are several reasons why this happened. See more details.",
             breakdown_metadata=BreakdownMetadataBase(breakdown=FacebookBreakdownEnum.NONE,
                                                      action_breakdown=FacebookActionBreakdownEnum.NONE),
             time_interval=DaysEnum.THREE,
             connective=Connective(LogicOperatorEnum.AND),
             antecedents=[
                 Antecedent(aid=1,
                            atype=AntecedentTypeEnum.FUZZY_TREND,
                            metric=FacebookAvailableSingleMetricEnum.SPEND.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=FacebookLinguisticVariableEnum.INCREASING),
                 Antecedent(aid=2,
                            atype=AntecedentTypeEnum.VARIANCE,
                            metric=FacebookAvailableSingleMetricEnum.SPEND.value,
                            operator=LogicOperatorEnum.EQUAL_OR_GREATER_THAN,
                            expected_value=15)
             ]),
    RuleBase(rtype=FacebookRuleTypeEnum.BUDGET_AND_BID,
             channel=ChannelEnum.FACEBOOK,
             category=FacebookRuleCategoryEnum.IMPROVE_CPR,
             importance=FacebookRuleImportanceEnum.LOW,
             source=FacebookRuleSourceEnum.DEXTER,
             level=LevelEnum.AD,
             action=FacebookActionEnum.NONE,
             redirect=FacebookRuleRedirectEnum.EDIT_STRUCTURE,
             template="Dexter noticed that your __id=1&metric_name=SPEND&metric_type=1&antecedent_type=8__ "
                      "increased by __id=1&value=null__%, "
                      "compared to the last __id=1&time_interval=7__ days average "
                      "of __id=2&value=null__ __id=2&metric_name=SPEND&metric_type=1&antecedent_type=11__. "
                      "There are several reasons why this happened. See more details.",
             breakdown_metadata=BreakdownMetadataBase(breakdown=FacebookBreakdownEnum.NONE,
                                                      action_breakdown=FacebookActionBreakdownEnum.NONE),
             time_interval=DaysEnum.SEVEN,
             connective=Connective(LogicOperatorEnum.AND),
             antecedents=[
                 Antecedent(aid=1,
                            atype=AntecedentTypeEnum.FUZZY_TREND,
                            metric=FacebookAvailableSingleMetricEnum.SPEND.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=FacebookLinguisticVariableEnum.INCREASING),
                 Antecedent(aid=2,
                            atype=AntecedentTypeEnum.VARIANCE,
                            metric=FacebookAvailableSingleMetricEnum.SPEND.value,
                            operator=LogicOperatorEnum.EQUAL_OR_GREATER_THAN,
                            expected_value=15)
             ]),
    RuleBase(rtype=FacebookRuleTypeEnum.BUDGET_AND_BID,
             channel=ChannelEnum.FACEBOOK,
             category=FacebookRuleCategoryEnum.IMPROVE_CPR,
             importance=FacebookRuleImportanceEnum.LOW,
             source=FacebookRuleSourceEnum.DEXTER,
             level=LevelEnum.AD,
             action=FacebookActionEnum.NONE,
             redirect=FacebookRuleRedirectEnum.EDIT_STRUCTURE,
             template="Dexter noticed that your __id=1&metric_name=SPEND&metric_type=1&antecedent_type=8__ "
                      "increased by __id=1&value=null__%, "
                      "compared to the last __id=1&time_interval=14__ days average "
                      "of __id=2&value=null__ __id=2&metric_name=SPEND&metric_type=1&antecedent_type=11__. "
                      "There are several reasons why this happened. See more details.",
             breakdown_metadata=BreakdownMetadataBase(breakdown=FacebookBreakdownEnum.NONE,
                                                      action_breakdown=FacebookActionBreakdownEnum.NONE),
             time_interval=DaysEnum.FOURTEEN,
             connective=Connective(LogicOperatorEnum.AND),
             antecedents=[
                 Antecedent(aid=1,
                            atype=AntecedentTypeEnum.FUZZY_TREND,
                            metric=FacebookAvailableSingleMetricEnum.SPEND.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=FacebookLinguisticVariableEnum.INCREASING),
                 Antecedent(aid=2,
                            atype=AntecedentTypeEnum.VARIANCE,
                            metric=FacebookAvailableSingleMetricEnum.SPEND.value,
                            operator=LogicOperatorEnum.EQUAL_OR_GREATER_THAN,
                            expected_value=15)
             ]),
    RuleBase(rtype=FacebookRuleTypeEnum.BUDGET_AND_BID,
             channel=ChannelEnum.FACEBOOK,
             category=FacebookRuleCategoryEnum.IMPROVE_CPR,
             importance=FacebookRuleImportanceEnum.LOW,
             source=FacebookRuleSourceEnum.DEXTER,
             level=LevelEnum.AD,
             action=FacebookActionEnum.NONE,
             redirect=FacebookRuleRedirectEnum.EDIT_STRUCTURE,
             template="Dexter noticed that your __id=1&metric_name=SPEND&metric_type=1&antecedent_type=8__ "
                      "increased by __id=1&value=null__%, "
                      "compared to the last __id=1&time_interval=30__ days average "
                      "of __id=2&value=null__ __id=2&metric_name=SPEND&metric_type=1&antecedent_type=11__. "
                      "There are several reasons why this happened. See more details.",
             breakdown_metadata=BreakdownMetadataBase(breakdown=FacebookBreakdownEnum.NONE,
                                                      action_breakdown=FacebookActionBreakdownEnum.NONE),
             time_interval=DaysEnum.MONTH,
             connective=Connective(LogicOperatorEnum.AND),
             antecedents=[
                 Antecedent(aid=1,
                            atype=AntecedentTypeEnum.FUZZY_TREND,
                            metric=FacebookAvailableSingleMetricEnum.SPEND.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=FacebookLinguisticVariableEnum.INCREASING),
                 Antecedent(aid=2,
                            atype=AntecedentTypeEnum.VARIANCE,
                            metric=FacebookAvailableSingleMetricEnum.SPEND.value,
                            operator=LogicOperatorEnum.EQUAL_OR_GREATER_THAN,
                            expected_value=10)
             ]),
    RuleBase(rtype=FacebookRuleTypeEnum.BUDGET_AND_BID,
             channel=ChannelEnum.FACEBOOK,
             category=FacebookRuleCategoryEnum.IMPROVE_CPR,
             importance=FacebookRuleImportanceEnum.LOW,
             source=FacebookRuleSourceEnum.DEXTER,
             level=LevelEnum.AD,
             action=FacebookActionEnum.NONE,
             redirect=FacebookRuleRedirectEnum.EDIT_STRUCTURE,
             template="Dexter noticed that your __id=1&metric_name=SPEND&metric_type=1&antecedent_type=8__ "
                      "decreased by __id=1&value=null__%, "
                      "compared to the last __id=1&time_interval=3__ days average "
                      "of __id=2&value=null__ __id=2&metric_name=SPEND&metric_type=1&antecedent_type=11__. "
                      "There are several reasons why this happened. See more details.",
             breakdown_metadata=BreakdownMetadataBase(breakdown=FacebookBreakdownEnum.NONE,
                                                      action_breakdown=FacebookActionBreakdownEnum.NONE),
             time_interval=DaysEnum.THREE,
             connective=Connective(LogicOperatorEnum.AND),
             antecedents=[
                 Antecedent(aid=1,
                            atype=AntecedentTypeEnum.FUZZY_TREND,
                            metric=FacebookAvailableSingleMetricEnum.SPEND.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=FacebookLinguisticVariableEnum.DECREASING),
                 Antecedent(aid=2,
                            atype=AntecedentTypeEnum.VARIANCE,
                            metric=FacebookAvailableSingleMetricEnum.SPEND.value,
                            operator=LogicOperatorEnum.EQUAL_OR_GREATER_THAN,
                            expected_value=15)
             ]),
    RuleBase(rtype=FacebookRuleTypeEnum.BUDGET_AND_BID,
             channel=ChannelEnum.FACEBOOK,
             category=FacebookRuleCategoryEnum.IMPROVE_CPR,
             importance=FacebookRuleImportanceEnum.LOW,
             source=FacebookRuleSourceEnum.DEXTER,
             level=LevelEnum.AD,
             action=FacebookActionEnum.NONE,
             redirect=FacebookRuleRedirectEnum.EDIT_STRUCTURE,
             template="Dexter noticed that your __id=1&metric_name=SPEND&metric_type=1&antecedent_type=8__ "
                      "decreased by __id=1&value=null__%, "
                      "compared to the last __id=1&time_interval=7__ days average "
                      "of __id=2&value=null__ __id=2&metric_name=SPEND&metric_type=1&antecedent_type=11__. "
                      "There are several reasons why this happened. See more details.",
             breakdown_metadata=BreakdownMetadataBase(breakdown=FacebookBreakdownEnum.NONE,
                                                      action_breakdown=FacebookActionBreakdownEnum.NONE),
             time_interval=DaysEnum.SEVEN,
             connective=Connective(LogicOperatorEnum.AND),
             antecedents=[
                 Antecedent(aid=1,
                            atype=AntecedentTypeEnum.FUZZY_TREND,
                            metric=FacebookAvailableSingleMetricEnum.SPEND.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=FacebookLinguisticVariableEnum.DECREASING),
                 Antecedent(aid=2,
                            atype=AntecedentTypeEnum.VARIANCE,
                            metric=FacebookAvailableSingleMetricEnum.SPEND.value,
                            operator=LogicOperatorEnum.EQUAL_OR_GREATER_THAN,
                            expected_value=15)
             ]),
    RuleBase(rtype=FacebookRuleTypeEnum.BUDGET_AND_BID,
             channel=ChannelEnum.FACEBOOK,
             category=FacebookRuleCategoryEnum.IMPROVE_CPR,
             importance=FacebookRuleImportanceEnum.LOW,
             source=FacebookRuleSourceEnum.DEXTER,
             level=LevelEnum.AD,
             action=FacebookActionEnum.NONE,
             redirect=FacebookRuleRedirectEnum.EDIT_STRUCTURE,
             template="Dexter noticed that your __id=1&metric_name=SPEND&metric_type=1&antecedent_type=8__ "
                      "decreased by __id=1&value=null__%, "
                      "compared to the last __id=1&time_interval=14__ days average "
                      "of __id=2&value=null__ __id=2&metric_name=SPEND&metric_type=1&antecedent_type=11__. "
                      "There are several reasons why this happened. See more details.",
             breakdown_metadata=BreakdownMetadataBase(breakdown=FacebookBreakdownEnum.NONE,
                                                      action_breakdown=FacebookActionBreakdownEnum.NONE),
             time_interval=DaysEnum.FOURTEEN,
             connective=Connective(LogicOperatorEnum.AND),
             antecedents=[
                 Antecedent(aid=1,
                            atype=AntecedentTypeEnum.FUZZY_TREND,
                            metric=FacebookAvailableSingleMetricEnum.SPEND.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=FacebookLinguisticVariableEnum.DECREASING),
                 Antecedent(aid=2,
                            atype=AntecedentTypeEnum.VARIANCE,
                            metric=FacebookAvailableSingleMetricEnum.SPEND.value,
                            operator=LogicOperatorEnum.EQUAL_OR_GREATER_THAN,
                            expected_value=15)
             ]),
    RuleBase(rtype=FacebookRuleTypeEnum.BUDGET_AND_BID,
             channel=ChannelEnum.FACEBOOK,
             category=FacebookRuleCategoryEnum.IMPROVE_CPR,
             importance=FacebookRuleImportanceEnum.LOW,
             source=FacebookRuleSourceEnum.DEXTER,
             level=LevelEnum.AD,
             action=FacebookActionEnum.NONE,
             redirect=FacebookRuleRedirectEnum.EDIT_STRUCTURE,
             template="Dexter noticed that your __id=1&metric_name=SPEND&metric_type=1&antecedent_type=8__ "
                      "decreased by __id=1&value=null__%, "
                      "compared to the last __id=1&time_interval=30__ days average "
                      "of __id=2&value=null__ __id=2&metric_name=SPEND&metric_type=1&antecedent_type=11__. "
                      "There are several reasons why this happened. See more details.",
             breakdown_metadata=BreakdownMetadataBase(breakdown=FacebookBreakdownEnum.NONE,
                                                      action_breakdown=FacebookActionBreakdownEnum.NONE),
             time_interval=DaysEnum.MONTH,
             connective=Connective(LogicOperatorEnum.AND),
             antecedents=[
                 Antecedent(aid=1,
                            atype=AntecedentTypeEnum.FUZZY_TREND,
                            metric=FacebookAvailableSingleMetricEnum.SPEND.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=FacebookLinguisticVariableEnum.DECREASING),
                 Antecedent(aid=2,
                            atype=AntecedentTypeEnum.VARIANCE,
                            metric=FacebookAvailableSingleMetricEnum.SPEND.value,
                            operator=LogicOperatorEnum.EQUAL_OR_GREATER_THAN,
                            expected_value=10)
             ]),
    RuleBase(rtype=FacebookRuleTypeEnum.BUDGET_AND_BID,
             channel=ChannelEnum.FACEBOOK,
             category=FacebookRuleCategoryEnum.IMPROVE_CPR,
             importance=FacebookRuleImportanceEnum.HIGH,
             source=FacebookRuleSourceEnum.DEXTER,
             level=LevelEnum.AD,
             action=FacebookActionEnum.NONE,
             redirect=FacebookRuleRedirectEnum.EDIT_STRUCTURE,
             template="Dexter noticed that your __id=1&metric_name=ROAS&metric_type=1&antecedent_type=8__ "
                      "decreased by __id=1&value=null__%, "
                      "compared to the last __id=1&time_interval=3__ days average "
                      "of __id=2&value=null__ __id=2&metric_name=ROAS&metric_type=1&antecedent_type=11__. "
                      "This means either your CPC increased or the average order value has decreased. "
                      "Let's decrease the CPC by increasing the quality ranking. Change your ad creative now.",
             breakdown_metadata=BreakdownMetadataBase(breakdown=FacebookBreakdownEnum.NONE,
                                                      action_breakdown=FacebookActionBreakdownEnum.NONE),
             time_interval=DaysEnum.THREE,
             connective=Connective(LogicOperatorEnum.AND),
             antecedents=[
                 Antecedent(aid=1,
                            atype=AntecedentTypeEnum.FUZZY_TREND,
                            metric=FacebookAvailableSingleMetricEnum.ROAS.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=FacebookLinguisticVariableEnum.DECREASING),
                 Antecedent(aid=2,
                            atype=AntecedentTypeEnum.VARIANCE,
                            metric=FacebookAvailableSingleMetricEnum.ROAS.value,
                            operator=LogicOperatorEnum.EQUAL_OR_GREATER_THAN,
                            expected_value=20)
             ]),
    RuleBase(rtype=FacebookRuleTypeEnum.BUDGET_AND_BID,
             channel=ChannelEnum.FACEBOOK,
             category=FacebookRuleCategoryEnum.IMPROVE_CPR,
             importance=FacebookRuleImportanceEnum.HIGH,
             source=FacebookRuleSourceEnum.DEXTER,
             level=LevelEnum.AD,
             action=FacebookActionEnum.NONE,
             redirect=FacebookRuleRedirectEnum.EDIT_STRUCTURE,
             template="Dexter noticed that your __id=1&metric_name=ROAS&metric_type=1&antecedent_type=8__ "
                      "decreased by __id=1&value=null__%, "
                      "compared to the last __id=1&time_interval=7__ days average "
                      "of __id=2&value=null__ __id=2&metric_name=ROAS&metric_type=1&antecedent_type=11__. "
                      "This means either your CPC increased or the average order value has decreased. "
                      "Let's decrease the CPC by increasing the quality ranking. Change your ad creative now.",
             breakdown_metadata=BreakdownMetadataBase(breakdown=FacebookBreakdownEnum.NONE,
                                                      action_breakdown=FacebookActionBreakdownEnum.NONE),
             time_interval=DaysEnum.SEVEN,
             connective=Connective(LogicOperatorEnum.AND),
             antecedents=[
                 Antecedent(aid=1,
                            atype=AntecedentTypeEnum.FUZZY_TREND,
                            metric=FacebookAvailableSingleMetricEnum.ROAS.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=FacebookLinguisticVariableEnum.DECREASING),
                 Antecedent(aid=2,
                            atype=AntecedentTypeEnum.VARIANCE,
                            metric=FacebookAvailableSingleMetricEnum.ROAS.value,
                            operator=LogicOperatorEnum.EQUAL_OR_GREATER_THAN,
                            expected_value=15)
             ]),
    RuleBase(rtype=FacebookRuleTypeEnum.BUDGET_AND_BID,
             channel=ChannelEnum.FACEBOOK,
             category=FacebookRuleCategoryEnum.IMPROVE_CPR,
             importance=FacebookRuleImportanceEnum.HIGH,
             source=FacebookRuleSourceEnum.DEXTER,
             level=LevelEnum.AD,
             action=FacebookActionEnum.NONE,
             redirect=FacebookRuleRedirectEnum.EDIT_STRUCTURE,
             template="Dexter noticed that your __id=1&metric_name=ROAS&metric_type=1&antecedent_type=8__ "
                      "decreased by __id=1&value=null__%, "
                      "compared to the last __id=1&time_interval=14__ days average "
                      "of __id=2&value=null__ __id=2&metric_name=ROAS&metric_type=1&antecedent_type=11__. "
                      "This means either your CPC increased or the average order value has decreased. "
                      "Let's decrease the CPC by increasing the quality ranking. Change your ad creative now.",
             breakdown_metadata=BreakdownMetadataBase(breakdown=FacebookBreakdownEnum.NONE,
                                                      action_breakdown=FacebookActionBreakdownEnum.NONE),
             time_interval=DaysEnum.FOURTEEN,
             connective=Connective(LogicOperatorEnum.AND),
             antecedents=[
                 Antecedent(aid=1,
                            atype=AntecedentTypeEnum.FUZZY_TREND,
                            metric=FacebookAvailableSingleMetricEnum.ROAS.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=FacebookLinguisticVariableEnum.DECREASING),
                 Antecedent(aid=2,
                            atype=AntecedentTypeEnum.VARIANCE,
                            metric=FacebookAvailableSingleMetricEnum.ROAS.value,
                            operator=LogicOperatorEnum.EQUAL_OR_GREATER_THAN,
                            expected_value=10)
             ]),
    RuleBase(rtype=FacebookRuleTypeEnum.BUDGET_AND_BID,
             channel=ChannelEnum.FACEBOOK,
             category=FacebookRuleCategoryEnum.IMPROVE_CPR,
             importance=FacebookRuleImportanceEnum.HIGH,
             source=FacebookRuleSourceEnum.DEXTER,
             level=LevelEnum.AD,
             action=FacebookActionEnum.NONE,
             redirect=FacebookRuleRedirectEnum.EDIT_STRUCTURE,
             template="Dexter noticed that your __id=1&metric_name=ROAS&metric_type=1&antecedent_type=8__ "
                      "decreased by __id=1&value=null__%, "
                      "compared to the last __id=1&time_interval=30__ days average "
                      "of __id=2&value=null__ __id=2&metric_name=ROAS&metric_type=1&antecedent_type=11__. "
                      "This means either your CPC increased or the average order value has decreased. "
                      "Let's decrease the CPC by increasing the quality ranking. Change your ad creative now.",
             breakdown_metadata=BreakdownMetadataBase(breakdown=FacebookBreakdownEnum.NONE,
                                                      action_breakdown=FacebookActionBreakdownEnum.NONE),
             time_interval=DaysEnum.MONTH,
             connective=Connective(LogicOperatorEnum.AND),
             antecedents=[
                 Antecedent(aid=1,
                            atype=AntecedentTypeEnum.FUZZY_TREND,
                            metric=FacebookAvailableSingleMetricEnum.ROAS.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=FacebookLinguisticVariableEnum.DECREASING),
                 Antecedent(aid=2,
                            atype=AntecedentTypeEnum.VARIANCE,
                            metric=FacebookAvailableSingleMetricEnum.ROAS.value,
                            operator=LogicOperatorEnum.EQUAL_OR_GREATER_THAN,
                            expected_value=10)
             ]),
    RuleBase(rtype=FacebookRuleTypeEnum.BUDGET_AND_BID,
             channel=ChannelEnum.FACEBOOK,
             category=FacebookRuleCategoryEnum.IMPROVE_CPR,
             importance=FacebookRuleImportanceEnum.HIGH,
             source=FacebookRuleSourceEnum.DEXTER,
             level=LevelEnum.AD,
             action=FacebookActionEnum.NONE,
             redirect=FacebookRuleRedirectEnum.EDIT_STRUCTURE,
             template="Dexter noticed that your __id=1&metric_name=LANDING_PAGE_CONVERSION_RATE&metric_type=1&antecedent_type=8__ "
                      "decreased by __id=1&value=null__%, "
                      "compared to the last __id=1&time_interval=3__ days average "
                      "of __id=2&value=null__ __id=2&metric_name=LANDING_PAGE_CONVERSION_RATE&metric_type=1&antecedent_type=11__. "
                      "This means your Landing Page has some issues or your ad creative doesn't "
                      "resonate with the Landing Page. Change your ad creative now. ",
             breakdown_metadata=BreakdownMetadataBase(breakdown=FacebookBreakdownEnum.NONE,
                                                      action_breakdown=FacebookActionBreakdownEnum.NONE),
             time_interval=DaysEnum.THREE,
             connective=Connective(LogicOperatorEnum.AND),
             antecedents=[
                 Antecedent(aid=1,
                            atype=AntecedentTypeEnum.FUZZY_TREND,
                            metric=FacebookAvailableSingleMetricEnum.LANDING_PAGE_CONVERSION_RATE.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=FacebookLinguisticVariableEnum.DECREASING),
                 Antecedent(aid=2,
                            atype=AntecedentTypeEnum.VARIANCE,
                            metric=FacebookAvailableSingleMetricEnum.LANDING_PAGE_CONVERSION_RATE.value,
                            operator=LogicOperatorEnum.EQUAL_OR_GREATER_THAN,
                            expected_value=20)
             ]),
    RuleBase(rtype=FacebookRuleTypeEnum.BUDGET_AND_BID,
             channel=ChannelEnum.FACEBOOK,
             category=FacebookRuleCategoryEnum.IMPROVE_CPR,
             importance=FacebookRuleImportanceEnum.HIGH,
             source=FacebookRuleSourceEnum.DEXTER,
             level=LevelEnum.AD,
             action=FacebookActionEnum.NONE,
             redirect=FacebookRuleRedirectEnum.EDIT_STRUCTURE,
             template="Dexter noticed that your __id=1&metric_name=LANDING_PAGE_CONVERSION_RATE&metric_type=1&antecedent_type=8__ "
                      "decreased by __id=1&value=null__%, "
                      "compared to the last __id=1&time_interval=7__ days average "
                      "of __id=2&value=null__ __id=2&metric_name=LANDING_PAGE_CONVERSION_RATE&metric_type=1&antecedent_type=11__. "
                      "This means your Landing Page has some issues or your ad creative doesn't "
                      "resonate with the Landing Page. Change your ad creative now. ",
             breakdown_metadata=BreakdownMetadataBase(breakdown=FacebookBreakdownEnum.NONE,
                                                      action_breakdown=FacebookActionBreakdownEnum.NONE),
             time_interval=DaysEnum.SEVEN,
             connective=Connective(LogicOperatorEnum.AND),
             antecedents=[
                 Antecedent(aid=1,
                            atype=AntecedentTypeEnum.FUZZY_TREND,
                            metric=FacebookAvailableSingleMetricEnum.LANDING_PAGE_CONVERSION_RATE.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=FacebookLinguisticVariableEnum.DECREASING),
                 Antecedent(aid=2,
                            atype=AntecedentTypeEnum.VARIANCE,
                            metric=FacebookAvailableSingleMetricEnum.LANDING_PAGE_CONVERSION_RATE.value,
                            operator=LogicOperatorEnum.EQUAL_OR_GREATER_THAN,
                            expected_value=15)
             ]),
    RuleBase(rtype=FacebookRuleTypeEnum.BUDGET_AND_BID,
             channel=ChannelEnum.FACEBOOK,
             category=FacebookRuleCategoryEnum.IMPROVE_CPR,
             importance=FacebookRuleImportanceEnum.HIGH,
             source=FacebookRuleSourceEnum.DEXTER,
             level=LevelEnum.AD,
             action=FacebookActionEnum.NONE,
             redirect=FacebookRuleRedirectEnum.EDIT_STRUCTURE,
             template="Dexter noticed that your __id=1&metric_name=LANDING_PAGE_CONVERSION_RATE&metric_type=1&antecedent_type=8__ "
                      "decreased by __id=1&value=null__%, "
                      "compared to the last __id=1&time_interval=14__ days average "
                      "of __id=2&value=null__ __id=2&metric_name=LANDING_PAGE_CONVERSION_RATE&metric_type=1&antecedent_type=11__. "
                      "This means your Landing Page has some issues or your ad creative doesn't "
                      "resonate with the Landing Page. Change your ad creative now. ",
             breakdown_metadata=BreakdownMetadataBase(breakdown=FacebookBreakdownEnum.NONE,
                                                      action_breakdown=FacebookActionBreakdownEnum.NONE),
             time_interval=DaysEnum.FOURTEEN,
             connective=Connective(LogicOperatorEnum.AND),
             antecedents=[
                 Antecedent(aid=1,
                            atype=AntecedentTypeEnum.FUZZY_TREND,
                            metric=FacebookAvailableSingleMetricEnum.LANDING_PAGE_CONVERSION_RATE.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=FacebookLinguisticVariableEnum.DECREASING),
                 Antecedent(aid=2,
                            atype=AntecedentTypeEnum.VARIANCE,
                            metric=FacebookAvailableSingleMetricEnum.LANDING_PAGE_CONVERSION_RATE.value,
                            operator=LogicOperatorEnum.EQUAL_OR_GREATER_THAN,
                            expected_value=10)
             ]),
    RuleBase(rtype=FacebookRuleTypeEnum.BUDGET_AND_BID,
             channel=ChannelEnum.FACEBOOK,
             category=FacebookRuleCategoryEnum.IMPROVE_CPR,
             importance=FacebookRuleImportanceEnum.HIGH,
             source=FacebookRuleSourceEnum.DEXTER,
             level=LevelEnum.AD,
             action=FacebookActionEnum.NONE,
             redirect=FacebookRuleRedirectEnum.EDIT_STRUCTURE,
             template="Dexter noticed that your __id=1&metric_name=LANDING_PAGE_CONVERSION_RATE&metric_type=1&antecedent_type=8__ "
                      "decreased by __id=1&value=null__%, "
                      "compared to the last __id=1&time_interval=30__ days average "
                      "of __id=2&value=null__ __id=2&metric_name=LANDING_PAGE_CONVERSION_RATE&metric_type=1&antecedent_type=11__. "
                      "This means your Landing Page has some issues or your ad creative doesn't "
                      "resonate with the Landing Page. Change your ad creative now. ",
             breakdown_metadata=BreakdownMetadataBase(breakdown=FacebookBreakdownEnum.NONE,
                                                      action_breakdown=FacebookActionBreakdownEnum.NONE),
             time_interval=DaysEnum.MONTH,
             connective=Connective(LogicOperatorEnum.AND),
             antecedents=[
                 Antecedent(aid=1,
                            atype=AntecedentTypeEnum.FUZZY_TREND,
                            metric=FacebookAvailableSingleMetricEnum.LANDING_PAGE_CONVERSION_RATE.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=FacebookLinguisticVariableEnum.DECREASING),
                 Antecedent(aid=2,
                            atype=AntecedentTypeEnum.VARIANCE,
                            metric=FacebookAvailableSingleMetricEnum.LANDING_PAGE_CONVERSION_RATE.value,
                            operator=LogicOperatorEnum.EQUAL_OR_GREATER_THAN,
                            expected_value=10)
             ]),
    RuleBase(rtype=FacebookRuleTypeEnum.BUDGET_AND_BID,
             channel=ChannelEnum.FACEBOOK,
             category=FacebookRuleCategoryEnum.IMPROVE_CPR,
             importance=FacebookRuleImportanceEnum.LOW,
             source=FacebookRuleSourceEnum.DEXTER,
             level=LevelEnum.AD,
             action=FacebookActionEnum.NONE,
             redirect=FacebookRuleRedirectEnum.EDIT_STRUCTURE,
             template="Dexter noticed that your __id=1&metric_name=THRUPLAYS&metric_type=1&antecedent_type=8__ "
                      "decreased by __id=1&value=null__%, "
                      "compared to the last __id=1&time_interval=3__ days average "
                      "of __id=2&value=null__ __id=2&metric_name=THRUPLAYS&metric_type=1&antecedent_type=11__. "
                      "This means your audience saw the video/s too many times or your video content "
                      "doesn't resonate with current selected audience. "
                      "Check your ads now to see which one is the less performing.",
             breakdown_metadata=BreakdownMetadataBase(breakdown=FacebookBreakdownEnum.NONE,
                                                      action_breakdown=FacebookActionBreakdownEnum.NONE),
             time_interval=DaysEnum.THREE,
             connective=Connective(LogicOperatorEnum.AND),
             antecedents=[
                 Antecedent(aid=1,
                            atype=AntecedentTypeEnum.FUZZY_TREND,
                            metric=FacebookAvailableSingleMetricEnum.THRUPLAYS.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=FacebookLinguisticVariableEnum.DECREASING),
                 Antecedent(aid=2,
                            atype=AntecedentTypeEnum.VARIANCE,
                            metric=FacebookAvailableSingleMetricEnum.THRUPLAYS.value,
                            operator=LogicOperatorEnum.EQUAL_OR_GREATER_THAN,
                            expected_value=20)
             ]),
    RuleBase(rtype=FacebookRuleTypeEnum.BUDGET_AND_BID,
             channel=ChannelEnum.FACEBOOK,
             category=FacebookRuleCategoryEnum.IMPROVE_CPR,
             importance=FacebookRuleImportanceEnum.LOW,
             source=FacebookRuleSourceEnum.DEXTER,
             level=LevelEnum.AD,
             action=FacebookActionEnum.NONE,
             redirect=FacebookRuleRedirectEnum.EDIT_STRUCTURE,
             template="Dexter noticed that your __id=1&metric_name=THRUPLAYS&metric_type=1&antecedent_type=8__ "
                      "decreased by __id=1&value=null__%, "
                      "compared to the last __id=1&time_interval=7__ days average "
                      "of __id=2&value=null__ __id=2&metric_name=THRUPLAYS&metric_type=1&antecedent_type=11__. "
                      "This means your audience saw the video/s too many times or your video content "
                      "doesn't resonate with current selected audience. "
                      "Check your ads now to see which one is the less performing.",
             breakdown_metadata=BreakdownMetadataBase(breakdown=FacebookBreakdownEnum.NONE,
                                                      action_breakdown=FacebookActionBreakdownEnum.NONE),
             time_interval=DaysEnum.SEVEN,
             connective=Connective(LogicOperatorEnum.AND),
             antecedents=[
                 Antecedent(aid=1,
                            atype=AntecedentTypeEnum.FUZZY_TREND,
                            metric=FacebookAvailableSingleMetricEnum.THRUPLAYS.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=FacebookLinguisticVariableEnum.DECREASING),
                 Antecedent(aid=2,
                            atype=AntecedentTypeEnum.VARIANCE,
                            metric=FacebookAvailableSingleMetricEnum.THRUPLAYS.value,
                            operator=LogicOperatorEnum.EQUAL_OR_GREATER_THAN,
                            expected_value=15)
             ]),
    RuleBase(rtype=FacebookRuleTypeEnum.BUDGET_AND_BID,
             channel=ChannelEnum.FACEBOOK,
             category=FacebookRuleCategoryEnum.IMPROVE_CPR,
             importance=FacebookRuleImportanceEnum.LOW,
             source=FacebookRuleSourceEnum.DEXTER,
             level=LevelEnum.AD,
             action=FacebookActionEnum.NONE,
             redirect=FacebookRuleRedirectEnum.EDIT_STRUCTURE,
             template="Dexter noticed that your __id=1&metric_name=THRUPLAYS&metric_type=1&antecedent_type=8__ "
                      "decreased by __id=1&value=null__%, "
                      "compared to the last __id=1&time_interval=14__ days average "
                      "of __id=2&value=null__ __id=2&metric_name=THRUPLAYS&metric_type=1&antecedent_type=11__. "
                      "This means your audience saw the video/s too many times or your video content "
                      "doesn't resonate with current selected audience. "
                      "Check your ads now to see which one is the less performing.",
             breakdown_metadata=BreakdownMetadataBase(breakdown=FacebookBreakdownEnum.NONE,
                                                      action_breakdown=FacebookActionBreakdownEnum.NONE),
             time_interval=DaysEnum.FOURTEEN,
             connective=Connective(LogicOperatorEnum.AND),
             antecedents=[
                 Antecedent(aid=1,
                            atype=AntecedentTypeEnum.FUZZY_TREND,
                            metric=FacebookAvailableSingleMetricEnum.THRUPLAYS.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=FacebookLinguisticVariableEnum.DECREASING),
                 Antecedent(aid=2,
                            atype=AntecedentTypeEnum.VARIANCE,
                            metric=FacebookAvailableSingleMetricEnum.THRUPLAYS.value,
                            operator=LogicOperatorEnum.EQUAL_OR_GREATER_THAN,
                            expected_value=10)
             ]),
    RuleBase(rtype=FacebookRuleTypeEnum.BUDGET_AND_BID,
             channel=ChannelEnum.FACEBOOK,
             category=FacebookRuleCategoryEnum.IMPROVE_CPR,
             importance=FacebookRuleImportanceEnum.LOW,
             source=FacebookRuleSourceEnum.DEXTER,
             level=LevelEnum.AD,
             action=FacebookActionEnum.NONE,
             redirect=FacebookRuleRedirectEnum.EDIT_STRUCTURE,
             template="Dexter noticed that your __id=1&metric_name=THRUPLAYS&metric_type=1&antecedent_type=8__ "
                      "decreased by __id=1&value=null__%, "
                      "compared to the last __id=1&time_interval=30__ days average "
                      "of __id=2&value=null__ __id=2&metric_name=THRUPLAYS&metric_type=1&antecedent_type=11__. "
                      "This means your audience saw the video/s too many times or your video content "
                      "doesn't resonate with current selected audience. "
                      "Check your ads now to see which one is the less performing.",
             breakdown_metadata=BreakdownMetadataBase(breakdown=FacebookBreakdownEnum.NONE,
                                                      action_breakdown=FacebookActionBreakdownEnum.NONE),
             time_interval=DaysEnum.MONTH,
             connective=Connective(LogicOperatorEnum.AND),
             antecedents=[
                 Antecedent(aid=1,
                            atype=AntecedentTypeEnum.FUZZY_TREND,
                            metric=FacebookAvailableSingleMetricEnum.THRUPLAYS.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=FacebookLinguisticVariableEnum.DECREASING),
                 Antecedent(aid=2,
                            atype=AntecedentTypeEnum.VARIANCE,
                            metric=FacebookAvailableSingleMetricEnum.THRUPLAYS.value,
                            operator=LogicOperatorEnum.EQUAL_OR_GREATER_THAN,
                            expected_value=10)
             ]),
    RuleBase(rtype=FacebookRuleTypeEnum.BUDGET_AND_BID,
             channel=ChannelEnum.FACEBOOK,
             category=FacebookRuleCategoryEnum.IMPROVE_CPR,
             importance=FacebookRuleImportanceEnum.HIGH,
             source=FacebookRuleSourceEnum.DEXTER,
             level=LevelEnum.AD,
             action=FacebookActionEnum.NONE,
             redirect=FacebookRuleRedirectEnum.EDIT_STRUCTURE,
             template="Dexter noticed that your __id=1&metric_name=COST_PER_THRUPLAY&metric_type=1&antecedent_type=8__ "
                      "increased by __id=1&value=null__%, "
                      "compared to the last __id=1&time_interval=3__ days average "
                      "of __id=2&value=null__ __id=2&metric_name=COST_PER_THRUPLAY&metric_type=1&antecedent_type=11__. "
                      "Try to get more thruplays by modifying the video's content. "
                      "Check your ads now to see which one is the less performing.",
             breakdown_metadata=BreakdownMetadataBase(breakdown=FacebookBreakdownEnum.NONE,
                                                      action_breakdown=FacebookActionBreakdownEnum.NONE),
             time_interval=DaysEnum.THREE,
             connective=Connective(LogicOperatorEnum.AND),
             antecedents=[
                 Antecedent(aid=1,
                            atype=AntecedentTypeEnum.FUZZY_TREND,
                            metric=FacebookAvailableSingleMetricEnum.COST_PER_THRUPLAY.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=FacebookLinguisticVariableEnum.INCREASING),
                 Antecedent(aid=2,
                            atype=AntecedentTypeEnum.VARIANCE,
                            metric=FacebookAvailableSingleMetricEnum.COST_PER_THRUPLAY.value,
                            operator=LogicOperatorEnum.EQUAL_OR_GREATER_THAN,
                            expected_value=20)
             ]),
    RuleBase(rtype=FacebookRuleTypeEnum.BUDGET_AND_BID,
             channel=ChannelEnum.FACEBOOK,
             category=FacebookRuleCategoryEnum.IMPROVE_CPR,
             importance=FacebookRuleImportanceEnum.HIGH,
             source=FacebookRuleSourceEnum.DEXTER,
             level=LevelEnum.AD,
             action=FacebookActionEnum.NONE,
             redirect=FacebookRuleRedirectEnum.EDIT_STRUCTURE,
             template="Dexter noticed that your __id=1&metric_name=COST_PER_THRUPLAY&metric_type=1&antecedent_type=8__ "
                      "increased by __id=1&value=null__%, "
                      "compared to the last __id=1&time_interval=7__ days average "
                      "of __id=2&value=null__ __id=2&metric_name=COST_PER_THRUPLAY&metric_type=1&antecedent_type=11__. "
                      "Try to get more thruplays by modifying the video's content. "
                      "Check your ads now to see which one is the less performing.",
             breakdown_metadata=BreakdownMetadataBase(breakdown=FacebookBreakdownEnum.NONE,
                                                      action_breakdown=FacebookActionBreakdownEnum.NONE),
             time_interval=DaysEnum.SEVEN,
             connective=Connective(LogicOperatorEnum.AND),
             antecedents=[
                 Antecedent(aid=1,
                            atype=AntecedentTypeEnum.FUZZY_TREND,
                            metric=FacebookAvailableSingleMetricEnum.COST_PER_THRUPLAY.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=FacebookLinguisticVariableEnum.INCREASING),
                 Antecedent(aid=2,
                            atype=AntecedentTypeEnum.VARIANCE,
                            metric=FacebookAvailableSingleMetricEnum.COST_PER_THRUPLAY.value,
                            operator=LogicOperatorEnum.EQUAL_OR_GREATER_THAN,
                            expected_value=15)
             ]),
    RuleBase(rtype=FacebookRuleTypeEnum.BUDGET_AND_BID,
             channel=ChannelEnum.FACEBOOK,
             category=FacebookRuleCategoryEnum.IMPROVE_CPR,
             importance=FacebookRuleImportanceEnum.HIGH,
             source=FacebookRuleSourceEnum.DEXTER,
             level=LevelEnum.AD,
             action=FacebookActionEnum.NONE,
             redirect=FacebookRuleRedirectEnum.EDIT_STRUCTURE,
             template="Dexter noticed that your __id=1&metric_name=COST_PER_THRUPLAY&metric_type=1&antecedent_type=8__ "
                      "increased by __id=1&value=null__%, "
                      "compared to the last __id=1&time_interval=14__ days average "
                      "of __id=2&value=null__ __id=2&metric_name=COST_PER_THRUPLAY&metric_type=1&antecedent_type=11__. "
                      "Try to get more thruplays by modifying the video's content. "
                      "Check your ads now to see which one is the less performing.",
             breakdown_metadata=BreakdownMetadataBase(breakdown=FacebookBreakdownEnum.NONE,
                                                      action_breakdown=FacebookActionBreakdownEnum.NONE),
             time_interval=DaysEnum.FOURTEEN,
             connective=Connective(LogicOperatorEnum.AND),
             antecedents=[
                 Antecedent(aid=1,
                            atype=AntecedentTypeEnum.FUZZY_TREND,
                            metric=FacebookAvailableSingleMetricEnum.COST_PER_THRUPLAY.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=FacebookLinguisticVariableEnum.INCREASING),
                 Antecedent(aid=2,
                            atype=AntecedentTypeEnum.VARIANCE,
                            metric=FacebookAvailableSingleMetricEnum.COST_PER_THRUPLAY.value,
                            operator=LogicOperatorEnum.EQUAL_OR_GREATER_THAN,
                            expected_value=10)
             ]),
    RuleBase(rtype=FacebookRuleTypeEnum.BUDGET_AND_BID,
             channel=ChannelEnum.FACEBOOK,
             category=FacebookRuleCategoryEnum.IMPROVE_CPR,
             importance=FacebookRuleImportanceEnum.HIGH,
             source=FacebookRuleSourceEnum.DEXTER,
             level=LevelEnum.AD,
             action=FacebookActionEnum.NONE,
             redirect=FacebookRuleRedirectEnum.EDIT_STRUCTURE,
             template="Dexter noticed that your __id=1&metric_name=COST_PER_THRUPLAY&metric_type=1&antecedent_type=8__ "
                      "increased by __id=1&value=null__%, "
                      "compared to the last __id=1&time_interval=30__ days average "
                      "of __id=2&value=null__ __id=2&metric_name=COST_PER_THRUPLAY&metric_type=1&antecedent_type=11__. "
                      "Try to get more thruplays by modifying the video's content. "
                      "Check your ads now to see which one is the less performing.",
             breakdown_metadata=BreakdownMetadataBase(breakdown=FacebookBreakdownEnum.NONE,
                                                      action_breakdown=FacebookActionBreakdownEnum.NONE),
             time_interval=DaysEnum.MONTH,
             connective=Connective(LogicOperatorEnum.AND),
             antecedents=[
                 Antecedent(aid=1,
                            atype=AntecedentTypeEnum.FUZZY_TREND,
                            metric=FacebookAvailableSingleMetricEnum.COST_PER_THRUPLAY.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=FacebookLinguisticVariableEnum.INCREASING),
                 Antecedent(aid=2,
                            atype=AntecedentTypeEnum.VARIANCE,
                            metric=FacebookAvailableSingleMetricEnum.COST_PER_THRUPLAY.value,
                            operator=LogicOperatorEnum.EQUAL_OR_GREATER_THAN,
                            expected_value=10)
             ]),
    RuleBase(rtype=FacebookRuleTypeEnum.BUDGET_AND_BID,
             channel=ChannelEnum.FACEBOOK,
             category=FacebookRuleCategoryEnum.IMPROVE_CPR,
             importance=FacebookRuleImportanceEnum.HIGH,
             source=FacebookRuleSourceEnum.DEXTER,
             level=LevelEnum.AD,
             action=FacebookActionEnum.NONE,
             redirect=FacebookRuleRedirectEnum.EDIT_STRUCTURE,
             template="Dexter noticed that your __id=1&metric_name=CONVERSIONS&metric_type=1&antecedent_type=8__ "
                      "decreased by __id=1&value=null__%, "
                      "compared to the last __id=1&time_interval=3__ days average "
                      "of __id=2&value=null__ __id=2&metric_name=CONVERSIONS&metric_type=1&antecedent_type=11__. "
                      "Let people engage more by changing the ad creative now. Change your ad creative now.",
             breakdown_metadata=BreakdownMetadataBase(breakdown=FacebookBreakdownEnum.NONE,
                                                      action_breakdown=FacebookActionBreakdownEnum.NONE),
             time_interval=DaysEnum.THREE,
             connective=Connective(LogicOperatorEnum.AND),
             antecedents=[
                 Antecedent(aid=1,
                            atype=AntecedentTypeEnum.FUZZY_TREND,
                            metric=FacebookAvailableSingleMetricEnum.CONVERSIONS.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=FacebookLinguisticVariableEnum.DECREASING),
                 Antecedent(aid=2,
                            atype=AntecedentTypeEnum.VARIANCE,
                            metric=FacebookAvailableSingleMetricEnum.CONVERSIONS.value,
                            operator=LogicOperatorEnum.EQUAL_OR_GREATER_THAN,
                            expected_value=25)
             ]),
    RuleBase(rtype=FacebookRuleTypeEnum.BUDGET_AND_BID,
             channel=ChannelEnum.FACEBOOK,
             category=FacebookRuleCategoryEnum.IMPROVE_CPR,
             importance=FacebookRuleImportanceEnum.HIGH,
             source=FacebookRuleSourceEnum.DEXTER,
             level=LevelEnum.AD,
             action=FacebookActionEnum.NONE,
             redirect=FacebookRuleRedirectEnum.EDIT_STRUCTURE,
             template="Dexter noticed that your __id=1&metric_name=CONVERSIONS&metric_type=1&antecedent_type=8__ "
                      "decreased by __id=1&value=null__%, "
                      "compared to the last __id=1&time_interval=7__ days average "
                      "of __id=2&value=null__ __id=2&metric_name=CONVERSIONS&metric_type=1&antecedent_type=11__. "
                      "Let people engage more by changing the ad creative now. Change your ad creative now.",
             breakdown_metadata=BreakdownMetadataBase(breakdown=FacebookBreakdownEnum.NONE,
                                                      action_breakdown=FacebookActionBreakdownEnum.NONE),
             time_interval=DaysEnum.SEVEN,
             connective=Connective(LogicOperatorEnum.AND),
             antecedents=[
                 Antecedent(aid=1,
                            atype=AntecedentTypeEnum.FUZZY_TREND,
                            metric=FacebookAvailableSingleMetricEnum.CONVERSIONS.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=FacebookLinguisticVariableEnum.DECREASING),
                 Antecedent(aid=2,
                            atype=AntecedentTypeEnum.VARIANCE,
                            metric=FacebookAvailableSingleMetricEnum.CONVERSIONS.value,
                            operator=LogicOperatorEnum.EQUAL_OR_GREATER_THAN,
                            expected_value=20)
             ]),
    RuleBase(rtype=FacebookRuleTypeEnum.BUDGET_AND_BID,
             channel=ChannelEnum.FACEBOOK,
             category=FacebookRuleCategoryEnum.IMPROVE_CPR,
             importance=FacebookRuleImportanceEnum.HIGH,
             source=FacebookRuleSourceEnum.DEXTER,
             level=LevelEnum.AD,
             action=FacebookActionEnum.NONE,
             redirect=FacebookRuleRedirectEnum.EDIT_STRUCTURE,
             template="Dexter noticed that your __id=1&metric_name=CONVERSIONS&metric_type=1&antecedent_type=8__ "
                      "decreased by __id=1&value=null__%, "
                      "compared to the last __id=1&time_interval=14__ days average "
                      "of __id=2&value=null__ __id=2&metric_name=CONVERSIONS&metric_type=1&antecedent_type=11__. "
                      "Let people engage more by changing the ad creative now. Change your ad creative now.",
             breakdown_metadata=BreakdownMetadataBase(breakdown=FacebookBreakdownEnum.NONE,
                                                      action_breakdown=FacebookActionBreakdownEnum.NONE),
             time_interval=DaysEnum.FOURTEEN,
             connective=Connective(LogicOperatorEnum.AND),
             antecedents=[
                 Antecedent(aid=1,
                            atype=AntecedentTypeEnum.FUZZY_TREND,
                            metric=FacebookAvailableSingleMetricEnum.CONVERSIONS.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=FacebookLinguisticVariableEnum.DECREASING),
                 Antecedent(aid=2,
                            atype=AntecedentTypeEnum.VARIANCE,
                            metric=FacebookAvailableSingleMetricEnum.CONVERSIONS.value,
                            operator=LogicOperatorEnum.EQUAL_OR_GREATER_THAN,
                            expected_value=15)
             ]),
    RuleBase(rtype=FacebookRuleTypeEnum.BUDGET_AND_BID,
             channel=ChannelEnum.FACEBOOK,
             category=FacebookRuleCategoryEnum.IMPROVE_CPR,
             importance=FacebookRuleImportanceEnum.HIGH,
             source=FacebookRuleSourceEnum.DEXTER,
             level=LevelEnum.AD,
             action=FacebookActionEnum.NONE,
             redirect=FacebookRuleRedirectEnum.EDIT_STRUCTURE,
             template="Dexter noticed that your __id=1&metric_name=CONVERSIONS&metric_type=1&antecedent_type=8__ "
                      "decreased by __id=1&value=null__%, "
                      "compared to the last __id=1&time_interval=30__ days average "
                      "of __id=2&value=null__ __id=2&metric_name=CONVERSIONS&metric_type=1&antecedent_type=11__. "
                      "Let people engage more by changing the ad creative now. Change your ad creative now.",
             breakdown_metadata=BreakdownMetadataBase(breakdown=FacebookBreakdownEnum.NONE,
                                                      action_breakdown=FacebookActionBreakdownEnum.NONE),
             time_interval=DaysEnum.MONTH,
             connective=Connective(LogicOperatorEnum.AND),
             antecedents=[
                 Antecedent(aid=1,
                            atype=AntecedentTypeEnum.FUZZY_TREND,
                            metric=FacebookAvailableSingleMetricEnum.CONVERSIONS.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=FacebookLinguisticVariableEnum.DECREASING),
                 Antecedent(aid=2,
                            atype=AntecedentTypeEnum.VARIANCE,
                            metric=FacebookAvailableSingleMetricEnum.CONVERSIONS.value,
                            operator=LogicOperatorEnum.EQUAL_OR_GREATER_THAN,
                            expected_value=10)
             ]),
    RuleBase(rtype=FacebookRuleTypeEnum.BUDGET_AND_BID,
             channel=ChannelEnum.FACEBOOK,
             category=FacebookRuleCategoryEnum.IMPROVE_CPR,
             importance=FacebookRuleImportanceEnum.HIGH,
             source=FacebookRuleSourceEnum.DEXTER,
             level=LevelEnum.AD,
             action=FacebookActionEnum.NONE,
             redirect=FacebookRuleRedirectEnum.EDIT_STRUCTURE,
             template="Dexter noticed that your __id=1&metric_name=PURCHASES&metric_type=1&antecedent_type=8__ "
                      "decreased by __id=1&value=null__%, "
                      "compared to the last __id=1&time_interval=3__ days average "
                      "of __id=2&value=null__ __id=2&metric_name=PURCHASES&metric_type=1&antecedent_type=11__. "
                      "Let people engage more by changing the ad creative now. Change your ad creative now.",
             breakdown_metadata=BreakdownMetadataBase(breakdown=FacebookBreakdownEnum.NONE,
                                                      action_breakdown=FacebookActionBreakdownEnum.NONE),
             time_interval=DaysEnum.THREE,
             connective=Connective(LogicOperatorEnum.AND),
             antecedents=[
                 Antecedent(aid=1,
                            atype=AntecedentTypeEnum.FUZZY_TREND,
                            metric=FacebookAvailableSingleMetricEnum.PURCHASES.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=FacebookLinguisticVariableEnum.DECREASING),
                 Antecedent(aid=2,
                            atype=AntecedentTypeEnum.VARIANCE,
                            metric=FacebookAvailableSingleMetricEnum.PURCHASES.value,
                            operator=LogicOperatorEnum.EQUAL_OR_GREATER_THAN,
                            expected_value=25)
             ]),
    RuleBase(rtype=FacebookRuleTypeEnum.BUDGET_AND_BID,
             channel=ChannelEnum.FACEBOOK,
             category=FacebookRuleCategoryEnum.IMPROVE_CPR,
             importance=FacebookRuleImportanceEnum.HIGH,
             source=FacebookRuleSourceEnum.DEXTER,
             level=LevelEnum.AD,
             action=FacebookActionEnum.NONE,
             redirect=FacebookRuleRedirectEnum.EDIT_STRUCTURE,
             template="Dexter noticed that your __id=1&metric_name=PURCHASES&metric_type=1&antecedent_type=8__ "
                      "decreased by __id=1&value=null__%, "
                      "compared to the last __id=1&time_interval=7__ days average "
                      "of __id=2&value=null__ __id=2&metric_name=PURCHASES&metric_type=1&antecedent_type=11__. "
                      "Let people engage more by changing the ad creative now. Change your ad creative now.",
             breakdown_metadata=BreakdownMetadataBase(breakdown=FacebookBreakdownEnum.NONE,
                                                      action_breakdown=FacebookActionBreakdownEnum.NONE),
             time_interval=DaysEnum.SEVEN,
             connective=Connective(LogicOperatorEnum.AND),
             antecedents=[
                 Antecedent(aid=1,
                            atype=AntecedentTypeEnum.FUZZY_TREND,
                            metric=FacebookAvailableSingleMetricEnum.PURCHASES.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=FacebookLinguisticVariableEnum.DECREASING),
                 Antecedent(aid=2,
                            atype=AntecedentTypeEnum.VARIANCE,
                            metric=FacebookAvailableSingleMetricEnum.PURCHASES.value,
                            operator=LogicOperatorEnum.EQUAL_OR_GREATER_THAN,
                            expected_value=20)
             ]),
    RuleBase(rtype=FacebookRuleTypeEnum.BUDGET_AND_BID,
             channel=ChannelEnum.FACEBOOK,
             category=FacebookRuleCategoryEnum.IMPROVE_CPR,
             importance=FacebookRuleImportanceEnum.HIGH,
             source=FacebookRuleSourceEnum.DEXTER,
             level=LevelEnum.AD,
             action=FacebookActionEnum.NONE,
             redirect=FacebookRuleRedirectEnum.EDIT_STRUCTURE,
             template="Dexter noticed that your __id=1&metric_name=PURCHASES&metric_type=1&antecedent_type=8__ "
                      "decreased by __id=1&value=null__%, "
                      "compared to the last __id=1&time_interval=14__ days average "
                      "of __id=2&value=null__ __id=2&metric_name=PURCHASES&metric_type=1&antecedent_type=11__. "
                      "Let people engage more by changing the ad creative now. Change your ad creative now.",
             breakdown_metadata=BreakdownMetadataBase(breakdown=FacebookBreakdownEnum.NONE,
                                                      action_breakdown=FacebookActionBreakdownEnum.NONE),
             time_interval=DaysEnum.FOURTEEN,
             connective=Connective(LogicOperatorEnum.AND),
             antecedents=[
                 Antecedent(aid=1,
                            atype=AntecedentTypeEnum.FUZZY_TREND,
                            metric=FacebookAvailableSingleMetricEnum.PURCHASES.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=FacebookLinguisticVariableEnum.DECREASING),
                 Antecedent(aid=2,
                            atype=AntecedentTypeEnum.VARIANCE,
                            metric=FacebookAvailableSingleMetricEnum.PURCHASES.value,
                            operator=LogicOperatorEnum.EQUAL_OR_GREATER_THAN,
                            expected_value=15)
             ]),
    RuleBase(rtype=FacebookRuleTypeEnum.BUDGET_AND_BID,
             channel=ChannelEnum.FACEBOOK,
             category=FacebookRuleCategoryEnum.IMPROVE_CPR,
             importance=FacebookRuleImportanceEnum.HIGH,
             source=FacebookRuleSourceEnum.DEXTER,
             level=LevelEnum.AD,
             action=FacebookActionEnum.NONE,
             redirect=FacebookRuleRedirectEnum.EDIT_STRUCTURE,
             template="Dexter noticed that your __id=1&metric_name=PURCHASES&metric_type=1&antecedent_type=8__ "
                      "decreased by __id=1&value=null__%, "
                      "compared to the last __id=1&time_interval=30__ days average "
                      "of __id=2&value=null__ __id=2&metric_name=PURCHASES&metric_type=1&antecedent_type=11__. "
                      "Let people engage more by changing the ad creative now. Change your ad creative now.",
             breakdown_metadata=BreakdownMetadataBase(breakdown=FacebookBreakdownEnum.NONE,
                                                      action_breakdown=FacebookActionBreakdownEnum.NONE),
             time_interval=DaysEnum.MONTH,
             connective=Connective(LogicOperatorEnum.AND),
             antecedents=[
                 Antecedent(aid=1,
                            atype=AntecedentTypeEnum.FUZZY_TREND,
                            metric=FacebookAvailableSingleMetricEnum.PURCHASES.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=FacebookLinguisticVariableEnum.DECREASING),
                 Antecedent(aid=2,
                            atype=AntecedentTypeEnum.VARIANCE,
                            metric=FacebookAvailableSingleMetricEnum.PURCHASES.value,
                            operator=LogicOperatorEnum.EQUAL_OR_GREATER_THAN,
                            expected_value=10)
             ]),
    RuleBase(rtype=FacebookRuleTypeEnum.BUDGET_AND_BID,
             channel=ChannelEnum.FACEBOOK,
             category=FacebookRuleCategoryEnum.IMPROVE_CPR,
             importance=FacebookRuleImportanceEnum.HIGH,
             source=FacebookRuleSourceEnum.DEXTER,
             level=LevelEnum.AD,
             action=FacebookActionEnum.NONE,
             redirect=FacebookRuleRedirectEnum.EDIT_STRUCTURE,
             template="Dexter noticed that your __id=1&metric_name=COST_PER_PURCHASE&metric_type=1&antecedent_type=8__ "
                      "increased by __id=1&value=null__%, "
                      "compared to the last __id=1&time_interval=3__ days average "
                      "of __id=2&value=null__ __id=2&metric_name=COST_PER_PURCHASE&metric_type=1&antecedent_type=11__. "
                      "This means your Link Clicks decreased and less people made a purchase. Try to get more "
                      "clicks by writing more compelling messages that match your "
                      "audience's interests. Change your ad creative now. ",
             breakdown_metadata=BreakdownMetadataBase(breakdown=FacebookBreakdownEnum.NONE,
                                                      action_breakdown=FacebookActionBreakdownEnum.NONE),
             time_interval=DaysEnum.THREE,
             connective=Connective(LogicOperatorEnum.AND),
             antecedents=[
                 Antecedent(aid=1,
                            atype=AntecedentTypeEnum.FUZZY_TREND,
                            metric=FacebookAvailableSingleMetricEnum.COST_PER_PURCHASE.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=FacebookLinguisticVariableEnum.INCREASING),
                 Antecedent(aid=2,
                            atype=AntecedentTypeEnum.VARIANCE,
                            metric=FacebookAvailableSingleMetricEnum.COST_PER_PURCHASE.value,
                            operator=LogicOperatorEnum.EQUAL_OR_GREATER_THAN,
                            expected_value=20)
             ]),
    RuleBase(rtype=FacebookRuleTypeEnum.BUDGET_AND_BID,
             channel=ChannelEnum.FACEBOOK,
             category=FacebookRuleCategoryEnum.IMPROVE_CPR,
             importance=FacebookRuleImportanceEnum.HIGH,
             source=FacebookRuleSourceEnum.DEXTER,
             level=LevelEnum.AD,
             action=FacebookActionEnum.NONE,
             redirect=FacebookRuleRedirectEnum.EDIT_STRUCTURE,
             template="Dexter noticed that your __id=1&metric_name=COST_PER_PURCHASE&metric_type=1&antecedent_type=8__ "
                      "increased by __id=1&value=null__%, "
                      "compared to the last __id=1&time_interval=7__ days average "
                      "of __id=2&value=null__ __id=2&metric_name=COST_PER_PURCHASE&metric_type=1&antecedent_type=11__. "
                      "This means your Link Clicks decreased and less people made a purchase. Try to get more "
                      "clicks by writing more compelling messages that match your "
                      "audience's interests. Change your ad creative now. ",
             breakdown_metadata=BreakdownMetadataBase(breakdown=FacebookBreakdownEnum.NONE,
                                                      action_breakdown=FacebookActionBreakdownEnum.NONE),
             time_interval=DaysEnum.SEVEN,
             connective=Connective(LogicOperatorEnum.AND),
             antecedents=[
                 Antecedent(aid=1,
                            atype=AntecedentTypeEnum.FUZZY_TREND,
                            metric=FacebookAvailableSingleMetricEnum.COST_PER_PURCHASE.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=FacebookLinguisticVariableEnum.INCREASING),
                 Antecedent(aid=2,
                            atype=AntecedentTypeEnum.VARIANCE,
                            metric=FacebookAvailableSingleMetricEnum.COST_PER_PURCHASE.value,
                            operator=LogicOperatorEnum.EQUAL_OR_GREATER_THAN,
                            expected_value=15)
             ]),
    RuleBase(rtype=FacebookRuleTypeEnum.BUDGET_AND_BID,
             channel=ChannelEnum.FACEBOOK,
             category=FacebookRuleCategoryEnum.IMPROVE_CPR,
             importance=FacebookRuleImportanceEnum.HIGH,
             source=FacebookRuleSourceEnum.DEXTER,
             level=LevelEnum.AD,
             action=FacebookActionEnum.NONE,
             redirect=FacebookRuleRedirectEnum.EDIT_STRUCTURE,
             template="Dexter noticed that your __id=1&metric_name=COST_PER_PURCHASE&metric_type=1&antecedent_type=8__ "
                      "increased by __id=1&value=null__%, "
                      "compared to the last __id=1&time_interval=14__ days average "
                      "of __id=2&value=null__ __id=2&metric_name=COST_PER_PURCHASE&metric_type=1&antecedent_type=11__. "
                      "This means your Link Clicks decreased and less people made a purchase. Try to get more "
                      "clicks by writing more compelling messages that match your "
                      "audience's interests. Change your ad creative now. ",
             breakdown_metadata=BreakdownMetadataBase(breakdown=FacebookBreakdownEnum.NONE,
                                                      action_breakdown=FacebookActionBreakdownEnum.NONE),
             time_interval=DaysEnum.FOURTEEN,
             connective=Connective(LogicOperatorEnum.AND),
             antecedents=[
                 Antecedent(aid=1,
                            atype=AntecedentTypeEnum.FUZZY_TREND,
                            metric=FacebookAvailableSingleMetricEnum.COST_PER_PURCHASE.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=FacebookLinguisticVariableEnum.INCREASING),
                 Antecedent(aid=2,
                            atype=AntecedentTypeEnum.VARIANCE,
                            metric=FacebookAvailableSingleMetricEnum.COST_PER_PURCHASE.value,
                            operator=LogicOperatorEnum.EQUAL_OR_GREATER_THAN,
                            expected_value=10)
             ]),
    RuleBase(rtype=FacebookRuleTypeEnum.BUDGET_AND_BID,
             channel=ChannelEnum.FACEBOOK,
             category=FacebookRuleCategoryEnum.IMPROVE_CPR,
             importance=FacebookRuleImportanceEnum.HIGH,
             source=FacebookRuleSourceEnum.DEXTER,
             level=LevelEnum.AD,
             action=FacebookActionEnum.NONE,
             redirect=FacebookRuleRedirectEnum.EDIT_STRUCTURE,
             template="Dexter noticed that your __id=1&metric_name=COST_PER_PURCHASE&metric_type=1&antecedent_type=8__ "
                      "increased by __id=1&value=null__%, "
                      "compared to the last __id=1&time_interval=30__ days average "
                      "of __id=2&value=null__ __id=2&metric_name=COST_PER_PURCHASE&metric_type=1&antecedent_type=11__. "
                      "This means your Link Clicks decreased and less people made a purchase. Try to get more "
                      "clicks by writing more compelling messages that match your "
                      "audience's interests. Change your ad creative now. ",
             breakdown_metadata=BreakdownMetadataBase(breakdown=FacebookBreakdownEnum.NONE,
                                                      action_breakdown=FacebookActionBreakdownEnum.NONE),
             time_interval=DaysEnum.MONTH,
             connective=Connective(LogicOperatorEnum.AND),
             antecedents=[
                 Antecedent(aid=1,
                            atype=AntecedentTypeEnum.FUZZY_TREND,
                            metric=FacebookAvailableSingleMetricEnum.COST_PER_PURCHASE.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=FacebookLinguisticVariableEnum.INCREASING),
                 Antecedent(aid=2,
                            atype=AntecedentTypeEnum.VARIANCE,
                            metric=FacebookAvailableSingleMetricEnum.COST_PER_PURCHASE.value,
                            operator=LogicOperatorEnum.EQUAL_OR_GREATER_THAN,
                            expected_value=10)
             ]),
    RuleBase(rtype=FacebookRuleTypeEnum.BUDGET_AND_BID,
             channel=ChannelEnum.FACEBOOK,
             category=FacebookRuleCategoryEnum.IMPROVE_CPR,
             importance=FacebookRuleImportanceEnum.HIGH,
             source=FacebookRuleSourceEnum.DEXTER,
             level=LevelEnum.AD,
             action=FacebookActionEnum.NONE,
             redirect=FacebookRuleRedirectEnum.EDIT_STRUCTURE,
             template="Dexter noticed that your __id=1&metric_name=REACH&metric_type=1&antecedent_type=8__ "
                      "decreased by __id=1&value=null__%, "
                      "compared to the last __id=1&time_interval=3__ days average "
                      "of __id=2&value=null__ __id=2&metric_name=REACH&metric_type=1&antecedent_type=11__. "
                      "Let people engage more by changing the ad creative now. Change your ad creative now.",
             breakdown_metadata=BreakdownMetadataBase(breakdown=FacebookBreakdownEnum.NONE,
                                                      action_breakdown=FacebookActionBreakdownEnum.NONE),
             time_interval=DaysEnum.THREE,
             connective=Connective(LogicOperatorEnum.AND),
             antecedents=[
                 Antecedent(aid=1,
                            atype=AntecedentTypeEnum.FUZZY_TREND,
                            metric=FacebookAvailableSingleMetricEnum.REACH.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=FacebookLinguisticVariableEnum.DECREASING),
                 Antecedent(aid=2,
                            atype=AntecedentTypeEnum.VARIANCE,
                            metric=FacebookAvailableSingleMetricEnum.REACH.value,
                            operator=LogicOperatorEnum.EQUAL_OR_GREATER_THAN,
                            expected_value=25)
             ]),
    RuleBase(rtype=FacebookRuleTypeEnum.BUDGET_AND_BID,
             channel=ChannelEnum.FACEBOOK,
             category=FacebookRuleCategoryEnum.IMPROVE_CPR,
             importance=FacebookRuleImportanceEnum.HIGH,
             source=FacebookRuleSourceEnum.DEXTER,
             level=LevelEnum.AD,
             action=FacebookActionEnum.NONE,
             redirect=FacebookRuleRedirectEnum.EDIT_STRUCTURE,
             template="Dexter noticed that your __id=1&metric_name=REACH&metric_type=1&antecedent_type=8__ "
                      "decreased by __id=1&value=null__%, "
                      "compared to the last __id=1&time_interval=7__ days average "
                      "of __id=2&value=null__ __id=2&metric_name=REACH&metric_type=1&antecedent_type=11__. "
                      "Let people engage more by changing the ad creative now. Change your ad creative now.",
             breakdown_metadata=BreakdownMetadataBase(breakdown=FacebookBreakdownEnum.NONE,
                                                      action_breakdown=FacebookActionBreakdownEnum.NONE),
             time_interval=DaysEnum.SEVEN,
             connective=Connective(LogicOperatorEnum.AND),
             antecedents=[
                 Antecedent(aid=1,
                            atype=AntecedentTypeEnum.FUZZY_TREND,
                            metric=FacebookAvailableSingleMetricEnum.REACH.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=FacebookLinguisticVariableEnum.DECREASING),
                 Antecedent(aid=2,
                            atype=AntecedentTypeEnum.VARIANCE,
                            metric=FacebookAvailableSingleMetricEnum.REACH.value,
                            operator=LogicOperatorEnum.EQUAL_OR_GREATER_THAN,
                            expected_value=20)
             ]),
    RuleBase(rtype=FacebookRuleTypeEnum.BUDGET_AND_BID,
             channel=ChannelEnum.FACEBOOK,
             category=FacebookRuleCategoryEnum.IMPROVE_CPR,
             importance=FacebookRuleImportanceEnum.HIGH,
             source=FacebookRuleSourceEnum.DEXTER,
             level=LevelEnum.AD,
             action=FacebookActionEnum.NONE,
             redirect=FacebookRuleRedirectEnum.EDIT_STRUCTURE,
             template="Dexter noticed that your __id=1&metric_name=REACH&metric_type=1&antecedent_type=8__ "
                      "decreased by __id=1&value=null__%, "
                      "compared to the last __id=1&time_interval=14__ days average "
                      "of __id=2&value=null__ __id=2&metric_name=REACH&metric_type=1&antecedent_type=11__. "
                      "Let people engage more by changing the ad creative now. Change your ad creative now.",
             breakdown_metadata=BreakdownMetadataBase(breakdown=FacebookBreakdownEnum.NONE,
                                                      action_breakdown=FacebookActionBreakdownEnum.NONE),
             time_interval=DaysEnum.FOURTEEN,
             connective=Connective(LogicOperatorEnum.AND),
             antecedents=[
                 Antecedent(aid=1,
                            atype=AntecedentTypeEnum.FUZZY_TREND,
                            metric=FacebookAvailableSingleMetricEnum.REACH.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=FacebookLinguisticVariableEnum.DECREASING),
                 Antecedent(aid=2,
                            atype=AntecedentTypeEnum.VARIANCE,
                            metric=FacebookAvailableSingleMetricEnum.REACH.value,
                            operator=LogicOperatorEnum.EQUAL_OR_GREATER_THAN,
                            expected_value=15)
             ]),
    RuleBase(rtype=FacebookRuleTypeEnum.BUDGET_AND_BID,
             channel=ChannelEnum.FACEBOOK,
             category=FacebookRuleCategoryEnum.IMPROVE_CPR,
             importance=FacebookRuleImportanceEnum.HIGH,
             source=FacebookRuleSourceEnum.DEXTER,
             level=LevelEnum.AD,
             action=FacebookActionEnum.NONE,
             redirect=FacebookRuleRedirectEnum.EDIT_STRUCTURE,
             template="Dexter noticed that your __id=1&metric_name=REACH&metric_type=1&antecedent_type=8__ "
                      "decreased by __id=1&value=null__%, "
                      "compared to the last __id=1&time_interval=30__ days average "
                      "of __id=2&value=null__ __id=2&metric_name=REACH&metric_type=1&antecedent_type=11__. "
                      "Let people engage more by changing the ad creative now. Change your ad creative now.",
             breakdown_metadata=BreakdownMetadataBase(breakdown=FacebookBreakdownEnum.NONE,
                                                      action_breakdown=FacebookActionBreakdownEnum.NONE),
             time_interval=DaysEnum.MONTH,
             connective=Connective(LogicOperatorEnum.AND),
             antecedents=[
                 Antecedent(aid=1,
                            atype=AntecedentTypeEnum.FUZZY_TREND,
                            metric=FacebookAvailableSingleMetricEnum.REACH.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=FacebookLinguisticVariableEnum.DECREASING),
                 Antecedent(aid=2,
                            atype=AntecedentTypeEnum.VARIANCE,
                            metric=FacebookAvailableSingleMetricEnum.REACH.value,
                            operator=LogicOperatorEnum.EQUAL_OR_GREATER_THAN,
                            expected_value=10)
             ]),
    RuleBase(rtype=FacebookRuleTypeEnum.BUDGET_AND_BID,
             channel=ChannelEnum.FACEBOOK,
             category=FacebookRuleCategoryEnum.IMPROVE_CPR,
             importance=FacebookRuleImportanceEnum.HIGH,
             source=FacebookRuleSourceEnum.DEXTER,
             level=LevelEnum.AD,
             action=FacebookActionEnum.NONE,
             redirect=FacebookRuleRedirectEnum.EDIT_STRUCTURE,
             template="Dexter noticed that your __id=1&metric_name=LINK_CLICKS&metric_type=1&antecedent_type=8__ "
                      "decreased by __id=1&value=null__%, "
                      "compared to the last __id=1&time_interval=3__ days average "
                      "of __id=2&value=null__ __id=2&metric_name=LINK_CLICKS&metric_type=1&antecedent_type=11__. "
                      "Let people engage more by changing the ad creative now. Change your ad creative now.",
             breakdown_metadata=BreakdownMetadataBase(breakdown=FacebookBreakdownEnum.NONE,
                                                      action_breakdown=FacebookActionBreakdownEnum.NONE),
             time_interval=DaysEnum.THREE,
             connective=Connective(LogicOperatorEnum.AND),
             antecedents=[
                 Antecedent(aid=1,
                            atype=AntecedentTypeEnum.FUZZY_TREND,
                            metric=FacebookAvailableSingleMetricEnum.LINK_CLICKS.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=FacebookLinguisticVariableEnum.DECREASING),
                 Antecedent(aid=2,
                            atype=AntecedentTypeEnum.VARIANCE,
                            metric=FacebookAvailableSingleMetricEnum.LINK_CLICKS.value,
                            operator=LogicOperatorEnum.EQUAL_OR_GREATER_THAN,
                            expected_value=25)
             ]),
    RuleBase(rtype=FacebookRuleTypeEnum.BUDGET_AND_BID,
             channel=ChannelEnum.FACEBOOK,
             category=FacebookRuleCategoryEnum.IMPROVE_CPR,
             importance=FacebookRuleImportanceEnum.HIGH,
             source=FacebookRuleSourceEnum.DEXTER,
             level=LevelEnum.AD,
             action=FacebookActionEnum.NONE,
             redirect=FacebookRuleRedirectEnum.EDIT_STRUCTURE,
             template="Dexter noticed that your __id=1&metric_name=LINK_CLICKS&metric_type=1&antecedent_type=8__ "
                      "decreased by __id=1&value=null__%, "
                      "compared to the last __id=1&time_interval=7__ days average "
                      "of __id=2&value=null__ __id=2&metric_name=LINK_CLICKS&metric_type=1&antecedent_type=11__. "
                      "Let people engage more by changing the ad creative now. Change your ad creative now.",
             breakdown_metadata=BreakdownMetadataBase(breakdown=FacebookBreakdownEnum.NONE,
                                                      action_breakdown=FacebookActionBreakdownEnum.NONE),
             time_interval=DaysEnum.SEVEN,
             connective=Connective(LogicOperatorEnum.AND),
             antecedents=[
                 Antecedent(aid=1,
                            atype=AntecedentTypeEnum.FUZZY_TREND,
                            metric=FacebookAvailableSingleMetricEnum.LINK_CLICKS.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=FacebookLinguisticVariableEnum.DECREASING),
                 Antecedent(aid=2,
                            atype=AntecedentTypeEnum.VARIANCE,
                            metric=FacebookAvailableSingleMetricEnum.LINK_CLICKS.value,
                            operator=LogicOperatorEnum.EQUAL_OR_GREATER_THAN,
                            expected_value=20)
             ]),
    RuleBase(rtype=FacebookRuleTypeEnum.BUDGET_AND_BID,
             channel=ChannelEnum.FACEBOOK,
             category=FacebookRuleCategoryEnum.IMPROVE_CPR,
             importance=FacebookRuleImportanceEnum.HIGH,
             source=FacebookRuleSourceEnum.DEXTER,
             level=LevelEnum.AD,
             action=FacebookActionEnum.NONE,
             redirect=FacebookRuleRedirectEnum.EDIT_STRUCTURE,
             template="Dexter noticed that your __id=1&metric_name=LINK_CLICKS&metric_type=1&antecedent_type=8__ "
                      "decreased by __id=1&value=null__%, "
                      "compared to the last __id=1&time_interval=14__ days average "
                      "of __id=2&value=null__ __id=2&metric_name=LINK_CLICKS&metric_type=1&antecedent_type=11__. "
                      "Let people engage more by changing the ad creative now. Change your ad creative now.",
             breakdown_metadata=BreakdownMetadataBase(breakdown=FacebookBreakdownEnum.NONE,
                                                      action_breakdown=FacebookActionBreakdownEnum.NONE),
             time_interval=DaysEnum.FOURTEEN,
             connective=Connective(LogicOperatorEnum.AND),
             antecedents=[
                 Antecedent(aid=1,
                            atype=AntecedentTypeEnum.FUZZY_TREND,
                            metric=FacebookAvailableSingleMetricEnum.LINK_CLICKS.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=FacebookLinguisticVariableEnum.DECREASING),
                 Antecedent(aid=2,
                            atype=AntecedentTypeEnum.VARIANCE,
                            metric=FacebookAvailableSingleMetricEnum.LINK_CLICKS.value,
                            operator=LogicOperatorEnum.EQUAL_OR_GREATER_THAN,
                            expected_value=15)
             ]),
    RuleBase(rtype=FacebookRuleTypeEnum.BUDGET_AND_BID,
             channel=ChannelEnum.FACEBOOK,
             category=FacebookRuleCategoryEnum.IMPROVE_CPR,
             importance=FacebookRuleImportanceEnum.HIGH,
             source=FacebookRuleSourceEnum.DEXTER,
             level=LevelEnum.AD,
             action=FacebookActionEnum.NONE,
             redirect=FacebookRuleRedirectEnum.EDIT_STRUCTURE,
             template="Dexter noticed that your __id=1&metric_name=LINK_CLICKS&metric_type=1&antecedent_type=8__ "
                      "decreased by __id=1&value=null__%, "
                      "compared to the last __id=1&time_interval=30__ days average "
                      "of __id=2&value=null__ __id=2&metric_name=LINK_CLICKS&metric_type=1&antecedent_type=11__. "
                      "Let people engage more by changing the ad creative now. Change your ad creative now.",
             breakdown_metadata=BreakdownMetadataBase(breakdown=FacebookBreakdownEnum.NONE,
                                                      action_breakdown=FacebookActionBreakdownEnum.NONE),
             time_interval=DaysEnum.MONTH,
             connective=Connective(LogicOperatorEnum.AND),
             antecedents=[
                 Antecedent(aid=1,
                            atype=AntecedentTypeEnum.FUZZY_TREND,
                            metric=FacebookAvailableSingleMetricEnum.LINK_CLICKS.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=FacebookLinguisticVariableEnum.DECREASING),
                 Antecedent(aid=2,
                            atype=AntecedentTypeEnum.VARIANCE,
                            metric=FacebookAvailableSingleMetricEnum.LINK_CLICKS.value,
                            operator=LogicOperatorEnum.EQUAL_OR_GREATER_THAN,
                            expected_value=10)
             ]),
    RuleBase(rtype=FacebookRuleTypeEnum.BUDGET_AND_BID,
             channel=ChannelEnum.FACEBOOK,
             category=FacebookRuleCategoryEnum.IMPROVE_CPR,
             importance=FacebookRuleImportanceEnum.HIGH,
             source=FacebookRuleSourceEnum.DEXTER,
             level=LevelEnum.AD,
             action=FacebookActionEnum.NONE,
             redirect=FacebookRuleRedirectEnum.EDIT_STRUCTURE,
             template="Dexter noticed that your __id=1&metric_name=PAGE_LIKES&metric_type=1&antecedent_type=8__ "
                      "decreased by __id=1&value=null__%, "
                      "compared to the last __id=1&time_interval=3__ days average "
                      "of __id=2&value=null__ __id=2&metric_name=PAGE_LIKES&metric_type=1&antecedent_type=11__. "
                      " Let people engage more by changing the ad creative now. Change your ad creative now.",
             breakdown_metadata=BreakdownMetadataBase(breakdown=FacebookBreakdownEnum.NONE,
                                                      action_breakdown=FacebookActionBreakdownEnum.NONE),
             time_interval=DaysEnum.THREE,
             connective=Connective(LogicOperatorEnum.AND),
             antecedents=[
                 Antecedent(aid=1,
                            atype=AntecedentTypeEnum.FUZZY_TREND,
                            metric=FacebookAvailableSingleMetricEnum.PAGE_LIKES.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=FacebookLinguisticVariableEnum.DECREASING),
                 Antecedent(aid=2,
                            atype=AntecedentTypeEnum.VARIANCE,
                            metric=FacebookAvailableSingleMetricEnum.PAGE_LIKES.value,
                            operator=LogicOperatorEnum.EQUAL_OR_GREATER_THAN,
                            expected_value=25)
             ]),
    RuleBase(rtype=FacebookRuleTypeEnum.BUDGET_AND_BID,
             channel=ChannelEnum.FACEBOOK,
             category=FacebookRuleCategoryEnum.IMPROVE_CPR,
             importance=FacebookRuleImportanceEnum.HIGH,
             source=FacebookRuleSourceEnum.DEXTER,
             level=LevelEnum.AD,
             action=FacebookActionEnum.NONE,
             redirect=FacebookRuleRedirectEnum.EDIT_STRUCTURE,
             template="Dexter noticed that your __id=1&metric_name=PAGE_LIKES&metric_type=1&antecedent_type=8__ "
                      "decreased by __id=1&value=null__%, "
                      "compared to the last __id=1&time_interval=7__ days average "
                      "of __id=2&value=null__ __id=2&metric_name=PAGE_LIKES&metric_type=1&antecedent_type=11__. "
                      " Let people engage more by changing the ad creative now. Change your ad creative now.",
             breakdown_metadata=BreakdownMetadataBase(breakdown=FacebookBreakdownEnum.NONE,
                                                      action_breakdown=FacebookActionBreakdownEnum.NONE),
             time_interval=DaysEnum.SEVEN,
             connective=Connective(LogicOperatorEnum.AND),
             antecedents=[
                 Antecedent(aid=1,
                            atype=AntecedentTypeEnum.FUZZY_TREND,
                            metric=FacebookAvailableSingleMetricEnum.PAGE_LIKES.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=FacebookLinguisticVariableEnum.DECREASING),
                 Antecedent(aid=2,
                            atype=AntecedentTypeEnum.VARIANCE,
                            metric=FacebookAvailableSingleMetricEnum.PAGE_LIKES.value,
                            operator=LogicOperatorEnum.EQUAL_OR_GREATER_THAN,
                            expected_value=20)
             ]),
    RuleBase(rtype=FacebookRuleTypeEnum.BUDGET_AND_BID,
             channel=ChannelEnum.FACEBOOK,
             category=FacebookRuleCategoryEnum.IMPROVE_CPR,
             importance=FacebookRuleImportanceEnum.HIGH,
             source=FacebookRuleSourceEnum.DEXTER,
             level=LevelEnum.AD,
             action=FacebookActionEnum.NONE,
             redirect=FacebookRuleRedirectEnum.EDIT_STRUCTURE,
             template="Dexter noticed that your __id=1&metric_name=PAGE_LIKES&metric_type=1&antecedent_type=8__ "
                      "decreased by __id=1&value=null__%, "
                      "compared to the last __id=1&time_interval=14__ days average "
                      "of __id=2&value=null__ __id=2&metric_name=PAGE_LIKES&metric_type=1&antecedent_type=11__. "
                      " Let people engage more by changing the ad creative now. Change your ad creative now.",
             breakdown_metadata=BreakdownMetadataBase(breakdown=FacebookBreakdownEnum.NONE,
                                                      action_breakdown=FacebookActionBreakdownEnum.NONE),
             time_interval=DaysEnum.FOURTEEN,
             connective=Connective(LogicOperatorEnum.AND),
             antecedents=[
                 Antecedent(aid=1,
                            atype=AntecedentTypeEnum.FUZZY_TREND,
                            metric=FacebookAvailableSingleMetricEnum.PAGE_LIKES.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=FacebookLinguisticVariableEnum.DECREASING),
                 Antecedent(aid=2,
                            atype=AntecedentTypeEnum.VARIANCE,
                            metric=FacebookAvailableSingleMetricEnum.PAGE_LIKES.value,
                            operator=LogicOperatorEnum.EQUAL_OR_GREATER_THAN,
                            expected_value=15)
             ]),
    RuleBase(rtype=FacebookRuleTypeEnum.BUDGET_AND_BID,
             channel=ChannelEnum.FACEBOOK,
             category=FacebookRuleCategoryEnum.IMPROVE_CPR,
             importance=FacebookRuleImportanceEnum.HIGH,
             source=FacebookRuleSourceEnum.DEXTER,
             level=LevelEnum.AD,
             action=FacebookActionEnum.NONE,
             redirect=FacebookRuleRedirectEnum.EDIT_STRUCTURE,
             template="Dexter noticed that your __id=1&metric_name=PAGE_LIKES&metric_type=1&antecedent_type=8__ "
                      "decreased by __id=1&value=null__%, "
                      "compared to the last __id=1&time_interval=30__ days average "
                      "of __id=2&value=null__ __id=2&metric_name=PAGE_LIKES&metric_type=1&antecedent_type=11__. "
                      " Let people engage more by changing the ad creative now. Change your ad creative now.",
             breakdown_metadata=BreakdownMetadataBase(breakdown=FacebookBreakdownEnum.NONE,
                                                      action_breakdown=FacebookActionBreakdownEnum.NONE),
             time_interval=DaysEnum.MONTH,
             connective=Connective(LogicOperatorEnum.AND),
             antecedents=[
                 Antecedent(aid=1,
                            atype=AntecedentTypeEnum.FUZZY_TREND,
                            metric=FacebookAvailableSingleMetricEnum.PAGE_LIKES.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=FacebookLinguisticVariableEnum.DECREASING),
                 Antecedent(aid=2,
                            atype=AntecedentTypeEnum.VARIANCE,
                            metric=FacebookAvailableSingleMetricEnum.PAGE_LIKES.value,
                            operator=LogicOperatorEnum.EQUAL_OR_GREATER_THAN,
                            expected_value=10)
             ]),
    RuleBase(rtype=FacebookRuleTypeEnum.BUDGET_AND_BID,
             channel=ChannelEnum.FACEBOOK,
             category=FacebookRuleCategoryEnum.IMPROVE_CPR,
             importance=FacebookRuleImportanceEnum.HIGH,
             source=FacebookRuleSourceEnum.DEXTER,
             level=LevelEnum.AD,
             action=FacebookActionEnum.NONE,
             redirect=FacebookRuleRedirectEnum.EDIT_STRUCTURE,
             template="Dexter noticed that your __id=1&metric_name=APP_INSTALLS&metric_type=1&antecedent_type=8__ "
                      "decreased by __id=1&value=null__%, "
                      "compared to the last __id=1&time_interval=3__ days average "
                      "of __id=2&value=null__ __id=2&metric_name=APP_INSTALLS&metric_type=1&antecedent_type=11__. "
                      " Let people engage more by changing the ad creative now. Change your ad creative now.",
             breakdown_metadata=BreakdownMetadataBase(breakdown=FacebookBreakdownEnum.NONE,
                                                      action_breakdown=FacebookActionBreakdownEnum.NONE),
             time_interval=DaysEnum.THREE,
             connective=Connective(LogicOperatorEnum.AND),
             antecedents=[
                 Antecedent(aid=1,
                            atype=AntecedentTypeEnum.FUZZY_TREND,
                            metric=FacebookAvailableSingleMetricEnum.APP_INSTALLS.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=FacebookLinguisticVariableEnum.DECREASING),
                 Antecedent(aid=2,
                            atype=AntecedentTypeEnum.VARIANCE,
                            metric=FacebookAvailableSingleMetricEnum.APP_INSTALLS.value,
                            operator=LogicOperatorEnum.EQUAL_OR_GREATER_THAN,
                            expected_value=25)
             ]),
    RuleBase(rtype=FacebookRuleTypeEnum.BUDGET_AND_BID,
             channel=ChannelEnum.FACEBOOK,
             category=FacebookRuleCategoryEnum.IMPROVE_CPR,
             importance=FacebookRuleImportanceEnum.HIGH,
             source=FacebookRuleSourceEnum.DEXTER,
             level=LevelEnum.AD,
             action=FacebookActionEnum.NONE,
             redirect=FacebookRuleRedirectEnum.EDIT_STRUCTURE,
             template="Dexter noticed that your __id=1&metric_name=APP_INSTALLS&metric_type=1&antecedent_type=8__ "
                      "decreased by __id=1&value=null__%, "
                      "compared to the last __id=1&time_interval=7__ days average "
                      "of __id=2&value=null__ __id=2&metric_name=APP_INSTALLS&metric_type=1&antecedent_type=11__. "
                      " Let people engage more by changing the ad creative now. Change your ad creative now.",
             breakdown_metadata=BreakdownMetadataBase(breakdown=FacebookBreakdownEnum.NONE,
                                                      action_breakdown=FacebookActionBreakdownEnum.NONE),
             time_interval=DaysEnum.SEVEN,
             connective=Connective(LogicOperatorEnum.AND),
             antecedents=[
                 Antecedent(aid=1,
                            atype=AntecedentTypeEnum.FUZZY_TREND,
                            metric=FacebookAvailableSingleMetricEnum.APP_INSTALLS.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=FacebookLinguisticVariableEnum.DECREASING),
                 Antecedent(aid=2,
                            atype=AntecedentTypeEnum.VARIANCE,
                            metric=FacebookAvailableSingleMetricEnum.APP_INSTALLS.value,
                            operator=LogicOperatorEnum.EQUAL_OR_GREATER_THAN,
                            expected_value=20)
             ]),
    RuleBase(rtype=FacebookRuleTypeEnum.BUDGET_AND_BID,
             channel=ChannelEnum.FACEBOOK,
             category=FacebookRuleCategoryEnum.IMPROVE_CPR,
             importance=FacebookRuleImportanceEnum.HIGH,
             source=FacebookRuleSourceEnum.DEXTER,
             level=LevelEnum.AD,
             action=FacebookActionEnum.NONE,
             redirect=FacebookRuleRedirectEnum.EDIT_STRUCTURE,
             template="Dexter noticed that your __id=1&metric_name=APP_INSTALLS&metric_type=1&antecedent_type=8__ "
                      "decreased by __id=1&value=null__%, "
                      "compared to the last __id=1&time_interval=14__ days average "
                      "of __id=2&value=null__ __id=2&metric_name=APP_INSTALLS&metric_type=1&antecedent_type=11__. "
                      " Let people engage more by changing the ad creative now. Change your ad creative now.",
             breakdown_metadata=BreakdownMetadataBase(breakdown=FacebookBreakdownEnum.NONE,
                                                      action_breakdown=FacebookActionBreakdownEnum.NONE),
             time_interval=DaysEnum.FOURTEEN,
             connective=Connective(LogicOperatorEnum.AND),
             antecedents=[
                 Antecedent(aid=1,
                            atype=AntecedentTypeEnum.FUZZY_TREND,
                            metric=FacebookAvailableSingleMetricEnum.APP_INSTALLS.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=FacebookLinguisticVariableEnum.DECREASING),
                 Antecedent(aid=2,
                            atype=AntecedentTypeEnum.VARIANCE,
                            metric=FacebookAvailableSingleMetricEnum.APP_INSTALLS.value,
                            operator=LogicOperatorEnum.EQUAL_OR_GREATER_THAN,
                            expected_value=15)
             ]),
    RuleBase(rtype=FacebookRuleTypeEnum.BUDGET_AND_BID,
             channel=ChannelEnum.FACEBOOK,
             category=FacebookRuleCategoryEnum.IMPROVE_CPR,
             importance=FacebookRuleImportanceEnum.HIGH,
             source=FacebookRuleSourceEnum.DEXTER,
             level=LevelEnum.AD,
             action=FacebookActionEnum.NONE,
             redirect=FacebookRuleRedirectEnum.EDIT_STRUCTURE,
             template="Dexter noticed that your __id=1&metric_name=APP_INSTALLS&metric_type=1&antecedent_type=8__ "
                      "decreased by __id=1&value=null__%, "
                      "compared to the last __id=1&time_interval=30__ days average "
                      "of __id=2&value=null__ __id=2&metric_name=APP_INSTALLS&metric_type=1&antecedent_type=11__. "
                      " Let people engage more by changing the ad creative now. Change your ad creative now.",
             breakdown_metadata=BreakdownMetadataBase(breakdown=FacebookBreakdownEnum.NONE,
                                                      action_breakdown=FacebookActionBreakdownEnum.NONE),
             time_interval=DaysEnum.MONTH,
             connective=Connective(LogicOperatorEnum.AND),
             antecedents=[
                 Antecedent(aid=1,
                            atype=AntecedentTypeEnum.FUZZY_TREND,
                            metric=FacebookAvailableSingleMetricEnum.APP_INSTALLS.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=FacebookLinguisticVariableEnum.DECREASING),
                 Antecedent(aid=2,
                            atype=AntecedentTypeEnum.VARIANCE,
                            metric=FacebookAvailableSingleMetricEnum.APP_INSTALLS.value,
                            operator=LogicOperatorEnum.EQUAL_OR_GREATER_THAN,
                            expected_value=10)
             ]),
    RuleBase(rtype=FacebookRuleTypeEnum.BUDGET_AND_BID,
             channel=ChannelEnum.FACEBOOK,
             category=FacebookRuleCategoryEnum.IMPROVE_CPR,
             importance=FacebookRuleImportanceEnum.HIGH,
             source=FacebookRuleSourceEnum.DEXTER,
             level=LevelEnum.AD,
             action=FacebookActionEnum.NONE,
             redirect=FacebookRuleRedirectEnum.EDIT_STRUCTURE,
             template="Dexter noticed that your __id=1&metric_name=COST_PER_APP_INSTALL&metric_type=1&antecedent_type=8__ "
                      "increased by __id=1&value=null__%, "
                      "compared to the last __id=1&time_interval=3__ days average "
                      "of __id=2&value=null__ __id=2&metric_name=COST_PER_APP_INSTALL&metric_type=1&antecedent_type=11__. "
                      "Try to get more results by writing more compelling messages "
                      "that match your audience's interests. Change your ad creative now.",
             breakdown_metadata=BreakdownMetadataBase(breakdown=FacebookBreakdownEnum.NONE,
                                                      action_breakdown=FacebookActionBreakdownEnum.NONE),
             time_interval=DaysEnum.THREE,
             connective=Connective(LogicOperatorEnum.AND),
             antecedents=[
                 Antecedent(aid=1,
                            atype=AntecedentTypeEnum.FUZZY_TREND,
                            metric=FacebookAvailableSingleMetricEnum.COST_PER_APP_INSTALL.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=FacebookLinguisticVariableEnum.INCREASING),
                 Antecedent(aid=2,
                            atype=AntecedentTypeEnum.VARIANCE,
                            metric=FacebookAvailableSingleMetricEnum.COST_PER_APP_INSTALL.value,
                            operator=LogicOperatorEnum.EQUAL_OR_GREATER_THAN,
                            expected_value=20)
             ]),
    RuleBase(rtype=FacebookRuleTypeEnum.BUDGET_AND_BID,
             channel=ChannelEnum.FACEBOOK,
             category=FacebookRuleCategoryEnum.IMPROVE_CPR,
             importance=FacebookRuleImportanceEnum.HIGH,
             source=FacebookRuleSourceEnum.DEXTER,
             level=LevelEnum.AD,
             action=FacebookActionEnum.NONE,
             redirect=FacebookRuleRedirectEnum.EDIT_STRUCTURE,
             template="Dexter noticed that your __id=1&metric_name=COST_PER_APP_INSTALL&metric_type=1&antecedent_type=8__ "
                      "increased by __id=1&value=null__%, "
                      "compared to the last __id=1&time_interval=7__ days average "
                      "of __id=2&value=null__ __id=2&metric_name=COST_PER_APP_INSTALL&metric_type=1&antecedent_type=11__. "
                      "Try to get more results by writing more compelling messages "
                      "that match your audience's interests. Change your ad creative now.",
             breakdown_metadata=BreakdownMetadataBase(breakdown=FacebookBreakdownEnum.NONE,
                                                      action_breakdown=FacebookActionBreakdownEnum.NONE),
             time_interval=DaysEnum.SEVEN,
             connective=Connective(LogicOperatorEnum.AND),
             antecedents=[
                 Antecedent(aid=1,
                            atype=AntecedentTypeEnum.FUZZY_TREND,
                            metric=FacebookAvailableSingleMetricEnum.COST_PER_APP_INSTALL.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=FacebookLinguisticVariableEnum.INCREASING),
                 Antecedent(aid=2,
                            atype=AntecedentTypeEnum.VARIANCE,
                            metric=FacebookAvailableSingleMetricEnum.COST_PER_APP_INSTALL.value,
                            operator=LogicOperatorEnum.EQUAL_OR_GREATER_THAN,
                            expected_value=15)
             ]),
    RuleBase(rtype=FacebookRuleTypeEnum.BUDGET_AND_BID,
             channel=ChannelEnum.FACEBOOK,
             category=FacebookRuleCategoryEnum.IMPROVE_CPR,
             importance=FacebookRuleImportanceEnum.HIGH,
             source=FacebookRuleSourceEnum.DEXTER,
             level=LevelEnum.AD,
             action=FacebookActionEnum.NONE,
             redirect=FacebookRuleRedirectEnum.EDIT_STRUCTURE,
             template="Dexter noticed that your __id=1&metric_name=COST_PER_APP_INSTALL&metric_type=1&antecedent_type=8__ "
                      "increased by __id=1&value=null__%, "
                      "compared to the last __id=1&time_interval=14__ days average "
                      "of __id=2&value=null__ __id=2&metric_name=COST_PER_APP_INSTALL&metric_type=1&antecedent_type=11__. "
                      "Try to get more results by writing more compelling messages "
                      "that match your audience's interests. Change your ad creative now.",
             breakdown_metadata=BreakdownMetadataBase(breakdown=FacebookBreakdownEnum.NONE,
                                                      action_breakdown=FacebookActionBreakdownEnum.NONE),
             time_interval=DaysEnum.FOURTEEN,
             connective=Connective(LogicOperatorEnum.AND),
             antecedents=[
                 Antecedent(aid=1,
                            atype=AntecedentTypeEnum.FUZZY_TREND,
                            metric=FacebookAvailableSingleMetricEnum.COST_PER_APP_INSTALL.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=FacebookLinguisticVariableEnum.INCREASING),
                 Antecedent(aid=2,
                            atype=AntecedentTypeEnum.VARIANCE,
                            metric=FacebookAvailableSingleMetricEnum.COST_PER_APP_INSTALL.value,
                            operator=LogicOperatorEnum.EQUAL_OR_GREATER_THAN,
                            expected_value=10)
             ]),
    RuleBase(rtype=FacebookRuleTypeEnum.BUDGET_AND_BID,
             channel=ChannelEnum.FACEBOOK,
             category=FacebookRuleCategoryEnum.IMPROVE_CPR,
             importance=FacebookRuleImportanceEnum.HIGH,
             source=FacebookRuleSourceEnum.DEXTER,
             level=LevelEnum.AD,
             action=FacebookActionEnum.NONE,
             redirect=FacebookRuleRedirectEnum.EDIT_STRUCTURE,
             template="Dexter noticed that your __id=1&metric_name=COST_PER_APP_INSTALL&metric_type=1&antecedent_type=8__ "
                      "increased by __id=1&value=null__%, "
                      "compared to the last __id=1&time_interval=30__ days average "
                      "of __id=2&value=null__ __id=2&metric_name=COST_PER_APP_INSTALL&metric_type=1&antecedent_type=11__. "
                      "Try to get more results by writing more compelling messages "
                      "that match your audience's interests. Change your ad creative now.",
             breakdown_metadata=BreakdownMetadataBase(breakdown=FacebookBreakdownEnum.NONE,
                                                      action_breakdown=FacebookActionBreakdownEnum.NONE),
             time_interval=DaysEnum.MONTH,
             connective=Connective(LogicOperatorEnum.AND),
             antecedents=[
                 Antecedent(aid=1,
                            atype=AntecedentTypeEnum.FUZZY_TREND,
                            metric=FacebookAvailableSingleMetricEnum.COST_PER_APP_INSTALL.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=FacebookLinguisticVariableEnum.INCREASING),
                 Antecedent(aid=2,
                            atype=AntecedentTypeEnum.VARIANCE,
                            metric=FacebookAvailableSingleMetricEnum.COST_PER_APP_INSTALL.value,
                            operator=LogicOperatorEnum.EQUAL_OR_GREATER_THAN,
                            expected_value=10)
             ]),
    RuleBase(rtype=FacebookRuleTypeEnum.BUDGET_AND_BID,
             channel=ChannelEnum.FACEBOOK,
             category=FacebookRuleCategoryEnum.IMPROVE_CPR,
             importance=FacebookRuleImportanceEnum.HIGH,
             source=FacebookRuleSourceEnum.DEXTER,
             level=LevelEnum.AD,
             action=FacebookActionEnum.NONE,
             redirect=FacebookRuleRedirectEnum.EDIT_STRUCTURE,
             template="Dexter noticed that your __id=1&metric_name=LEADS&metric_type=1&antecedent_type=8__ "
                      "increased by __id=1&value=null__%, "
                      "compared to the last __id=1&time_interval=3__ days average "
                      "of __id=2&value=null__ __id=2&metric_name=LEADS&metric_type=1&antecedent_type=11__. "
                      "Let people engage more by changing the ad creative now. Change your ad creative now.",
             breakdown_metadata=BreakdownMetadataBase(breakdown=FacebookBreakdownEnum.NONE,
                                                      action_breakdown=FacebookActionBreakdownEnum.NONE),
             time_interval=DaysEnum.THREE,
             connective=Connective(LogicOperatorEnum.AND),
             antecedents=[
                 Antecedent(aid=1,
                            atype=AntecedentTypeEnum.FUZZY_TREND,
                            metric=FacebookAvailableSingleMetricEnum.LEADS.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=FacebookLinguisticVariableEnum.INCREASING),
                 Antecedent(aid=2,
                            atype=AntecedentTypeEnum.VARIANCE,
                            metric=FacebookAvailableSingleMetricEnum.LEADS.value,
                            operator=LogicOperatorEnum.EQUAL_OR_GREATER_THAN,
                            expected_value=25)
             ]),
    RuleBase(rtype=FacebookRuleTypeEnum.BUDGET_AND_BID,
             channel=ChannelEnum.FACEBOOK,
             category=FacebookRuleCategoryEnum.IMPROVE_CPR,
             importance=FacebookRuleImportanceEnum.HIGH,
             source=FacebookRuleSourceEnum.DEXTER,
             level=LevelEnum.AD,
             action=FacebookActionEnum.NONE,
             redirect=FacebookRuleRedirectEnum.EDIT_STRUCTURE,
             template="Dexter noticed that your __id=1&metric_name=LEADS&metric_type=1&antecedent_type=8__ "
                      "increased by __id=1&value=null__%, "
                      "compared to the last __id=1&time_interval=7__ days average "
                      "of __id=2&value=null__ __id=2&metric_name=LEADS&metric_type=1&antecedent_type=11__. "
                      "Let people engage more by changing the ad creative now. Change your ad creative now.",
             breakdown_metadata=BreakdownMetadataBase(breakdown=FacebookBreakdownEnum.NONE,
                                                      action_breakdown=FacebookActionBreakdownEnum.NONE),
             time_interval=DaysEnum.SEVEN,
             connective=Connective(LogicOperatorEnum.AND),
             antecedents=[
                 Antecedent(aid=1,
                            atype=AntecedentTypeEnum.FUZZY_TREND,
                            metric=FacebookAvailableSingleMetricEnum.LEADS.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=FacebookLinguisticVariableEnum.INCREASING),
                 Antecedent(aid=2,
                            atype=AntecedentTypeEnum.VARIANCE,
                            metric=FacebookAvailableSingleMetricEnum.LEADS.value,
                            operator=LogicOperatorEnum.EQUAL_OR_GREATER_THAN,
                            expected_value=20)
             ]),
    RuleBase(rtype=FacebookRuleTypeEnum.BUDGET_AND_BID,
             channel=ChannelEnum.FACEBOOK,
             category=FacebookRuleCategoryEnum.IMPROVE_CPR,
             importance=FacebookRuleImportanceEnum.HIGH,
             source=FacebookRuleSourceEnum.DEXTER,
             level=LevelEnum.AD,
             action=FacebookActionEnum.NONE,
             redirect=FacebookRuleRedirectEnum.EDIT_STRUCTURE,
             template="Dexter noticed that your __id=1&metric_name=LEADS&metric_type=1&antecedent_type=8__ "
                      "increased by __id=1&value=null__%, "
                      "compared to the last __id=1&time_interval=14__ days average "
                      "of __id=2&value=null__ __id=2&metric_name=LEADS&metric_type=1&antecedent_type=11__. "
                      "Let people engage more by changing the ad creative now. Change your ad creative now.",
             breakdown_metadata=BreakdownMetadataBase(breakdown=FacebookBreakdownEnum.NONE,
                                                      action_breakdown=FacebookActionBreakdownEnum.NONE),
             time_interval=DaysEnum.FOURTEEN,
             connective=Connective(LogicOperatorEnum.AND),
             antecedents=[
                 Antecedent(aid=1,
                            atype=AntecedentTypeEnum.FUZZY_TREND,
                            metric=FacebookAvailableSingleMetricEnum.LEADS.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=FacebookLinguisticVariableEnum.INCREASING),
                 Antecedent(aid=2,
                            atype=AntecedentTypeEnum.VARIANCE,
                            metric=FacebookAvailableSingleMetricEnum.LEADS.value,
                            operator=LogicOperatorEnum.EQUAL_OR_GREATER_THAN,
                            expected_value=15)
             ]),
    RuleBase(rtype=FacebookRuleTypeEnum.BUDGET_AND_BID,
             channel=ChannelEnum.FACEBOOK,
             category=FacebookRuleCategoryEnum.IMPROVE_CPR,
             importance=FacebookRuleImportanceEnum.HIGH,
             source=FacebookRuleSourceEnum.DEXTER,
             level=LevelEnum.AD,
             action=FacebookActionEnum.NONE,
             redirect=FacebookRuleRedirectEnum.EDIT_STRUCTURE,
             template="Dexter noticed that your __id=1&metric_name=LEADS&metric_type=1&antecedent_type=8__ "
                      "increased by __id=1&value=null__%, "
                      "compared to the last __id=1&time_interval=30__ days average "
                      "of __id=2&value=null__ __id=2&metric_name=LEADS&metric_type=1&antecedent_type=11__. "
                      "Let people engage more by changing the ad creative now. Change your ad creative now.",
             breakdown_metadata=BreakdownMetadataBase(breakdown=FacebookBreakdownEnum.NONE,
                                                      action_breakdown=FacebookActionBreakdownEnum.NONE),
             time_interval=DaysEnum.MONTH,
             connective=Connective(LogicOperatorEnum.AND),
             antecedents=[
                 Antecedent(aid=1,
                            atype=AntecedentTypeEnum.FUZZY_TREND,
                            metric=FacebookAvailableSingleMetricEnum.LEADS.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=FacebookLinguisticVariableEnum.INCREASING),
                 Antecedent(aid=2,
                            atype=AntecedentTypeEnum.VARIANCE,
                            metric=FacebookAvailableSingleMetricEnum.LEADS.value,
                            operator=LogicOperatorEnum.EQUAL_OR_GREATER_THAN,
                            expected_value=10)
             ])
]
