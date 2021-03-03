from typing import Dict, Optional, Tuple

import requests

from Core.Dexter.Infrastructure.Domain.Recommendations.RecommendationFields import RecommendationField
from Core.settings_models import Model
from FacebookDexter.Infrastructure.Domain.Actions.ActionEnums import FacebookBudgetTypeEnum

INVALID_METRIC_VALUE = -1
TOTAL_KEY = "total"
UNKNOWN_KEY = "unknown"


def _does_budget_exist(structure_details: Dict) -> bool:
    lifetime_budget = structure_details.get(FacebookBudgetTypeEnum.LIFETIME.value)
    daily_budget = structure_details.get(FacebookBudgetTypeEnum.DAILY.value)

    if lifetime_budget or daily_budget:
        return True

    return False


def _get_budget_value_and_type(
    structure_details: Dict,
) -> Tuple[Optional[int], Optional[str]]:
    if not _does_budget_exist(structure_details):
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


def _update_turing_structure(config: Model, recommendation: Dict, headers: str):
    url = config.external_services.facebook_auto_apply.format(
        level=recommendation.get(RecommendationField.LEVEL.value),
        structureId=recommendation.get(RecommendationField.STRUCTURE_ID.value),
    )
    apply_request = requests.put(
        url,
        json=recommendation.get(RecommendationField.APPLY_PARAMETERS.value),
        headers=headers,
    )

    if apply_request.status_code != 200:
        raise Exception(f"Could not update structure {recommendation.get(RecommendationField.STRUCTURE_ID.value)}")
