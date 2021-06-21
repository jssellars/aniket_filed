from dataclasses import dataclass
from typing import ClassVar, Dict, Optional

from FacebookDexter.Infrastructure.DexterApplyActions.ApplyActionsUtils import (
    _does_budget_exist,
    _get_budget_value_and_type,
    update_turing_structure,
)
from FacebookDexter.Infrastructure.DexterApplyActions.RecommendationApplyActions import (
    ApplyButtonType,
    ApplyParameters,
    RecommendationAction,
)

BUDGET_INCREASE_PERCENTAGE = 0.20
BUDGET_DECREASE_PERCENTAGE = 0.20


@dataclass
class BudgetAlterAction(RecommendationAction):
    def process_action(
        self,
        recommendation: Dict,
        headers: str,
        apply_button_type: ApplyButtonType,
        command: dict = None,
    ):
        update_turing_structure(self.config, recommendation, headers)
        return None

    def get_action_parameters(self, apply_parameters: ApplyParameters, structure_details: Dict) -> Optional[Dict]:
        raise NotImplementedError


@dataclass
class BudgetIncreaseAction(BudgetAlterAction):
    APPLY_TOOLTIP: ClassVar[str] = (
        f"Selecting apply will increase the budget for this {{level}} by " f"{BUDGET_INCREASE_PERCENTAGE * 100}%"
    )

    SUCCESS_FEEDBACK: ClassVar[
        str
    ] = f"Dexter successfully increased the budget {BUDGET_INCREASE_PERCENTAGE * 100}% for this AdSet."
    FAILURE_FEEDBACK: ClassVar[str] = "Failure (due to error): Dexter was unsuccessful in increasing the budget."

    def get_action_parameters(self, apply_parameters: ApplyParameters, structure_details: Dict) -> Optional[Dict]:
        if not apply_parameters:
            return None

        if not _does_budget_exist(structure_details):
            return None

        budget, budget_type = _get_budget_value_and_type(structure_details)

        if not budget or not budget_type:
            return

        new_budget = budget + apply_parameters.budget_increase * budget
        action_details = {"details": {budget_type: new_budget}}

        return action_details


@dataclass
class BudgetDecreaseAction(BudgetAlterAction):
    APPLY_TOOLTIP = (
        f"Selecting apply will decrease the budget for this {{level}} by" f" {BUDGET_DECREASE_PERCENTAGE * 100}%"
    )

    SUCCESS_FEEDBACK: ClassVar[
        str
    ] = f"Success: Dexter successfully reduced the budget {BUDGET_DECREASE_PERCENTAGE * 100}% for this AdSet."
    FAILURE_FEEDBACK: ClassVar[str] = "Failure (due to error): Dexter was unsuccessful in reducing the budget"

    def get_action_parameters(self, apply_parameters: ApplyParameters, structure_details: Dict) -> Optional[Dict]:
        if not apply_parameters:
            return None

        if not _does_budget_exist(structure_details):
            return None

        budget, budget_type = _get_budget_value_and_type(structure_details)

        if not budget or not budget_type:
            return

        new_budget = budget - apply_parameters.budget_decrease * budget
        action_details = {"details": {budget_type: new_budget}}

        return action_details
