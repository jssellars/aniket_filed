from dataclasses import dataclass
from typing import ClassVar, Dict, Optional

from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.adobjects.adset import AdSet
from facebook_business.adobjects.customaudience import CustomAudience

from Core.Dexter.Infrastructure.Domain.Recommendations.RecommendationFields import RecommendationField
from Core.Tools.QueryBuilder.QueryBuilderLogicalOperator import AgGridFacebookOperator
from Core.Web.FacebookGraphAPI.GraphAPI.SdkGetStructures import create_facebook_filter
from Core.Web.FacebookGraphAPI.GraphAPIDomain.GraphAPIInsightsFields import GraphAPIInsightsFields
from FacebookDexter.Infrastructure.DexterApplyActions.ApplyActionsUtils import duplicate_fb_adset
from FacebookDexter.Infrastructure.DexterApplyActions.RecommendationApplyActions import (
    ApplyParameters,
    RecommendationAction,
)


@dataclass
class CreateLookalike(RecommendationAction):
    APPLY_TOOLTIP: ClassVar[
        str
    ] = "Selecting apply with create a new adset with a new lookalike audience as custom audience"

    def get_action_parameters(self, apply_parameters: ApplyParameters, structure_details: Dict) -> Optional[Dict]:
        """
        Save the db context needed to apply recommendation
        :param apply_parameters: The dataclass that encapsulates all the required things for the apply
        :param structure_details: The structure for which the recommendation is triggered
        :return: The dictionary with the parameters required to write in the DB
        """
        return {}

    def process_action(self, recommendation: Dict, headers: str):
        """
        Applies the action for the recommendation based on the context saved into the DB

        :param recommendation: The database entry
        :param headers: Required for cross-service-called
        :return:
        """
        ad_account = AdAccount(recommendation[RecommendationField.ACCOUNT_ID.value])

        initial_adset = AdSet(recommendation[RecommendationField.STRUCTURE_ID.value])
        initial_adset.api_get(fields=[GraphAPIInsightsFields.promoted_object, GraphAPIInsightsFields.targeting])

        promoted_object = initial_adset.get(GraphAPIInsightsFields.promoted_object)
        if not promoted_object:
            return

        pixel_id = promoted_object.get(GraphAPIInsightsFields.facebook_pixel_structure)

        generic_pixel_audience = get_existing_generic_audience(ad_account, pixel_id)
        lookalike = get_lookalike(ad_account, initial_adset, generic_pixel_audience, pixel_id)

        if not lookalike:
            return

        new_adset_id = duplicate_fb_adset(recommendation, self.fixtures)
        new_adset = AdSet(new_adset_id)
        new_adset.api_get(fields=[GraphAPIInsightsFields.promoted_object, GraphAPIInsightsFields.targeting])

        targeting = new_adset.get(GraphAPIInsightsFields.targeting)
        targeting["custom_audiences"] = [{CustomAudience.Field.id: lookalike.get(CustomAudience.Field.id)}]
        new_adset.api_update(params={"targeting": targeting})


def create_pixel_rule(pixel_id: str, no_of_days: int) -> Dict:
    """
    Returns a pixel rule for all events compatible with Facebook Graph API pixel rule creation

    :param pixel_id: The pixel id of the initial adset
    :param no_of_days: The number of days required for the lookalike
    :return: pixel_rule: The pixel rule in a JSON format as Facebook Graph API expects it
    """
    return {
        "inclusions": {
            "operator": "or",
            "rules": [
                {
                    "event_sources": [{"type": "pixel", "id": pixel_id}],
                    "retention_seconds": no_of_days * 24 * 3600,
                    "filter": {"operator": "and", "filters": [{"field": "url", "operator": "i_contains", "value": ""}]},
                    "template": "ALL_VISITORS",
                }
            ],
        }
    }


def get_existing_generic_audience(ad_account: AdAccount, pixel_id: str) -> CustomAudience:
    """
    Returns the generic pixel audience if exists, else create it and return it

    :param ad_account: The AdAccount object
    :param pixel_id: The pixel id of the initial AdSet
    :return: The new generic custom audience based on the pixel
    """
    params = {
        CustomAudience.Field.name: f"Filed Pixel {pixel_id} Custom Audience",
        CustomAudience.Field.rule: create_pixel_rule(pixel_id, 180),
    }

    existing_audience = ad_account.get_custom_audiences(
        fields=[CustomAudience.Field.name, CustomAudience.Field.rule, CustomAudience.Field.id],
        params={
            "filtering": [
                create_facebook_filter(
                    CustomAudience.Field.name, AgGridFacebookOperator.CONTAIN, params[CustomAudience.Field.name]
                )
            ]
        },
    )

    if not existing_audience:
        # If there is no generic lookalike audience, create one
        existing_audience = ad_account.create_custom_audience(params=params)
    else:
        existing_audience = existing_audience[0]

    return existing_audience


def get_lookalike(
    ad_account: AdAccount, initial_adset: AdSet, existing_audience: CustomAudience, pixel_id: str
) -> CustomAudience:
    """
    Return the lookalike audience if it exists, else create it and return it

    :param ad_account: The AdAccount object instance
    :param existing_audience: The generic pixel audience
    :param pixel_id: The pixel_id used for naming the lookalike if needed
    :return:
    """
    existing_lookalikes = ad_account.get_custom_audiences(
        fields=[CustomAudience.Field.name, CustomAudience.Field.id, CustomAudience.Field.lookalike_spec],
        params={
            "filtering": [
                create_facebook_filter(
                    CustomAudience.Field.subtype, AgGridFacebookOperator.EQUAL, CustomAudience.Subtype.lookalike
                )
            ]
        },
    )

    lookalike = None
    for existing_lookalike in existing_lookalikes:
        existing_lookalike_spec = existing_lookalike.get(CustomAudience.Field.lookalike_spec)
        if not existing_lookalike_spec:
            continue

        lookalike_spec_origin = existing_lookalike_spec.get("origin")
        if not lookalike_spec_origin:
            continue

        if lookalike_spec_origin[0].get(CustomAudience.Field.id) == existing_audience.get_id():
            lookalike = existing_lookalike
            break

    if not lookalike:

        targeting = initial_adset.get(GraphAPIInsightsFields.targeting)
        if targeting:
            targeting = targeting.export_all_data()

        lookalike_params = {
            CustomAudience.Field.name: f"Filed Pixel {pixel_id} Lookalike",
            CustomAudience.Field.subtype: CustomAudience.Subtype.lookalike,
            CustomAudience.Field.origin_audience_id: existing_audience.get_id(),
            CustomAudience.Field.lookalike_spec: {
                "starting_ratio": 0.01,
                "ratio": 0.02,
                "location_spec": targeting.get("geo_locations"),
                "conversion_type": "purchases",
            },
        }
        lookalike = ad_account.create_custom_audience(params=lookalike_params)

    return lookalike
