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
    LOW_QUALITY_RANKING
from FacebookDexter.Infrastructure.Domain.Actions.ActionEnums import FacebookActionEnum
from FacebookDexter.Infrastructure.Domain.Breakdowns import FacebookBreakdownEnum, FacebookActionBreakdownEnum
from FacebookDexter.Infrastructure.Domain.FuzzyEngine.FacebookFuzzySets import FacebookLinguisticVariableEnum
from FacebookDexter.Infrastructure.Domain.Rules.FacebookRuleEnums import FacebookRuleTypeEnum, \
    FacebookRuleCategoryEnum, FacebookRuleImportanceEnum, FacebookRuleSourceEnum, FacebookRuleRedirectEnum

RULES_AD_GENERAL = [
    RuleBase(rtype=FacebookRuleTypeEnum.BUDGET_AND_BID,
             channel=ChannelEnum.FACEBOOK,
             category=FacebookRuleCategoryEnum.IMPROVE_CPR,
             importance=FacebookRuleImportanceEnum.HIGH,
             source=FacebookRuleSourceEnum.DEXTER,
             level=LevelEnum.AD,
             action=FacebookActionEnum.NONE,
             redirect=FacebookRuleRedirectEnum.EDIT_STRUCTURE,
             template="Dexter noticed your reach has decreased! Your ads quality is also low, at this point your "
                      "ads are being penalized and delivery "
                      "is being affected. Dexter suggests creating new ads with new targeting.",
             breakdown_metadata=BreakdownMetadataBase(breakdown=FacebookBreakdownEnum.NONE,
                                                      action_breakdown=FacebookActionBreakdownEnum.NONE),
             time_interval=DaysEnum.THREE_MONTHS,
             connective=Connective(LogicOperatorEnum.AND),
             antecedents=[
                 # Antecedent(aid=1,
                 #            atype=AntecedentTypeEnum.VALUE,
                 #            metric=FacebookAvailableMetricEnum.OBJECTIVE.value,
                 #            operator=LogicOperatorEnum.EQUALS,
                 #            expected_value=ObjectiveEnum.REACH),
                 Antecedent(aid=1,
                            atype=AntecedentTypeEnum.FUZZY_VALUE,
                            metric=FacebookAvailableMetricEnum.REACH.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=FacebookLinguisticVariableEnum.DECREASING),
                 Antecedent(aid=2,
                            atype=AntecedentTypeEnum.VALUE,
                            metric=FacebookAvailableMetricEnum.QUALITY_RANKING.value,
                            operator=LogicOperatorEnum.IN,
                            expected_value=LOW_QUALITY_RANKING)
             ]),
    RuleBase(rtype=FacebookRuleTypeEnum.PERFORMANCE,
             channel=ChannelEnum.FACEBOOK,
             category=FacebookRuleCategoryEnum.IMPROVE_ENGAGEMENT,
             importance=FacebookRuleImportanceEnum.LOW,
             source=FacebookRuleSourceEnum.DEXTER,
             level=LevelEnum.AD,
             action=FacebookActionEnum.NONE,
             redirect=FacebookRuleRedirectEnum.CAMPAIGN_MANAGER,
             template="Dexter noticed your ad isn’t receiving much engagement. More engagement on brand "
                      "awareness campaigns helps deliver ads for a reduced cost, "
                      "so Dexter suggests asking a question in the first part of the adcopy to "
                      "create more engagement.",
             breakdown_metadata=BreakdownMetadataBase(breakdown=FacebookBreakdownEnum.NONE,
                                                      action_breakdown=FacebookActionBreakdownEnum.NONE),
             time_interval=DaysEnum.THREE_MONTHS,
             connective=Connective(LogicOperatorEnum.AND),
             antecedents=[
                 # Antecedent(aid=1,
                 #            atype=AntecedentTypeEnum.VALUE,
                 #            metric=FacebookAvailableMetricEnum.OBJECTIVE.value,
                 #            operator=LogicOperatorEnum.EQUALS,
                 #            expected_value=ObjectiveEnum.BRAND_AWARENESS.value),
                 Antecedent(aid=1,
                            atype=AntecedentTypeEnum.FUZZY_TREND,
                            metric=FacebookAvailableMetricEnum.ENGAGEMENT_RATE.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=FacebookLinguisticVariableEnum.DECREASING)
             ]),
    RuleBase(rtype=FacebookRuleTypeEnum.CREATIVE,
             channel=ChannelEnum.FACEBOOK,
             category=FacebookRuleCategoryEnum.IMPROVE_CONVERSION_RATE,
             importance=FacebookRuleImportanceEnum.LOW,
             source=FacebookRuleSourceEnum.DEXTER,
             level=LevelEnum.AD,
             action=FacebookActionEnum.NONE,
             redirect=FacebookRuleRedirectEnum.CAMPAIGN_MANAGER,
             template="Dexter noticed that your __id=1&metric_name=CR&metric_type=1&antecedent_type=8__ has fallen by"
                      " __id=1&value=null__% over the last __id=1&time_interval=7__ days. "
                      "Dexter knows video is king right now is proven to help with results. Have you tried "
                      "uploading a video? Try it now!",
             breakdown_metadata=BreakdownMetadataBase(breakdown=FacebookBreakdownEnum.NONE,
                                                      action_breakdown=FacebookActionBreakdownEnum.NONE),
             time_interval=DaysEnum.THREE_MONTHS,
             connective=Connective(LogicOperatorEnum.AND),
             antecedents=[
                 # Antecedent(aid=1,
                 #            atype=AntecedentTypeEnum.VALUE,
                 #            metric=FacebookAvailableMetricEnum.OBJECTIVE.value,
                 #            operator=LogicOperatorEnum.EQUALS,
                 #            expected_value=ObjectiveEnum.CONVERSIONS.value),
                 Antecedent(aid=1,
                            atype=AntecedentTypeEnum.FUZZY_TREND,
                            metric=FacebookAvailableMetricEnum.CR.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=FacebookLinguisticVariableEnum.DECREASING)
             ]),
    # post engagement
    RuleBase(rtype=FacebookRuleTypeEnum.CREATIVE,
             channel=ChannelEnum.FACEBOOK,
             category=FacebookRuleCategoryEnum.IMPROVE_ENGAGEMENT,
             importance=FacebookRuleImportanceEnum.HIGH,
             source=FacebookRuleSourceEnum.DEXTER,
             level=LevelEnum.AD,
             action=FacebookActionEnum.NONE,
             redirect=FacebookRuleRedirectEnum.CAMPAIGN_MANAGER,
             template="You can drastically improve your post engagement by asking a question in the first "
                      "sentence of your ad? Dexter "
                      "suggests making this change to help get more engagement on your ad.",
             breakdown_metadata=BreakdownMetadataBase(breakdown=FacebookBreakdownEnum.NONE,
                                                      action_breakdown=FacebookActionBreakdownEnum.NONE),
             time_interval=DaysEnum.THREE_MONTHS,
             connective=Connective(LogicOperatorEnum.AND),
             antecedents=[
                 # Antecedent(aid=1,
                 #            atype=AntecedentTypeEnum.VALUE,
                 #            metric=FacebookAvailableMetricEnum.OBJECTIVE.value,
                 #            operator=LogicOperatorEnum.EQUALS,
                 #            expected_value=ObjectiveEnum.POST_ENGAGEMENT.value),
                 Antecedent(aid=1,
                            atype=AntecedentTypeEnum.FUZZY_TREND,
                            metric=FacebookAvailableMetricEnum.RESULTS.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=FacebookLinguisticVariableEnum.DECREASING)
             ]),
    RuleBase(rtype=FacebookRuleTypeEnum.CREATIVE,
             channel=ChannelEnum.FACEBOOK,
             category=FacebookRuleCategoryEnum.IMPROVE_ENGAGEMENT,
             importance=FacebookRuleImportanceEnum.HIGH,
             source=FacebookRuleSourceEnum.DEXTER,
             level=LevelEnum.AD,
             action=FacebookActionEnum.NONE,
             redirect=FacebookRuleRedirectEnum.CAMPAIGN_MANAGER,
             template="Did you know that your cost per result will decrease as you "
                      "get more post engagement on your ad? "
                      "Dexter suggests you should try asking a question, keeping in mind who your audience is, "
                      "to further engage your audience!",
             breakdown_metadata=BreakdownMetadataBase(breakdown=FacebookBreakdownEnum.NONE,
                                                      action_breakdown=FacebookActionBreakdownEnum.NONE),
             time_interval=DaysEnum.THREE_MONTHS,
             connective=Connective(LogicOperatorEnum.AND),
             antecedents=[
                 # Antecedent(aid=1,
                 #            atype=AntecedentTypeEnum.VALUE,
                 #            metric=FacebookAvailableMetricEnum.OBJECTIVE.value,
                 #            operator=LogicOperatorEnum.EQUALS,
                 #            expected_value=ObjectiveEnum.POST_ENGAGEMENT.value),
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
             level=LevelEnum.AD,
             action=FacebookActionEnum.NONE,
             redirect=FacebookRuleRedirectEnum.EDIT_STRUCTURE,
             template="Dexter noticed that your reach has decreased and your relevancy score is low. "
                      "It's possible your ads are being penalized and your ad delivery could be affected "
                      "because of this. Dexter suggests creating new ads with new targeting "
                      "to improve your performance.",
             breakdown_metadata=BreakdownMetadataBase(breakdown=FacebookBreakdownEnum.NONE,
                                                      action_breakdown=FacebookActionBreakdownEnum.NONE),
             time_interval=DaysEnum.THREE_MONTHS,
             connective=Connective(LogicOperatorEnum.AND),
             antecedents=[
                 # Antecedent(aid=1,
                 #            atype=AntecedentTypeEnum.VALUE,
                 #            metric=FacebookAvailableMetricEnum.OBJECTIVE.value,
                 #            operator=LogicOperatorEnum.EQUALS,
                 #            expected_value=ObjectiveEnum.REACH.value),
                 Antecedent(aid=1,
                            atype=AntecedentTypeEnum.FUZZY_TREND,
                            metric=FacebookAvailableMetricEnum.REACH.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=FacebookLinguisticVariableEnum.DECREASING)
             ]),
    RuleBase(rtype=FacebookRuleTypeEnum.AUDIENCE,
             channel=ChannelEnum.FACEBOOK,
             category=FacebookRuleCategoryEnum.IMPROVE_CPR,
             importance=FacebookRuleImportanceEnum.HIGH,
             source=FacebookRuleSourceEnum.DEXTER,
             level=LevelEnum.AD,
             action=FacebookActionEnum.NONE,
             redirect=FacebookRuleRedirectEnum.CAMPAIGN_MANAGER,
             template="Dexter noticed your __id=1&metric_name=FREQUENCY&metric_type=1&antecedent_type=1__ "
                      "is fairly high __id=1&value=null__ in the last "
                      "__id=1&time_interval=7__ days compared to our industry benchmarks. Have you considered these "
                      "__id=2&metric_name=INTERESTS&metric_type=4&antecedent_type=6"
                      "&metric_count=5__ __id=2&value=null__? "
                      "Let's test them now, and we'll find the best performing ad for you!",
             breakdown_metadata=BreakdownMetadataBase(breakdown=FacebookBreakdownEnum.NONE,
                                                      action_breakdown=FacebookActionBreakdownEnum.NONE),
             time_interval=DaysEnum.THREE_MONTHS,
             connective=Connective(LogicOperatorEnum.AND),
             antecedents=[
                 # Antecedent(aid=1,
                 #            atype=AntecedentTypeEnum.VALUE,
                 #            metric=FacebookAvailableMetricEnum.OBJECTIVE.value,
                 #            operator=LogicOperatorEnum.EQUALS,
                 #            expected_value=ObjectiveEnum.REACH.value),
                 Antecedent(aid=1,
                            atype=AntecedentTypeEnum.FUZZY_VALUE,
                            metric=FacebookAvailableMetricEnum.FREQUENCY.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=FacebookLinguisticVariableEnum.HIGH)
             ]),
]
