from enum import Enum
from typing import Any

from FacebookDexter.Infrastructure.DexterApplyActions.BreakdownSplitActions import AgeGenderBreakdownSplit
from FacebookDexter.Infrastructure.DexterApplyActions.BudgetActions import BudgetDecreaseAction, BudgetIncreaseAction
from FacebookDexter.Infrastructure.DexterApplyActions.CreateLookalike import CreateLookalike
from FacebookDexter.Infrastructure.DexterApplyActions.DuplicateAdsets import DuplicateAdset


class ApplyActionType(Enum):
    BUDGET_INCREASE = BudgetIncreaseAction
    BUDGET_DECREASE = BudgetDecreaseAction
    AGE_GENDER_BREAKDOWN_SPLIT = AgeGenderBreakdownSplit
    DUPLICATE_AND_PAUSE_STRUCTURE = DuplicateAdset
    CREATE_LOOKALIKE = CreateLookalike


def get_apply_action(action_type: ApplyActionType, config: Any, fixtures: Any):
    if not action_type:
        return None

    return ApplyActionType(action_type).value(config, fixtures)
