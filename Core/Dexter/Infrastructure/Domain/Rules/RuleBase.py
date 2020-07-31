import typing

from Core.Dexter.Infrastructure.Domain.Actions.ActionEnumBase import ActionEnumBase
from Core.Dexter.Infrastructure.Domain.Breakdowns import BreakdownMetadataBase
from Core.Dexter.Infrastructure.Domain.ChannelEnum import ChannelEnum
from Core.Dexter.Infrastructure.Domain.DaysEnum import DaysEnum
from Core.Dexter.Infrastructure.Domain.LevelEnums import LevelEnum
from Core.Dexter.Infrastructure.Domain.LogicalOperatorEnum import LogicOperatorEnum
from Core.Dexter.Infrastructure.Domain.Rules.Antecedent import Antecedent
from Core.Dexter.Infrastructure.Domain.Rules.Connective import Connective
from Core.Dexter.Infrastructure.Domain.Rules.RuleEnums import RuleTypeEnumBase, RuleCategoryEnumBase, \
    RuleRedirectEnumBase, RuleImportanceEnumBase, RuleSourceEnumBase


class RuleBase:
    def __init__(self,
                 action: ActionEnumBase = None,
                 rtype: RuleTypeEnumBase = None,
                 antecedents: typing.List[Antecedent] = None,
                 connective: Connective = None,
                 template: typing.AnyStr = None,
                 alternative_template: typing.AnyStr = None,
                 importance: RuleImportanceEnumBase = None,
                 source: RuleSourceEnumBase = None,
                 level: LevelEnum = None,
                 breakdown_metadata: BreakdownMetadataBase = None,
                 time_interval: DaysEnum = None,
                 channel: ChannelEnum = None,
                 category: RuleCategoryEnumBase = None,
                 redirect: RuleRedirectEnumBase = None,
                 variance: int = None):
        self.action = action
        self.type = rtype
        self.antecedents = antecedents
        self.connective = connective if connective else Connective(LogicOperatorEnum.AND)
        self.template = template
        self.alternative_template = alternative_template
        self.importance = importance
        self.source = source
        self.level = level
        self.breakdown_metadata = breakdown_metadata
        self.time_interval = time_interval
        self.channel = channel
        self.category = category
        self.redirect = redirect
        self.variance = variance

    def get_antecedents_by_metric(self, metric_name: typing.AnyStr = None):
        return [antecedent for antecedent in self.antecedents if antecedent.metric_name == metric_name]

    def get_rule_number_of_metrics(self):
        return len(self.antecedents)
