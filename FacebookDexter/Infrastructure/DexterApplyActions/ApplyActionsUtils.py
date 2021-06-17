import concurrent.futures
import logging
from dataclasses import asdict
from typing import Any, Dict, List, Optional, Tuple

import requests
from facebook_business.adobjects.ad import Ad
from facebook_business.adobjects.adset import AdSet

from Core.Dexter.Infrastructure.Domain.Recommendations.RecommendationFields import RecommendationField
from Core.settings_models import Model
from Core.Web.FacebookGraphAPI.GraphAPIDomain.FacebookMiscFields import FacebookMiscFields
from Core.Web.FacebookGraphAPI.GraphAPIMappings.LevelMapping import LevelToGraphAPIStructure
from Core.Web.FacebookGraphAPI.Tools import Tools
from FacebookDexter.Infrastructure.DexterApplyActions.RecommendationApplyActions import (
    ApplyButtonType,
    RecommendationAction,
)
from FacebookDexter.Infrastructure.Domain.Actions.ActionEnums import FacebookBudgetTypeEnum
from FacebookDexter.Infrastructure.IntegrationEvents.DexterNewCreatedStructuresHandler import (
    DexterCreatedEventMapping,
    DexterNewCreatedStructureEvent,
    NewCreatedStructureKeys,
)

logger = logging.getLogger(__name__)

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


def make_ad_copies(ad_ids: List, adset_ids: List):
    new_copies = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []
        for adset_id in adset_ids:
            for ad_id in ad_ids:
                futures.append(
                    executor.submit(
                        _duplicate_ads_on_adset,
                        ad_id,
                        adset_id,
                    )
                )

        for future in concurrent.futures.as_completed(futures):
            new_copies.append(future.result())

        return new_copies


def _duplicate_ads_on_adset(ad_id, adset_id, retry=0):
    ad = Ad(fbid=ad_id)
    parameters = {"adset_id": adset_id, "status_option": Ad.StatusOption.inherited_from_source}
    try:
        new_ad_id = ad.create_copy(params=parameters)
        new_ad_id = Tools.convert_to_json(new_ad_id)

        if "copied_ad_id" in new_ad_id:
            return new_ad_id["copied_ad_id"]
        else:
            raise ValueError("Invalid duplicated Ad id.")

    except Exception as e:
        # retrying ad copy request if there is "unexpected error" from FB
        if e.api_error_code() == 2 and retry < 3:
            logger.exception(
                f"Unable to copy and publish ad {ad_id} to adset {adset_id} || {repr(e)} || retry count: {retry}"
            )
            return _duplicate_ads_on_adset(ad_id, adset_id, retry + 1)

        logger.exception(f"Unable to copy and publish ad {ad_id} to adset {adset_id} || {repr(e)}")
        return None


def duplicate_fb_adset(
    recommendation: Dict,
    fixtures: Any,
    level: str = None,
    best_adset_id: str = None,
    name_suffix: str = None,
    name_prefix: str = None,
) -> Tuple[str, int, int]:
    if not best_adset_id:
        facebook_id = recommendation.get(RecommendationField.STRUCTURE_ID.value)
    else:
        facebook_id = best_adset_id

    if not level:
        level = recommendation.get(RecommendationField.LEVEL.value)

    structure = LevelToGraphAPIStructure.get(level, facebook_id)

    params = {
        "campaign_id": recommendation.get(RecommendationField.STRUCTURE_ID.value),
        "deep_copy": False,
        "status_option": AdSet.StatusOption.inherited_from_source,
    }

    if name_suffix and name_prefix:
        params.update({"rename_options": {"rename_suffix": name_suffix, "rename_prefix": name_prefix}})
    else:
        params.update({"rename_options": {"rename_suffix": " - Duplicate"}})

    new_structure = structure.create_copy(params=params)
    new_adset_id = new_structure[FacebookMiscFields.copied_adset_id]

    # get all the ads from the original adset
    orig_fb_adset = AdSet(fbid=facebook_id)
    ad_ids = [ad.get_id() for ad in (orig_fb_adset.get_ads(fields=["id"]))]

    # publish copies of ads to all new adsets
    new_ad_ids = make_ad_copies(ad_ids, [new_adset_id])

    new_created_structures_event = DexterNewCreatedStructureEvent(
        recommendation.get(RecommendationField.BUSINESS_OWNER_ID.value),
        [
            NewCreatedStructureKeys(
                level,
                recommendation.get(RecommendationField.ACCOUNT_ID.value),
                new_adset_id,
            )
        ],
    )
    mapper = DexterCreatedEventMapping(target=DexterNewCreatedStructureEvent)
    response = mapper.load(asdict(new_created_structures_event))
    RecommendationAction.publish_response(response, fixtures)

    return new_adset_id, len(new_ad_ids), len(ad_ids)


def duplicate_fb_adset_for_hidden_interests(
    recommendation: Dict, fixtures: Any, level: str = None, adset_id: str = None
) -> Tuple[str, int, int]:
    """
    Duplicate Facebook Adset For Hidden Interests.

    Parameters
    ----------
    recommendation: Dict
        Db Entry Recommendations
    fixtures: object
        Fixtures for Rabbit MQ
    adset_name: str, default = None
        Adset Name for Duplicated Adset with Hidden Interests
    level: str, default = None
        Level for Graph API Params
    adset_id: str, default = None
        Adset ID for Duplicated Adset with Hidden Interests

    Returns
    -------
    new_adset_id: str
        Adset ID of the Duplicated Adset with Hidden Interests
    """
    # Check if adset if provided.
    if not adset_id:
        facebook_id = recommendation.get(RecommendationField.STRUCTURE_ID.value)
    else:
        facebook_id = adset_id

    # Check if level is provided.
    if not level:
        level = recommendation.get(RecommendationField.LEVEL.value)

    # Grab Structure.
    structure = LevelToGraphAPIStructure.get(level, facebook_id)
    params = {
        "campaign_id": recommendation.get(RecommendationField.CAMPAIGN_ID.value),
        "deep_copy": False,
        "status_option": AdSet.StatusOption.inherited_from_source,
    }

    # Update Adset Name to the New name: {adset_name}: Dexter - {adset_name} Hidden Interests - copy"
    params.update({"rename_options": {"rename_prefix": "Dexter - ", "rename_suffix": f" - Hidden Interests"}})

    new_structure = structure.create_copy(params=params)
    new_adset_id = new_structure[FacebookMiscFields.copied_adset_id]

    # Get all the ads from the original adset
    orig_fb_adset = AdSet(fbid=facebook_id)
    ad_ids = [ad.get_id() for ad in (orig_fb_adset.get_ads(fields=["id"]))]

    # Publish copies of ads to all new adsets
    new_ad_ids = make_ad_copies(ad_ids, [new_adset_id])

    new_created_structures_event = DexterNewCreatedStructureEvent(
        recommendation.get(RecommendationField.BUSINESS_OWNER_ID.value),
        [
            NewCreatedStructureKeys(
                level,
                recommendation.get(RecommendationField.ACCOUNT_ID.value),
                new_adset_id,
            )
        ],
    )
    # Publish Response to Rabbit MQ.
    mapper = DexterCreatedEventMapping(target=DexterNewCreatedStructureEvent)
    response = mapper.load(asdict(new_created_structures_event))
    RecommendationAction.publish_response(response, fixtures)

    return new_adset_id, len(new_ad_ids), len(ad_ids)


def get_adset_id(recommendation: Dict, apply_button_type: ApplyButtonType, adset_id: str = None):
    if apply_button_type in [ApplyButtonType.BEST_PERFORMING, ApplyButtonType.DEFAULT]:
        return recommendation[RecommendationField.APPLY_PARAMETERS.value][
            RecommendationField.BEST_ADSET_ID_LOOKALIKE.value
        ]
    elif apply_button_type in [ApplyButtonType.NEW, ApplyButtonType.CHOOSE_OTHER] and adset_id:
        return adset_id
    else:
        raise ValueError("invalid apply button or adset id")
