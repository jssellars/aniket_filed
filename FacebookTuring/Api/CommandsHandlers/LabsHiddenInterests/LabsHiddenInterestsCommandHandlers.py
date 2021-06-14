"""
Labs Hidden Interests Command Handlers

"""
import logging

# Standard Imports.
from typing import AnyStr, Dict, List

from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.adobjects.targetingsearch import TargetingSearch
from facebook_business.exceptions import FacebookRequestError

from Core.Dexter.Infrastructure.Domain.LevelEnums import LevelEnum
from Core.Tools.QueryBuilder.QueryBuilderLogicalOperator import AgGridFacebookOperator

# Core Imports.
from Core.Web.FacebookGraphAPI.GraphAPI.SdkGetStructures import (  # for structures
    create_facebook_filter,
    get_and_map_structures,
)

# for filtering.
from Core.Web.FacebookGraphAPI.Models.FieldsMetadata import FieldsMetadata
from Core.Web.FacebookGraphAPI.Tools import Tools  # for utility.

# Local Imports.
from FacebookTuring.Api.CommandsHandlers.LabsHiddenInterests.LabsHiddenInterestsCommandHandlersBase import (
    LabsHiddenInterestsCommandHandlersBase,
)

# Logger Init.
logger = logging.getLogger(__name__)


class GetInterestsHandler(LabsHiddenInterestsCommandHandlersBase):
    def __init__(self):
        self.ad_account = None
        self.adset_structure_details = None

    def handle(self, query_json: Dict, business_owner_id: AnyStr):
        """
        Parses & Returns Source, Suggested, & Hidden Interests for the Adset.

        Parameters
        ----------
        query_json: Dict
            Query Json

        business_owner_id: str, default = None
            Facebook Business Owner ID

        Returns
        -------
        interests: list[dict]
            Returns Source, Suggested, & Hidden Interests for specified Adset

        """
        # Grab fields from Payload.
        adset_id = query_json["adset_id"]
        account_id = query_json["account_id"]
        interests_type = query_json["interests_type"]
        limit = query_json["limit"]
        interests_list = query_json["interests_list"]

        # Grab Structure for the specified Adset.
        filtering = create_facebook_filter(
            field=FieldsMetadata.adset_id.name.replace("_", "."), operator=AgGridFacebookOperator.EQUAL, value=adset_id
        )

        adset_structure = get_and_map_structures(ad_account_id=account_id, level=LevelEnum.ADSET, filtering=filtering)
        adset_structure = adset_structure[0]
        adset_structure_details = adset_structure.get("details")
        self.adset_structure_details = adset_structure_details

        targeting_spec = adset_structure_details["targeting"]
        flexible_spec = targeting_spec["flexible_spec"][0]["interests"]

        # init AdAccount.
        ad_account = AdAccount(fbid=account_id)
        self.ad_account = ad_account

        # Find Source Interests.
        if interests_type == "source":
            source_interests = self.get_source_interests(flexible_spec=flexible_spec)

            return source_interests

        # Find Suggested Interests.
        elif interests_type == "suggested":
            suggested_interests = self.get_suggested_interests(interests_list=interests_list, limit=limit)
            return suggested_interests

        # Find Hidden Interests.
        elif interests_type == "hidden":
            hidden_interests = self.get_hidden_interests(interests_list=interests_list, limit=limit)
            return hidden_interests

        # Find Overlap.
        elif interests_type == "overlap":
            audience_overlap_percent = self.get_audience_overlap_percent(interests_list=interests_list)

            return audience_overlap_percent

    def get_source_interests(self, flexible_spec: list):
        """
        Returns Source Interests for a Specified Adset.

        Parameters
        ----------
        flexible_spec: list[dict]
            Flexible Spec with Interests Filtered defined for the Adset

        Returns
        -------
        source_interests: list[dict]
            Source Interests for the Specified Adset

        """
        source_interests_list = []
        targeting_search_response = None

        for interest in flexible_spec:
            params = {"q": interest.get("name"), "type": TargetingSearch.TargetingSearchTypes.interest}
            try:
                targeting_search_response = self.ad_account.get_targeting_search(params=params)
            except FacebookRequestError:
                logger.info(
                    f"Facebook Request Error: Facebook Graph API Failed for Adset ID {self.adset_structure_details['adset_id']}"
                )

            if targeting_search_response:
                interests_response = [Tools.convert_to_json(targeting_search_response[0])][0]
                source_interests_list.append(
                    {
                        "name": interests_response.get("name"),
                        "id": interests_response.get("id"),
                        "audience_size": interests_response.get("audience_size"),
                    }
                )
            else:
                source_interests_list.append(
                    {"name": interest.get("name"), "id": interest.get("id"), "audience_size": 0}
                )
        return {"source_interests": source_interests_list}

    def get_suggested_interests(self, interests_list: list, limit: int = 5):
        """
        Returns Suggested Interests for each Interests.

        Parameters
        ----------
        interests_list: list
            Interests List
        limit: int
            Limit on Number of Suggested Interests

        Returns
        -------
        suggested_interests_list: list[dict]
            Suggested Interests
        """
        suggested_interests_list = []
        targeting_search_response = None

        for interest in interests_list:
            params = {"q": interest, "limit": limit, "type": TargetingSearch.TargetingSearchTypes.interest}

            try:
                targeting_search_response = self.ad_account.get_targeting_search(params=params)
            except FacebookRequestError:
                logger.info(
                    f"Facebook Request Error: Facebook Graph API Failed for Adset ID {self.adset_structure_details['adset_id']}"
                )

            suggested_interests = [
                Tools.convert_to_json(suggested_interest) for suggested_interest in targeting_search_response
            ]

            if len(suggested_interests) > 0:
                for suggested_interest in suggested_interests:
                    suggested_interest.pop("type", None)
                    suggested_interest.pop("path", None)
                    suggested_interest.pop("description", None)

            suggested_interests_list.append(
                {"name": interest, "suggested_interests": suggested_interests if len(suggested_interests) > 0 else None}
            )

        return suggested_interests_list

    def get_hidden_interests(
        self,
        interests_list: List[Dict],
        limit: int = 5,
    ) -> List[Dict]:
        """
        Returns Hidden Interests for each Interest List.

        Parameters
        ----------
        interests_list: list[dict]
            Interests with Name & ID
        limit: int, default=5
            Hidden Interests Limit

        Returns
        -------
        hidden_interests: list[dict]
            Hidden Interests Associated with Particular Interest
        """
        # init Targeting.
        targeting_spec = self.adset_structure_details["targeting"]
        hidden_interests_list = []
        hidden_interests_response = None

        # For Each Interests.
        for interests in interests_list:

            # Grab Targeting Search Parameters set = Age & Location.
            targeting_search_params = {
                "interest_list": [interests],
                "type": TargetingSearch.TargetingSearchTypes.interest_suggestion,
                "age_max": targeting_spec["age_max"],
                "age_min": targeting_spec["age_min"],
                "geo_locations": targeting_spec["geo_locations"],
                "limit": limit,
            }

            # Obtain Hidden Interests.
            try:
                hidden_interests_response = TargetingSearch.search(params=targeting_search_params)
            except FacebookRequestError:
                logger.info(
                    f"Facebook Request Error: Facebook Graph API Failed for Adset ID {self.adset_structure_details['adset_id']}"
                )

            hidden_interests = [
                Tools.convert_to_json(suggested_interest) for suggested_interest in hidden_interests_response
            ]
            hidden_interests = sorted(hidden_interests, key=lambda x: x["audience_size"], reverse=True)

            hidden_interests_list.append(
                {"name": interests, "hidden_interests": hidden_interests if len(hidden_interests) > 0 else None}
            )

        return hidden_interests_list

    def get_audience_overlap_percent(self, interests_list: List):
        """
        Returns Audience Overlap Percentage

        Parameters
        ----------
        interests_list: list
            Interests List from the Payload

        Returns
        -------
        audience_overlap_percent: dict
            Percentage of Audience Overlap

        """
        audience_size_x_y = 0
        for interests in interests_list:
            audience_size_x_y += interests.get("audience_size")

        overlap_audience_size_z = self.get_overlap_audience_size(interests_list=interests_list)

        # Computing Audience Overlap Percent, a = x + y - z
        if overlap_audience_size_z:
            intersection_a = audience_size_x_y - overlap_audience_size_z
            audience_overlap_percent = 100 * (intersection_a / overlap_audience_size_z)

            audience_overlap_percent_response = {
                "audience_overlap_percent": 100
                if audience_overlap_percent >= 100
                else round(audience_overlap_percent, 4)
            }
            return audience_overlap_percent_response

        else:

            audience_overlap_percent_response = {"audience_overlap_percent": None}
            return audience_overlap_percent_response

    def get_overlap_audience_size(self, interests_list: List):
        """
        Returns Overlapping Audience Size Estimate for Multiple Interests.

        Parameters
        ----------
        interests_list: list
            Interests List from the Payload

        Returns
        -------
        overlap_audience_size: int
            Overlapping Audience Size Estimate for Multiple Interests

        """
        overlap_audience_size_response = None

        # init Targeting.
        targeting_spec = self.adset_structure_details["targeting"]
        optimization_goal = self.adset_structure_details.get("optimization_goal")

        # Remove audience_size & source for inputting to facebook api.
        params_interests = interests_list.copy()
        for interest in params_interests:
            interest.pop("audience_size", None)

        # Grab Targeting Spec Parameters.
        targeting_spec_params = {
            "age_max": targeting_spec["age_max"],
            "age_min": targeting_spec["age_min"],
            "geo_locations": targeting_spec["geo_locations"],
            "flexible_spec": [{"interests": params_interests}],
        }
        try:
            overlap_audience_size_response = self.ad_account.get_delivery_estimate(
                fields=["estimate_mau"],
                params={"targeting_spec": targeting_spec_params, "optimization_goal": optimization_goal},
            )
        except FacebookRequestError:
            logger.info(
                f"Facebook Request Error: Facebook Graph API Failed for Adset ID {self.adset_structure_details['adset_id']}"
            )

        if overlap_audience_size_response:
            response = Tools.convert_to_json(overlap_audience_size_response[0])
            overlap_audience_size = response.get("estimate_mau", None)
            return overlap_audience_size
        else:
            return None
