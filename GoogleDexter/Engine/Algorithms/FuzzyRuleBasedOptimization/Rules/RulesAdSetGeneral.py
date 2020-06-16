from GoogleDexter.Engine.Algorithms.FuzzyRuleBasedOptimization.Metrics.AvailableMetricEnum import AvailableMetricEnum
from GoogleDexter.Infrastructure.Domain.Actions.ActionEnums import ActionEnum
from GoogleDexter.Infrastructure.Domain.Breakdowns import BreakdownMetadata, BreakdownEnum, ActionBreakdownEnum
from GoogleDexter.Infrastructure.Domain.ChannelEnum import ChannelEnum
from GoogleDexter.Infrastructure.Domain.DaysEnum import DaysEnum
from GoogleDexter.Infrastructure.Domain.LevelEnums import LevelEnum
from GoogleDexter.Infrastructure.Domain.LogicalOperatorEnum import LogicOperatorEnum
from GoogleDexter.Infrastructure.Domain.Rules.Antecedent import Antecedent
from GoogleDexter.Infrastructure.Domain.Rules.AntecedentEnums import AntecedentTypeEnum
from GoogleDexter.Infrastructure.Domain.Rules.Connective import Connective
from GoogleDexter.Infrastructure.Domain.Rules.RuleBase import RuleBase
from GoogleDexter.Infrastructure.Domain.Rules.RuleEnums import RuleTypeEnum, RuleCategoryEnum, RuleImportanceEnum, \
    RuleSourceEnum, RuleRedirectEnum

RULES_ADSET_GENERAL = [
    RuleBase(rtype=RuleTypeEnum.PERFORMANCE,
             channel=ChannelEnum.GOOGLE,
             category=RuleCategoryEnum.OPTIMIZE_TARGETING,
             importance=RuleImportanceEnum.HIGH,
             source=RuleSourceEnum.DEXTER,
             level=LevelEnum.ADGROUP,
             action=ActionEnum.NONE,
             redirect=RuleRedirectEnum.CAMPAIGN_MANAGER,
             template="You have multiple keywords in your ad groups!",
             breakdown_metadata=BreakdownMetadata(breakdown=BreakdownEnum.NONE,
                                                  action_breakdown=ActionBreakdownEnum.NONE),
             time_interval=DaysEnum.THREE_MONTHS,
             connective=Connective(LogicOperatorEnum.AND),
             antecedents=[
                 Antecedent(aid=1,
                            atype=AntecedentTypeEnum.VALUE,
                            metric=AvailableMetricEnum.MULTIPLE_KEYWORDS_PER_ADGROUP.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=True),
             ]),
]
