"""
Duplicate Adset using Hidden Interests.

"""
# Standard Imports.
from dataclasses import dataclass
from typing import ClassVar, Dict, Optional
import logging

from facebook_business.adobjects.adset import AdSet

# Core Imports.
from Core.Dexter.Infrastructure.Domain.LevelEnums import LevelEnum
from Core.Dexter.Infrastructure.Domain.Recommendations.RecommendationFields import RecommendationField
from Core.Web.FacebookGraphAPI.GraphAPIDomain.GraphAPIInsightsFields import GraphAPIInsightsFields

# Local Imports.
from FacebookDexter.Infrastructure.DexterApplyActions.RecommendationApplyActions import (
    RecommendationAction,
    ApplyParameters,
    ApplyButtonType
)
from FacebookDexter.Infrastructure.DexterApplyActions.ApplyActionsUtils import duplicate_fb_adset_for_hidden_interests

# init Logger.
logger = logging.getLogger(__name__)


@dataclass
class HiddenInterestsDuplicateAdset(RecommendationAction):
    APPLY_TOOLTIP: ClassVar[
        str] = "Selecting ‘Choose Interests’ will allow you to select your new interests to target, using our hidden interests technology. Dexter will duplicate your AdSet with these new interests or you can choose to Create a new AdSet to target them"

    def get_action_parameters(self, apply_parameters: ApplyParameters, structure_details: Dict) -> Optional[Dict]:
        """
        Save the DB Context needed to apply recommedations.

        Parameters
        ----------
        apply_parameters: ApplyParameters
            Dataclass that encapsulates all the required things to apply
        structure_details: Dict
            Structure for which recommendation is triggered

        Returns
        -------
        The dictionary with the parameters required to write in the DB

        """
        return {}

    def process_action(self, recommendation: Dict, headers: str, apply_button_type: ApplyButtonType,
                       command: Dict = None):
        """
        Applies the action for the Recommendation.

        Parameters
        ----------
        recommendation: Dict
            The Database Entry

        headers: str
            Required for cross-service-called

        apply_button_type: ApplyButtonType
            Default Apply Button

        command: Dict
            Hidden Interests Data from the Payload.
        """
        # Grab Adset ID & Name from Apply Parameters.
        adset_id = recommendation[RecommendationField.APPLY_PARAMETERS.value]["adset_id"]
        adset_name = recommendation[RecommendationField.APPLY_PARAMETERS.value]["adset_name"]

        # Generate Duplicates.
        new_adset_id = duplicate_fb_adset_for_hidden_interests(
            recommendation=recommendation,
            fixtures=self.fixtures,
            adset_name=adset_name,
            level=LevelEnum.ADSET.value,
            adset_id=adset_id
        )

        # Grab Targeting related fields.
        new_adset = AdSet(fbid=new_adset_id)
        new_adset.api_get(fields=[GraphAPIInsightsFields.promoted_object, GraphAPIInsightsFields.targeting])
        targeting = new_adset.get(GraphAPIInsightsFields.targeting)

        # Update Flexible Spec to the Interests selected by the user.
        targeting["flexible_spec"] = {"interests": command["interests"]}
        new_adset.api_update(params={"targeting": targeting})

        logger.info(
            f"Creating Adset with Hidden Interests for New adset {adset_name}: {new_adset_id} was a success."
        )
