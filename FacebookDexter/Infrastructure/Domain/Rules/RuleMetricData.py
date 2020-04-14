import typing
from dataclasses import dataclass

from FacebookDexter.Infrastructure.Domain.Breakdowns import BreakdownEnum, ActionBreakdownEnum
from FacebookDexter.Infrastructure.Domain.DaysEnum import DaysEnum
from FacebookDexter.Infrastructure.Domain.Rules.RuleEnums import RuleDataFieldTypeEnum


@dataclass
class RuleMetricFields:
    name: typing.AnyStr = None
    type: RuleDataFieldTypeEnum = RuleDataFieldTypeEnum.AVERAGE
    days: DaysEnum = DaysEnum.THREE
    breakdown: BreakdownEnum = BreakdownEnum.NONE
    action_breakdown: ActionBreakdownEnum = ActionBreakdownEnum.NONE
