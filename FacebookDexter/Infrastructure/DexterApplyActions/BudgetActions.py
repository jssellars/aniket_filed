from dataclasses import dataclass
from typing import Dict, Optional

from FacebookDexter.Infrastructure.DexterApplyActions.ApplyActionsUtils import (
    _does_budget_exist,
    _get_budget_value_and_type,
    _update_turing_structure,
)
from FacebookDexter.Infrastructure.DexterApplyActions.RecommendationApplyActions import (
    ApplyParameters,
    RecommendationAction,
)


@dataclass
class BudgetAlterAction(RecommendationAction):
    def process_action(self, recommendation: Dict, headers: str):
        _update_turing_structure(self.config, recommendation, headers)
        return

    def get_action_parameters(self, apply_parameters: ApplyParameters, structure_details: Dict) -> Optional[Dict]:
        raise NotImplementedError


@dataclass
class BudgetIncreaseAction(BudgetAlterAction):
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
