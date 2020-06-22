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

RULES_CAMPAIGN_CREATE_AUDIENCE = [
    RuleBase(rtype=RuleTypeEnum.AUDIENCE,
             channel=ChannelEnum.FACEBOOK,
             category=RuleCategoryEnum.IMPROVE_CPR,
             importance=RuleImportanceEnum.HIGH,
             source=RuleSourceEnum.DEXTER,
             level=LevelEnum.CAMPAIGN,
             action=ActionEnum.NONE,
             redirect=RuleRedirectEnum.CREATE_RETARGETING_AUDIENCE,
             template="Dexter noticed your __id=1&metric_name=COST_PER_RESULT&metric_type=1&antecedent_type=8__ has increased by __id=1&value=null__% in the last "
                      "__id=1&time_interval=14__ days. You should create a retargeting audience and give your campaign a boost.",
             breakdown_metadata=BreakdownMetadata(breakdown=BreakdownEnum.NONE,
                                                  action_breakdown=ActionBreakdownEnum.NONE),
             time_interval=DaysEnum.THREE_MONTHS,
             connective=Connective(LogicOperatorEnum.AND),
             antecedents=[
                 Antecedent(aid=1,
                            atype=AntecedentTypeEnum.FUZZY_TREND,
                            metric=AvailableMetricEnum.COST_PER_RESULT.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=LinguisticVariableEnum.INCREASING),
                 Antecedent(aid=2,
                            atype=AntecedentTypeEnum.VALUE,
                            metric=AvailableMetricEnum.PROSPECTING_CAMPAIGN.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=True)
             ]),
    # TODO: check with Chase if this is value or percentage
    RuleBase(rtype=RuleTypeEnum.AUDIENCE,
             channel=ChannelEnum.FACEBOOK,
             category=RuleCategoryEnum.IMPROVE_CPR,
             importance=RuleImportanceEnum.HIGH,
             source=RuleSourceEnum.DEXTER,
             level=LevelEnum.CAMPAIGN,
             action=ActionEnum.NONE,
             redirect=RuleRedirectEnum.CREATE_RETARGETING_AUDIENCE,
             template="Dexter noticed your __id=1&metric_name=ROAS&metric_type=1&antecedent_type=7__ has decreased by __id=1&value=null__ in the last "
                      "__id=1&time_interval=14__ days. You should create a retargeting audience and give your campaign a boost.",
             breakdown_metadata=BreakdownMetadata(breakdown=BreakdownEnum.NONE,
                                                  action_breakdown=ActionBreakdownEnum.NONE),
             time_interval=DaysEnum.THREE_MONTHS,
             connective=Connective(LogicOperatorEnum.AND),
             antecedents=[
                 Antecedent(aid=1,
                            atype=AntecedentTypeEnum.FUZZY_TREND,
                            metric=AvailableMetricEnum.ROAS.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=LinguisticVariableEnum.DECREASING),
                 Antecedent(aid=2,
                            atype=AntecedentTypeEnum.VALUE,
                            metric=AvailableMetricEnum.PROSPECTING_CAMPAIGN.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=True)
             ]),
]
