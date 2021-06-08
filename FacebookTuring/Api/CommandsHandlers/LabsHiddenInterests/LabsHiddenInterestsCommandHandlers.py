"""
Labs Hidden Interests Command Handlers

"""
# Standard Imports.
from typing import Dict, AnyStr, List

from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.adobjects.targetingsearch import TargetingSearch

# Core Imports.
from Core.Web.FacebookGraphAPI.GraphAPI.SdkGetStructures import get_and_map_structures  # for structures
from Core.Web.FacebookGraphAPI.Tools import Tools  # for utility.

# for filtering.
from Core.Web.FacebookGraphAPI.Models.FieldsMetadata import FieldsMetadata
from Core.Tools.QueryBuilder.QueryBuilderLogicalOperator import AgGridFacebookOperator
from Core.Web.FacebookGraphAPI.GraphAPIMappings.FacebookToTuringStatusMapping import EffectiveStatusEnum
from Core.Dexter.Infrastructure.Domain.LevelEnums import LevelEnum


class GetInterestsHandler:
    def handle(self, ad_account_id: AnyStr = None, adset_id: AnyStr = None):
        """
        Parses & Returns Interests for the specified Adset.
        Parameters
        ----------
        ad_account_id: str, default = None
            Ad Account ID
        adset_id: str, default=None
            Adset ID associated with Facebook Ad Account ID
        Returns
        -------
        # todo: Add Returns & Returns Typing.
        """

        filtering = {
            "field": FieldsMetadata.effective_status.name,
            "operator": AgGridFacebookOperator.IN.name,
            "value": [EffectiveStatusEnum.ACTIVE.value]
        }

        structures = get_and_map_structures(
            ad_account_id=ad_account_id,
            level=LevelEnum.ADSET,
            filtering=filtering
        )
        for structure in structures:
            if structure["adset_id"] == adset_id:
                adset_structure = structure

        adset_structure_details = adset_structure.get("details")
        targeting_spec = adset_structure_details["targeting"]
        flexible_spec_interests = targeting_spec["flexible_spec"][0]["interests"]

        source_interests = self.get_interests(ad_account_id=ad_account_id,
                                              flexible_spec_interests=flexible_spec_interests)

        response = {
            "source_interests": source_interests
        }

        return response

    def get_interests(self, ad_account_id: AnyStr, flexible_spec_interests: List[Dict]):
        """
        Returns Source, Suggested, and Hidden Interests.
        Parameters
        ----------
        ad_account_id: str
            Facebook Ad Account ID
        flexible_spec_interests: list[dict]
            Interests List from Flexible Spec of Targeting for the specified Adset
        Returns
        -------
        interests_list: list[dict]
            List of Hidden & Suggested Interest for Source Interests
        """
        ad_account = AdAccount(fbid=ad_account_id)

        interests_list = []
        for interests in flexible_spec_interests:
            interests_response = ad_account.get_by_ids(ids=[interests["id"]])
            interests_response = Tools.convert_to_json(interests_response[0])
            suggested_interests = self.get_suggested_interests(interest_list=[interests["name"]],
                                                               ad_account=ad_account)
            hidden_interests = self.get_hidden_interests(interest_list=[interests["name"]])

            source_interests = {
                "id": interests_response["id"],
                "name": interests_response["name"],
                "audience_size": interests_response["audience_size"],
                "suggested_interests": suggested_interests,
                "hidden_interests": hidden_interests
            }
            interests_list.append(source_interests)

        return interests_list

    @staticmethod
    def get_hidden_interests(interest_list: List[Dict], limit: int = 5) -> List[Dict]:
        """
        Returns Hidden Interests for each Interest List.
        Parameters
        ----------
        interest_list: list[dict]
            Interests with Name & ID
        limit: int, default=5
            Hidden Interests Limit
        Returns
        -------
        hidden_interests: list[dict]
            Hidden Interests Associated with Particular Interest
        """
        # Suggested Interests.
        targeting_search_params = {
            "interest_list": interest_list,
            "type": TargetingSearch.TargetingSearchTypes.interest_suggestion,
            "limit": limit
        }

        hidden_interests = TargetingSearch.search(params=targeting_search_params)
        hidden_interests = [Tools.convert_to_json(suggested_interest) for suggested_interest in
                            hidden_interests]
        hidden_interests = sorted(hidden_interests, key=lambda x: x["audience_size"], reverse=True)

        return hidden_interests

    @staticmethod
    def get_suggested_interests(interest_list: List[Dict], limit: int = 5, ad_account: AdAccount = None) -> List[Dict]:
        """
        Returns Suggested Interests for each Interest List.
        Parameters
        ----------
        interest_list: list[dict]
            Interests with Name & ID
        limit: int, default=5
            Hidden Interests Limit
        ad_account: AdAccount, default=None
            SDK AdAccount Instance
        Returns
        -------
        suggested_interests: list[dict]
            Suggested Interests Associated with Particular Interest
        """
        # Suggested Interests.
        targeting_search_params = {
            "q": interest_list,
            "type": TargetingSearch.TargetingSearchTypes.interest,
            "limit": limit
        }
        suggested_interests_responses = ad_account.get_targeting_suggestions(
            params=targeting_search_params
        )
        suggested_interests = []

        for suggested_interests_response in suggested_interests_responses:
            suggested_interests_json = Tools.convert_to_json(suggested_interests_response)
            suggested_interests.append(
                {
                    "id": suggested_interests_json["id"],
                    "name": suggested_interests_json["name"],
                    "audience_size": suggested_interests_json["audience_size"]
                }
            )

        return suggested_interests


class GetAudienceOverlapHandler:
    def handle(self, query_json: Dict, ad_account_id: AnyStr = None, adset_id: AnyStr = None):
        """
        Parses & Returns Audience Overlap for the specified Adset.
        Parameters
        ----------
        query_json: dict
            Payload From the POST Request
        ad_account_id: str, default = None
            Ad Account ID
        adset_id: str, default=None
            Adset ID associated with Facebook Ad Account ID
        Returns
        -------
        # todo: Add Returns & Returns Typing.
        """
        x = int(query_json["source_interests"]["audience_size"])
        y = int(query_json["hidden_interests"]["audience_size"])

        interest_list = [query_json["source_interests"]["name"], query_json["hidden_interests"]["name"]]

        self.get_overlap_audience_size(interest_list=interest_list,
                                       ad_account_id=ad_account_id)

        return "Hello World"

    @staticmethod
    def get_overlap_audience_size(interest_list: List, ad_account_id, limit: int = 5):
        # Suggested Interests.
        targeting_search_params = {
            "interests": interest_list,
            "type": TargetingSearch.TargetingSearchTypes.interest,
            "limit": limit
        }
        overlap_audience_size = TargetingSearch.search(
            params=targeting_search_params
        )
        pass
