import logging
from dataclasses import dataclass
from typing import ClassVar, Dict, Optional

from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.adobjects.adset import AdSet
from facebook_business.adobjects.customaudience import CustomAudience

from Core.Dexter.Infrastructure.Domain.LevelEnums import LevelEnum
from Core.Dexter.Infrastructure.Domain.Recommendations.RecommendationFields import RecommendationField
from Core.Tools.QueryBuilder.QueryBuilderLogicalOperator import AgGridFacebookOperator
from Core.Web.FacebookGraphAPI.GraphAPI.SdkGetStructures import create_facebook_filter
from Core.Web.FacebookGraphAPI.GraphAPIDomain.GraphAPIInsightsFields import GraphAPIInsightsFields
from FacebookDexter.Api.Commands.RecommendationPageCommand import ApplyRecommendationCommand
from FacebookDexter.Infrastructure.DexterApplyActions.ApplyActionsUtils import duplicate_fb_adset, get_adset_id
from FacebookDexter.Infrastructure.DexterApplyActions.RecommendationApplyActions import (
    ApplyButtonType,
    ApplyParameters,
    RecommendationAction,
)

logger = logging.getLogger(__name__)


@dataclass
class CreateLookalike(RecommendationAction):
    APPLY_TOOLTIP: ClassVar[
        str
    ] = "Selecting apply with create a new adset with a new lookalike audience as custom audience"

    SUCCESS_FEEDBACK: str = (
        "Dexter successfully applied lookalike audience of customers who have purchased from you recently to Adset."
    )
    FAILURE_FEEDBACK: ClassVar[
        str
    ] = "Failure (due to error): Dexter was unsuccessful in creating the lookalike audience"

    def get_action_parameters(self, apply_parameters: ApplyParameters, structure_details: Dict) -> Optional[Dict]:
        """
        Save the db context needed to apply recommendation
        :param apply_parameters: The dataclass that encapsulates all the required things for the apply
        :param structure_details: The structure for which the recommendation is triggered
        :return: The dictionary with the parameters required to write in the DB
        """
        return {}

    def process_action(
        self,
        recommendation: Dict,
        headers: str,
        apply_button_type: ApplyButtonType,
        command: ApplyRecommendationCommand = None,
    ):
        """
        Applies the action for the recommendation based on the context saved into the DB

        :param recommendation: The database entry
        :param headers: Required for cross-service-called
        :apply_button_type: determine which type of action to apply: best performing adset, existing adset, new adset
        :return:
        """
        ad_account = AdAccount(recommendation[RecommendationField.ACCOUNT_ID.value])

        initial_adset_id = get_adset_id(recommendation, apply_button_type, command.adset_id)

        initial_adset = AdSet(initial_adset_id)
        initial_adset.api_get(fields=[GraphAPIInsightsFields.promoted_object, GraphAPIInsightsFields.targeting])

        pixel_id = recommendation[RecommendationField.APPLY_PARAMETERS.value][RecommendationField.PIXEL_ID.value]

        generic_pixel_audience = get_existing_generic_audience(ad_account, pixel_id)
        lookalike = get_lookalike(
            ad_account,
            initial_adset,
            generic_pixel_audience,
            pixel_id,
            recommendation[RecommendationField.STRUCTURE_NAME.value],
            recommendation[RecommendationField.APPLY_PARAMETERS.value][RecommendationField.MOST_FREQUENT_COUNTRY.value],
        )

        if not lookalike:
            logger.info(f"Lookalike audience creation failed.")

        suffix = f" Lookalike {pixel_id} - copy"
        prefix = "Dexter "
        new_adset_id, number_new_ad, number_ad = duplicate_fb_adset(
            recommendation, self.fixtures, LevelEnum.ADSET.value, initial_adset_id, suffix, prefix
        )
        if not new_adset_id:
            logger.info(f"Adset duplication failed.")

        lookalike.api_get(fields=[GraphAPIInsightsFields.name])

        new_adset = AdSet(new_adset_id)
        new_adset.api_get(fields=[GraphAPIInsightsFields.promoted_object, GraphAPIInsightsFields.targeting])

        targeting = new_adset.get(GraphAPIInsightsFields.targeting)
        targeting["custom_audiences"] = [{CustomAudience.Field.id: lookalike.get(CustomAudience.Field.id)}]
        new_adset.api_update(params={"targeting": targeting})

        logger.info(
            f"Creating lookalike audience {lookalike.get(CustomAudience.Field.id)} for new adset {new_adset_id} "
            f"was a success."
        )

        self._create_success_message(number_ad, number_new_ad, lookalike.get(CustomAudience.Field.name))
        return self.SUCCESS_FEEDBACK

    def _create_success_message(self, number_ad, number_new_ad, lookalike_name):

        if number_new_ad == number_ad:
            self.SUCCESS_FEEDBACK = (
                f"Success: Dexter successfully duplicated {number_new_ad} out of {number_ad} live ads in this AdSet, "
                f"using the lookalike audience - {lookalike_name} of customers who have purchased from you recently."
            )
        else:
            self.SUCCESS_FEEDBACK = (
                f"Failure of specific Ads (due to IOS 14 privacy restrictions): Dexter could only duplicate "
                f"{number_new_ad} out of {number_ad} live ads in this AdSet, "
                f"using the lookalike audience ({lookalike_name}) of customers who have purchased from you recently."
            )


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
                    "filter": {
                        "operator": "and",
                        "filters": [{"field": "event", "operator": "=", "value": "Purchase"}],
                    },
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
    ad_account: AdAccount,
    initial_adset: AdSet,
    existing_audience: CustomAudience,
    pixel_id: str,
    structure_name: str,
    most_frequent_country: str,
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
        lookalike_params = {
            CustomAudience.Field.name: f"Dexter Audience - {structure_name} - Lookalike {pixel_id}",
            CustomAudience.Field.subtype: CustomAudience.Subtype.lookalike,
            CustomAudience.Field.origin_audience_id: existing_audience.get_id(),
        }

        targeting = initial_adset.get(GraphAPIInsightsFields.targeting)
        if targeting:
            targeting = targeting.export_all_data()

            try:
                lookalike_params.update(
                    {
                        CustomAudience.Field.lookalike_spec: {
                            "starting_ratio": 0.01,
                            "ratio": 0.05,
                            "location_spec": {"geo_locations": targeting.get("geo_locations")},
                            "conversion_type": "purchases",
                        },
                    }
                )
                lookalike = ad_account.create_custom_audience(params=lookalike_params)

            except Exception as e:
                # if source audience of adset is small try again with most frequent country
                logger.exception("Failed to create lookalike audience, retrying with most frequent country", e)
                lookalike = create_lookalike_most_frequent_country(ad_account, lookalike_params, most_frequent_country)
        else:
            # if there is no retargeting geo location in adset then copy most frequent country
            logger.info("No targeting found in adset, trying with most frequent country")
            lookalike = create_lookalike_most_frequent_country(ad_account, lookalike_params, most_frequent_country)

    return lookalike


def create_lookalike_most_frequent_country(ad_account, lookalike_params, most_frequent_country):
    lookalike_params.update(
        {
            CustomAudience.Field.lookalike_spec: {
                "starting_ratio": 0.01,
                "ratio": 0.05,
                "country": most_frequent_country,
                "conversion_type": "purchases",
            },
        }
    )
    lookalike = ad_account.create_custom_audience(params=lookalike_params)
    return lookalike
