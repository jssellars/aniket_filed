import json
from datetime import datetime
from typing import Dict, List, Union

import humps
from flask_restful import reqparse

from FiledInfluencer.Api.db_query import InfluencerProfileQuery
from FiledInfluencer.Api.models import EmailTemplates, Influencers
from FiledInfluencer.Api.schemas import EmailTemplateResponse, InfluencersResponse
from FiledInfluencer.Api.startup import session_scope
from FiledInfluencer.influencer_enum import AccountTypeEnum


class InfluencerProfilesHandler:
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
        )
        return humps.camelize(pydantic_influencer.dict())

    @classmethod
    def get_profiles(
        cls,
        name: str,
        last_influencer_id: int,
        engagement_rate: Dict,
        page_size: int,
        get_total_count: bool,
        engagement_per_post: Dict,
        account_type: int,
        is_verified: bool,
        followers: Dict,
    ) -> Union[List[Dict[str, str]], Dict[str, str]]:

        # last_influencer_id was already sent in previous request
        last_influencer_id += 1
        global account_type_enum1, account_type_enum2, EngagementPerPost_filters

        Followers_filters = (
            Influencers.Followers >= followers["min_count"],
            Influencers.Followers <= followers["max_count"],
        )

        if engagement_per_post is not None:
            EngagementPerPost_filters = (
                Influencers.MinEngagementPerPost >= engagement_per_post["min_count"],
                Influencers.MaxEngagementPerPost <= engagement_per_post["max_count"],
            )

        Engagement_filters = (
            Influencers.Engagement >= engagement_rate["min_count"],
            Influencers.Engagement <= engagement_rate["max_count"],
        )

        if account_type is not None:
            if account_type == AccountTypeEnum.BUSINESS.value:
                account_type_enum1 = "Business"
                account_type_enum2 = "Business, Professional"

            elif account_type == AccountTypeEnum.PROFESSIONAL.value:
                account_type_enum1 = "Professional"
                account_type_enum2 = "Business, Professional"

            elif account_type == AccountTypeEnum.PERSONAL.value:
                account_type_enum1 = "Personal"
                account_type_enum2 = "Personal"

        # Initializing session to execute query
        query = InfluencerProfileQuery()

        # for infinite scrolling
        # offset queries are inefficient
        if get_total_count:
            results = query.get_total_count_query()

        elif name and engagement_per_post and is_verified and account_type is not None:
            results = query.get_name_engagementperpost_isverified_accountype_query(
                name,
                EngagementPerPost_filters,
                account_type,
                account_type_enum1,
                account_type_enum2,
                is_verified,
                Followers_filters,
                last_influencer_id,
                page_size,
                Engagement_filters,
            )

        elif name and engagement_per_post and account_type is not None:
            results = query.get_name_engagementperpost_accountype_query(
                name,
                EngagementPerPost_filters,
                account_type,
                account_type_enum1,
                account_type_enum2,
                Followers_filters,
                last_influencer_id,
                page_size,
                Engagement_filters,
            )

        elif name and engagement_per_post and is_verified is not None:
            results = query.get_name_engagementperpost_isverified_query(
                name,
                EngagementPerPost_filters,
                is_verified,
                Followers_filters,
                last_influencer_id,
                page_size,
                Engagement_filters,
            )

        elif name and is_verified and account_type is not None:
            results = query.get_name_isverified_accountype_query(
                name,
                is_verified,
                account_type,
                account_type_enum1,
                account_type_enum2,
                Followers_filters,
                last_influencer_id,
                page_size,
                Engagement_filters,
            )

        elif is_verified and engagement_per_post and account_type is not None:
            results = query.get_isverified_engagementperpost_accountype_query(
                is_verified,
                EngagementPerPost_filters,
                account_type,
                account_type_enum1,
                account_type_enum2,
                Followers_filters,
                last_influencer_id,
                page_size,
                Engagement_filters,
            )

        elif engagement_per_post and account_type is not None:
            results = query.get_engagementperpost_accountype_query(
                EngagementPerPost_filters,
                account_type,
                account_type_enum1,
                account_type_enum2,
                Followers_filters,
                last_influencer_id,
                page_size,
                Engagement_filters,
            )

        elif name and account_type is not None:
            results = query.get_name_accounttype_query(
                name,
                account_type,
                account_type_enum1,
                account_type_enum2,
                Followers_filters,
                last_influencer_id,
                page_size,
                Engagement_filters,
            )

        elif name and engagement_per_post:
            results = query.get_name_engagementperpost_query(
                name, EngagementPerPost_filters, Followers_filters, last_influencer_id, page_size, Engagement_filters
            )

        elif engagement_per_post and is_verified is not None:
            results = query.get_engagementperpost_isverified_query(
                EngagementPerPost_filters,
                is_verified,
                Followers_filters,
                last_influencer_id,
                page_size,
                Engagement_filters,
            )

        elif is_verified and account_type is not None:
            results = query.get_isverified_accountype_query(
                is_verified,
                account_type,
                account_type_enum1,
                account_type_enum2,
                Followers_filters,
                last_influencer_id,
                page_size,
                Engagement_filters,
            )

        elif is_verified and name is not None:
            results = query.get_isverified_name_query(
                is_verified, name, Followers_filters, last_influencer_id, page_size, Engagement_filters
            )

        elif engagement_per_post:
            results = query.get_engagementperpost_query(
                EngagementPerPost_filters, Followers_filters, last_influencer_id, page_size, Engagement_filters
            )

        elif name:
            results = query.get_name_query(name, Followers_filters, last_influencer_id, page_size, Engagement_filters)

        elif account_type is not None:
            results = query.get_accounttype_query(
                account_type,
                account_type_enum1,
                account_type_enum2,
                Followers_filters,
                last_influencer_id,
                page_size,
                Engagement_filters,
            )

        elif is_verified:
            results = query.get_isverified_query(
                is_verified, Followers_filters, last_influencer_id, page_size, Engagement_filters
            )

        else:
            results = query.get_default_query(Followers_filters, last_influencer_id, page_size, Engagement_filters)

        if isinstance(results, dict):
            return results
        return [cls.convert_to_json(result) for result in results]


class EmailTemplateHandler:
    blank_field_error_msg = "This field cannot be left blank"

    @classmethod
    def email_template_parser(cls):
        """
        Parser the fields coming from the request
        """

        parser = reqparse.RequestParser()
        parser.add_argument(
            "name",
            type=str,
            required=False,
        )
        parser.add_argument(
            "subject",
            type=str,
            required=False,
        )
        parser.add_argument(
            "body",
            type=str,
            required=False,
        )

        parser.add_argument("campaign", type=int, required=True, help=cls.blank_field_error_msg)
        return parser

    @staticmethod
    def convert_to_json(email_template: EmailTemplates) -> Dict[str, str]:
        """
        Convert a sqlalchemy model to pydantic schema camelized json

        :returns: camelized dictionary keys
        """

        pydantic_email_template = EmailTemplateResponse.from_orm(email_template)
        # Datetime is not JSON serializable
        json_email_template = pydantic_email_template.json()
        return humps.camelize(json.loads(json_email_template))

    @classmethod
    def get_email_templates(cls, user_id) -> List[Dict[str, str]]:
        with session_scope() as session:
            # for infinite scrolling
            # offset queries are inefficient
            results = session.query(EmailTemplates).filter(EmailTemplates.CreatedById == user_id)

        return [cls.convert_to_json(result) for result in results]

    @classmethod
    def populate_model(cls, data):
        email_template = EmailTemplates(
            Name=data["name"],
            Subject=data["subject"],
            Body=data["body"],
            CampaignId=data["campaign"],
            CreatedById=data["created_by"],
            CreatedAt=datetime.utcnow(),
        )
        return email_template

    @classmethod
    def write_to_db(cls, data):
        value = cls.populate_model(data)
        with session_scope() as session:
            session.add(value)
        value = cls.convert_to_json(value)
        return value
