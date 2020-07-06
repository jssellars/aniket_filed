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

RULES_ADSET_REMOVE_AGE_GROUPS = [
    RuleBase(rtype=RuleTypeEnum.AUDIENCE,
             channel=ChannelEnum.FACEBOOK,
             category=RuleCategoryEnum.OPTIMIZE_TARGETING,
             importance=RuleImportanceEnum.MEDIUM,
             source=RuleSourceEnum.DEXTER,
             level=LevelEnum.ADSET,
             action=ActionEnum.REMOVE,
             redirect=RuleRedirectEnum.CAMPAIGN_MANAGER,
             template="Your __id=1&metric_name=RESULTS&metric_type=1&antecedent_type=8__ have decreased by "
                      "__id=1&value=null__% in the last "
                      "__id=1&time_interval=7__ days for some of the age groups you are targeting. Dexter recommends "
                      "you stop targeting the "
                      "following age ranges __id=1&breakdown_values=null__.",
             alternative_template="Your __id=1&metric_name=RESULTS&metric_type=1&antecedent_type=8__ have decreased by __id=1&value=null__% in the last "
                                  "__id=1&time_interval=7__ days for all age groups you are targeting. Dexter recommends "
                                  "you pause this ad set.",
             breakdown_metadata=BreakdownMetadata(breakdown=BreakdownEnum.AGE,
                                                  action_breakdown=ActionBreakdownEnum.NONE),
             time_interval=DaysEnum.THREE_MONTHS,
             connective=Connective(LogicOperatorEnum.AND),
             antecedents=[
                 Antecedent(aid=1,
                            atype=AntecedentTypeEnum.FUZZY_VALUE,
                            metric=AvailableMetricEnum.SPEND.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=LinguisticVariableEnum.HIGH),
                 Antecedent(aid=2,
                            atype=AntecedentTypeEnum.FUZZY_VALUE,
                            metric=AvailableMetricEnum.RESULTS.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=LinguisticVariableEnum.LOW),
                 Antecedent(aid=3,
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
             template="Your __id=1&metric_name=RESULTS&metric_type=1&antecedent_type=8__ have decreased by "
                      "__id=1&value=null__% in the last "
                      "__id=1&time_interval=7__ days for some of the age groups you are targeting. Dexter recommends "
                      "you stop targeting the "
                      "following age ranges __id=1&breakdown_values=null__.",
             alternative_template="Your __id=1&metric_name=RESULTS&metric_type=1&antecedent_type=8__ have decreased by __id=1&value=null__% in the last "
                                  "__id=1&time_interval=7__ days for all age groups you are targeting. Dexter recommends "
                                  "you pause this ad set.",
             breakdown_metadata=BreakdownMetadata(breakdown=BreakdownEnum.AGE,
                                                  action_breakdown=ActionBreakdownEnum.NONE),
             time_interval=DaysEnum.THREE_MONTHS,
             connective=Connective(LogicOperatorEnum.AND),
             antecedents=[
                 Antecedent(aid=1,
                            atype=AntecedentTypeEnum.FUZZY_VALUE,
                            metric=AvailableMetricEnum.SPEND.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=LinguisticVariableEnum.HIGH),
                 Antecedent(aid=2,
                            atype=AntecedentTypeEnum.FUZZY_VALUE,
                            metric=AvailableMetricEnum.RESULTS.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=LinguisticVariableEnum.LOW),
                 Antecedent(aid=3,
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
             template="Your __id=1&metric_name=RESULTS&metric_type=1&antecedent_type=8__ have decreased by "
                      "__id=1&value=null__% in the last "
                      "__id=1&time_interval=7__ days for some of the age groups you are targeting. Dexter recommends "
                      "you stop targeting the "
                      "following age ranges __id=1&breakdown_values=null__.",
             alternative_template="Your __id=1&metric_name=RESULTS&metric_type=1&antecedent_type=8__ have decreased by __id=1&value=null__% in the last "
                                  "__id=1&time_interval=7__ days for all age groups you are targeting. Dexter recommends "
                                  "you pause this ad set.",
             breakdown_metadata=BreakdownMetadata(breakdown=BreakdownEnum.AGE,
                                                  action_breakdown=ActionBreakdownEnum.NONE),
             time_interval=DaysEnum.THREE_MONTHS,
             connective=Connective(LogicOperatorEnum.AND),
             antecedents=[
                 Antecedent(aid=1,
                            atype=AntecedentTypeEnum.FUZZY_VALUE,
                            metric=AvailableMetricEnum.CPC.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=LinguisticVariableEnum.HIGH),
                 Antecedent(aid=2,
                            atype=AntecedentTypeEnum.FUZZY_VALUE,
                            metric=AvailableMetricEnum.RESULTS.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=LinguisticVariableEnum.LOW),
             ]),
    RuleBase(rtype=RuleTypeEnum.AUDIENCE,
             channel=ChannelEnum.FACEBOOK,
             category=RuleCategoryEnum.OPTIMIZE_TARGETING,
             importance=RuleImportanceEnum.MEDIUM,
             source=RuleSourceEnum.DEXTER,
             level=LevelEnum.ADSET,
             action=ActionEnum.REMOVE,
             redirect=RuleRedirectEnum.CAMPAIGN_MANAGER,
             template="Your __id=1&metric_name=RESULTS&metric_type=1&antecedent_type=8__ have decreased by "
                      "__id=1&value=null__% in the last "
                      "__id=1&time_interval=7__ days for some of the age groups you are targeting. Dexter recommends "
                      "you stop targeting the "
                      "following age ranges __id=1&breakdown_values=null__.",
             alternative_template="Your __id=1&metric_name=RESULTS&metric_type=1&antecedent_type=8__ have decreased by __id=1&value=null__% in the last "
                                  "__id=1&time_interval=7__ days for all age groups you are targeting. Dexter recommends "
                                  "you pause this ad set.",
             breakdown_metadata=BreakdownMetadata(breakdown=BreakdownEnum.AGE,
                                                  action_breakdown=ActionBreakdownEnum.NONE),
             time_interval=DaysEnum.THREE_MONTHS,
             connective=Connective(LogicOperatorEnum.AND),
             antecedents=[
                 Antecedent(aid=1,
                            atype=AntecedentTypeEnum.FUZZY_VALUE,
                            metric=AvailableMetricEnum.CPC.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=LinguisticVariableEnum.HIGH),
                 Antecedent(aid=2,
                            atype=AntecedentTypeEnum.VALUE,
                            metric=AvailableMetricEnum.RESULTS.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=0),
             ])
]
