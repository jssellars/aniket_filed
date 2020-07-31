from Core.Dexter.Infrastructure.Domain.Breakdowns import BreakdownMetadataBase
from Core.Dexter.Infrastructure.Domain.ChannelEnum import ChannelEnum
from Core.Dexter.Infrastructure.Domain.DaysEnum import DaysEnum
from Core.Dexter.Infrastructure.Domain.LevelEnums import LevelEnum
from Core.Dexter.Infrastructure.Domain.LogicalOperatorEnum import LogicOperatorEnum
from Core.Dexter.Infrastructure.Domain.Rules.Antecedent import Antecedent
from Core.Dexter.Infrastructure.Domain.Rules.AntecedentEnums import AntecedentTypeEnum
from Core.Dexter.Infrastructure.Domain.Rules.Connective import Connective
from Core.Dexter.Infrastructure.Domain.Rules.RuleBase import RuleBase
from GoogleDexter.Engine.Algorithms.FuzzyRuleBasedOptimization.Metrics.GoogleAvailableMetricEnum import GoogleAvailableMetricEnum
from GoogleDexter.Infrastructure.Domain.Actions.ActionEnums import GoogleActionEnum
from GoogleDexter.Infrastructure.Domain.Breakdowns import GoogleBreakdownEnum, GoogleActionBreakdownEnum
from GoogleDexter.Infrastructure.Domain.Rules.GoogleRuleEnums import GoogleRuleTypeEnum, GoogleRuleCategoryEnum, \
    GoogleRuleImportanceEnum, GoogleRuleSourceEnum, GoogleRuleRedirectEnum

RULES_ADSET_GENERAL = [
    RuleBase(rtype=GoogleRuleTypeEnum.PERFORMANCE,
             channel=ChannelEnum.GOOGLE,
             category=GoogleRuleCategoryEnum.OPTIMIZE_TARGETING,
             importance=GoogleRuleImportanceEnum.HIGH,
             source=GoogleRuleSourceEnum.DEXTER,
             level=LevelEnum.ADGROUP,
             action=GoogleActionEnum.NONE,
             redirect=GoogleRuleRedirectEnum.CAMPAIGN_MANAGER,
             template="You have multiple keywords in your ad groups!",
             breakdown_metadata=BreakdownMetadataBase(breakdown=GoogleBreakdownEnum.NONE,
                                                  action_breakdown=GoogleActionBreakdownEnum.NONE),
             time_interval=DaysEnum.THREE_MONTHS,
             connective=Connective(LogicOperatorEnum.AND),
             antecedents=[
                 Antecedent(aid=1,
                            atype=AntecedentTypeEnum.VALUE,
                            metric=GoogleAvailableMetricEnum.MULTIPLE_KEYWORDS_PER_ADGROUP.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=True),
             ]),
]
