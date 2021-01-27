from dataclasses import dataclass
from enum import Enum
from typing import Dict, Optional, Tuple

import requests

from Core.Dexter.Infrastructure.Domain.Recommendations.RecommendationFields import RecommendationField
from Core.settings_models import ExternalServices
from FacebookDexter.Infrastructure.Domain.Actions.ActionEnums import FacebookBudgetTypeEnum

BUDGET_INCREASE_PARAM = "budget_increase"
BUDGET_DECREASE_PARAM = "budget_increase"


@dataclass
class ApplyParameters:
    budget_increase: Optional[float] = None
    budget_decrease: Optional[float] = None


@dataclass
class RecommendationAction:

    def process_action(self, external_services: ExternalServices, recommendation: Dict, headers: str):
        raise NotImplementedError

    def get_action_parameters(self, apply_parameters: ApplyParameters, structure_details: Dict) -> Optional[Dict]:
        raise NotImplementedError


@dataclass
class BudgetAlterAction(RecommendationAction):

    def process_action(self, external_services: ExternalServices, recommendation: Dict, headers: str):
        url = external_services.facebook_auto_apply.format(
            level=recommendation.get(RecommendationField.LEVEL.value),
            structureId=recommendation.get(RecommendationField.STRUCTURE_ID.value),
        )
        apply_request = requests.put(
            url, json=recommendation.get(RecommendationField.APPLY_PARAMETERS.value), headers=headers
        )

        if apply_request.status_code != 200:
            raise Exception(f"Could not update structure {recommendation.get(RecommendationField.STRUCTURE_ID.value)}")

        return None

    @staticmethod
    def get_budget_value_and_type(apply_parameters: ApplyParameters, structure_details: Dict) -> Tuple[Optional[int], Optional[str]]:
        if not apply_parameters:
            return None, None

        if not does_budget_exist(structure_details):
            return None, None

        lifetime_budget = structure_details.get(FacebookBudgetTypeEnum.LIFETIME.value)
        daily_budget = structure_details.get(FacebookBudgetTypeEnum.DAILY.value)

        if daily_budget:
            budget = int(daily_budget)
            budget_type = FacebookBudgetTypeEnum.DAILY.value
        elif lifetime_budget:
            budget = int(lifetime_budget)
            budget_type = FacebookBudgetTypeEnum.LIFETIME.value
        else:
            return None, None

        return budget, budget_type

    def get_action_parameters(self, apply_parameters: ApplyParameters, structure_details: Dict) -> Optional[Dict]:
        raise NotImplementedError


@dataclass
class BudgetIncreaseAction(BudgetAlterAction):

    def get_action_parameters(self, apply_parameters: ApplyParameters, structure_details: Dict) -> Optional[Dict]:
        if not apply_parameters:
            return None

        if not does_budget_exist(structure_details):
            return None

        budget, budget_type = BudgetAlterAction.get_budget_value_and_type(apply_parameters, structure_details)

        if not budget or not budget_type:
            return

        new_budget = budget + apply_parameters.budget_increase * budget
        action_details = {
            "details": {
                budget_type: new_budget
            }
        }

        return action_details


@dataclass
class BudgetDecreaseAction(BudgetAlterAction):

    def get_action_parameters(self, apply_parameters: ApplyParameters, structure_details: Dict) -> Optional[Dict]:
        if not apply_parameters:
            return None

        if not does_budget_exist(structure_details):
            return None

        budget, budget_type = BudgetAlterAction.get_budget_value_and_type(apply_parameters, structure_details)

        if not budget or not budget_type:
            return

        new_budget = budget + apply_parameters.budget_increase * budget
        action_details = {
            "details": {
                budget_type: new_budget
            }
        }

        return action_details


class ApplyActionType(Enum):
    BUDGET_INCREASE = BudgetIncreaseAction
    BUDGET_DECREASE = BudgetDecreaseAction


def does_budget_exist(structure_details: Dict) -> bool:
    lifetime_budget = structure_details.get(FacebookBudgetTypeEnum.LIFETIME.value)
    daily_budget = structure_details.get(FacebookBudgetTypeEnum.DAILY.value)

    if lifetime_budget or daily_budget:
        return True

    return False


def get_apply_action(action_type: ApplyActionType):
    if not action_type:
        return None

    return ApplyActionType(action_type).value()
