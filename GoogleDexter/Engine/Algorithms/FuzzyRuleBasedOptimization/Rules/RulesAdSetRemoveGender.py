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
from GoogleDexter.Infrastructure.Domain.Breakdowns import GoogleBreakdownEnum, GoogleActionBreakdownEnum
from GoogleDexter.Infrastructure.Domain.Rules.GoogleRuleEnums import GoogleRuleTypeEnum, GoogleRuleImportanceEnum, \
    GoogleRuleSourceEnum, GoogleRuleRedirectEnum, GoogleRuleCategoryEnum
from GoogleDexter.Infrastructure.FuzzyEngine.GoogleFuzzySets import GoogleLinguisticVariableEnum

RULES_ADSET_REMOVE_GENDER = [
    RuleBase(rtype=GoogleRuleTypeEnum.AUDIENCE,
             channel=ChannelEnum.GOOGLE,
             category=GoogleRuleCategoryEnum.OPTIMIZE_TARGETING,
             importance=GoogleRuleImportanceEnum.MEDIUM,
             source=GoogleRuleSourceEnum.DEXTER,
             level=LevelEnum.ADGROUP,
             action=GoogleActionEnum.REMOVE,
             redirect=GoogleRuleRedirectEnum.CAMPAIGN_MANAGER,
             template="Your <id=1&metric_name=RESULTS&metric_type=1&antecedent_type=8> has decreased by <id=1&value=null>% in the last "
                      "<id=1&time_interval=7> days for some of the genders you are targeting. Dexter recommends you stop targeting the "
                      "following genders <id=1&breakdown_values=null>.",
             breakdown_metadata=BreakdownMetadataBase(breakdown=GoogleBreakdownEnum.GENDER,
                                                      action_breakdown=GoogleActionBreakdownEnum.NONE),
             time_interval=DaysEnum.THREE_MONTHS,
             connective=Connective(LogicOperatorEnum.AND),
             antecedents=[
                 Antecedent(aid=1,
                            atype=AntecedentTypeEnum.FUZZY_TREND,
                            metric=GoogleAvailableMetricEnum.RESULTS.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=GoogleLinguisticVariableEnum.DECREASING)
             ]),
    # RuleBase(rtype=GoogleRuleTypeEnum.AUDIENCE,
    #          channel=ChannelEnum.GOOGLE,
    #          category=GoogleRuleCategoryEnum.OPTIMIZE_TARGETING,
    #          importance=GoogleRuleImportanceEnum.MEDIUM,
    #          source=GoogleRuleSourceEnum.DEXTER,
    #          level=LevelEnum.ADGROUP,
    #          action=GoogleActionEnum.REMOVE,
    #          redirect=GoogleRuleRedirectEnum.CAMPAIGN_MANAGER,
    #          template="Your <id=1&metric_name=COST_PER_APP_INSTALL&metric_type=1&antecedent_type=8> has increased by <id=1&value=null> % in the last "
    #                   "<id=1&time_interval=7> for some of the genders you are targeting. Dexter recommends you stop targeting the "
    #                   "following genders <id=1&breakdown_values=null>.",
    #          breakdown_metadata=BreakdownMetadataBase(breakdown=GoogleBreakdownEnum.GENDER,
    #                                               action_breakdown=GoogleActionBreakdownEnum.NONE),
    #          time_interval=DaysEnum.THREE_MONTHS,
    #          connective=Connective(LogicOperatorEnum.AND),
    #          antecedents=[
    #              Antecedent(aid=1,
    #                         atype=AntecedentTypeEnum.FUZZY_TREND,
    #                         metric=AvailableMetricEnum.COST_PER_APP_INSTALL.value,
    #                         operator=LogicOperatorEnum.EQUALS,
    #                         expected_value=GoogleLinguisticVariableEnum.INCREASING)
    #          ]),
    RuleBase(rtype=GoogleRuleTypeEnum.AUDIENCE,
             channel=ChannelEnum.GOOGLE,
             category=GoogleRuleCategoryEnum.OPTIMIZE_TARGETING,
             importance=GoogleRuleImportanceEnum.MEDIUM,
             source=GoogleRuleSourceEnum.DEXTER,
             level=LevelEnum.ADGROUP,
             action=GoogleActionEnum.REMOVE,
             redirect=GoogleRuleRedirectEnum.CAMPAIGN_MANAGER,
             template="Your <id=1&metric_name=CPM&metric_type=1&antecedent_type=8> has increased by <id=1&value=null>% in the last "
                      "<id=1&time_interval=7> days for some of the genders you are targeting. Dexter recommends you stop targeting the "
                      "following genders <id=1&breakdown_values=null>.",
             breakdown_metadata=BreakdownMetadataBase(breakdown=GoogleBreakdownEnum.GENDER,
                                                      action_breakdown=GoogleActionBreakdownEnum.NONE),
             time_interval=DaysEnum.THREE_MONTHS,
             connective=Connective(LogicOperatorEnum.AND),
             antecedents=[
                 Antecedent(aid=1,
                            atype=AntecedentTypeEnum.FUZZY_TREND,
                            metric=GoogleAvailableMetricEnum.CPM.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=GoogleLinguisticVariableEnum.INCREASING)
             ]),
    RuleBase(rtype=GoogleRuleTypeEnum.AUDIENCE,
             channel=ChannelEnum.GOOGLE,
             category=GoogleRuleCategoryEnum.OPTIMIZE_TARGETING,
             importance=GoogleRuleImportanceEnum.MEDIUM,
             source=GoogleRuleSourceEnum.DEXTER,
             level=LevelEnum.ADGROUP,
             action=GoogleActionEnum.REMOVE,
             redirect=GoogleRuleRedirectEnum.CAMPAIGN_MANAGER,
             template="Your <id=1&metric_name=REACH&metric_type=1&antecedent_type=8> has decreased by <id=1&value=null>% in the last "
                      "<id=1&time_interval=7> days for some of the genders you are targeting. Dexter recommends you stop targeting the "
                      "following genders <id=1&breakdown_values=null>.",
             breakdown_metadata=BreakdownMetadataBase(breakdown=GoogleBreakdownEnum.GENDER,
                                                      action_breakdown=GoogleActionBreakdownEnum.NONE),
             time_interval=DaysEnum.THREE_MONTHS,
             connective=Connective(LogicOperatorEnum.AND),
             antecedents=[
                 Antecedent(aid=1,
                            atype=AntecedentTypeEnum.FUZZY_TREND,
                            metric=GoogleAvailableMetricEnum.REACH.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=GoogleLinguisticVariableEnum.DECREASING)
             ]),
    # RuleBase(rtype=GoogleRuleTypeEnum.AUDIENCE,
    #          channel=ChannelEnum.GOOGLE,
    #          category=GoogleRuleCategoryEnum.OPTIMIZE_TARGETING,
    #          importance=GoogleRuleImportanceEnum.MEDIUM,
    #          source=GoogleRuleSourceEnum.DEXTER,
    #          level=LevelEnum.ADGROUP,
    #          action=GoogleActionEnum.REMOVE,
    #          redirect=GoogleRuleRedirectEnum.CAMPAIGN_MANAGER,
    #          template="Your <id=1&metric_name=ENGAGEMENT_RATE&metric_type=1&antecedent_type=8> has decreased by <id=1&value=null> % in the last "
    #                   "<id=1&time_interval=7> for some of the genders you are targeting. Dexter recommends you stop targeting the "
    #                   "following genders <id=1&breakdown_values=null>.",
    #          breakdown_metadata=BreakdownMetadataBase(breakdown=GoogleBreakdownEnum.GENDER,
    #                                               action_breakdown=GoogleActionBreakdownEnum.NONE),
    #          time_interval=DaysEnum.THREE_MONTHS,
    #          connective=Connective(LogicOperatorEnum.AND),
    #          antecedents=[
    #              Antecedent(aid=1,
    #                         atype=AntecedentTypeEnum.FUZZY_TREND,
    #                         metric=AvailableMetricEnum.ENGAGEMENT_RATE.value,
    #                         operator=LogicOperatorEnum.EQUALS,
    #                         expected_value=GoogleLinguisticVariableEnum.DECREASING)
    #          ]),
    # RuleBase(rtype=GoogleRuleTypeEnum.AUDIENCE,
    #          channel=ChannelEnum.GOOGLE,
    #          category=GoogleRuleCategoryEnum.OPTIMIZE_TARGETING,
    #          importance=GoogleRuleImportanceEnum.MEDIUM,
    #          source=GoogleRuleSourceEnum.DEXTER,
    #          level=LevelEnum.ADGROUP,
    #          action=GoogleActionEnum.REMOVE,
    #          redirect=GoogleRuleRedirectEnum.CAMPAIGN_MANAGER,
    #          template="Your <id=1&metric_name=ENGAGEMENT_RATE&metric_type=1&antecedent_type=8> has increased by <id=1&value=null> % in the last "
    #                   "<id=1&time_interval=7> for some of the genders you are targeting. Dexter recommends you stop targeting the "
    #                   "following genders <id=1&breakdown_values=null>.",
    #          breakdown_metadata=BreakdownMetadataBase(breakdown=GoogleBreakdownEnum.GENDER,
    #                                               action_breakdown=GoogleActionBreakdownEnum.NONE),
    #          time_interval=DaysEnum.THREE_MONTHS,
    #          connective=Connective(LogicOperatorEnum.AND),
    #          antecedents=[
    #              Antecedent(aid=1,
    #                         atype=AntecedentTypeEnum.FUZZY_TREND,
    #                         metric=AvailableMetricEnum.COST_PER_RESULT.value,
    #                         operator=LogicOperatorEnum.EQUALS,
    #                         expected_value=GoogleLinguisticVariableEnum.INCREASING)
    #          ]),
    RuleBase(rtype=GoogleRuleTypeEnum.AUDIENCE,
             channel=ChannelEnum.GOOGLE,
             category=GoogleRuleCategoryEnum.OPTIMIZE_TARGETING,
             importance=GoogleRuleImportanceEnum.MEDIUM,
             source=GoogleRuleSourceEnum.DEXTER,
             level=LevelEnum.ADGROUP,
             action=GoogleActionEnum.REMOVE,
             redirect=GoogleRuleRedirectEnum.CAMPAIGN_MANAGER,
             template="Your <id=1&metric_name=ROAS&metric_type=1&antecedent_type=7> has decreased by <id=1&value=null>% in the last "
                      "<id=1&time_interval=7> days for some of the genders you are targeting. Dexter recommends you stop targeting the "
                      "following genders <id=1&breakdown_values=null>.",
             breakdown_metadata=BreakdownMetadataBase(breakdown=GoogleBreakdownEnum.GENDER,
                                                      action_breakdown=GoogleActionBreakdownEnum.NONE),
             time_interval=DaysEnum.THREE_MONTHS,
             connective=Connective(LogicOperatorEnum.AND),
             antecedents=[
                 Antecedent(aid=1,
                            atype=AntecedentTypeEnum.FUZZY_TREND,
                            metric=GoogleAvailableMetricEnum.ROAS.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=GoogleLinguisticVariableEnum.DECREASING)
             ]),
    RuleBase(rtype=GoogleRuleTypeEnum.AUDIENCE,
             channel=ChannelEnum.GOOGLE,
             category=GoogleRuleCategoryEnum.OPTIMIZE_TARGETING,
             importance=GoogleRuleImportanceEnum.MEDIUM,
             source=GoogleRuleSourceEnum.DEXTER,
             level=LevelEnum.ADGROUP,
             action=GoogleActionEnum.REMOVE,
             redirect=GoogleRuleRedirectEnum.CAMPAIGN_MANAGER,
             template="Your <id=1&metric_name=CR&metric_type=1&antecedent_type=8> has decreased by <id=1&value=null>% in the last "
                      "<id=1&time_interval=7> days for some of the genders you are targeting. Dexter recommends you stop targeting the "
                      "following genders <id=1&breakdown_values=null>.",
             breakdown_metadata=BreakdownMetadataBase(breakdown=GoogleBreakdownEnum.GENDER,
                                                      action_breakdown=GoogleActionBreakdownEnum.NONE),
             time_interval=DaysEnum.THREE_MONTHS,
             connective=Connective(LogicOperatorEnum.AND),
             antecedents=[
                 Antecedent(aid=1,
                            atype=AntecedentTypeEnum.FUZZY_TREND,
                            metric=GoogleAvailableMetricEnum.CR.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=GoogleLinguisticVariableEnum.DECREASING)
             ]),
    # RuleBase(rtype=GoogleRuleTypeEnum.AUDIENCE,
    #          channel=ChannelEnum.GOOGLE,
    #          category=GoogleRuleCategoryEnum.OPTIMIZE_TARGETING,
    #          importance=GoogleRuleImportanceEnum.MEDIUM,
    #          source=GoogleRuleSourceEnum.DEXTER,
    #          level=LevelEnum.ADGROUP,
    #          action=GoogleActionEnum.REMOVE,
    #          redirect=GoogleRuleRedirectEnum.CAMPAIGN_MANAGER,
    #          template="Your <id=1&metric_name=RSVPS&metric_type=1&antecedent_type=8> have decreased by <id=1&value=null> % in the last "
    #                   "<id=1&time_interval=7> for some of the genders you are targeting. Dexter recommends you stop targeting the "
    #                   "following genders <id=1&breakdown_values=null>.",
    #          breakdown_metadata=BreakdownMetadataBase(breakdown=GoogleBreakdownEnum.GENDER,
    #                                               action_breakdown=GoogleActionBreakdownEnum.NONE),
    #          time_interval=DaysEnum.THREE_MONTHS,
    #          connective=Connective(LogicOperatorEnum.AND),
    #          antecedents=[
    #              Antecedent(aid=1,
    #                         atype=AntecedentTypeEnum.FUZZY_TREND,
    #                         metric=AvailableMetricEnum.RSVPS.value,
    #                         operator=LogicOperatorEnum.EQUALS,
    #                         expected_value=GoogleLinguisticVariableEnum.DECREASING)
    #          ]),
    RuleBase(rtype=GoogleRuleTypeEnum.AUDIENCE,
             channel=ChannelEnum.GOOGLE,
             category=GoogleRuleCategoryEnum.OPTIMIZE_TARGETING,
             importance=GoogleRuleImportanceEnum.MEDIUM,
             source=GoogleRuleSourceEnum.DEXTER,
             level=LevelEnum.ADGROUP,
             action=GoogleActionEnum.REMOVE,
             redirect=GoogleRuleRedirectEnum.CAMPAIGN_MANAGER,
             template="Your <id=1&metric_name=LEADS&metric_type=1&antecedent_type=8> have decreased by <id=1&value=null>% in the last "
                      "<id=1&time_interval=7> days for some of the genders you are targeting. Dexter recommends you stop targeting the "
                      "following genders <id=1&breakdown_values=null>.",
             breakdown_metadata=BreakdownMetadataBase(breakdown=GoogleBreakdownEnum.GENDER,
                                                      action_breakdown=GoogleActionBreakdownEnum.NONE),
             time_interval=DaysEnum.THREE_MONTHS,
             connective=Connective(LogicOperatorEnum.AND),
             antecedents=[
                 Antecedent(aid=1,
                            atype=AntecedentTypeEnum.FUZZY_TREND,
                            metric=GoogleAvailableMetricEnum.LEADS.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=GoogleLinguisticVariableEnum.DECREASING)
             ]),
    RuleBase(rtype=GoogleRuleTypeEnum.AUDIENCE,
             channel=ChannelEnum.GOOGLE,
             category=GoogleRuleCategoryEnum.OPTIMIZE_TARGETING,
             importance=GoogleRuleImportanceEnum.MEDIUM,
             source=GoogleRuleSourceEnum.DEXTER,
             level=LevelEnum.ADGROUP,
             action=GoogleActionEnum.REMOVE,
             redirect=GoogleRuleRedirectEnum.CAMPAIGN_MANAGER,
             template="Your <id=1&metric_name=CTR&metric_type=1&antecedent_type=8> has decreased by <id=1&value=null>% in the last "
                      "<id=1&time_interval=7> days for some of the genders you are targeting. Dexter recommends you stop targeting the "
                      "following genders <id=1&breakdown_values=null>.",
             breakdown_metadata=BreakdownMetadataBase(breakdown=GoogleBreakdownEnum.GENDER,
                                                      action_breakdown=GoogleActionBreakdownEnum.NONE),
             time_interval=DaysEnum.THREE_MONTHS,
             connective=Connective(LogicOperatorEnum.AND),
             antecedents=[
                 Antecedent(aid=1,
                            atype=AntecedentTypeEnum.FUZZY_TREND,
                            metric=GoogleAvailableMetricEnum.CTR.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=GoogleLinguisticVariableEnum.DECREASING)
             ]),
    RuleBase(rtype=GoogleRuleTypeEnum.AUDIENCE,
             channel=ChannelEnum.GOOGLE,
             category=GoogleRuleCategoryEnum.OPTIMIZE_TARGETING,
             importance=GoogleRuleImportanceEnum.MEDIUM,
             source=GoogleRuleSourceEnum.DEXTER,
             level=LevelEnum.ADGROUP,
             action=GoogleActionEnum.REMOVE,
             redirect=GoogleRuleRedirectEnum.CAMPAIGN_MANAGER,
             template="Your <id=1&metric_name=CPC&metric_type=1&antecedent_type=8> has increased by <id=1&value=null>% in the last "
                      "<id=1&time_interval=7> days for some of the genders you are targeting. Dexter recommends you stop targeting the "
                      "following genders <id=1&breakdown_values=null>.",
             breakdown_metadata=BreakdownMetadataBase(breakdown=GoogleBreakdownEnum.GENDER,
                                                      action_breakdown=GoogleActionBreakdownEnum.NONE),
             time_interval=DaysEnum.THREE_MONTHS,
             connective=Connective(LogicOperatorEnum.AND),
             antecedents=[
                 Antecedent(aid=1,
                            atype=AntecedentTypeEnum.FUZZY_TREND,
                            metric=GoogleAvailableMetricEnum.CPC.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=GoogleLinguisticVariableEnum.INCREASING)
             ]),
    RuleBase(rtype=GoogleRuleTypeEnum.AUDIENCE,
             channel=ChannelEnum.GOOGLE,
             category=GoogleRuleCategoryEnum.OPTIMIZE_TARGETING,
             importance=GoogleRuleImportanceEnum.MEDIUM,
             source=GoogleRuleSourceEnum.DEXTER,
             level=LevelEnum.ADGROUP,
             action=GoogleActionEnum.REMOVE,
             redirect=GoogleRuleRedirectEnum.CAMPAIGN_MANAGER,
             template="Your <id=1&metric_name=LINK_CLICKS&metric_type=1&antecedent_type=8> have decreased by <id=1&value=null>% in the last "
                      "<id=1&time_interval=7> days for some of the genders you are targeting. Dexter recommends you stop targeting the "
                      "following genders <id=1&breakdown_values=null>.",
             breakdown_metadata=BreakdownMetadataBase(breakdown=GoogleBreakdownEnum.GENDER,
                                                      action_breakdown=GoogleActionBreakdownEnum.NONE),
             time_interval=DaysEnum.THREE_MONTHS,
             connective=Connective(LogicOperatorEnum.AND),
             antecedents=[
                 Antecedent(aid=1,
                            atype=AntecedentTypeEnum.FUZZY_TREND,
                            metric=GoogleAvailableMetricEnum.LINK_CLICKS.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=GoogleLinguisticVariableEnum.DECREASING)
             ]),
    # RuleBase(rtype=GoogleRuleTypeEnum.AUDIENCE,
    #          channel=ChannelEnum.GOOGLE,
    #          category=GoogleRuleCategoryEnum.OPTIMIZE_TARGETING,
    #          importance=GoogleRuleImportanceEnum.MEDIUM,
    #          source=GoogleRuleSourceEnum.DEXTER,
    #          level=LevelEnum.ADGROUP,
    #          action=GoogleActionEnum.REMOVE,
    #          redirect=GoogleRuleRedirectEnum.CAMPAIGN_MANAGER,
    #          template="Your <id=1&metric_name=PAGE_LIKES&metric_type=1&antecedent_type=8> have decreased by <id=1&value=null> % in the last "
    #                   "<id=1&time_interval=7> for some of the genders you are targeting. Dexter recommends you stop targeting the "
    #                   "following genders <id=1&breakdown_values=null>.",
    #          breakdown_metadata=BreakdownMetadataBase(breakdown=GoogleBreakdownEnum.GENDER,
    #                                               action_breakdown=GoogleActionBreakdownEnum.NONE),
    #          time_interval=DaysEnum.THREE_MONTHS,
    #          connective=Connective(LogicOperatorEnum.AND),
    #          antecedents=[
    #              Antecedent(aid=1,
    #                         atype=AntecedentTypeEnum.FUZZY_TREND,
    #                         metric=AvailableMetricEnum.PAGE_LIKES.value,
    #                         operator=LogicOperatorEnum.EQUALS,
    #                         expected_value=GoogleLinguisticVariableEnum.DECREASING)
    #          ]),
    RuleBase(rtype=GoogleRuleTypeEnum.AUDIENCE,
             channel=ChannelEnum.GOOGLE,
             category=GoogleRuleCategoryEnum.OPTIMIZE_TARGETING,
             importance=GoogleRuleImportanceEnum.MEDIUM,
             source=GoogleRuleSourceEnum.DEXTER,
             level=LevelEnum.ADGROUP,
             action=GoogleActionEnum.REMOVE,
             redirect=GoogleRuleRedirectEnum.CAMPAIGN_MANAGER,
             template="Your <id=1&metric_name=IMPRESSIONS&metric_type=1&antecedent_type=8> have decreased by <id=1&value=null>% in the last "
                      "<id=1&time_interval=7> days for some of the genders you are targeting. Dexter recommends you stop targeting the "
                      "following genders <id=1&breakdown_values=null>.",
             breakdown_metadata=BreakdownMetadataBase(breakdown=GoogleBreakdownEnum.GENDER,
                                                      action_breakdown=GoogleActionBreakdownEnum.NONE),
             time_interval=DaysEnum.THREE_MONTHS,
             connective=Connective(LogicOperatorEnum.AND),
             antecedents=[
                 Antecedent(aid=1,
                            atype=AntecedentTypeEnum.FUZZY_TREND,
                            metric=GoogleAvailableMetricEnum.IMPRESSIONS.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=GoogleLinguisticVariableEnum.DECREASING)
             ]),
    RuleBase(rtype=GoogleRuleTypeEnum.AUDIENCE,
             channel=ChannelEnum.GOOGLE,
             category=GoogleRuleCategoryEnum.OPTIMIZE_TARGETING,
             importance=GoogleRuleImportanceEnum.MEDIUM,
             source=GoogleRuleSourceEnum.DEXTER,
             level=LevelEnum.ADGROUP,
             action=GoogleActionEnum.REMOVE,
             redirect=GoogleRuleRedirectEnum.CAMPAIGN_MANAGER,
             template="Your <id=1&metric_name=PURCHASES&metric_type=1&antecedent_type=8> have decreased by <id=1&value=null>% in the last "
                      "<id=1&time_interval=7> days for some of the genders you are targeting. Dexter recommends you stop targeting the "
                      "following genders <id=1&breakdown_values=null>.",
             breakdown_metadata=BreakdownMetadataBase(breakdown=GoogleBreakdownEnum.GENDER,
                                                      action_breakdown=GoogleActionBreakdownEnum.NONE),
             time_interval=DaysEnum.THREE_MONTHS,
             connective=Connective(LogicOperatorEnum.AND),
             antecedents=[
                 Antecedent(aid=1,
                            atype=AntecedentTypeEnum.FUZZY_TREND,
                            metric=GoogleAvailableMetricEnum.PURCHASES.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=GoogleLinguisticVariableEnum.DECREASING)
             ]),
    RuleBase(rtype=GoogleRuleTypeEnum.AUDIENCE,
             channel=ChannelEnum.GOOGLE,
             category=GoogleRuleCategoryEnum.OPTIMIZE_TARGETING,
             importance=GoogleRuleImportanceEnum.MEDIUM,
             source=GoogleRuleSourceEnum.DEXTER,
             level=LevelEnum.ADGROUP,
             action=GoogleActionEnum.REMOVE,
             redirect=GoogleRuleRedirectEnum.CAMPAIGN_MANAGER,
             template="Your <id=1&metric_name=COST_PER_PURCHASE&metric_type=1&antecedent_type=8> has increased by <id=1&value=null>% in the last "
                      "<id=1&time_interval=7> days for some of the genders you are targeting. Dexter recommends you stop targeting the "
                      "following genders <id=1&breakdown_values=null>.",
             breakdown_metadata=BreakdownMetadataBase(breakdown=GoogleBreakdownEnum.GENDER,
                                                      action_breakdown=GoogleActionBreakdownEnum.NONE),
             time_interval=DaysEnum.THREE_MONTHS,
             connective=Connective(LogicOperatorEnum.AND),
             antecedents=[
                 Antecedent(aid=1,
                            atype=AntecedentTypeEnum.FUZZY_TREND,
                            metric=GoogleAvailableMetricEnum.COST_PER_CONVERSION.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=GoogleLinguisticVariableEnum.INCREASING)
             ]),
    # RuleBase(rtype=GoogleRuleTypeEnum.AUDIENCE,
    #          channel=ChannelEnum.GOOGLE,
    #          category=GoogleRuleCategoryEnum.OPTIMIZE_TARGETING,
    #          importance=GoogleRuleImportanceEnum.MEDIUM,
    #          source=GoogleRuleSourceEnum.DEXTER,
    #          level=LevelEnum.ADGROUP,
    #          action=GoogleActionEnum.REMOVE,
    #          redirect=GoogleRuleRedirectEnum.CAMPAIGN_MANAGER,
    #          template="Your <id=1&metric_name=COST_PER_THRUPLAY&metric_type=1&antecedent_type=8> has increased by <id=1&value=null> % in the last "
    #                   "<id=1&time_interval=7> for some of the genders you are targeting. Dexter recommends you stop targeting the "
    #                   "following genders <id=1&breakdown_values=null>.",
    #          breakdown_metadata=BreakdownMetadataBase(breakdown=GoogleBreakdownEnum.GENDER,
    #                                               action_breakdown=GoogleActionBreakdownEnum.NONE),
    #          time_interval=DaysEnum.THREE_MONTHS,
    #          connective=Connective(LogicOperatorEnum.AND),
    #          antecedents=[
    #              Antecedent(aid=1,
    #                         atype=AntecedentTypeEnum.FUZZY_TREND,
    #                         metric=AvailableMetricEnum.COST_PER_THRUPLAY.value,
    #                         operator=LogicOperatorEnum.EQUALS,
    #                         expected_value=GoogleLinguisticVariableEnum.INCREASING)
    #          ]),
    # RuleBase(rtype=GoogleRuleTypeEnum.AUDIENCE,
    #          channel=ChannelEnum.GOOGLE,
    #          category=GoogleRuleCategoryEnum.OPTIMIZE_TARGETING,
    #          importance=GoogleRuleImportanceEnum.MEDIUM,
    #          source=GoogleRuleSourceEnum.DEXTER,
    #          level=LevelEnum.ADGROUP,
    #          action=GoogleActionEnum.REMOVE,
    #          redirect=GoogleRuleRedirectEnum.CAMPAIGN_MANAGER,
    #          template="Your <id=1&metric_name=VIDEO_PLAYS&metric_type=1&antecedent_type=8> have decreased by <id=1&value=null> % in the last "
    #                   "<id=1&time_interval=7> for some of the genders you are targeting. Dexter recommends you stop targeting the "
    #                   "following genders <id=1&breakdown_values=null>.",
    #          breakdown_metadata=BreakdownMetadataBase(breakdown=GoogleBreakdownEnum.GENDER,
    #                                               action_breakdown=GoogleActionBreakdownEnum.NONE),
    #          time_interval=DaysEnum.THREE_MONTHS,
    #          connective=Connective(LogicOperatorEnum.AND),
    #          antecedents=[
    #              Antecedent(aid=1,
    #                         atype=AntecedentTypeEnum.FUZZY_TREND,
    #                         metric=AvailableMetricEnum.VIDEO_PLAYS.value,
    #                         operator=LogicOperatorEnum.EQUALS,
    #                         expected_value=GoogleLinguisticVariableEnum.DECREASING)
    #          ]),
]
