"""
Duplicate Adset using Hidden Interests.

"""
import logging

# Standard Imports.
from dataclasses import dataclass
from typing import ClassVar, Dict, Optional

from facebook_business.adobjects.adset import AdSet

# Core Imports.
from Core.Dexter.Infrastructure.Domain.LevelEnums import LevelEnum
from Core.Dexter.Infrastructure.Domain.Recommendations.RecommendationFields import RecommendationField
from Core.Web.FacebookGraphAPI.GraphAPIDomain.GraphAPIInsightsFields import GraphAPIInsightsFields
from FacebookDexter.Infrastructure.DexterApplyActions.ApplyActionsUtils import duplicate_fb_adset_for_hidden_interests

# Local Imports.
from FacebookDexter.Infrastructure.DexterApplyActions.RecommendationApplyActions import (
    ApplyButtonType,
    ApplyParameters,
    RecommendationAction,
)

# init Logger.
logger = logging.getLogger(__name__)


@dataclass
class HiddenInterestsDuplicateAdset(RecommendationAction):
    APPLY_TOOLTIP: ClassVar[str] = (
        "Selecting ‘Choose Interests’ will allow you to select your new interests to target, "
        "using our hidden interests technology. Dexter will duplicate your AdSet with these new interests or "
        "you can choose to Create a new AdSet to target them"
    )

    SUCCESS_FEEDBACK: ClassVar[
        str
    ] = "Dexter successfully applied hiddden interests that may result in cheaper conversions."
    FAILURE_FEEDBACK: ClassVar[str] = "Failure (due to error): Dexter was unsuccessful in applying hidden interests."

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

    def process_action(
        self,
        recommendation: Dict,
        headers: str,
        apply_button_type: ApplyButtonType,
        command: dict = None,
    ):
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
           Contains Hidden Interests Data from the Payload.
        """
        # Grab Adset ID & Name based on apply button type
        adset_id = self.get_adset_id(recommendation, apply_button_type, command["adset_id"])

        # Generate Duplicates.
        new_adset_id, number_new_ad, number_ad = duplicate_fb_adset_for_hidden_interests(
            recommendation=recommendation,
            fixtures=self.fixtures,
            level=LevelEnum.ADSET.value,
            adset_id=adset_id,
        )

        # Grab Targeting related fields.
        new_adset = AdSet(fbid=new_adset_id)
        new_adset.api_get(fields=[GraphAPIInsightsFields.promoted_object, GraphAPIInsightsFields.targeting])
        targeting = new_adset.get(GraphAPIInsightsFields.targeting)

        # Update Flexible Spec to the Interests selected by the user.
        targeting["flexible_spec"] = {"interests": command["hidden_interests_data"]["interests"]}
        new_adset.api_update(params={"targeting": targeting})

        logger.info(f"Creating Adset with Hidden Interests for New adset {adset_id}: {new_adset_id} was a success.")
        self._create_success_message(number_ad, number_new_ad)
        return self.SUCCESS_FEEDBACK

    def _create_success_message(self, number_ad, number_new_ad):

        if number_new_ad == number_ad:
            self.SUCCESS_FEEDBACK = (
                f"Success: Dexter successfully duplicated {number_new_ad} out of {number_ad} live ads in this AdSet, "
                f"using the hidden interest targeting that may result in cheaper conversions."
            )
        else:
            self.SUCCESS_FEEDBACK = (
                f"Failure of specific Ads (due to IOS 14 privacy restrictions): Dexter could only duplicate "
                f"{number_new_ad} out of {number_ad} live ads in this AdSet, "
                f"using the hidden interest targeting that may result in cheaper conversions."
            )

    def get_adset_id(self, recommendation, apply_button_type, adset_id):
        if apply_button_type in [ApplyButtonType.BEST_PERFORMING, ApplyButtonType.DEFAULT]:
            return recommendation[RecommendationField.APPLY_PARAMETERS.value][RecommendationField.ADSET_ID.value]
        elif apply_button_type in [ApplyButtonType.NEW] and adset_id:
            return adset_id
        else:
            raise ValueError("invalid apply button or adset id")
