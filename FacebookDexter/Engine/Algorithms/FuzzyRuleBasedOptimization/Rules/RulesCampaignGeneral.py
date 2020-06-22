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

RULES_CAMPAIGN_GENERAL = [
    # brand awareness
    RuleBase(rtype=RuleTypeEnum.BUDGET_AND_BID,
             channel=ChannelEnum.FACEBOOK,
             category=RuleCategoryEnum.OPTIMIZE_BUDGET,
             importance=RuleImportanceEnum.HIGH,
             source=RuleSourceEnum.DEXTER,
             level=LevelEnum.CAMPAIGN,
             action=ActionEnum.NONE,
             redirect=RuleRedirectEnum.EDIT_STRUCTURE,
             template="You’re __id=1&metric_name=REACH&metric_type=1&antecedent_type=1__ing tons of new people each day, "
                      "__id=1&value=null__ people in the last __id=1&time_interval=7__ days to be "
                      "exact. Your cost per click is relatively stable, too. Dexter suggests increasing your budget by 25%.",
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
                            metric=AvailableMetricEnum.REACH.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=LinguisticVariableEnum.INCREASING)
             ]),
    # conversions
    RuleBase(rtype=RuleTypeEnum.CREATIVE,
             channel=ChannelEnum.FACEBOOK,
             category=RuleCategoryEnum.IMPROVE_CPR,
             importance=RuleImportanceEnum.HIGH,
             source=RuleSourceEnum.DEXTER,
             level=LevelEnum.CAMPAIGN,
             action=ActionEnum.NONE,
             redirect=RuleRedirectEnum.CAMPAIGN_MANAGER,
             template="Your __id=1&metric_name=COST_PER_RESULT&metric_type=1&antecedent_type=8__ has increased by __id=1&value=null__% in last "
                      "__id=1&time_interval=7__ days. Have you tried targeting a more specific audience and excluding audiences you "
                      "know won't work or who have converted already?",
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
             level=LevelEnum.CAMPAIGN,
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
    # TODO: also check with chase if difference or percentage
    RuleBase(rtype=RuleTypeEnum.CREATIVE,
             channel=ChannelEnum.FACEBOOK,
             category=RuleCategoryEnum.IMPROVE_CPC,
             importance=RuleImportanceEnum.HIGH,
             source=RuleSourceEnum.DEXTER,
             level=LevelEnum.CAMPAIGN,
             action=ActionEnum.NONE,
             redirect=RuleRedirectEnum.EDIT_STRUCTURE,
             template="Dexter noticed your __id=1&metric_name=LINK_CLICKS&metric_type=1&antecedent_type=8__ have fallen by "
                      "__id=1&value=null__% over the last __id=1&time_interval=7__ days. "
                      "Have you considered testing different variations of ad copy or creative?",
             breakdown_metadata=BreakdownMetadata(breakdown=BreakdownEnum.NONE,
                                                  action_breakdown=ActionBreakdownEnum.NONE),
             time_interval=DaysEnum.THREE_MONTHS,
             connective=Connective(LogicOperatorEnum.AND),
             antecedents=[
                 # Antecedent(aid=1,
                 #            atype=AntecedentTypeEnum.VALUE,
                 #            metric=AvailableMetricEnum.OBJECTIVE.value,
                 #            operator=LogicOperatorEnum.EQUALS,
                 #            expected_value=ObjectiveEnum.LINK_CLICKS.value),
                 Antecedent(aid=1,
                            atype=AntecedentTypeEnum.FUZZY_TREND,
                            metric=AvailableMetricEnum.LINK_CLICKS.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=LinguisticVariableEnum.DECREASING)
             ]),
    # reach
    RuleBase(rtype=RuleTypeEnum.BUDGET_AND_BID,
             channel=ChannelEnum.FACEBOOK,
             category=RuleCategoryEnum.IMPROVE_CPR,
             importance=RuleImportanceEnum.HIGH,
             source=RuleSourceEnum.DEXTER,
             level=LevelEnum.CAMPAIGN,
             action=ActionEnum.NONE,
             redirect=RuleRedirectEnum.EDIT_STRUCTURE,
             template="Your clicks are decreasing and your CPM is increasing, while results are low. "
                      "Dexter suggests decreasing the budget by 25%.",
             breakdown_metadata=BreakdownMetadata(breakdown=BreakdownEnum.NONE,
                                                  action_breakdown=ActionBreakdownEnum.NONE),
             time_interval=DaysEnum.THREE_MONTHS,
             connective=Connective(LogicOperatorEnum.AND),
             antecedents=[
                 Antecedent(aid=1,
                            atype=AntecedentTypeEnum.FUZZY_TREND,
                            metric=AvailableMetricEnum.CLICKS.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=LinguisticVariableEnum.DECREASING),
                 Antecedent(aid=2,
                            atype=AntecedentTypeEnum.FUZZY_TREND,
                            metric=AvailableMetricEnum.CPM.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=LinguisticVariableEnum.INCREASING),
                 Antecedent(aid=3,
                            atype=AntecedentTypeEnum.VALUE,
                            metric=AvailableMetricEnum.RESULTS.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=LinguisticVariableEnum.LOW)
             ])
]
