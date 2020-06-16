import typing

from GoogleDexter.Infrastructure.Domain.Actions.ActionDetailsBuilder import ActionEnum
from GoogleDexter.Infrastructure.Domain.Breakdowns import BreakdownMetadata
from GoogleDexter.Infrastructure.Domain.ChannelEnum import ChannelEnum
from GoogleDexter.Infrastructure.Domain.DaysEnum import DaysEnum
from GoogleDexter.Infrastructure.Domain.LevelEnums import LevelEnum
from GoogleDexter.Infrastructure.Domain.LogicalOperatorEnum import LogicOperatorEnum
from GoogleDexter.Infrastructure.Domain.Rules.Antecedent import Antecedent
from GoogleDexter.Infrastructure.Domain.Rules.Connective import Connective
from GoogleDexter.Infrastructure.Domain.Rules.RuleEnums import RuleTypeEnum, RuleImportanceEnum, RuleSourceEnum, \
    RuleCategoryEnum, RuleRedirectEnum


class RuleBase:
    def __init__(self,
                 action: ActionEnum = None,
                 rtype: RuleTypeEnum = RuleTypeEnum.PERFORMANCE,
                 antecedents: typing.List[Antecedent] = None,
                 connective: Connective = None,
                 template: typing.AnyStr = None,
                 importance: RuleImportanceEnum = RuleImportanceEnum.HIGH,
                 source: RuleSourceEnum = RuleSourceEnum.DEXTER,
                 level: LevelEnum = None,
                 breakdown_metadata: BreakdownMetadata = None,
                 time_interval: DaysEnum = None,
                 channel: ChannelEnum = None,
                 category: RuleCategoryEnum = None,
                 redirect: RuleRedirectEnum = None):
        self.action = action
        self.type = rtype
        self.antecedents = antecedents
        self.connective = connective if connective else Connective(LogicOperatorEnum.AND)
        self.template = template
        self.importance = importance
        self.source = source
        self.level = level
        self.breakdown_metadata = breakdown_metadata
        self.time_interval = time_interval
        self.channel = channel
        self.category = category
        self.redirect = redirect

    def get_antecedents_by_metric(self, metric_name: typing.AnyStr = None):
        return [antecedent for antecedent in self.antecedents if antecedent.metric_name == metric_name]
