import typing

from FacebookDexter.Infrastructure.Domain.Actions.ActionDetailsBuilder import ActionEnum
from FacebookDexter.Infrastructure.Domain.Breakdowns import BreakdownMetadata
from FacebookDexter.Infrastructure.Domain.ChannelEnum import ChannelEnum
from FacebookDexter.Infrastructure.Domain.DaysEnum import DaysEnum
from FacebookDexter.Infrastructure.Domain.LevelEnums import LevelEnum
from FacebookDexter.Infrastructure.Domain.LogicalOperatorEnum import LogicOperatorEnum
from FacebookDexter.Infrastructure.Domain.Rules.Antecedent import Antecedent
from FacebookDexter.Infrastructure.Domain.Rules.RuleEnums import RuleTypeEnum, RuleImportanceEnum, RuleSourceEnum, RuleCategoryEnum


class RuleBase:
    def __init__(self,
                 action: ActionEnum = None,
                 rtype: RuleTypeEnum = RuleTypeEnum.PERFORMANCE,
                 antecedents: typing.List[Antecedent] = None,
                 connective: LogicOperatorEnum = None,
                 template: typing.AnyStr = None,
                 importance: RuleImportanceEnum = RuleImportanceEnum.HIGH,
                 source: RuleSourceEnum = RuleSourceEnum.DEXTER,
                 level: LevelEnum = None,
                 breakdown_metadata: BreakdownMetadata = None,
                 time_interval: DaysEnum = None,
                 channel: ChannelEnum = None,
                 category: RuleCategoryEnum = None):
        self.action = action
        self.type = rtype
        self.antecedents = antecedents
        self.connective = connective if connective else LogicOperatorEnum.AND
        self.template = template
        self.importance = importance
        self.source = source
        self.level = level
        self.breakdown_metadata = breakdown_metadata
        self.time_interval = time_interval
        self.channel = channel
        self.category = category

    def get_antecedents_by_metric(self, metric_name: typing.AnyStr = None):
        return [antecedent for antecedent in self.antecedents if antecedent.metric_name == metric_name]
