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
from FacebookDexter.Infrastructure.Domain.Actions.ActionEnums import FacebookActionEnum
from FacebookDexter.Infrastructure.Domain.Breakdowns import FacebookActionBreakdownEnum, FacebookBreakdownEnum
from FacebookDexter.Infrastructure.Domain.FacebookObjectiveEnum import FacebookObjectiveEnum
from FacebookDexter.Infrastructure.Domain.FuzzyEngine.FacebookFuzzySets import FacebookLinguisticVariableEnum
from FacebookDexter.Infrastructure.Domain.Rules.FacebookRuleEnums import FacebookRuleSourceEnum, \
    FacebookRuleRedirectEnum, FacebookRuleImportanceEnum, FacebookRuleCategoryEnum, FacebookRuleTypeEnum

RULES_ADSET_GENERAL = [
    # catalog sales
    RuleBase(rtype=FacebookRuleTypeEnum.PERFORMANCE,
             channel=ChannelEnum.FACEBOOK,
             category=FacebookRuleCategoryEnum.IMPROVE_ROAS,
             importance=FacebookRuleImportanceEnum.HIGH,
             source=FacebookRuleSourceEnum.DEXTER,
             level=LevelEnum.ADSET,
             action=FacebookActionEnum.DUPLICATE,
             redirect=FacebookRuleRedirectEnum.DUPLICATE,
             template="Bring your cost per purchase down significantly by running retargeting campaigns. "
                      "Start this process now to see better results! You can do this by duplicating "
                      "your best performing ad "
                      "<strong>__id=1&metric_name=DUPLICATE_AD&metric_type=10&antecedent_type=1&"
                      "display_metric_name=0____id=1&value=null__</strong> "
                      "and adding retargeting in as your next audience to target.",
             breakdown_metadata=BreakdownMetadataBase(breakdown=FacebookBreakdownEnum.NONE,
                                                      action_breakdown=FacebookActionBreakdownEnum.NONE),
             time_interval=DaysEnum.THREE_MONTHS,
             connective=Connective(LogicOperatorEnum.AND),
             antecedents=[
                 # Antecedent(aid=1,
                 #            atype=AntecedentTypeEnum.VALUE,
                 #            metric=FacebookAvailableMetricEnum.OBJECTIVE.value,
                 #            operator=LogicOperatorEnum.EQUALS,
                 #            expected_value=FacebookObjectiveEnum.PRODUCT_CATALOG_SALES.value),
                 Antecedent(aid=1,
                            atype=AntecedentTypeEnum.FUZZY_TREND,
                            metric=FacebookAvailableMetricEnum.COST_PER_PURCHASE.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=FacebookLinguisticVariableEnum.INCREASING)
             ]),
    RuleBase(rtype=FacebookRuleTypeEnum.PERFORMANCE,
             channel=ChannelEnum.FACEBOOK,
             category=FacebookRuleCategoryEnum.IMPROVE_CPR,
             importance=FacebookRuleImportanceEnum.MEDIUM,
             source=FacebookRuleSourceEnum.DEXTER,
             level=LevelEnum.ADSET,
             action=FacebookActionEnum.DUPLICATE,
             redirect=FacebookRuleRedirectEnum.DUPLICATE,
             template="Dexter has noticed that your cost per result has increased over the last "
                      "__id=1&time_interval=7__ days. "
                      "Dexter suggests that you try creating a lookalike campaign on "
                      "messenger to bring your cost down even more! "
                      "You can do this by duplicating your best performing ad "
                      "<strong>__id=2&metric_name=DUPLICATE_AD&metric_type=10&"
                      "antecedent_type=1&display_metric_name=0____id=2&value=null__</strong> "
                      "and adding retargeting or lookalikes as your next audience to target.",
             breakdown_metadata=BreakdownMetadataBase(breakdown=FacebookBreakdownEnum.NONE,
                                                      action_breakdown=FacebookActionBreakdownEnum.NONE),
             time_interval=DaysEnum.THREE_MONTHS,
             connective=Connective(LogicOperatorEnum.AND),
             antecedents=[
                 # Antecedent(aid=1,
                 #            atype=AntecedentTypeEnum.VALUE,
                 #            metric=FacebookAvailableMetricEnum.OBJECTIVE.value,
                 #            operator=LogicOperatorEnum.EQUALS,
                 #            expected_value=FacebookObjectiveEnum.LINK_CLICKS.value),
                 Antecedent(aid=1,
                            atype=AntecedentTypeEnum.FUZZY_TREND,
                            metric=FacebookAvailableMetricEnum.COST_PER_RESULT.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=FacebookLinguisticVariableEnum.INCREASING)
             ]),
    # messenger
    RuleBase(rtype=FacebookRuleTypeEnum.CREATIVE,
             channel=ChannelEnum.FACEBOOK,
             category=FacebookRuleCategoryEnum.IMPROVE_CPR,
             importance=FacebookRuleImportanceEnum.MEDIUM,
             source=FacebookRuleSourceEnum.DEXTER,
             level=LevelEnum.ADSET,
             action=FacebookActionEnum.DUPLICATE,
             redirect=FacebookRuleRedirectEnum.DUPLICATE,
             template="Dexter has seen your results decrease lately. Have you considered "
                      "launching new ad copy or creatives to boost your results? "
                      "You can do this by duplicating your best performing "
                      "ad <strong>__id=1&metric_name=DUPLICATE_AD&metric_type=10&antecedent_type=1&"
                      "display_metric_name=0____id=1&value=null__</strong> "
                      "now and changing the adcopy or creatives.",
             breakdown_metadata=BreakdownMetadataBase(breakdown=FacebookBreakdownEnum.NONE,
                                                      action_breakdown=FacebookActionBreakdownEnum.NONE),
             time_interval=DaysEnum.THREE_MONTHS,
             connective=Connective(LogicOperatorEnum.AND),
             antecedents=[
                 # Antecedent(aid=1,
                 #            atype=AntecedentTypeEnum.VALUE,
                 #            metric=FacebookAvailableMetricEnum.OBJECTIVE.value,
                 #            operator=LogicOperatorEnum.EQUALS,
                 #            expected_value=FacebookObjectiveEnum.MESSAGES.value),
                 Antecedent(aid=1,
                            atype=AntecedentTypeEnum.FUZZY_TREND,
                            metric=FacebookAvailableMetricEnum.RESULTS.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=FacebookLinguisticVariableEnum.DECREASING)
             ]),

    RuleBase(rtype=FacebookRuleTypeEnum.CREATIVE,
             channel=ChannelEnum.FACEBOOK,
             category=FacebookRuleCategoryEnum.IMPROVE_CTR,
             importance=FacebookRuleImportanceEnum.MEDIUM,
             source=FacebookRuleSourceEnum.DEXTER,
             level=LevelEnum.ADSET,
             action=FacebookActionEnum.DUPLICATE,
             redirect=FacebookRuleRedirectEnum.DUPLICATE,
             template="Dexter noticed that your __id=1&metric_name=CTR&metric_type=1&antecedent_type=8__ "
                      "decreasing over __id=1&time_interval=7__ days which is a sign of ad fatigue. "
                      "Dexter suggests launching new ad creatives to help with this. "
                      "Adding new creatives will give a boost to an existing campaign. "
                      "You do this quickly by duplicating your best performing ad "
                      "<strong>__id=2&metric_name=DUPLICATE_AD&metric_type=10&antecedent_type=1&"
                      "display_metric_name=0____id=2&value=null__</strong> now "
                      "and adding new creatives to this adset.",
             breakdown_metadata=BreakdownMetadataBase(breakdown=FacebookBreakdownEnum.NONE,
                                                      action_breakdown=FacebookActionBreakdownEnum.NONE),
             time_interval=DaysEnum.THREE_MONTHS,
             connective=Connective(LogicOperatorEnum.AND),
             antecedents=[
                 # Antecedent(aid=1,
                 #            atype=AntecedentTypeEnum.VALUE,
                 #            metric=FacebookAvailableMetricEnum.OBJECTIVE.value,
                 #            operator=LogicOperatorEnum.EQUALS,
                 #            expected_value=FacebookObjectiveEnum.LEAD_GENERATION.value),
                 Antecedent(aid=1,
                            atype=AntecedentTypeEnum.FUZZY_TREND,
                            metric=FacebookAvailableMetricEnum.CTR.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=FacebookLinguisticVariableEnum.DECREASING)
             ]),
    RuleBase(rtype=FacebookRuleTypeEnum.CREATIVE,
             channel=ChannelEnum.FACEBOOK,
             category=FacebookRuleCategoryEnum.IMPROVE_CONVERSION_RATE,
             importance=FacebookRuleImportanceEnum.LOW,
             source=FacebookRuleSourceEnum.DEXTER,
             level=LevelEnum.ADSET,
             action=FacebookActionEnum.DUPLICATE,
             redirect=FacebookRuleRedirectEnum.DUPLICATE,
             template="Dexter doesn’t like __id=1&metric_name=CR&metric_type=1&antecedent_type=8__ "
                      "rates dropping by __id=1&value=null__% "
                      "in the last __id=1&time_interval=7__ days. Usually CR drops are from ad fatigue, "
                      "or it can be bad targeting. Refresh your ad creatives "
                      "as a first step to give them a boost. You can do this by duplicating your best performing ad "
                      "<strong>__id=2&metric_name=DUPLICATE_AD&metric_type=10&antecedent_type=1&"
                      "display_metric_name=0____id=2&value=null__</strong> now!",
             breakdown_metadata=BreakdownMetadataBase(breakdown=FacebookBreakdownEnum.NONE,
                                                      action_breakdown=FacebookActionBreakdownEnum.NONE),
             time_interval=DaysEnum.THREE_MONTHS,
             connective=Connective(LogicOperatorEnum.AND),
             antecedents=[
                 # Antecedent(aid=1,
                 #            atype=AntecedentTypeEnum.VALUE,
                 #            metric=FacebookAvailableMetricEnum.OBJECTIVE.value,
                 #            operator=LogicOperatorEnum.EQUALS,
                 #            expected_value=FacebookObjectiveEnum.LEAD_GENERATION.value),
                 Antecedent(aid=1,
                            atype=AntecedentTypeEnum.FUZZY_TREND,
                            metric=FacebookAvailableMetricEnum.CR.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=FacebookLinguisticVariableEnum.DECREASING)
             ]),
    # lead generation
    RuleBase(rtype=FacebookRuleTypeEnum.PERFORMANCE,
             channel=ChannelEnum.FACEBOOK,
             category=FacebookRuleCategoryEnum.IMPROVE_CPR,
             importance=FacebookRuleImportanceEnum.HIGH,
             source=FacebookRuleSourceEnum.DEXTER,
             level=LevelEnum.ADSET,
             action=FacebookActionEnum.DUPLICATE,
             redirect=FacebookRuleRedirectEnum.DUPLICATE,
             template="Dexter noticed your __id=1&metric_name=COST_PER_RESULT&metric_type=1&antecedent_type=8__ "
                      "has decreased by __id=1&value=null__% in the last __id=1&time_interval=7__ days. "
                      "Dexter suggests creating lookalikes from your most engaged customer base. You can do this by "
                      "duplicating your best performing ad <strong>__id=2&metric_name=DUPLICATE_AD&metric_type=10&"
                      "antecedent_type=1&display_metric_name=0__"
                      "__id=2&value=null__</strong> and adding a lookalike as your next audience to target.",
             breakdown_metadata=BreakdownMetadataBase(breakdown=FacebookBreakdownEnum.NONE,
                                                      action_breakdown=FacebookActionBreakdownEnum.NONE),
             time_interval=DaysEnum.THREE_MONTHS,
             connective=Connective(LogicOperatorEnum.AND),
             antecedents=[
                 # Antecedent(aid=1,
                 #            atype=AntecedentTypeEnum.VALUE,
                 #            metric=FacebookAvailableMetricEnum.OBJECTIVE.value,
                 #            operator=LogicOperatorEnum.EQUALS,
                 #            expected_value=FacebookObjectiveEnum.LEAD_GENERATION.value),
                 Antecedent(aid=1,
                            atype=AntecedentTypeEnum.FUZZY_TREND,
                            metric=FacebookAvailableMetricEnum.COST_PER_RESULT.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=FacebookLinguisticVariableEnum.DECREASING)
             ]),
    RuleBase(rtype=FacebookRuleTypeEnum.PERFORMANCE,
             channel=ChannelEnum.FACEBOOK,
             category=FacebookRuleCategoryEnum.IMPROVE_ROAS,
             importance=FacebookRuleImportanceEnum.MEDIUM,
             source=FacebookRuleSourceEnum.DEXTER,
             level=LevelEnum.ADSET,
             action=FacebookActionEnum.DUPLICATE,
             redirect=FacebookRuleRedirectEnum.DUPLICATE,
             template="Dexter noticed your __id=1&metric_name=ROAS&metric_type=1&antecedent_type=7__ has decreased by "
                      "__id=1&value=null__ in the last __id=1&time_interval=7__ days. "
                      "Dexter suggests you consider using lookalike audiences or custom audiences to increase "
                      "your score. You can do this by duplicating your best performing ad "
                      "<strong>__id=2&metric_name=DUPLICATE_AD&metric_type=10&antecedent_type=1&"
                      "display_metric_name=0____id=2&value=null__</strong> "
                      "and adding retargeting or lookalikes as your next audience to target.",
             breakdown_metadata=BreakdownMetadataBase(breakdown=FacebookBreakdownEnum.NONE,
                                                      action_breakdown=FacebookActionBreakdownEnum.NONE),
             time_interval=DaysEnum.THREE_MONTHS,
             connective=Connective(LogicOperatorEnum.AND),
             antecedents=[
                 # Antecedent(aid=1,
                 #            atype=AntecedentTypeEnum.VALUE,
                 #            metric=FacebookAvailableMetricEnum.OBJECTIVE.value,
                 #            operator=LogicOperatorEnum.EQUALS,
                 #            expected_value=FacebookObjectiveEnum.CONVERSIONS.value),
                 Antecedent(aid=1,
                            atype=AntecedentTypeEnum.FUZZY_TREND,
                            metric=FacebookAvailableMetricEnum.ROAS.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=FacebookLinguisticVariableEnum.DECREASING)
             ]),
    RuleBase(rtype=FacebookRuleTypeEnum.CREATIVE,
             channel=ChannelEnum.FACEBOOK,
             category=FacebookRuleCategoryEnum.IMPROVE_CPC,
             importance=FacebookRuleImportanceEnum.HIGH,
             source=FacebookRuleSourceEnum.DEXTER,
             level=LevelEnum.ADSET,
             action=FacebookActionEnum.DUPLICATE,
             redirect=FacebookRuleRedirectEnum.DUPLICATE,
             template="Dexter noticed your __id=1&metric_name=APP_INSTALLS&metric_type=1&antecedent_type=8__ "
                      "has increased by __id=1&value=null__% in the last __id=1&time_interval=7__ days. "
                      "Dexter recommends combining your best performing ad copy and creatives to decrease your "
                      "cost per install. You could do this now by duplicating your best ad "
                      "<strong>__id=2&metric_name=DUPLICATE_AD&metric_type=10&antecedent_type=1&"
                      "display_metric_name=0____id=2&value=null__</strong> now.",
             breakdown_metadata=BreakdownMetadataBase(breakdown=FacebookBreakdownEnum.NONE,
                                                      action_breakdown=FacebookActionBreakdownEnum.NONE),
             time_interval=DaysEnum.THREE_MONTHS,
             connective=Connective(LogicOperatorEnum.AND),
             antecedents=[
                 Antecedent(aid=1,
                            atype=AntecedentTypeEnum.VALUE,
                            metric=FacebookAvailableMetricEnum.OBJECTIVE.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=FacebookObjectiveEnum.APP_INSTALLS.value),
                 Antecedent(aid=2,
                            atype=AntecedentTypeEnum.FUZZY_TREND,
                            metric=FacebookAvailableMetricEnum.COST_PER_APP_INSTALL.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=FacebookLinguisticVariableEnum.INCREASING)
             ]),
    RuleBase(rtype=FacebookRuleTypeEnum.CREATIVE,
             channel=ChannelEnum.FACEBOOK,
             category=FacebookRuleCategoryEnum.IMPROVE_CPC,
             importance=FacebookRuleImportanceEnum.LOW,
             source=FacebookRuleSourceEnum.DEXTER,
             level=LevelEnum.ADSET,
             action=FacebookActionEnum.DUPLICATE,
             redirect=FacebookRuleRedirectEnum.DUPLICATE,
             template="Dexter noticed that your ad frequency on your campaign is near or above 3.0, which is when "
                      "ads start to lose their effectiveness. Dexter suggests launching new ad creatives to help "
                      "bring the score back down. Do this now by duplicating your best ad "
                      "<strong>__id=1&metric_name=DUPLICATE_AD&metric_type=10&antecedent_type=1&"
                      "display_metric_name=0__"
                      "__id=1&value=null__ </strong> now!",
             breakdown_metadata=BreakdownMetadataBase(breakdown=FacebookBreakdownEnum.NONE,
                                                      action_breakdown=FacebookActionBreakdownEnum.NONE),
             time_interval=DaysEnum.THREE_MONTHS,
             connective=Connective(LogicOperatorEnum.AND),
             antecedents=[
                 # Antecedent(aid=1,
                 #            atype=AntecedentTypeEnum.VALUE,
                 #            metric=FacebookAvailableMetricEnum.OBJECTIVE.value,
                 #            operator=LogicOperatorEnum.EQUALS,
                 #            expected_value=FacebookObjectiveEnum.APP_INSTALLS.value),
                 Antecedent(aid=1,
                            atype=AntecedentTypeEnum.FUZZY_VALUE,
                            metric=FacebookAvailableMetricEnum.FREQUENCY.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=FacebookLinguisticVariableEnum.HIGH)
             ]),
    # app installs
    RuleBase(rtype=FacebookRuleTypeEnum.CREATIVE,
             channel=ChannelEnum.FACEBOOK,
             category=FacebookRuleCategoryEnum.IMPROVE_CPR,
             importance=FacebookRuleImportanceEnum.HIGH,
             source=FacebookRuleSourceEnum.DEXTER,
             level=LevelEnum.ADSET,
             action=FacebookActionEnum.DUPLICATE,
             redirect=FacebookRuleRedirectEnum.DUPLICATE,
             template="Dexter noticed your __id=1&metric_name=APP_INSTALLS&metric_type=1&antecedent_type=8__ "
                      "are decreasing in the last __id=1&time_interval=7__ days. Dexter recommends AB testing "
                      "new ad copy or new creatives to drive a better results with your app installs. "
                      "You could start by duplicating this ad <strong>__id=2&metric_name=DUPLICATE_AD&metric_type=10&"
                      "antecedent_type=1&display_metric_name=0__"
                      "__id=2&value=null__</strong> now!.",
             breakdown_metadata=BreakdownMetadataBase(breakdown=FacebookBreakdownEnum.NONE,
                                                      action_breakdown=FacebookActionBreakdownEnum.NONE),
             time_interval=DaysEnum.THREE_MONTHS,
             connective=Connective(LogicOperatorEnum.AND),
             antecedents=[
                 Antecedent(aid=1,
                            atype=AntecedentTypeEnum.VALUE,
                            metric=FacebookAvailableMetricEnum.OBJECTIVE.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=FacebookObjectiveEnum.APP_INSTALLS.value),
                 Antecedent(aid=2,
                            atype=AntecedentTypeEnum.FUZZY_TREND,
                            metric=FacebookAvailableMetricEnum.RESULTS.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=FacebookLinguisticVariableEnum.DECREASING)
             ]),

    # app Installs
    RuleBase(rtype=FacebookRuleTypeEnum.AUDIENCE,
             channel=ChannelEnum.FACEBOOK,
             category=FacebookRuleCategoryEnum.IMPROVE_CPC,
             importance=FacebookRuleImportanceEnum.MEDIUM,
             source=FacebookRuleSourceEnum.DEXTER,
             level=LevelEnum.ADSET,
             action=FacebookActionEnum.NONE,
             redirect=FacebookRuleRedirectEnum.DUPLICATE,
             template="Dexter noticed your __id=1&metric_name=CPM&metric_type=1&antecedent_type=1__ "
                      "has increased too much for Dexter in the last __id=1&time_interval=7__ days. "
                      "This could mean several things. Right now, Dexter suggests that you launch "
                      "your best performing ads with __id=2&metric_name=INTERESTS&metric_type=4&antecedent_type=6&"
                      "metric_count=3__ __id=2&value=null__. You can do this by duplicating this ad now "
                      "<strong>__id=3&metric_name=DUPLICATE_AD&metric_type=10&antecedent_type=1&"
                      "display_metric_name=0____id=3&value=null__</strong>.",
             breakdown_metadata=BreakdownMetadataBase(breakdown=FacebookBreakdownEnum.NONE,
                                                      action_breakdown=FacebookActionBreakdownEnum.NONE),
             time_interval=DaysEnum.THREE_MONTHS,
             connective=Connective(LogicOperatorEnum.AND),
             antecedents=[
                 # Antecedent(aid=1,
                 #            atype=AntecedentTypeEnum.VALUE,
                 #            metric=FacebookAvailableMetricEnum.OBJECTIVE.value,
                 #            operator=LogicOperatorEnum.EQUALS,
                 #            expected_value=FacebookObjectiveEnum.APP_INSTALLS.value),
                 Antecedent(aid=1,
                            atype=AntecedentTypeEnum.FUZZY_TREND,
                            metric=FacebookAvailableMetricEnum.CPM.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=FacebookLinguisticVariableEnum.INCREASING)
             ]),

    # brand awareness
    # TODO: should cpm be % in the value field?
    RuleBase(rtype=FacebookRuleTypeEnum.AUDIENCE,
             channel=ChannelEnum.FACEBOOK,
             category=FacebookRuleCategoryEnum.OPTIMIZE_TARGETING,
             importance=FacebookRuleImportanceEnum.MEDIUM,
             source=FacebookRuleSourceEnum.DEXTER,
             level=LevelEnum.ADSET,
             action=FacebookActionEnum.NONE,
             redirect=FacebookRuleRedirectEnum.CAMPAIGN_MANAGER,
             template="Dexter has been monitoring your campaigns very closely, and "
                      "your __id=1&metric_name=CPM&metric_type=1&antecedent_type=1__ "
                      "has increased by __id=1&value=null__% in the last __id=1&time_interval=7__ days. "
                      "Dexter suggests you try these new "
                      "__id=2&metric_name=INTERESTS&metric_type=4&antecedent_type=6&metric_count=3__: "
                      "__id=2&value=null__, to find the cheapest cost between interests that are similar.",
             breakdown_metadata=BreakdownMetadataBase(breakdown=FacebookBreakdownEnum.NONE,
                                                      action_breakdown=FacebookActionBreakdownEnum.NONE),
             time_interval=DaysEnum.THREE_MONTHS,
             connective=Connective(LogicOperatorEnum.AND),
             antecedents=[
                 # Antecedent(aid=1,
                 #            atype=AntecedentTypeEnum.VALUE,
                 #            metric=FacebookAvailableMetricEnum.OBJECTIVE.value,
                 #            operator=LogicOperatorEnum.EQUALS,
                 #            expected_value=FacebookObjectiveEnum.BRAND_AWARENESS.value),
                 Antecedent(aid=1,
                            atype=AntecedentTypeEnum.FUZZY_TREND,
                            metric=FacebookAvailableMetricEnum.CPM.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=FacebookLinguisticVariableEnum.INCREASING)
             ]),

    # conversions
    RuleBase(rtype=FacebookRuleTypeEnum.AUDIENCE,
             channel=ChannelEnum.FACEBOOK,
             category=FacebookRuleCategoryEnum.IMPROVE_CONVERSION_RATE,
             importance=FacebookRuleImportanceEnum.HIGH,
             source=FacebookRuleSourceEnum.DEXTER,
             level=LevelEnum.ADSET,
             action=FacebookActionEnum.NONE,
             redirect=FacebookRuleRedirectEnum.CAMPAIGN_MANAGER,
             template="Dexter noticed your __id=1&metric_name=CONVERSIONS&metric_type=1&antecedent_type=1__ "
                      "have decreased over the last __id=1&time_interval=7__ days. Dexter "
                      "suggests testing these __id=2&metric_name=INTERESTS&metric_type=4&"
                      "antecedent_type=6&metric_count=5__ __id=2&value=null__ to "
                      "help broaden your reach and get more results.",
             breakdown_metadata=BreakdownMetadataBase(breakdown=FacebookBreakdownEnum.NONE,
                                                      action_breakdown=FacebookActionBreakdownEnum.NONE),
             time_interval=DaysEnum.THREE_MONTHS,
             connective=Connective(LogicOperatorEnum.AND),
             antecedents=[
                 # Antecedent(aid=1,
                 #            atype=AntecedentTypeEnum.VALUE,
                 #            metric=FacebookAvailableMetricEnum.OBJECTIVE.value,
                 #            operator=LogicOperatorEnum.EQUALS,
                 #            expected_value=FacebookObjectiveEnum.CONVERSIONS.value),
                 Antecedent(aid=1,
                            atype=AntecedentTypeEnum.FUZZY_TREND,
                            metric=FacebookAvailableMetricEnum.RESULTS.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=FacebookLinguisticVariableEnum.DECREASING)
             ]),

    # event responses
    RuleBase(rtype=FacebookRuleTypeEnum.AUDIENCE,
             channel=ChannelEnum.FACEBOOK,
             category=FacebookRuleCategoryEnum.OPTIMIZE_TARGETING,
             importance=FacebookRuleImportanceEnum.HIGH,
             source=FacebookRuleSourceEnum.DEXTER,
             level=LevelEnum.ADSET,
             action=FacebookActionEnum.NONE,
             redirect=FacebookRuleRedirectEnum.CAMPAIGN_MANAGER,
             template="Dexter noticed your __id=1&metric_name=RSVPS&metric_type=1&antecedent_type=8__ are decreasing "
                      "by __id=1&value=null__% over the last __id=1&time_interval=7__ days. Have you tried opening up "
                      "your targeting to be broader? Dexter suggests targeting these "
                      "__id=2&metric_name=INTERESTS&metric_type=4&antecedent_type=6&metric_count=5__: "
                      "__id=2&value=null__ to get started.",
             breakdown_metadata=BreakdownMetadataBase(breakdown=FacebookBreakdownEnum.NONE,
                                                      action_breakdown=FacebookActionBreakdownEnum.NONE),
             time_interval=DaysEnum.THREE_MONTHS,
             connective=Connective(LogicOperatorEnum.AND),
             antecedents=[
                 # Antecedent(aid=1,
                 #            atype=AntecedentTypeEnum.VALUE,
                 #            metric=FacebookAvailableMetricEnum.OBJECTIVE.value,
                 #            operator=LogicOperatorEnum.EQUALS,
                 #            expected_value=FacebookObjectiveEnum.EVENT_RESPONSES.value),
                 Antecedent(aid=1,
                            atype=AntecedentTypeEnum.FUZZY_TREND,
                            metric=FacebookAvailableMetricEnum.RSVPS.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=FacebookLinguisticVariableEnum.DECREASING)
             ]),
    RuleBase(rtype=FacebookRuleTypeEnum.AUDIENCE,
             channel=ChannelEnum.FACEBOOK,
             category=FacebookRuleCategoryEnum.OPTIMIZE_TARGETING,
             importance=FacebookRuleImportanceEnum.HIGH,
             source=FacebookRuleSourceEnum.DEXTER,
             level=LevelEnum.ADSET,
             action=FacebookActionEnum.NONE,
             redirect=FacebookRuleRedirectEnum.CAMPAIGN_MANAGER,
             template="Your __id=1&metric_name=COST_PER_RESULT&metric_type=1&antecedent_type=8__ "
                      "has increased by __id=1&value=null__% in the last __id=1&time_interval=7__ days. "
                      "Dexter thinks you should add more interests in your targeting. Add these suggested "
                      "__id=2&metric_name=INTERESTS&metric_type=4&antecedent_type=6&metric_count=5__: "
                      "__id=2&value=null__ to get started.",
             breakdown_metadata=BreakdownMetadataBase(breakdown=FacebookBreakdownEnum.NONE,
                                                      action_breakdown=FacebookActionBreakdownEnum.NONE),
             time_interval=DaysEnum.THREE_MONTHS,
             connective=Connective(LogicOperatorEnum.AND),
             antecedents=[
                 # Antecedent(aid=1,
                 #            atype=AntecedentTypeEnum.VALUE,
                 #            metric=FacebookAvailableMetricEnum.OBJECTIVE.value,
                 #            operator=LogicOperatorEnum.EQUALS,
                 #            expected_value=FacebookObjectiveEnum.EVENT_RESPONSES.value),
                 Antecedent(aid=1,
                            atype=AntecedentTypeEnum.FUZZY_TREND,
                            metric=FacebookAvailableMetricEnum.COST_PER_RESULT.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=FacebookLinguisticVariableEnum.INCREASING)
             ]),

    # link clicks
    RuleBase(rtype=FacebookRuleTypeEnum.AUDIENCE,
             channel=ChannelEnum.FACEBOOK,
             category=FacebookRuleCategoryEnum.IMPROVE_CPC,
             importance=FacebookRuleImportanceEnum.HIGH,
             source=FacebookRuleSourceEnum.DEXTER,
             level=LevelEnum.ADSET,
             action=FacebookActionEnum.NONE,
             redirect=FacebookRuleRedirectEnum.CAMPAIGN_MANAGER,
             template="Dexter noticed your __id=1&metric_name=CPC&metric_type=1&antecedent_type=8__ has increased by "
                      "__id=1&value=null__% over the last __id=1&time_interval=7__ days. Dexter suggests launching "
                      "these new __id=2&metric_name=INTERESTS&metric_type=4&antecedent_type=6&metric_count=3__ "
                      "__id=2&value=null__ to help grow your reach and find new "
                      "users that'll convert at a lower cost.",
             breakdown_metadata=BreakdownMetadataBase(breakdown=FacebookBreakdownEnum.NONE,
                                                      action_breakdown=FacebookActionBreakdownEnum.NONE),
             time_interval=DaysEnum.THREE_MONTHS,
             connective=Connective(LogicOperatorEnum.AND),
             antecedents=[
                 # Antecedent(aid=1,
                 #            atype=AntecedentTypeEnum.VALUE,
                 #            metric=FacebookAvailableMetricEnum.OBJECTIVE.value,
                 #            operator=LogicOperatorEnum.EQUALS,
                 #            expected_value=FacebookObjectiveEnum.LINK_CLICKS.value),
                 Antecedent(aid=1,
                            atype=AntecedentTypeEnum.FUZZY_TREND,
                            metric=FacebookAvailableMetricEnum.CPC.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=FacebookLinguisticVariableEnum.INCREASING)
             ]),

    # messenger
    RuleBase(rtype=FacebookRuleTypeEnum.AUDIENCE,
             channel=ChannelEnum.FACEBOOK,
             category=FacebookRuleCategoryEnum.IMPROVE_CPR,
             importance=FacebookRuleImportanceEnum.HIGH,
             source=FacebookRuleSourceEnum.DEXTER,
             level=LevelEnum.ADSET,
             action=FacebookActionEnum.NONE,
             redirect=FacebookRuleRedirectEnum.CAMPAIGN_MANAGER,
             template="Dexter noticed that your cost per result has increased lately. Dexter suggests adding new "
                      "interests to target? Do so now by adding the following __id=1&metric_name=INTERESTS&"
                      "metric_type=4&antecedent_type=6&metric_count=3__ __id=1&value=null__.",
             breakdown_metadata=BreakdownMetadataBase(breakdown=FacebookBreakdownEnum.NONE,
                                                      action_breakdown=FacebookActionBreakdownEnum.NONE),
             time_interval=DaysEnum.THREE_MONTHS,
             connective=Connective(LogicOperatorEnum.AND),
             antecedents=[
                 # Antecedent(aid=1,
                 #            atype=AntecedentTypeEnum.VALUE,
                 #            metric=FacebookAvailableMetricEnum.OBJECTIVE.value,
                 #            operator=LogicOperatorEnum.EQUALS,
                 #            expected_value=FacebookObjectiveEnum.MESSAGES.value),
                 Antecedent(aid=1,
                            atype=AntecedentTypeEnum.FUZZY_TREND,
                            metric=FacebookAvailableMetricEnum.COST_PER_RESULT.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=FacebookLinguisticVariableEnum.INCREASING)
             ]),

    RuleBase(rtype=FacebookRuleTypeEnum.AUDIENCE,
             channel=ChannelEnum.FACEBOOK,
             category=FacebookRuleCategoryEnum.OPTIMIZE_TARGETING,
             importance=FacebookRuleImportanceEnum.MEDIUM,
             source=FacebookRuleSourceEnum.DEXTER,
             level=LevelEnum.ADSET,
             action=FacebookActionEnum.NONE,
             redirect=FacebookRuleRedirectEnum.CAMPAIGN_MANAGER,
             template="Dexter noticed your messenger ads aren't reaching enough people. Dexter suggests these "
                      "__id=1&metric_name=INTERESTS&metric_type=4&antecedent_type=6&metric_count=3__: "
                      "__id=1&value=null__ to find new prospects you wouldn't have normally found otherwise!",
             breakdown_metadata=BreakdownMetadataBase(breakdown=FacebookBreakdownEnum.NONE,
                                                      action_breakdown=FacebookActionBreakdownEnum.NONE),
             time_interval=DaysEnum.THREE_MONTHS,
             connective=Connective(LogicOperatorEnum.AND),
             antecedents=[
                 # Antecedent(aid=1,
                 #            atype=AntecedentTypeEnum.VALUE,
                 #            metric=FacebookAvailableMetricEnum.OBJECTIVE.value,
                 #            operator=LogicOperatorEnum.EQUALS,
                 #            expected_value=FacebookObjectiveEnum.MESSAGES.value),
                 Antecedent(aid=1,
                            atype=AntecedentTypeEnum.FUZZY_TREND,
                            metric=FacebookAvailableMetricEnum.REACH.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=FacebookLinguisticVariableEnum.DECREASING)
             ]),

    # page likes
    RuleBase(rtype=FacebookRuleTypeEnum.AUDIENCE,
             channel=ChannelEnum.FACEBOOK,
             category=FacebookRuleCategoryEnum.IMPROVE_CPR,
             importance=FacebookRuleImportanceEnum.HIGH,
             source=FacebookRuleSourceEnum.DEXTER,
             level=LevelEnum.ADSET,
             action=FacebookActionEnum.NONE,
             redirect=FacebookRuleRedirectEnum.CAMPAIGN_MANAGER,
             template="Dexter noticed that your __id=1&metric_name=COST_PER_RESULT&metric_type=1&antecedent_type=8__ "
                      "has decreased over the last __id=1&time_interval=7__ days. Dexter suggests you create a new "
                      "adset and consider targeting the following __id=2&metric_name=INTERESTS&metric_type=4&"
                      "antecedent_type=6&metric_count=3__: __id=2&value=null__ to get more likes to your page.",
             breakdown_metadata=BreakdownMetadataBase(breakdown=FacebookBreakdownEnum.NONE,
                                                      action_breakdown=FacebookActionBreakdownEnum.NONE),
             time_interval=DaysEnum.THREE_MONTHS,
             connective=Connective(LogicOperatorEnum.AND),
             antecedents=[
                 # Antecedent(aid=1,
                 #            atype=AntecedentTypeEnum.VALUE,
                 #            metric=FacebookAvailableMetricEnum.OBJECTIVE.value,
                 #            operator=LogicOperatorEnum.EQUALS,
                 #            expected_value=FacebookObjectiveEnum.PAGE_LIKES.value),
                 Antecedent(aid=1,
                            atype=AntecedentTypeEnum.FUZZY_TREND,
                            metric=FacebookAvailableMetricEnum.COST_PER_RESULT.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=FacebookLinguisticVariableEnum.DECREASING)
             ]),
    RuleBase(rtype=FacebookRuleTypeEnum.AUDIENCE,
             channel=ChannelEnum.FACEBOOK,
             category=FacebookRuleCategoryEnum.IMPROVE_CPR,
             importance=FacebookRuleImportanceEnum.HIGH,
             source=FacebookRuleSourceEnum.DEXTER,
             level=LevelEnum.ADSET,
             action=FacebookActionEnum.NONE,
             redirect=FacebookRuleRedirectEnum.CAMPAIGN_MANAGER,
             template="Dexter noticed your __id=1&metric_name=PAGE_LIKES&metric_type=1&antecedent_type=8__ have "
                      "decreased by __id=1&value=null__% over the last __id=1&time_interval=7__ days. Dexter suggests "
                      "targeting these __id=2&metric_name=INTERESTS&metric_type=4&"
                      "antecedent_type=6&metric_count=3__: __id=2&value=null__?",
             breakdown_metadata=BreakdownMetadataBase(breakdown=FacebookBreakdownEnum.NONE,
                                                      action_breakdown=FacebookActionBreakdownEnum.NONE),
             time_interval=DaysEnum.THREE_MONTHS,
             connective=Connective(LogicOperatorEnum.AND),
             antecedents=[
                 # Antecedent(aid=1,
                 #            atype=AntecedentTypeEnum.VALUE,
                 #            metric=FacebookAvailableMetricEnum.OBJECTIVE.value,
                 #            operator=LogicOperatorEnum.EQUALS,
                 #            expected_value=FacebookObjectiveEnum.PAGE_LIKES.value),
                 Antecedent(aid=1,
                            atype=AntecedentTypeEnum.FUZZY_TREND,
                            metric=FacebookAvailableMetricEnum.PAGE_LIKES.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=FacebookLinguisticVariableEnum.DECREASING)
             ]),

    # post engagement
    RuleBase(rtype=FacebookRuleTypeEnum.AUDIENCE,
             channel=ChannelEnum.FACEBOOK,
             category=FacebookRuleCategoryEnum.OPTIMIZE_TARGETING,
             importance=FacebookRuleImportanceEnum.MEDIUM,
             source=FacebookRuleSourceEnum.DEXTER,
             level=LevelEnum.ADSET,
             action=FacebookActionEnum.NONE,
             redirect=FacebookRuleRedirectEnum.CAMPAIGN_MANAGER,
             template="The bigger the audience the more impressions. This also means the more "
                      "likely it is for your ad to be seen and engaged with. "
                      "Dexter suggests you target these "
                      "__id=2&metric_name=INTERESTS&metric_type=4&antecedent_type=6&metric_count=5__: "
                      "__id=2&value=null__ to reach more people.",
             breakdown_metadata=BreakdownMetadataBase(breakdown=FacebookBreakdownEnum.NONE,
                                                      action_breakdown=FacebookActionBreakdownEnum.NONE),
             time_interval=DaysEnum.THREE_MONTHS,
             connective=Connective(LogicOperatorEnum.AND),
             antecedents=[
                 # Antecedent(aid=1,
                 #            atype=AntecedentTypeEnum.VALUE,
                 #            metric=FacebookAvailableMetricEnum.OBJECTIVE.value,
                 #            operator=LogicOperatorEnum.EQUALS,
                 #            expected_value=FacebookObjectiveEnum.POST_ENGAGEMENT.value),
                 Antecedent(aid=1,
                            atype=AntecedentTypeEnum.FUZZY_TREND,
                            metric=FacebookAvailableMetricEnum.IMPRESSIONS.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=FacebookLinguisticVariableEnum.DECREASING)
             ]),

    # catalog sales
    RuleBase(rtype=FacebookRuleTypeEnum.AUDIENCE,
             channel=ChannelEnum.FACEBOOK,
             category=FacebookRuleCategoryEnum.IMPROVE_ROAS,
             importance=FacebookRuleImportanceEnum.HIGH,
             source=FacebookRuleSourceEnum.DEXTER,
             level=LevelEnum.ADSET,
             action=FacebookActionEnum.NONE,
             redirect=FacebookRuleRedirectEnum.CAMPAIGN_MANAGER,
             template="Dexter noticed your __id=1&metric_name=PURCHASES&metric_type=1&antecedent_type=8__ have slowed "
                      "down by __id=1&value=null__% over the last __id=1&time_interval=7__ days. Dexter suggests "
                      "trying targeting these __id=2&metric_name=INTERESTS&metric_type=4&antecedent_type=6&"
                      "metric_count=3__: __id=2&value=null__ to increase your sales!",
             breakdown_metadata=BreakdownMetadataBase(breakdown=FacebookBreakdownEnum.NONE,
                                                      action_breakdown=FacebookActionBreakdownEnum.NONE),
             time_interval=DaysEnum.THREE_MONTHS,
             connective=Connective(LogicOperatorEnum.AND),
             antecedents=[
                 # Antecedent(aid=1,
                 #            atype=AntecedentTypeEnum.VALUE,
                 #            metric=FacebookAvailableMetricEnum.OBJECTIVE.value,
                 #            operator=LogicOperatorEnum.EQUALS,
                 #            expected_value=FacebookObjectiveEnum.PRODUCT_CATALOG_SALES.value),
                 Antecedent(aid=1,
                            atype=AntecedentTypeEnum.FUZZY_TREND,
                            metric=FacebookAvailableMetricEnum.PURCHASES.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=FacebookLinguisticVariableEnum.DECREASING)
             ]),

    # reach
    RuleBase(rtype=FacebookRuleTypeEnum.AUDIENCE,
             channel=ChannelEnum.FACEBOOK,
             category=FacebookRuleCategoryEnum.IMPROVE_ROAS,
             importance=FacebookRuleImportanceEnum.MEDIUM,
             source=FacebookRuleSourceEnum.DEXTER,
             level=LevelEnum.ADSET,
             action=FacebookActionEnum.NONE,
             redirect=FacebookRuleRedirectEnum.CAMPAIGN_MANAGER,
             template="Dexter noticed your __id=1&metric_name=ROAS&metric_type=1&antecedent_type=7__ has decreased "
                      "by __id=1&value=null__ in the last __id=1&time_interval=7__ days. "
                      "Dexter suggests you for the best age and gender, or look at your best performing placement "
                      "to make sure your ad is set up for maximum success.",
             breakdown_metadata=BreakdownMetadataBase(breakdown=FacebookBreakdownEnum.NONE,
                                                      action_breakdown=FacebookActionBreakdownEnum.NONE),
             time_interval=DaysEnum.THREE_MONTHS,
             connective=Connective(LogicOperatorEnum.AND),
             antecedents=[
                 # Antecedent(aid=1,
                 #            atype=AntecedentTypeEnum.VALUE,
                 #            metric=FacebookAvailableMetricEnum.OBJECTIVE.value,
                 #            operator=LogicOperatorEnum.EQUALS,
                 #            expected_value=FacebookObjectiveEnum.PRODUCT_CATALOG_SALES.value),
                 Antecedent(aid=1,
                            atype=AntecedentTypeEnum.FUZZY_TREND,
                            metric=FacebookAvailableMetricEnum.ROAS.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=FacebookLinguisticVariableEnum.DECREASING)
             ]),
    # TODO: modified CPM from percentage to value
    RuleBase(rtype=FacebookRuleTypeEnum.PERFORMANCE,
             channel=ChannelEnum.FACEBOOK,
             category=FacebookRuleCategoryEnum.IMPROVE_CPR,
             importance=FacebookRuleImportanceEnum.MEDIUM,
             source=FacebookRuleSourceEnum.DEXTER,
             level=LevelEnum.ADSET,
             action=FacebookActionEnum.NONE,
             redirect=FacebookRuleRedirectEnum.EDIT_STRUCTURE,
             template="Dexter noticed your __id=1&metric_name=CPM&metric_type=1&antecedent_type=1__ has increased by "
                      "__id=1&value=null__ in the last __id=1&time_interval=3__ days. It’s one of two reasons: "
                      "Your frequency is high or your ad isn’t resonating with your "
                      "target audience. Dexter suggests taking a look and make the right adjustments!",
             breakdown_metadata=BreakdownMetadataBase(breakdown=FacebookBreakdownEnum.NONE,
                                                      action_breakdown=FacebookActionBreakdownEnum.NONE),
             time_interval=DaysEnum.THREE_MONTHS,
             connective=Connective(LogicOperatorEnum.AND),
             antecedents=[
                 # Antecedent(aid=1,
                 #            atype=AntecedentTypeEnum.VALUE,
                 #            metric=FacebookAvailableMetricEnum.OBJECTIVE.value,
                 #            operator=LogicOperatorEnum.EQUALS,
                 #            expected_value=FacebookObjectiveEnum.REACH.value),
                 Antecedent(aid=1,
                            atype=AntecedentTypeEnum.FUZZY_VALUE,
                            metric=FacebookAvailableMetricEnum.CPM.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=FacebookLinguisticVariableEnum.HIGH)
             ]),
    RuleBase(rtype=FacebookRuleTypeEnum.PERFORMANCE,
             channel=ChannelEnum.FACEBOOK,
             category=FacebookRuleCategoryEnum.IMPROVE_ENGAGEMENT,
             importance=FacebookRuleImportanceEnum.HIGH,
             source=FacebookRuleSourceEnum.DEXTER,
             level=LevelEnum.ADSET,
             action=FacebookActionEnum.NONE,
             redirect=FacebookRuleRedirectEnum.CAMPAIGN_MANAGER,
             template="Dexter noticed your __id=1&metric_name=COST_PER_THRUPLAY&metric_type=1&antecedent_type=8__ has "
                      "gone up by __id=1&value=null__% over the last __id=1&time_interval=7__ days. "
                      "Dexter suggests optimizing your delivery by age and gender or for the best "
                      "performing placement.",
             breakdown_metadata=BreakdownMetadataBase(breakdown=FacebookBreakdownEnum.NONE,
                                                      action_breakdown=FacebookActionBreakdownEnum.NONE),
             time_interval=DaysEnum.THREE_MONTHS,
             connective=Connective(LogicOperatorEnum.AND),
             antecedents=[
                 # Antecedent(aid=1,
                 #            atype=AntecedentTypeEnum.VALUE,
                 #            metric=FacebookAvailableMetricEnum.OBJECTIVE.value,
                 #            operator=LogicOperatorEnum.EQUALS,
                 #            expected_value=FacebookObjectiveEnum.VIDEO_VIEWS.value),
                 Antecedent(aid=1,
                            atype=AntecedentTypeEnum.FUZZY_TREND,
                            metric=FacebookAvailableMetricEnum.COST_PER_THRUPLAY.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=FacebookLinguisticVariableEnum.INCREASING)
             ]),
    RuleBase(rtype=FacebookRuleTypeEnum.CREATIVE,
             channel=ChannelEnum.FACEBOOK,
             category=FacebookRuleCategoryEnum.IMPROVE_ENGAGEMENT,
             importance=FacebookRuleImportanceEnum.HIGH,
             source=FacebookRuleSourceEnum.DEXTER,
             level=LevelEnum.ADSET,
             action=FacebookActionEnum.NONE,
             redirect=FacebookRuleRedirectEnum.EDIT_STRUCTURE,
             template="Dexter noticed your videos are smashing it and your cost per play is really competitive. "
                      "Dexter suggests creating more videos for other campaigns that you're running?",
             breakdown_metadata=BreakdownMetadataBase(breakdown=FacebookBreakdownEnum.NONE,
                                                      action_breakdown=FacebookActionBreakdownEnum.NONE),
             time_interval=DaysEnum.THREE_MONTHS,
             connective=Connective(LogicOperatorEnum.AND),
             antecedents=[
                 # Antecedent(aid=1,
                 #            atype=AntecedentTypeEnum.VALUE,
                 #            metric=FacebookAvailableMetricEnum.OBJECTIVE.value,
                 #            operator=LogicOperatorEnum.EQUALS,
                 #            expected_value=FacebookObjectiveEnum.VIDEO_VIEWS.value),
                 Antecedent(aid=1,
                            atype=AntecedentTypeEnum.FUZZY_TREND,
                            metric=FacebookAvailableMetricEnum.COST_PER_THRUPLAY.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=FacebookLinguisticVariableEnum.DECREASING),
                 Antecedent(aid=2,
                            atype=AntecedentTypeEnum.FUZZY_TREND,
                            metric=FacebookAvailableMetricEnum.VIDEO_PLAYS.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=FacebookLinguisticVariableEnum.INCREASING)
             ]),
    RuleBase(rtype=FacebookRuleTypeEnum.PERFORMANCE,
             channel=ChannelEnum.FACEBOOK,
             category=FacebookRuleCategoryEnum.IMPROVE_ROAS,
             importance=FacebookRuleImportanceEnum.MEDIUM,
             source=FacebookRuleSourceEnum.DEXTER,
             level=LevelEnum.ADSET,
             action=FacebookActionEnum.DUPLICATE,
             redirect=FacebookRuleRedirectEnum.CREATE_LOOKALIKE_AUDIENCE,
             template="Dexter believes that you can bring your "
                      "__id=1&metric_name=COST_PER_PURCHASE&metric_type=1&antecedent_type=8__ down significantly "
                      "by running retargeting campaigns? Start this process now to see better results! "
                      "You can do this by duplicating your best performing ad <strong>__id=2&metric_name=DUPLICATE_AD"
                      "&metric_type=10&antecedent_type=1&display_metric_name=0____id=2&value=null__</strong> "
                      "and adding retargeting in as your next audience to target.",
             breakdown_metadata=BreakdownMetadataBase(breakdown=FacebookBreakdownEnum.NONE,
                                                      action_breakdown=FacebookActionBreakdownEnum.NONE),
             time_interval=DaysEnum.THREE_MONTHS,
             connective=Connective(LogicOperatorEnum.AND),
             antecedents=[
                 # Antecedent(aid=1,
                 #            atype=AntecedentTypeEnum.VALUE,
                 #            metric=FacebookAvailableMetricEnum.OBJECTIVE.value,
                 #            operator=LogicOperatorEnum.EQUALS,
                 #            expected_value=FacebookObjectiveEnum.LEAD_GENERATION.value),
                 Antecedent(aid=1,
                            atype=AntecedentTypeEnum.FUZZY_TREND,
                            metric=FacebookAvailableMetricEnum.COST_PER_RESULT.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=FacebookLinguisticVariableEnum.DECREASING)
             ]),
]
