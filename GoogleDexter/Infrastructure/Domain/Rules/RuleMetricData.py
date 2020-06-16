import typing
from dataclasses import dataclass

from GoogleDexter.Infrastructure.Domain.Breakdowns import BreakdownEnum, ActionBreakdownEnum
from GoogleDexter.Infrastructure.Domain.DaysEnum import DaysEnum
from GoogleDexter.Infrastructure.Domain.Rules.RuleEnums import RuleDataFieldTypeEnum


@dataclass
class RuleMetricFields:
    name: typing.AnyStr = None
    type: RuleDataFieldTypeEnum = RuleDataFieldTypeEnum.AVERAGE
    days: DaysEnum = DaysEnum.THREE
    breakdown: BreakdownEnum = BreakdownEnum.NONE
    action_breakdown: ActionBreakdownEnum = ActionBreakdownEnum.NONE
