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
from FacebookDexter.Infrastructure.DexterApplyActions.ApplyActionsUtils import duplicate_fb_adset
from FacebookDexter.Infrastructure.DexterApplyActions.RecommendationApplyActions import (
    ApplyButtonType,
    ApplyParameters,
    RecommendationAction,
)

logger = logging.getLogger(__name__)


@dataclass
class CreateRetargeting(RecommendationAction):
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

    def process_action(
        self, recommendation: Dict, headers: str, apply_button_type: ApplyButtonType, command: Dict = None
    ):
        """
        Applies the action for the recommendation based on the context saved into the DB

        :param recommendation: The database entry
        :param headers: Required for cross-service-called
        :return:
        """
        ad_account = AdAccount(recommendation[RecommendationField.ACCOUNT_ID.value])
        best_adset_id = recommendation[RecommendationField.APPLY_PARAMETERS.value][
            RecommendationField.BEST_ADSET_ID_LOOKALIKE.value
        ]
        best_adset_name = recommendation[RecommendationField.APPLY_PARAMETERS.value][
            RecommendationField.BEST_ADSET_NAME_LOOKALIKE.value
        ]
        strategy = recommendation[RecommendationField.APPLY_PARAMETERS.value][RecommendationField.STRATEGY.value]
        pixel_id = recommendation[RecommendationField.APPLY_PARAMETERS.value][RecommendationField.PIXEL_ID.value]

        retargeting = create_retargeting_audience(ad_account, strategy, pixel_id)

        if not retargeting:
            return

        suffix = f" Retargeting {pixel_id} {strategy} - copy"
        prefix = "Dexter "
        new_adset_name = f"Dexter  {best_adset_name} Retargeting {pixel_id} {strategy} copy "
        new_adset_id = duplicate_fb_adset(
            recommendation, self.fixtures, LevelEnum.ADSET.value, best_adset_id, suffix, prefix
        )
        new_adset = AdSet(new_adset_id)
        new_adset.api_get(fields=[GraphAPIInsightsFields.promoted_object, GraphAPIInsightsFields.targeting])

        targeting = new_adset.get(GraphAPIInsightsFields.targeting)
        targeting["custom_audiences"] = [{CustomAudience.Field.id: retargeting.get(CustomAudience.Field.id)}]
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
                    "filter": {
                        "operator": "and",
                        "filters": [{"field": "event", "operator": "=", "value": "Initiate checkout"}],
                    },
                    "template": "ALL_VISITORS",
                }
            ],
        },
        "exclusions": {
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
        },
    }


def create_retargeting_audience(ad_account: AdAccount, strategy: str, pixel_id: str) -> CustomAudience:
    """
    Returns the generic pixel audience if exists, else create it and return it

    :param ad_account: The AdAccount object
    :param strategy: The strategy for targeting audience
    :return: The new generic custom audience based on the pixel
    """
    params = {
        CustomAudience.Field.name: f"Filed Pixel {pixel_id} Strategy  {strategy} Custom Audience",
        CustomAudience.Field.rule: create_pixel_rule(pixel_id, 30),
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
        try:
            existing_audience = ad_account.create_custom_audience(params=params)
        except Exception as e:
            logger.info("Failed to create custom audience")
    else:
        existing_audience = existing_audience[0]

    return existing_audience
