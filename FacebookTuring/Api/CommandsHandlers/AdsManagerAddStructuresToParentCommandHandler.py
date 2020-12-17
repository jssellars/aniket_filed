from typing import Any, Dict

from Core.Web.FacebookGraphAPI.GraphAPI.GraphAPISdkBase import GraphAPISdkBase
from Core.Web.FacebookGraphAPI.Tools import Tools
from facebook_business.adobjects.ad import Ad
from facebook_business.adobjects.adset import AdSet
from FacebookTuring.Infrastructure.Mappings.LevelMapping import Level, LevelToGraphAPIStructure


def publish_structures_to_parent(
    level: str,
    request: Dict = None,
    permanent_token: str = None,
    facebook_config: Any = None,
):
    GraphAPISdkBase(business_owner_permanent_token=permanent_token, facebook_config=facebook_config)

    parent_ids = request.get("parent_ids", None)
    child_ids = request.get("child_ids", None)

    if child_ids and parent_ids:
        new_structures = _publish_structures_from_ids(level, child_ids, parent_ids)
    else:
        # TODO Add another check for publishing structures without using Id
        raise ValueError("No valid existing keys found in request. Or list of Ids is empty.")

    return {level: new_structures}


def _publish_structures_from_ids(level, child_ids, parent_ids):
    results = []
    for parent_id in parent_ids:
        for child_id in child_ids:
            results.append(_duplicate_structure_on_facebook(level, child_id, parent_id))

    return results


def _duplicate_structure_on_facebook(level, facebook_id, parent_id=None):
    structure = LevelToGraphAPIStructure.get(level, facebook_id)
    params = _create_duplicate_parameters(level, parent_id)
    new_structure_id = structure.create_copy(params=params)
    new_structure_id = Tools.convert_to_json(new_structure_id)
    if "ad_object_ids" in new_structure_id:
        return new_structure_id["ad_object_ids"][0]["copied_id"]
    elif "copied_ad_id" in new_structure_id:
        return new_structure_id["copied_ad_id"]
    else:
        raise ValueError("Invalid duplicated structure id.")


def _create_duplicate_parameters(level, parent_id=None):
    if level == Level.ADSET.value:
        return _duplicate_adset_parameters(parent_id)
    elif level == Level.AD.value:
        return _duplicate_ad_parameters(parent_id)
    else:
        raise ValueError(f"Unknown level supplied: {level}. Please try again using adset or ad")


def _duplicate_adset_parameters(parent_id):
    parameters = {
        "campaign_id": parent_id,
        "deep_copy": False,
        "status_option": AdSet.StatusOption.paused,
    }
    return parameters


def _duplicate_ad_parameters(parent_id):
    parameters = {"adset_id": parent_id, "status_option": Ad.StatusOption.paused}
    return parameters
