from FacebookDexter.Engine.Algorithms.FuzzyRuleBasedOptimization.Metrics.AvailableMetricEnum import AvailableMetricEnum
from FacebookDexter.Infrastructure.Domain.Actions.ActionEnums import ActionEnum
from FacebookDexter.Infrastructure.Domain.Breakdowns import BreakdownMetadata, BreakdownEnum, ActionBreakdownEnum
from FacebookDexter.Infrastructure.Domain.ChannelEnum import ChannelEnum
from FacebookDexter.Infrastructure.Domain.DaysEnum import DaysEnum
from FacebookDexter.Infrastructure.Domain.LevelEnums import LevelEnum
from FacebookDexter.Infrastructure.Domain.LogicalOperatorEnum import LogicOperatorEnum
from FacebookDexter.Infrastructure.Domain.ObjectiveEnum import ObjectiveEnum
from FacebookDexter.Infrastructure.Domain.Rules.Antecedent import Antecedent
from FacebookDexter.Infrastructure.Domain.Rules.AntecedentEnums import AntecedentTypeEnum
from FacebookDexter.Infrastructure.Domain.Rules.Connective import Connective
from FacebookDexter.Infrastructure.Domain.Rules.RuleBase import RuleBase
from FacebookDexter.Infrastructure.Domain.Rules.RuleEnums import RuleTypeEnum, RuleCategoryEnum, RuleImportanceEnum, \
    RuleSourceEnum, RuleRedirectEnum
from FacebookDexter.Infrastructure.FuzzyEngine.FuzzySets.FuzzySets import LinguisticVariableEnum

RULES_ADSET_GENERAL = [
    # app Installs
    RuleBase(rtype=RuleTypeEnum.AUDIENCE,
             channel=ChannelEnum.FACEBOOK,
             category=RuleCategoryEnum.IMPROVE_CPC,
             importance=RuleImportanceEnum.MEDIUM,
             source=RuleSourceEnum.DEXTER,
             level=LevelEnum.ADSET,
             action=ActionEnum.NONE,
             redirect=RuleRedirectEnum.EDIT_STRUCTURE,
             template="Your <id=1&metric_name=CPM&metric_type=1&antecedent_type=1> has increased too much for Dexter in the last <id=1&time_interval=7> days."
                      " This could mean several things. However, Dexter suggests that you launch "
                      "your best performing ads with <id=2&metric_name=INTERESTS&metric_type=4&antecedent_type=6&metric_count=3> <id=2&value=null>. ",
             breakdown_metadata=BreakdownMetadata(breakdown=BreakdownEnum.NONE,
                                                  action_breakdown=ActionBreakdownEnum.NONE),
             time_interval=DaysEnum.THREE_MONTHS,
             connective=Connective(LogicOperatorEnum.AND),
             antecedents=[
                 Antecedent(aid=1,
                            atype=AntecedentTypeEnum.VALUE,
                            metric=AvailableMetricEnum.OBJECTIVE.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=ObjectiveEnum.APP_INSTALLS.value),
                 Antecedent(aid=2,
                            atype=AntecedentTypeEnum.FUZZY_TREND,
                            metric=AvailableMetricEnum.CPM.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=LinguisticVariableEnum.INCREASING)
             ]),

    # brand awareness
    RuleBase(rtype=RuleTypeEnum.AUDIENCE,
             channel=ChannelEnum.FACEBOOK,
             category=RuleCategoryEnum.OPTIMIZE_TARGETING,
             importance=RuleImportanceEnum.MEDIUM,
             source=RuleSourceEnum.DEXTER,
             level=LevelEnum.ADSET,
             action=ActionEnum.NONE,
             redirect=RuleRedirectEnum.CAMPAIGN_MANAGER,
             template="Dexter has been monitoring your campaigns very closely, and your <id=1&metric_name=CPM&metric_type=1&antecedent_type=1> "
                      "has increased by <id=1&value=null>% in the last <id=1&time_interval=7> days. He recommends you try these new interests "
                      "<id=2&metric_name=INTERESTS&metric_type=4&antecedent_type=6&metric_count=3>: <id=2&value=null>, to find the cheapest cost",
             breakdown_metadata=BreakdownMetadata(breakdown=BreakdownEnum.NONE,
                                                  action_breakdown=ActionBreakdownEnum.NONE),
             time_interval=DaysEnum.THREE_MONTHS,
             connective=Connective(LogicOperatorEnum.AND),
             antecedents=[
                 Antecedent(aid=1,
                            atype=AntecedentTypeEnum.VALUE,
                            metric=AvailableMetricEnum.OBJECTIVE.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=ObjectiveEnum.BRAND_AWARENESS.value),
                 Antecedent(aid=2,
                            atype=AntecedentTypeEnum.FUZZY_TREND,
                            metric=AvailableMetricEnum.CPM.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=LinguisticVariableEnum.INCREASING)
             ]),

    # conversions
    RuleBase(rtype=RuleTypeEnum.AUDIENCE,
             channel=ChannelEnum.FACEBOOK,
             category=RuleCategoryEnum.IMPROVE_CONVERSION_RATE,
             importance=RuleImportanceEnum.HIGH,
             source=RuleSourceEnum.DEXTER,
             level=LevelEnum.ADSET,
             action=ActionEnum.NONE,
             redirect=RuleRedirectEnum.CAMPAIGN_MANAGER,
             template="Your <id=1&metric_name=CONVERSIONS&metric_type=1&antecedent_type=1> have decreased over the last <id=1&time_interval=7> days. Dexter "
                      "suggests testing <id=2&metric_name=INTERESTS&metric_type=4&antecedent_type=6&metric_count=5>: <id=2&value=null> to "
                      "help broaden your reach and get more results.",
             breakdown_metadata=BreakdownMetadata(breakdown=BreakdownEnum.NONE,
                                                  action_breakdown=ActionBreakdownEnum.NONE),
             time_interval=DaysEnum.THREE_MONTHS,
             connective=Connective(LogicOperatorEnum.AND),
             antecedents=[
                 Antecedent(aid=1,
                            atype=AntecedentTypeEnum.VALUE,
                            metric=AvailableMetricEnum.OBJECTIVE.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=ObjectiveEnum.CONVERSIONS.value),
                 Antecedent(aid=2,
                            atype=AntecedentTypeEnum.FUZZY_TREND,
                            metric=AvailableMetricEnum.RESULTS.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=LinguisticVariableEnum.DECREASING)
             ]),

    # event responses
    RuleBase(rtype=RuleTypeEnum.AUDIENCE,
             channel=ChannelEnum.FACEBOOK,
             category=RuleCategoryEnum.OPTIMIZE_TARGETING,
             importance=RuleImportanceEnum.HIGH,
             source=RuleSourceEnum.DEXTER,
             level=LevelEnum.ADSET,
             action=ActionEnum.NONE,
             redirect=RuleRedirectEnum.CAMPAIGN_MANAGER,
             template="Dexter sees your <id=1&metric_name=RSVPS&metric_type=1&antecedent_type=8> are decreasing by <id=1&value=null>% "
                      "over the last <id=1&time_interval=7> days. Have you tried opening up your targeting to be broader? Dexter suggests targeting these interests "
                      "<id=2&metric_name=INTERESTS&metric_type=4&antecedent_type=6&metric_count=5> <id=2&value=null> to get started.",
             breakdown_metadata=BreakdownMetadata(breakdown=BreakdownEnum.NONE,
                                                  action_breakdown=ActionBreakdownEnum.NONE),
             time_interval=DaysEnum.THREE_MONTHS,
             connective=Connective(LogicOperatorEnum.AND),
             antecedents=[
                 Antecedent(aid=1,
                            atype=AntecedentTypeEnum.VALUE,
                            metric=AvailableMetricEnum.OBJECTIVE.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=ObjectiveEnum.EVENT_RESPONSES.value),
                 Antecedent(aid=2,
                            atype=AntecedentTypeEnum.FUZZY_TREND,
                            metric=AvailableMetricEnum.RSVPS.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=LinguisticVariableEnum.DECREASING)
             ]),
    RuleBase(rtype=RuleTypeEnum.AUDIENCE,
             channel=ChannelEnum.FACEBOOK,
             category=RuleCategoryEnum.OPTIMIZE_TARGETING,
             importance=RuleImportanceEnum.HIGH,
             source=RuleSourceEnum.DEXTER,
             level=LevelEnum.ADSET,
             action=ActionEnum.NONE,
             redirect=RuleRedirectEnum.CAMPAIGN_MANAGER,
             template="Your <id=1&metric_name=COST_PER_RESULT&metric_type=1&antecedent_type=8> has increased by <id=1&value=null>% in the last "
                      "<id=1&time_interval=7> days. Dexter thinks you should add more interests in your targeting. Add these suggested interests "
                      "<id=2&metric_name=INTERESTS&metric_type=4&antecedent_type=6&metric_count=5> <id=2&value=null> to get started.",
             breakdown_metadata=BreakdownMetadata(breakdown=BreakdownEnum.NONE,
                                                  action_breakdown=ActionBreakdownEnum.NONE),
             time_interval=DaysEnum.THREE_MONTHS,
             connective=Connective(LogicOperatorEnum.AND),
             antecedents=[
                 Antecedent(aid=1,
                            atype=AntecedentTypeEnum.VALUE,
                            metric=AvailableMetricEnum.OBJECTIVE.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=ObjectiveEnum.EVENT_RESPONSES.value),
                 Antecedent(aid=2,
                            atype=AntecedentTypeEnum.FUZZY_TREND,
                            metric=AvailableMetricEnum.COST_PER_RESULT.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=LinguisticVariableEnum.INCREASING)
             ]),

    # lead generation
    RuleBase(rtype=RuleTypeEnum.BUDGET_AND_BID,
             channel=ChannelEnum.FACEBOOK,
             category=RuleCategoryEnum.OPTIMIZE_BUDGET,
             importance=RuleImportanceEnum.HIGH,
             source=RuleSourceEnum.DEXTER,
             level=LevelEnum.ADSET,
             action=ActionEnum.NONE,
             redirect=RuleRedirectEnum.EDIT_STRUCTURE,
             template="We love a steady flow of leads on the cheap. Nice work on your lead gen campaign, you're smashing it! Dexter suggests you "
                      "increase your budget by 25% to maximize those leads!",
             breakdown_metadata=BreakdownMetadata(breakdown=BreakdownEnum.NONE,
                                                  action_breakdown=ActionBreakdownEnum.NONE),
             time_interval=DaysEnum.THREE_MONTHS,
             connective=Connective(LogicOperatorEnum.AND),
             antecedents=[
                 Antecedent(aid=1,
                            atype=AntecedentTypeEnum.VALUE,
                            metric=AvailableMetricEnum.OBJECTIVE.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=ObjectiveEnum.LEAD_GENERATION.value),
                 Antecedent(aid=2,
                            atype=AntecedentTypeEnum.FUZZY_TREND,
                            metric=AvailableMetricEnum.LEADS.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=LinguisticVariableEnum.INCREASING)
             ]),

    # link clicks
    RuleBase(rtype=RuleTypeEnum.AUDIENCE,
             channel=ChannelEnum.FACEBOOK,
             category=RuleCategoryEnum.IMPROVE_CPC,
             importance=RuleImportanceEnum.HIGH,
             source=RuleSourceEnum.DEXTER,
             level=LevelEnum.ADSET,
             action=ActionEnum.NONE,
             redirect=RuleRedirectEnum.CAMPAIGN_MANAGER,
             template="Dexter noticed your <id=1&metric_name=CPC&metric_type=1&antecedent_type=8> has increased by <id=1&value=null>% over "
                      "the last <id=1&time_interval=7> days. Consider launching these new "
                      "<id=2&metric_name=INTERESTS&metric_type=4&antecedent_type=6&metric_count=3> <id=2&value=null> "
                      "to help grow your reach and find new users that'll convert at a lower cost.",
             breakdown_metadata=BreakdownMetadata(breakdown=BreakdownEnum.NONE,
                                                  action_breakdown=ActionBreakdownEnum.NONE),
             time_interval=DaysEnum.THREE_MONTHS,
             connective=Connective(LogicOperatorEnum.AND),
             antecedents=[
                 Antecedent(aid=1,
                            atype=AntecedentTypeEnum.VALUE,
                            metric=AvailableMetricEnum.OBJECTIVE.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=ObjectiveEnum.LINK_CLICKS.value),
                 Antecedent(aid=2,
                            atype=AntecedentTypeEnum.FUZZY_TREND,
                            metric=AvailableMetricEnum.CPC.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=LinguisticVariableEnum.INCREASING)
             ]),

    # messenger
    RuleBase(rtype=RuleTypeEnum.AUDIENCE,
             channel=ChannelEnum.FACEBOOK,
             category=RuleCategoryEnum.IMPROVE_CPR,
             importance=RuleImportanceEnum.HIGH,
             source=RuleSourceEnum.DEXTER,
             level=LevelEnum.ADSET,
             action=ActionEnum.NONE,
             redirect=RuleRedirectEnum.CAMPAIGN_MANAGER,
             template="Dexter has identified that your cost per result has increased lately. Have you tried adding new interests to "
                      "target? Do so now by adding the following <id=1&metric_name=INTERESTS&metric_type=4&antecedent_type=6&metric_count=3> "
                      "<id=1&value=null>.",
             breakdown_metadata=BreakdownMetadata(breakdown=BreakdownEnum.NONE,
                                                  action_breakdown=ActionBreakdownEnum.NONE),
             time_interval=DaysEnum.THREE_MONTHS,
             connective=Connective(LogicOperatorEnum.AND),
             antecedents=[
                 Antecedent(aid=1,
                            atype=AntecedentTypeEnum.VALUE,
                            metric=AvailableMetricEnum.OBJECTIVE.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=ObjectiveEnum.MESSAGES.value),
                 Antecedent(aid=2,
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
             action=ActionEnum.NONE,
             redirect=RuleRedirectEnum.CAMPAIGN_MANAGER,
             template="Your messenger ads aren't reaching a enough people. Dexter suggests these "
                      "id=1&metric_name=INTERESTS&metric_type=4&antecedent_type=6&metric_count=3> <id=1&value=null> to find new prospects you wouldn't have "
                      "normally found otherwise!",
             breakdown_metadata=BreakdownMetadata(breakdown=BreakdownEnum.NONE,
                                                  action_breakdown=ActionBreakdownEnum.NONE),
             time_interval=DaysEnum.THREE_MONTHS,
             connective=Connective(LogicOperatorEnum.AND),
             antecedents=[
                 Antecedent(aid=1,
                            atype=AntecedentTypeEnum.VALUE,
                            metric=AvailableMetricEnum.OBJECTIVE.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=ObjectiveEnum.MESSAGES.value),
                 Antecedent(aid=2,
                            atype=AntecedentTypeEnum.FUZZY_TREND,
                            metric=AvailableMetricEnum.REACH.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=LinguisticVariableEnum.DECREASING)
             ]),

    #  page likes
    RuleBase(rtype=RuleTypeEnum.AUDIENCE,
             channel=ChannelEnum.FACEBOOK,
             category=RuleCategoryEnum.IMPROVE_CPR,
             importance=RuleImportanceEnum.HIGH,
             source=RuleSourceEnum.DEXTER,
             level=LevelEnum.ADSET,
             action=ActionEnum.NONE,
             redirect=RuleRedirectEnum.CAMPAIGN_MANAGER,
             template="Dexter has identified that your <id=1&metric_name=COST_PER_RESULT&metric_type=1&antecedent_type=1> has decreased over the last "
                      "<id=1&time_interval=7> days. We suggest you create a new adset and consider targeting the following "
                      "<id=2&metric_name=INTERESTS&metric_type=4&antecedent_type=6&metric_count=3> <id=2&value=null> "
                      "to get more likes to your page. ",
             breakdown_metadata=BreakdownMetadata(breakdown=BreakdownEnum.NONE,
                                                  action_breakdown=ActionBreakdownEnum.NONE),
             time_interval=DaysEnum.THREE_MONTHS,
             connective=Connective(LogicOperatorEnum.AND),
             antecedents=[
                 Antecedent(aid=1,
                            atype=AntecedentTypeEnum.VALUE,
                            metric=AvailableMetricEnum.OBJECTIVE.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=ObjectiveEnum.PAGE_LIKES.value),
                 Antecedent(aid=2,
                            atype=AntecedentTypeEnum.FUZZY_TREND,
                            metric=AvailableMetricEnum.COST_PER_RESULT.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=LinguisticVariableEnum.DECREASING)
             ]),
    RuleBase(rtype=RuleTypeEnum.AUDIENCE,
             channel=ChannelEnum.FACEBOOK,
             category=RuleCategoryEnum.IMPROVE_CPR,
             importance=RuleImportanceEnum.HIGH,
             source=RuleSourceEnum.DEXTER,
             level=LevelEnum.ADSET,
             action=ActionEnum.NONE,
             redirect=RuleRedirectEnum.CAMPAIGN_MANAGER,
             template="Your <id=1&metric_name=PAGE_LIKES&metric_type=1&antecedent_type=8> have decreased by  <id=1&value=null>% over the last "
                      "<id=1&time_interval=7>days. Have you considered targeting "
                      "these <id=2&metric_name=INTERESTS&metric_type=4&antecedent_type=6&metric_count=3> <id=2&value=null>?",
             breakdown_metadata=BreakdownMetadata(breakdown=BreakdownEnum.NONE,
                                                  action_breakdown=ActionBreakdownEnum.NONE),
             time_interval=DaysEnum.THREE_MONTHS,
             connective=Connective(LogicOperatorEnum.AND),
             antecedents=[
                 Antecedent(aid=1,
                            atype=AntecedentTypeEnum.VALUE,
                            metric=AvailableMetricEnum.OBJECTIVE.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=ObjectiveEnum.PAGE_LIKES.value),
                 Antecedent(aid=2,
                            atype=AntecedentTypeEnum.FUZZY_TREND,
                            metric=AvailableMetricEnum.PAGE_LIKES.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=LinguisticVariableEnum.DECREASING)
             ]),

    # post engagement
    RuleBase(rtype=RuleTypeEnum.AUDIENCE,
             channel=ChannelEnum.FACEBOOK,
             category=RuleCategoryEnum.OPTIMIZE_TARGETING,
             importance=RuleImportanceEnum.MEDIUM,
             source=RuleSourceEnum.DEXTER,
             level=LevelEnum.ADSET,
             action=ActionEnum.NONE,
             redirect=RuleRedirectEnum.CAMPAIGN_MANAGER,
             template="The bigger the audience the more impressions. This also means the more likely it is for your ad to be seen and engaged with. "
                      "Dexter recommends you target these "
                      "<id=2&metric_name=INTERESTS&metric_type=4&antecedent_type=6&metric_count=5> <id=2&value=null> to reach more people. ",
             breakdown_metadata=BreakdownMetadata(breakdown=BreakdownEnum.NONE,
                                                  action_breakdown=ActionBreakdownEnum.NONE),
             time_interval=DaysEnum.THREE_MONTHS,
             connective=Connective(LogicOperatorEnum.AND),
             antecedents=[
                 Antecedent(aid=1,
                            atype=AntecedentTypeEnum.VALUE,
                            metric=AvailableMetricEnum.OBJECTIVE.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=ObjectiveEnum.POST_ENGAGEMENT.value),
                 Antecedent(aid=2,
                            atype=AntecedentTypeEnum.FUZZY_TREND,
                            metric=AvailableMetricEnum.IMPRESSIONS.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=LinguisticVariableEnum.DECREASING)
             ]),

    # catalog sales
    RuleBase(rtype=RuleTypeEnum.AUDIENCE,
             channel=ChannelEnum.FACEBOOK,
             category=RuleCategoryEnum.IMPROVE_ROAS,
             importance=RuleImportanceEnum.HIGH,
             source=RuleSourceEnum.DEXTER,
             level=LevelEnum.ADSET,
             action=ActionEnum.NONE,
             redirect=RuleRedirectEnum.CAMPAIGN_MANAGER,
             template="Dexter has noticed your <id=1&metric_name=PURCHASES&metric_type=1&antecedent_type=8> have slowed down by <id=1&value=null>% "
                      "over the last <id=1&time_interval=7> days. Try targeting these interests "
                      "<id=2&metric_name=INTERESTS&metric_type=4&antecedent_type=6&metric_count=3> <id=2&value=null> to increase your sales!",
             breakdown_metadata=BreakdownMetadata(breakdown=BreakdownEnum.NONE,
                                                  action_breakdown=ActionBreakdownEnum.NONE),
             time_interval=DaysEnum.THREE_MONTHS,
             connective=Connective(LogicOperatorEnum.AND),
             antecedents=[
                 Antecedent(aid=1,
                            atype=AntecedentTypeEnum.VALUE,
                            metric=AvailableMetricEnum.OBJECTIVE.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=ObjectiveEnum.PRODUCT_CATALOG_SALES.value),
                 Antecedent(aid=2,
                            atype=AntecedentTypeEnum.FUZZY_TREND,
                            metric=AvailableMetricEnum.PURCHASES.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=LinguisticVariableEnum.DECREASING)
             ]),

    # reach
    RuleBase(rtype=RuleTypeEnum.AUDIENCE,
             channel=ChannelEnum.FACEBOOK,
             category=RuleCategoryEnum.IMPROVE_CPR,
             importance=RuleImportanceEnum.HIGH,
             source=RuleSourceEnum.DEXTER,
             level=LevelEnum.ADSET,
             action=ActionEnum.NONE,
             redirect=RuleRedirectEnum.CAMPAIGN_MANAGER,
             template="Your <id=1&metric_name=FREQUENCY&metric_type=1&antecedent_type=1> is fairly high <id=1&value=null>  in the last "
                      "id=1&time_interval=7> days compared to our industry benchmarks. Have you considered these audiences "
                      "<id=2&metric_name=INTERESTS&metric_type=4&antecedent_type=6&metric_count=5> <id=2&value=null>? "
                      "Let's test them now, and we'll find the best performing ad for you!",
             breakdown_metadata=BreakdownMetadata(breakdown=BreakdownEnum.NONE,
                                                  action_breakdown=ActionBreakdownEnum.NONE),
             time_interval=DaysEnum.THREE_MONTHS,
             connective=Connective(LogicOperatorEnum.AND),
             antecedents=[
                 Antecedent(aid=1,
                            atype=AntecedentTypeEnum.VALUE,
                            metric=AvailableMetricEnum.OBJECTIVE.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=ObjectiveEnum.REACH.value),
                 Antecedent(aid=2,
                            atype=AntecedentTypeEnum.FUZZY_VALUE,
                            metric=AvailableMetricEnum.FREQUENCY.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=LinguisticVariableEnum.HIGH)
             ]),

    #  video views
]
