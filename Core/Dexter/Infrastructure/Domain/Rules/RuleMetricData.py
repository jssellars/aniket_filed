import typing
from dataclasses import dataclass

from Core.Dexter.Infrastructure.Domain.Breakdowns import BreakdownBaseEnum, ActionBreakdownBaseEnum
from Core.Dexter.Infrastructure.Domain.DaysEnum import DaysEnum
from Core.Dexter.Infrastructure.Domain.Rules.RuleEnums import RuleDataFieldTypeBaseEnum


@dataclass
class RuleMetricFields:
    name: typing.AnyStr = None
    type: RuleDataFieldTypeBaseEnum = RuleDataFieldTypeBaseEnum.AVERAGE
    days: DaysEnum = DaysEnum.THREE
    breakdown: BreakdownBaseEnum = BreakdownBaseEnum.NONE
    action_breakdown: ActionBreakdownBaseEnum = ActionBreakdownBaseEnum.NONE
