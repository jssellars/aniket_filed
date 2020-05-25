from FacebookDexter.Engine.Algorithms.FuzzyRuleBasedOptimization.Metrics.AvailableMetricEnum import AvailableMetricEnum
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

RULES_ADSET_REMOVE_PLACEMENT = [
    RuleBase(rtype=RuleTypeEnum.AUDIENCE,
             channel=ChannelEnum.FACEBOOK,
             category=RuleCategoryEnum.OPTIMIZE_TARGETING,
             importance=RuleImportanceEnum.MEDIUM,
             source=RuleSourceEnum.DEXTER,
             level=LevelEnum.ADSET,
             action=ActionEnum.REMOVE,
             redirect=RuleRedirectEnum.CAMPAIGN_MANAGER,
             template="Your <id=1&metric_name=RESULTS&metric_type=1&antecedent_type=8> has decreased by <id=1&value=null>% in the last "
                      "<id=1&time_interval=7> days for some of the placements you are targeting. Dexter recommends you stop targeting the "
                      "following placements <id=1&breakdown_values=null>.",
             breakdown_metadata=BreakdownMetadata(breakdown=BreakdownEnum.PLACEMENT,
                                                  action_breakdown=ActionBreakdownEnum.NONE),
             time_interval=DaysEnum.THREE_MONTHS,
             connective=Connective(LogicOperatorEnum.AND),
             antecedents=[
                 Antecedent(aid=1,
                            atype=AntecedentTypeEnum.FUZZY_TREND,
                            metric=AvailableMetricEnum.RESULTS.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=LinguisticVariableEnum.DECREASING)
             ]),
    RuleBase(rtype=RuleTypeEnum.AUDIENCE,
             channel=ChannelEnum.FACEBOOK,
             category=RuleCategoryEnum.OPTIMIZE_TARGETING,
             importance=RuleImportanceEnum.MEDIUM,
             source=RuleSourceEnum.DEXTER,
             level=LevelEnum.ADSET,
             action=ActionEnum.REMOVE,
             redirect=RuleRedirectEnum.CAMPAIGN_MANAGER,
             template="Your <id=1&metric_name=COST_PER_APP_INSTALL&metric_type=1&antecedent_type=8> has increased by <id=1&value=null>% in the last "
                      "<id=1&time_interval=7> days for some of the placements you are targeting. Dexter recommends you stop targeting the "
                      "following placements <id=1&breakdown_values=null>.",
             breakdown_metadata=BreakdownMetadata(breakdown=BreakdownEnum.PLACEMENT,
                                                  action_breakdown=ActionBreakdownEnum.NONE),
             time_interval=DaysEnum.THREE_MONTHS,
             connective=Connective(LogicOperatorEnum.AND),
             antecedents=[
                 Antecedent(aid=1,
                            atype=AntecedentTypeEnum.FUZZY_TREND,
                            metric=AvailableMetricEnum.COST_PER_APP_INSTALL.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=LinguisticVariableEnum.INCREASING)
             ]),
    RuleBase(rtype=RuleTypeEnum.AUDIENCE,
             channel=ChannelEnum.FACEBOOK,
             category=RuleCategoryEnum.OPTIMIZE_TARGETING,
             importance=RuleImportanceEnum.MEDIUM,
             source=RuleSourceEnum.DEXTER,
             level=LevelEnum.ADSET,
             action=ActionEnum.REMOVE,
             redirect=RuleRedirectEnum.CAMPAIGN_MANAGER,
             template="Your <id=1&metric_name=CPM&metric_type=1&antecedent_type=8> has increased by <id=1&value=null>% in the last "
                      "<id=1&time_interval=7> days for some of the placements you are targeting. Dexter recommends you stop targeting the "
                      "following placements <id=1&breakdown_values=null>.",
             breakdown_metadata=BreakdownMetadata(breakdown=BreakdownEnum.PLACEMENT,
                                                  action_breakdown=ActionBreakdownEnum.NONE),
             time_interval=DaysEnum.THREE_MONTHS,
             connective=Connective(LogicOperatorEnum.AND),
             antecedents=[
                 Antecedent(aid=1,
                            atype=AntecedentTypeEnum.FUZZY_TREND,
                            metric=AvailableMetricEnum.CPM.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=LinguisticVariableEnum.INCREASING)
             ]),
    RuleBase(rtype=RuleTypeEnum.AUDIENCE,
             channel=ChannelEnum.FACEBOOK,
             category=RuleCategoryEnum.OPTIMIZE_TARGETING,
             importance=RuleImportanceEnum.MEDIUM,
             source=RuleSourceEnum.DEXTER,
             level=LevelEnum.ADSET,
             action=ActionEnum.REMOVE,
             redirect=RuleRedirectEnum.CAMPAIGN_MANAGER,
             template="Your <id=1&metric_name=REACH&metric_type=1&antecedent_type=8> has decreased by <id=1&value=null>% in the last "
                      "<id=1&time_interval=7> days for some of the placements you are targeting. Dexter recommends you stop targeting the "
                      "following placements <id=1&breakdown_values=null>.",
             breakdown_metadata=BreakdownMetadata(breakdown=BreakdownEnum.PLACEMENT,
                                                  action_breakdown=ActionBreakdownEnum.NONE),
             time_interval=DaysEnum.THREE_MONTHS,
             connective=Connective(LogicOperatorEnum.AND),
             antecedents=[
                 Antecedent(aid=1,
                            atype=AntecedentTypeEnum.FUZZY_TREND,
                            metric=AvailableMetricEnum.REACH.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=LinguisticVariableEnum.DECREASING)
             ]),
    RuleBase(rtype=RuleTypeEnum.AUDIENCE,
             channel=ChannelEnum.FACEBOOK,
             category=RuleCategoryEnum.OPTIMIZE_TARGETING,
             importance=RuleImportanceEnum.MEDIUM,
             source=RuleSourceEnum.DEXTER,
             level=LevelEnum.ADSET,
             action=ActionEnum.REMOVE,
             redirect=RuleRedirectEnum.CAMPAIGN_MANAGER,
             template="Your <id=1&metric_name=ENGAGEMENT_RATE&metric_type=1&antecedent_type=8> has decreased by <id=1&value=null>% in the last "
                      "<id=1&time_interval=7> days for some of the placements you are targeting. Dexter recommends you stop targeting the "
                      "following placements <id=1&breakdown_values=null>.",
             breakdown_metadata=BreakdownMetadata(breakdown=BreakdownEnum.PLACEMENT,
                                                  action_breakdown=ActionBreakdownEnum.NONE),
             time_interval=DaysEnum.THREE_MONTHS,
             connective=Connective(LogicOperatorEnum.AND),
             antecedents=[
                 Antecedent(aid=1,
                            atype=AntecedentTypeEnum.FUZZY_TREND,
                            metric=AvailableMetricEnum.ENGAGEMENT_RATE.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=LinguisticVariableEnum.DECREASING)
             ]),
    RuleBase(rtype=RuleTypeEnum.AUDIENCE,
             channel=ChannelEnum.FACEBOOK,
             category=RuleCategoryEnum.OPTIMIZE_TARGETING,
             importance=RuleImportanceEnum.MEDIUM,
             source=RuleSourceEnum.DEXTER,
             level=LevelEnum.ADSET,
             action=ActionEnum.REMOVE,
             redirect=RuleRedirectEnum.CAMPAIGN_MANAGER,
             template="Your <id=1&metric_name=ENGAGEMENT_RATE&metric_type=1&antecedent_type=8> has increased by <id=1&value=null>% in the last "
                      "<id=1&time_interval=7> days for some of the placements you are targeting. Dexter recommends you stop targeting the "
                      "following placements <id=1&breakdown_values=null>.",
             breakdown_metadata=BreakdownMetadata(breakdown=BreakdownEnum.PLACEMENT,
                                                  action_breakdown=ActionBreakdownEnum.NONE),
             time_interval=DaysEnum.THREE_MONTHS,
             connective=Connective(LogicOperatorEnum.AND),
             antecedents=[
                 Antecedent(aid=1,
                            atype=AntecedentTypeEnum.FUZZY_TREND,
                            metric=AvailableMetricEnum.COST_PER_RESULT.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=LinguisticVariableEnum.INCREASING)
             ]),
    RuleBase(rtype=RuleTypeEnum.AUDIENCE,
             channel=ChannelEnum.FACEBOOK,
             category=RuleCategoryEnum.OPTIMIZE_TARGETING,
             importance=RuleImportanceEnum.MEDIUM,
             source=RuleSourceEnum.DEXTER,
             level=LevelEnum.ADSET,
             action=ActionEnum.REMOVE,
             redirect=RuleRedirectEnum.CAMPAIGN_MANAGER,
             template="Your <id=1&metric_name=ROAS&metric_type=1&antecedent_type=8> has decreased by <id=1&value=null>% in the last "
                      "<id=1&time_interval=7> days for some of the placements you are targeting. Dexter recommends you stop targeting the "
                      "following placements <id=1&breakdown_values=null>.",
             breakdown_metadata=BreakdownMetadata(breakdown=BreakdownEnum.PLACEMENT,
                                                  action_breakdown=ActionBreakdownEnum.NONE),
             time_interval=DaysEnum.THREE_MONTHS,
             connective=Connective(LogicOperatorEnum.AND),
             antecedents=[
                 Antecedent(aid=1,
                            atype=AntecedentTypeEnum.FUZZY_TREND,
                            metric=AvailableMetricEnum.ROAS.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=LinguisticVariableEnum.DECREASING)
             ]),
    RuleBase(rtype=RuleTypeEnum.AUDIENCE,
             channel=ChannelEnum.FACEBOOK,
             category=RuleCategoryEnum.OPTIMIZE_TARGETING,
             importance=RuleImportanceEnum.MEDIUM,
             source=RuleSourceEnum.DEXTER,
             level=LevelEnum.ADSET,
             action=ActionEnum.REMOVE,
             redirect=RuleRedirectEnum.CAMPAIGN_MANAGER,
             template="Your <id=1&metric_name=CR&metric_type=1&antecedent_type=8> has decreased by <id=1&value=null>% in the last "
                      "<id=1&time_interval=7> days for some of the placements you are targeting. Dexter recommends you stop targeting the "
                      "following placements <id=1&breakdown_values=null>.",
             breakdown_metadata=BreakdownMetadata(breakdown=BreakdownEnum.PLACEMENT,
                                                  action_breakdown=ActionBreakdownEnum.NONE),
             time_interval=DaysEnum.THREE_MONTHS,
             connective=Connective(LogicOperatorEnum.AND),
             antecedents=[
                 Antecedent(aid=1,
                            atype=AntecedentTypeEnum.FUZZY_TREND,
                            metric=AvailableMetricEnum.CR.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=LinguisticVariableEnum.DECREASING)
             ]),
    RuleBase(rtype=RuleTypeEnum.AUDIENCE,
             channel=ChannelEnum.FACEBOOK,
             category=RuleCategoryEnum.OPTIMIZE_TARGETING,
             importance=RuleImportanceEnum.MEDIUM,
             source=RuleSourceEnum.DEXTER,
             level=LevelEnum.ADSET,
             action=ActionEnum.REMOVE,
             redirect=RuleRedirectEnum.CAMPAIGN_MANAGER,
             template="Your <id=1&metric_name=RSVPS&metric_type=1&antecedent_type=8> have decreased by <id=1&value=null>% in the last "
                      "<id=1&time_interval=7> days for some of the placements you are targeting. Dexter recommends you stop targeting the "
                      "following placements <id=1&breakdown_values=null>.",
             breakdown_metadata=BreakdownMetadata(breakdown=BreakdownEnum.PLACEMENT,
                                                  action_breakdown=ActionBreakdownEnum.NONE),
             time_interval=DaysEnum.THREE_MONTHS,
             connective=Connective(LogicOperatorEnum.AND),
             antecedents=[
                 Antecedent(aid=1,
                            atype=AntecedentTypeEnum.FUZZY_TREND,
                            metric=AvailableMetricEnum.RSVPS.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=LinguisticVariableEnum.DECREASING)
             ]),
    RuleBase(rtype=RuleTypeEnum.AUDIENCE,
             channel=ChannelEnum.FACEBOOK,
             category=RuleCategoryEnum.OPTIMIZE_TARGETING,
             importance=RuleImportanceEnum.MEDIUM,
             source=RuleSourceEnum.DEXTER,
             level=LevelEnum.ADSET,
             action=ActionEnum.REMOVE,
             redirect=RuleRedirectEnum.CAMPAIGN_MANAGER,
             template="Your <id=1&metric_name=LEADS&metric_type=1&antecedent_type=8> have decreased by <id=1&value=null>% in the last "
                      "<id=1&time_interval=7> days for some of the placements you are targeting. Dexter recommends you stop targeting the "
                      "following placements <id=1&breakdown_values=null>.",
             breakdown_metadata=BreakdownMetadata(breakdown=BreakdownEnum.PLACEMENT,
                                                  action_breakdown=ActionBreakdownEnum.NONE),
             time_interval=DaysEnum.THREE_MONTHS,
             connective=Connective(LogicOperatorEnum.AND),
             antecedents=[
                 Antecedent(aid=1,
                            atype=AntecedentTypeEnum.FUZZY_TREND,
                            metric=AvailableMetricEnum.LEADS.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=LinguisticVariableEnum.DECREASING)
             ]),
    RuleBase(rtype=RuleTypeEnum.AUDIENCE,
             channel=ChannelEnum.FACEBOOK,
             category=RuleCategoryEnum.OPTIMIZE_TARGETING,
             importance=RuleImportanceEnum.MEDIUM,
             source=RuleSourceEnum.DEXTER,
             level=LevelEnum.ADSET,
             action=ActionEnum.REMOVE,
             redirect=RuleRedirectEnum.CAMPAIGN_MANAGER,
             template="Your <id=1&metric_name=CTR&metric_type=1&antecedent_type=8> has decreased by <id=1&value=null>% in the last "
                      "<id=1&time_interval=7> days for some of the placements you are targeting. Dexter recommends you stop targeting the "
                      "following placements <id=1&breakdown_values=null>.",
             breakdown_metadata=BreakdownMetadata(breakdown=BreakdownEnum.PLACEMENT,
                                                  action_breakdown=ActionBreakdownEnum.NONE),
             time_interval=DaysEnum.THREE_MONTHS,
             connective=Connective(LogicOperatorEnum.AND),
             antecedents=[
                 Antecedent(aid=1,
                            atype=AntecedentTypeEnum.FUZZY_TREND,
                            metric=AvailableMetricEnum.CTR.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=LinguisticVariableEnum.DECREASING)
             ]),
    RuleBase(rtype=RuleTypeEnum.AUDIENCE,
             channel=ChannelEnum.FACEBOOK,
             category=RuleCategoryEnum.OPTIMIZE_TARGETING,
             importance=RuleImportanceEnum.MEDIUM,
             source=RuleSourceEnum.DEXTER,
             level=LevelEnum.ADSET,
             action=ActionEnum.REMOVE,
             redirect=RuleRedirectEnum.CAMPAIGN_MANAGER,
             template="Your <id=1&metric_name=CPC&metric_type=1&antecedent_type=8> has increased by <id=1&value=null>% in the last "
                      "<id=1&time_interval=7> days for some of the placements you are targeting. Dexter recommends you stop targeting the "
                      "following placements <id=1&breakdown_values=null>.",
             breakdown_metadata=BreakdownMetadata(breakdown=BreakdownEnum.PLACEMENT,
                                                  action_breakdown=ActionBreakdownEnum.NONE),
             time_interval=DaysEnum.THREE_MONTHS,
             connective=Connective(LogicOperatorEnum.AND),
             antecedents=[
                 Antecedent(aid=1,
                            atype=AntecedentTypeEnum.FUZZY_TREND,
                            metric=AvailableMetricEnum.CPC.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=LinguisticVariableEnum.INCREASING)
             ]),
    RuleBase(rtype=RuleTypeEnum.AUDIENCE,
             channel=ChannelEnum.FACEBOOK,
             category=RuleCategoryEnum.OPTIMIZE_TARGETING,
             importance=RuleImportanceEnum.MEDIUM,
             source=RuleSourceEnum.DEXTER,
             level=LevelEnum.ADSET,
             action=ActionEnum.REMOVE,
             redirect=RuleRedirectEnum.CAMPAIGN_MANAGER,
             template="Your <id=1&metric_name=LINK_CLICKS&metric_type=1&antecedent_type=8> have decreased by <id=1&value=null>% in the last "
                      "<id=1&time_interval=7> days for some of the placements you are targeting. Dexter recommends you stop targeting the "
                      "following placements <id=1&breakdown_values=null>.",
             breakdown_metadata=BreakdownMetadata(breakdown=BreakdownEnum.PLACEMENT,
                                                  action_breakdown=ActionBreakdownEnum.NONE),
             time_interval=DaysEnum.THREE_MONTHS,
             connective=Connective(LogicOperatorEnum.AND),
             antecedents=[
                 Antecedent(aid=1,
                            atype=AntecedentTypeEnum.FUZZY_TREND,
                            metric=AvailableMetricEnum.LINK_CLICKS.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=LinguisticVariableEnum.DECREASING)
             ]),
    RuleBase(rtype=RuleTypeEnum.AUDIENCE,
             channel=ChannelEnum.FACEBOOK,
             category=RuleCategoryEnum.OPTIMIZE_TARGETING,
             importance=RuleImportanceEnum.MEDIUM,
             source=RuleSourceEnum.DEXTER,
             level=LevelEnum.ADSET,
             action=ActionEnum.REMOVE,
             redirect=RuleRedirectEnum.CAMPAIGN_MANAGER,
             template="Your <id=1&metric_name=PAGE_LIKES&metric_type=1&antecedent_type=8> have decreased by <id=1&value=null>% in the last "
                      "<id=1&time_interval=7> days for some of the placements you are targeting. Dexter recommends you stop targeting the "
                      "following placements <id=1&breakdown_values=null>.",
             breakdown_metadata=BreakdownMetadata(breakdown=BreakdownEnum.PLACEMENT,
                                                  action_breakdown=ActionBreakdownEnum.NONE),
             time_interval=DaysEnum.THREE_MONTHS,
             connective=Connective(LogicOperatorEnum.AND),
             antecedents=[
                 Antecedent(aid=1,
                            atype=AntecedentTypeEnum.FUZZY_TREND,
                            metric=AvailableMetricEnum.PAGE_LIKES.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=LinguisticVariableEnum.DECREASING)
             ]),
    RuleBase(rtype=RuleTypeEnum.AUDIENCE,
             channel=ChannelEnum.FACEBOOK,
             category=RuleCategoryEnum.OPTIMIZE_TARGETING,
             importance=RuleImportanceEnum.MEDIUM,
             source=RuleSourceEnum.DEXTER,
             level=LevelEnum.ADSET,
             action=ActionEnum.REMOVE,
             redirect=RuleRedirectEnum.CAMPAIGN_MANAGER,
             template="Your <id=1&metric_name=IMPRESSIONS&metric_type=1&antecedent_type=8> have decreased by <id=1&value=null>% in the last "
                      "<id=1&time_interval=7> days for some of the placements you are targeting. Dexter recommends you stop targeting the "
                      "following placements <id=1&breakdown_values=null>.",
             breakdown_metadata=BreakdownMetadata(breakdown=BreakdownEnum.PLACEMENT,
                                                  action_breakdown=ActionBreakdownEnum.NONE),
             time_interval=DaysEnum.THREE_MONTHS,
             connective=Connective(LogicOperatorEnum.AND),
             antecedents=[
                 Antecedent(aid=1,
                            atype=AntecedentTypeEnum.FUZZY_TREND,
                            metric=AvailableMetricEnum.IMPRESSIONS.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=LinguisticVariableEnum.DECREASING)
             ]),
    RuleBase(rtype=RuleTypeEnum.AUDIENCE,
             channel=ChannelEnum.FACEBOOK,
             category=RuleCategoryEnum.OPTIMIZE_TARGETING,
             importance=RuleImportanceEnum.MEDIUM,
             source=RuleSourceEnum.DEXTER,
             level=LevelEnum.ADSET,
             action=ActionEnum.REMOVE,
             redirect=RuleRedirectEnum.CAMPAIGN_MANAGER,
             template="Your <id=1&metric_name=PURCHASES&metric_type=1&antecedent_type=8> have decreased by <id=1&value=null>% in the last "
                      "<id=1&time_interval=7> days for some of the placements you are targeting. Dexter recommends you stop targeting the "
                      "following placements <id=1&breakdown_values=null>.",
             breakdown_metadata=BreakdownMetadata(breakdown=BreakdownEnum.PLACEMENT,
                                                  action_breakdown=ActionBreakdownEnum.NONE),
             time_interval=DaysEnum.THREE_MONTHS,
             connective=Connective(LogicOperatorEnum.AND),
             antecedents=[
                 Antecedent(aid=1,
                            atype=AntecedentTypeEnum.FUZZY_TREND,
                            metric=AvailableMetricEnum.PURCHASES.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=LinguisticVariableEnum.DECREASING)
             ]),
    RuleBase(rtype=RuleTypeEnum.AUDIENCE,
             channel=ChannelEnum.FACEBOOK,
             category=RuleCategoryEnum.OPTIMIZE_TARGETING,
             importance=RuleImportanceEnum.MEDIUM,
             source=RuleSourceEnum.DEXTER,
             level=LevelEnum.ADSET,
             action=ActionEnum.REMOVE,
             redirect=RuleRedirectEnum.CAMPAIGN_MANAGER,
             template="Your <id=1&metric_name=COST_PER_PURCHASE&metric_type=1&antecedent_type=8> has increased by <id=1&value=null>% in the last "
                      "<id=1&time_interval=7> days for some of the placements you are targeting. Dexter recommends you stop targeting the "
                      "following placements <id=1&breakdown_values=null>.",
             breakdown_metadata=BreakdownMetadata(breakdown=BreakdownEnum.PLACEMENT,
                                                  action_breakdown=ActionBreakdownEnum.NONE),
             time_interval=DaysEnum.THREE_MONTHS,
             connective=Connective(LogicOperatorEnum.AND),
             antecedents=[
                 Antecedent(aid=1,
                            atype=AntecedentTypeEnum.FUZZY_TREND,
                            metric=AvailableMetricEnum.COST_PER_PURCHASE.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=LinguisticVariableEnum.INCREASING)
             ]),
    RuleBase(rtype=RuleTypeEnum.AUDIENCE,
             channel=ChannelEnum.FACEBOOK,
             category=RuleCategoryEnum.OPTIMIZE_TARGETING,
             importance=RuleImportanceEnum.MEDIUM,
             source=RuleSourceEnum.DEXTER,
             level=LevelEnum.ADSET,
             action=ActionEnum.REMOVE,
             redirect=RuleRedirectEnum.CAMPAIGN_MANAGER,
             template="Your <id=1&metric_name=COST_PER_THRUPLAY&metric_type=1&antecedent_type=8> has increased by <id=1&value=null>% in the last "
                      "<id=1&time_interval=7> days for some of the placements you are targeting. Dexter recommends you stop targeting the "
                      "following placements <id=1&breakdown_values=null>.",
             breakdown_metadata=BreakdownMetadata(breakdown=BreakdownEnum.PLACEMENT,
                                                  action_breakdown=ActionBreakdownEnum.NONE),
             time_interval=DaysEnum.THREE_MONTHS,
             connective=Connective(LogicOperatorEnum.AND),
             antecedents=[
                 Antecedent(aid=1,
                            atype=AntecedentTypeEnum.FUZZY_TREND,
                            metric=AvailableMetricEnum.COST_PER_THRUPLAY.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=LinguisticVariableEnum.INCREASING)
             ]),
    RuleBase(rtype=RuleTypeEnum.AUDIENCE,
             channel=ChannelEnum.FACEBOOK,
             category=RuleCategoryEnum.OPTIMIZE_TARGETING,
             importance=RuleImportanceEnum.MEDIUM,
             source=RuleSourceEnum.DEXTER,
             level=LevelEnum.ADSET,
             action=ActionEnum.REMOVE,
             redirect=RuleRedirectEnum.CAMPAIGN_MANAGER,
             template="Your <id=1&metric_name=VIDEO_PLAYS&metric_type=1&antecedent_type=8> have decreased by <id=1&value=null>% in the last "
                      "<id=1&time_interval=7> days for some of the placements you are targeting. Dexter recommends you stop targeting the "
                      "following placements <id=1&breakdown_values=null>.",
             breakdown_metadata=BreakdownMetadata(breakdown=BreakdownEnum.PLACEMENT,
                                                  action_breakdown=ActionBreakdownEnum.NONE),
             time_interval=DaysEnum.THREE_MONTHS,
             connective=Connective(LogicOperatorEnum.AND),
             antecedents=[
                 Antecedent(aid=1,
                            atype=AntecedentTypeEnum.FUZZY_TREND,
                            metric=AvailableMetricEnum.VIDEO_PLAYS.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=LinguisticVariableEnum.DECREASING)
             ]),
]
