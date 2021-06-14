import json

import humps
from flask_restful import reqparse
from sqlalchemy import or_
from typing import Optional, Dict, Union, List

from FiledInfluencer.Api.Common.services import CommonService
from FiledInfluencer.Api.InfluencerProfile.influencer_dataclass import InfluencerProfile, EngagementRate, Followers, \
    EngagementPerPost
from FiledInfluencer.Api.InfluencerProfile.influencer_enum import AccountTypeEnum
from FiledInfluencer.Api.InfluencerProfile.models import Influencers
from FiledInfluencer.Api.InfluencerProfile.schemas import InfluencersResponse
from FiledInfluencer.Api.startup import session_scope


class InfluencerParser:
    @staticmethod
    def influencer_profile_parser() -> reqparse.RequestParser:
        """
        Parser the fields coming from the request
        """

        parser = reqparse.RequestParser()
        parser.add_argument(
            "page_size",
            type=CommonService.check_positive_value,
            required=False,
            default=100,
        )
        parser.add_argument(
            "last_influencer_id",
            type=CommonService.check_positive_value,
            required=False,
            default=None,
        )
        parser.add_argument(
            "name",
            type=str,
            required=False,
        )
        parser.add_argument(
            "get_total_count",
            type=bool,
            required=False,
            default=False,
        )
        parser.add_argument(
            "account_type",
            type=int,
            required=False,
            default=None,
            choices=(0, 1, 3)
        )
        parser.add_argument(
            "is_verified",
            type=str,
            required=False,
            default=None,
        )
        parser.add_argument(
            "followers_min_count",
            type=CommonService.check_positive_value,
            required=False,
            default=None,
        )
        parser.add_argument(
            "followers_max_count",
            type=CommonService.check_positive_value,
            required=False,
            default=None,
        )
        parser.add_argument(
            "engagements_per_post_min_count",
            type=CommonService.check_positive_value,
            required=False,
            default=None,
        )
        parser.add_argument(
            "engagements_per_post_max_count",
            type=CommonService.check_positive_value,
            required=False,
            default=None,
        )
        parser.add_argument(
            "engagement_rate_min_count",
            type=CommonService.check_positive_value,
            required=False,
            default=None,
        )
        parser.add_argument(
            "engagement_rate_max_count",
            type=CommonService.check_positive_value,
            required=False,
            default=None,
            choices=list(range(0, 101))
        )
        return parser


class InfluencerProfilesHandler:

    @staticmethod
    def range_checker(
            min_value: Optional[int],
            max_value: Optional[int],
            param_name: str
    ) -> Optional[Dict[str, str]]:
        """
        This will check if any value is not missing or if min value is more than the max value
        @param min_value: Minimum value of the param
        @param max_value: Maximum value of the param
        @param param_name: Parameter we are performing these tests on
        @return: If any check fails we will return a message in a Dict, Else we will return None
        """
        if min_value is None and max_value is None:
            return None
        if min_value is None:
            return {"Message": f"Please provide min_value for {param_name}"}
        if max_value is None:
            return {"Message": f"Please provide max_value for {param_name}"}
        if max_value < min_value:
            return {"Message": f"{param_name} range is out of bounds"}

    @classmethod
    def perform_range_check(cls, variables: List[str], data: Dict) -> Optional[Dict[str, str]]:
        """
        This is used to get the param and there max values and min values to pass for checking range
        @param variables: all the params that needs to have range check
        @param data: all the data for the respective params
        @return: If any check fails we will return a message in a Dict.
        """
        for var in variables:
            min_value = data[f"{var}_min_count"]
            max_value = data[f"{var}_max_count"]
            result = cls.range_checker(min_value, max_value, var)
            if result:
                return result

    @classmethod
    def populate_profiles(cls, data: Dict) -> Union[InfluencerProfile, Dict[str, str]]:
        """
        This is used to Populate the Influencer Profiles dataclass
        @param data: All the data in the form of Dictionary
        @return: InfluncerProfile object
        """

        # Engagement_Rate
        range_check_variables = [
            "engagement_rate",
            "engagements_per_post",
            "followers",
        ]
        result = cls.perform_range_check(range_check_variables, data)
        if result:
            return result

        engagement_rate = None
        if data["engagement_rate_min_count"] and data["engagement_rate_max_count"]:
            engagement_rate = EngagementRate(
                engagement_rate_min_count=data["engagement_rate_min_count"],
                engagement_rate_max_count=data["engagement_rate_max_count"],
            )

        # Followers
        followers = None
        if data["followers_min_count"] and data["followers_max_count"]:
            followers = Followers(
                followers_min_count=data["followers_min_count"],
                followers_max_count=data["followers_max_count"],
            )

        # Engagement Per Post
        engagements_per_post = None
        if data["engagements_per_post_min_count"] and data["engagements_per_post_max_count"]:
            engagements_per_post = EngagementPerPost(
                engagements_per_post_min_count=data["engagements_per_post_min_count"],
                engagements_per_post_max_count=data["engagements_per_post_max_count"],
            )

        # Verified
        if data["is_verified"] == "both":
            is_verified = None
        else:
            is_verified = data["is_verified"]

        influencer_profile = InfluencerProfile(
            page_size=data["page_size"],
            last_influencer_id=data["last_influencer_id"],
            name=data["name"],
            get_total_count=data["get_total_count"],
            account_type=data["account_type"],
            is_verified=is_verified,
            followers=followers,
            engagement_per_post=engagements_per_post,
            engagement_rate=engagement_rate,
        )

        return influencer_profile

    @staticmethod
    def convert_to_json(influencer: Influencers) -> Dict[str, str]:
        """
        Convert a sqlalchemy model to pydantic schema camelized json

        :returns: camelized dictionary keys
        """
        details = json.loads(influencer.Details)

        pydantic_influencer = InfluencersResponse(
            Id=influencer.Id,
            Name=influencer.Name,
            Biography=influencer.Biography,
            Engagement=influencer.Engagement,
            ProfilePicture=details["profile_pic_url"],
            CategoryName=details["category_name"],
            AccountType=influencer.AccountType,
            IsVerified=influencer.IsVerified,
            Followers=influencer.Followers,
            MinEngagementPerPost=influencer.MinEngagementPerPost,
            MaxEngagementPerPost=influencer.MaxEngagementPerPost,
            Email=details.get('email_id'),
        )
        return humps.camelize(pydantic_influencer.dict())

    @classmethod
    def get_profiles(cls, profile: InfluencerProfile) -> Union[List[Dict[str, str]], Dict[str, str]]:
        """
        This will make sure to change the query according to which filter has been called and fetch the profiles
        based on those filtering
        @param profile: Influencer Profile object
        @return: Profiles in Json Format
        """

        get_total_count = profile.get_total_count
        page_size = profile.page_size
        last_influencer_id = profile.last_influencer_id
        name = profile.name
        account_type = profile.account_type
        is_verified = profile.is_verified
        followers = profile.followers
        engagement_per_post = profile.engagement_per_post
        engagement_rate = profile.engagement_rate

        # Initializing session to execute query
        with session_scope() as session:
            query = session.query(Influencers)

            if get_total_count:
                count = query.count()
                results = {"count": count}
                return results

            if last_influencer_id:
                # last_influencer_id was already sent in previous request
                last_influencer_id += 1
                query = query.filter(Influencers.Id >= last_influencer_id)

            if followers:
                followers_filters = (
                    Influencers.Followers >= followers.followers_min_count,
                    Influencers.Followers <= followers.followers_max_count,
                )
                query = query.filter(*followers_filters)

            if engagement_rate:
                engagement_filters = (
                    Influencers.Engagement >= engagement_rate.engagement_rate_min_count,
                    Influencers.Engagement <= engagement_rate.engagement_rate_max_count,
                )
                query = query.filter(*engagement_filters)

            if engagement_per_post:
                engagement_per_post_filters = (
                    Influencers.MinEngagementPerPost >= engagement_per_post.engagements_per_post_min_count,
                    Influencers.MaxEngagementPerPost <= engagement_per_post.engagements_per_post_max_count,
                )
                query = query.filter(*engagement_per_post_filters)

            if name:
                search = f"%{name}%"
                query = query.filter(Influencers.Name.like(search))

            if is_verified:
                query = query.filter(Influencers.IsVerified == is_verified)

            if account_type is not None:
                account_type_enum1 = ""
                account_type_enum2 = ""
                if account_type == AccountTypeEnum.BUSINESS.value:
                    account_type_enum1 = "Business"
                    account_type_enum2 = "Business, Professional"

                elif account_type == AccountTypeEnum.PROFESSIONAL.value:
                    account_type_enum1 = "Professional"
                    account_type_enum2 = "Business, Professional"

                elif account_type == AccountTypeEnum.PERSONAL.value:
                    account_type_enum1 = "Personal"
                    account_type_enum2 = "Personal"

                if account_type == AccountTypeEnum.PERSONAL.value:
                    query = query.filter(Influencers.AccountType == account_type_enum1)
                else:
                    query = query.filter(
                        or_(Influencers.AccountType == account_type_enum1,
                            Influencers.AccountType == account_type_enum2)
                    )

            query = query.limit(page_size)
            return [cls.convert_to_json(result) for result in query]
