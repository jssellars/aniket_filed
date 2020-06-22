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

RULES_AD_GENERAL = [
    RuleBase(rtype=RuleTypeEnum.BUDGET_AND_BID,
             channel=ChannelEnum.FACEBOOK,
             category=RuleCategoryEnum.IMPROVE_CPR,
             importance=RuleImportanceEnum.HIGH,
             source=RuleSourceEnum.DEXTER,
             level=LevelEnum.AD,
             action=ActionEnum.NONE,
             redirect=RuleRedirectEnum.EDIT_STRUCTURE,
             template="Your reach has decreased, but why? Your ads quality is also low, at this point your "
                      "ads are being penalized and delivery "
                      "is being affected. Dexter suggests creating new ads with new targeting.",
             breakdown_metadata=BreakdownMetadata(breakdown=BreakdownEnum.NONE,
                                                  action_breakdown=ActionBreakdownEnum.NONE),
             time_interval=DaysEnum.THREE_MONTHS,
             connective=Connective(LogicOperatorEnum.AND),
             antecedents=[
                 # Antecedent(aid=1,
                 #            atype=AntecedentTypeEnum.VALUE,
                 #            metric=AvailableMetricEnum.OBJECTIVE.value,
                 #            operator=LogicOperatorEnum.EQUALS,
                 #            expected_value=ObjectiveEnum.REACH),
                 Antecedent(aid=1,
                            atype=AntecedentTypeEnum.FUZZY_VALUE,
                            metric=AvailableMetricEnum.REACH.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=LinguisticVariableEnum.DECREASING),
                 Antecedent(aid=2,
                            atype=AntecedentTypeEnum.VALUE,
                            metric=AvailableMetricEnum.QUALITY_RANKING.value,
                            operator=LogicOperatorEnum.IN,
                            expected_value=LOW_QUALITY_RANKING)
             ]),
    RuleBase(rtype=RuleTypeEnum.PERFORMANCE,
             channel=ChannelEnum.FACEBOOK,
             category=RuleCategoryEnum.IMPROVE_ENGAGEMENT,
             importance=RuleImportanceEnum.LOW,
             source=RuleSourceEnum.DEXTER,
             level=LevelEnum.AD,
             action=ActionEnum.NONE,
             redirect=RuleRedirectEnum.CAMPAIGN_MANAGER,
             template="Your ad isn’t receiving much engagement. More engagement on brand awareness campaigns helps deliver ads for a reduced cost, "
                      "so Dexter suggests asking a question in the first part of the adcopy to create more engagement.",
             breakdown_metadata=BreakdownMetadata(breakdown=BreakdownEnum.NONE,
                                                  action_breakdown=ActionBreakdownEnum.NONE),
             time_interval=DaysEnum.THREE_MONTHS,
             connective=Connective(LogicOperatorEnum.AND),
             antecedents=[
                 # Antecedent(aid=1,
                 #            atype=AntecedentTypeEnum.VALUE,
                 #            metric=AvailableMetricEnum.OBJECTIVE.value,
                 #            operator=LogicOperatorEnum.EQUALS,
                 #            expected_value=ObjectiveEnum.BRAND_AWARENESS.value),
                 Antecedent(aid=1,
                            atype=AntecedentTypeEnum.FUZZY_TREND,
                            metric=AvailableMetricEnum.ENGAGEMENT_RATE.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=LinguisticVariableEnum.DECREASING)
             ]),
    RuleBase(rtype=RuleTypeEnum.CREATIVE,
             channel=ChannelEnum.FACEBOOK,
             category=RuleCategoryEnum.IMPROVE_CONVERSION_RATE,
             importance=RuleImportanceEnum.LOW,
             source=RuleSourceEnum.DEXTER,
             level=LevelEnum.AD,
             action=ActionEnum.NONE,
             redirect=RuleRedirectEnum.CAMPAIGN_MANAGER,
             template="Your __id=1&metric_name=CR&metric_type=1&antecedent_type=8__ has fallen by"
                      " __id=1&value=null__% over the last __id=1&time_interval=7__ days. "
                      "Dexter knows video is king right now is proven to help with results. Have you tried uploading a video? Try it now!",
             breakdown_metadata=BreakdownMetadata(breakdown=BreakdownEnum.NONE,
                                                  action_breakdown=ActionBreakdownEnum.NONE),
             time_interval=DaysEnum.THREE_MONTHS,
             connective=Connective(LogicOperatorEnum.AND),
             antecedents=[
                 # Antecedent(aid=1,
                 #            atype=AntecedentTypeEnum.VALUE,
                 #            metric=AvailableMetricEnum.OBJECTIVE.value,
                 #            operator=LogicOperatorEnum.EQUALS,
                 #            expected_value=ObjectiveEnum.CONVERSIONS.value),
                 Antecedent(aid=1,
                            atype=AntecedentTypeEnum.FUZZY_TREND,
                            metric=AvailableMetricEnum.CR.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=LinguisticVariableEnum.DECREASING)
             ]),
    # post engagement
    RuleBase(rtype=RuleTypeEnum.CREATIVE,
             channel=ChannelEnum.FACEBOOK,
             category=RuleCategoryEnum.IMPROVE_ENGAGEMENT,
             importance=RuleImportanceEnum.HIGH,
             source=RuleSourceEnum.DEXTER,
             level=LevelEnum.AD,
             action=ActionEnum.NONE,
             redirect=RuleRedirectEnum.CAMPAIGN_MANAGER,
             template="Did you know you can drastically improve your post engagement by asking a question in the first sentence of your ad? Dexter "
                      "suggests you make this change to help improve your results!",
             breakdown_metadata=BreakdownMetadata(breakdown=BreakdownEnum.NONE,
                                                  action_breakdown=ActionBreakdownEnum.NONE),
             time_interval=DaysEnum.THREE_MONTHS,
             connective=Connective(LogicOperatorEnum.AND),
             antecedents=[
                 # Antecedent(aid=1,
                 #            atype=AntecedentTypeEnum.VALUE,
                 #            metric=AvailableMetricEnum.OBJECTIVE.value,
                 #            operator=LogicOperatorEnum.EQUALS,
                 #            expected_value=ObjectiveEnum.POST_ENGAGEMENT.value),
                 Antecedent(aid=1,
                            atype=AntecedentTypeEnum.FUZZY_TREND,
                            metric=AvailableMetricEnum.RESULTS.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=LinguisticVariableEnum.DECREASING)
             ]),
    RuleBase(rtype=RuleTypeEnum.CREATIVE,
             channel=ChannelEnum.FACEBOOK,
             category=RuleCategoryEnum.IMPROVE_ENGAGEMENT,
             importance=RuleImportanceEnum.HIGH,
             source=RuleSourceEnum.DEXTER,
             level=LevelEnum.AD,
             action=ActionEnum.NONE,
             redirect=RuleRedirectEnum.CAMPAIGN_MANAGER,
             template="Did you know that your cost per result will decrease as you get more post engagement on your ad? Try asking a question, "
                      "keeping in mind who your audience is, to further engage your audience!",
             breakdown_metadata=BreakdownMetadata(breakdown=BreakdownEnum.NONE,
                                                  action_breakdown=ActionBreakdownEnum.NONE),
             time_interval=DaysEnum.THREE_MONTHS,
             connective=Connective(LogicOperatorEnum.AND),
             antecedents=[
                 # Antecedent(aid=1,
                 #            atype=AntecedentTypeEnum.VALUE,
                 #            metric=AvailableMetricEnum.OBJECTIVE.value,
                 #            operator=LogicOperatorEnum.EQUALS,
                 #            expected_value=ObjectiveEnum.POST_ENGAGEMENT.value),
                 Antecedent(aid=1,
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
             level=LevelEnum.AD,
             action=ActionEnum.NONE,
             redirect=RuleRedirectEnum.EDIT_STRUCTURE,
             template="Your reach has decreased, but why? Your relevancy score is below most likely very low, at this point your ads are being penalized "
                      "and delivery is being affected. Dexter suggests creating new ads with new targeting.",
             breakdown_metadata=BreakdownMetadata(breakdown=BreakdownEnum.NONE,
                                                  action_breakdown=ActionBreakdownEnum.NONE),
             time_interval=DaysEnum.THREE_MONTHS,
             connective=Connective(LogicOperatorEnum.AND),
             antecedents=[
                 # Antecedent(aid=1,
                 #            atype=AntecedentTypeEnum.VALUE,
                 #            metric=AvailableMetricEnum.OBJECTIVE.value,
                 #            operator=LogicOperatorEnum.EQUALS,
                 #            expected_value=ObjectiveEnum.REACH.value),
                 Antecedent(aid=1,
                            atype=AntecedentTypeEnum.FUZZY_TREND,
                            metric=AvailableMetricEnum.REACH.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=LinguisticVariableEnum.DECREASING)
             ]),
    RuleBase(rtype=RuleTypeEnum.AUDIENCE,
             channel=ChannelEnum.FACEBOOK,
             category=RuleCategoryEnum.IMPROVE_CPR,
             importance=RuleImportanceEnum.HIGH,
             source=RuleSourceEnum.DEXTER,
             level=LevelEnum.AD,
             action=ActionEnum.NONE,
             redirect=RuleRedirectEnum.CAMPAIGN_MANAGER,
             template="Your __id=1&metric_name=FREQUENCY&metric_type=1&antecedent_type=1__ is fairly high __id=1&value=null__ in the last "
                      "__id=1&time_interval=7__ days compared to our industry benchmarks. Have you considered these "
                      "__id=2&metric_name=INTERESTS&metric_type=4&antecedent_type=6&metric_count=5__ __id=2&value=null__? "
                      "Let's test them now, and we'll find the best performing ad for you!",
             breakdown_metadata=BreakdownMetadata(breakdown=BreakdownEnum.NONE,
                                                  action_breakdown=ActionBreakdownEnum.NONE),
             time_interval=DaysEnum.THREE_MONTHS,
             connective=Connective(LogicOperatorEnum.AND),
             antecedents=[
                 # Antecedent(aid=1,
                 #            atype=AntecedentTypeEnum.VALUE,
                 #            metric=AvailableMetricEnum.OBJECTIVE.value,
                 #            operator=LogicOperatorEnum.EQUALS,
                 #            expected_value=ObjectiveEnum.REACH.value),
                 Antecedent(aid=1,
                            atype=AntecedentTypeEnum.FUZZY_VALUE,
                            metric=AvailableMetricEnum.FREQUENCY.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=LinguisticVariableEnum.HIGH)
             ]),
]
