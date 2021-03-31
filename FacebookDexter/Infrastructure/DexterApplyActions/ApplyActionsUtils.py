from dataclasses import asdict
from typing import Any, Dict, Optional, Tuple

import requests
from facebook_business.adobjects.adset import AdSet

from Core.Dexter.Infrastructure.Domain.Recommendations.RecommendationFields import RecommendationField
from Core.settings_models import Model
from Core.Web.FacebookGraphAPI.GraphAPIDomain.FacebookMiscFields import FacebookMiscFields
from Core.Web.FacebookGraphAPI.GraphAPIMappings.LevelMapping import LevelToGraphAPIStructure
from FacebookDexter.Infrastructure.DexterApplyActions.RecommendationApplyActions import RecommendationAction
from FacebookDexter.Infrastructure.Domain.Actions.ActionEnums import FacebookBudgetTypeEnum
from FacebookDexter.Infrastructure.IntegrationEvents.DexterNewCreatedStructuresHandler import (
    DexterCreatedEventMapping,
    DexterNewCreatedStructureEvent,
    NewCreatedStructureKeys,
)

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


def update_turing_structure(config: Model, recommendation: Dict, headers: str):
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


def duplicate_fb_adset(recommendation: Dict, fixtures: Any) -> str:
    structure = LevelToGraphAPIStructure.get(
        recommendation[RecommendationField.LEVEL.value], recommendation[RecommendationField.STRUCTURE_ID.value]
    )

    new_structure = structure.create_copy(
        params={
            "campaign_id": recommendation.get(RecommendationField.CAMPAIGN_ID.value),
            "deep_copy": True,
            "status_option": AdSet.StatusOption.inherited_from_source,
            "rename_options": {"rename_suffix": " - Duplicate"},
        }
    )
    new_created_structures_event = DexterNewCreatedStructureEvent(
        recommendation.get(RecommendationField.BUSINESS_OWNER_ID.value),
        [
            NewCreatedStructureKeys(
                recommendation.get(RecommendationField.LEVEL.value),
                recommendation.get(RecommendationField.ACCOUNT_ID.value),
                new_structure[FacebookMiscFields.copied_adset_id],
            )
        ],
    )
    mapper = DexterCreatedEventMapping(target=DexterNewCreatedStructureEvent)
    response = mapper.load(asdict(new_created_structures_event))
    RecommendationAction.publish_response(response, fixtures)

    return new_structure[FacebookMiscFields.copied_adset_id]
