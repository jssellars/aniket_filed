import json
from datetime import datetime

from typing import Dict, List, Union

import humps
from flask_restful import reqparse

from FiledInfluencer.Api.db_query import InfluencerProfileQuery
from FiledInfluencer.Api.models import Influencers, EmailTemplates
from FiledInfluencer.Api.schemas import InfluencersResponse, EmailTemplateResponse
from FiledInfluencer.Api.startup import session_scope
from FiledInfluencer.enum import AccountTypeEnum


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
        )
        return humps.camelize(pydantic_influencer.dict())

    @classmethod
    def get_profiles(
        cls,
        name: str,
        engagement: Dict,
        last_influencer_id: int,
        page_size: int,
        get_total_count: bool,
        post_engagement: Dict,
        account_type: int,
        is_verified: bool,
    ) -> Union[List[Dict[str, str]], Dict[str, str]]:

        # last_influencer_id was already sent in previous request
        last_influencer_id += 1
        global account_type_enum1
        global account_type_enum2

        Engagement_filters = (
            Influencers.Engagement > engagement["min_count"],
            Influencers.Engagement < engagement["max_count"],
        )

        if account_type is not None:
            if account_type == AccountTypeEnum.BUSINESS.value:
                account_type_enum1 = 'Business'
                account_type_enum2 = 'Business, Professional'

            elif account_type == AccountTypeEnum.PROFESSIONAL.value:
                account_type_enum1 = 'Professional'
                account_type_enum2 = 'Business, Professional'

            elif account_type == AccountTypeEnum.PERSONAL.value:
                account_type_enum1 = 'Personal'
                account_type_enum2 = 'Personal'

        # Initializing session to execute query
        query = InfluencerProfileQuery()

        # for infinite scrolling
        # offset queries are inefficient
        if get_total_count:
            results = query.get_total_count_query()

        elif name and post_engagement and is_verified and account_type is not None:
            results = query.get_name_postengagement_isverified_accountype_query(
                                        name, post_engagement, account_type, account_type_enum1, account_type_enum2,
                                        is_verified, Engagement_filters, last_influencer_id, page_size)

        elif name and post_engagement and account_type is not None:
            results = query.get_name_postengagement_accountype_query(
                                        name, post_engagement, account_type, account_type_enum1, account_type_enum2,
                                        Engagement_filters, last_influencer_id, page_size)

        elif name and post_engagement and is_verified is not None:
            results = query.get_name_postengagement_isverified_query(
                                        name, post_engagement, is_verified,
                                        Engagement_filters, last_influencer_id, page_size)

        elif name and is_verified and account_type is not None:
            results = query.get_name_isverified_accountype_query(
                                        name, is_verified, account_type, account_type_enum1, account_type_enum2,
                                        Engagement_filters, last_influencer_id, page_size)

        elif is_verified and post_engagement and account_type is not None:
            results = query.get_isverified_postengagement_accountype_query(
                                        is_verified, post_engagement, account_type, account_type_enum1, account_type_enum2,
                                        Engagement_filters, last_influencer_id, page_size)

        elif post_engagement and account_type is not None:
            results = query.get_postengagement_accountype_query(
                                        post_engagement, account_type, account_type_enum1, account_type_enum2,
                                        Engagement_filters, last_influencer_id, page_size)

        elif name and account_type is not None:
            results = query.get_name_accounttype_query(
                                        name, account_type, account_type_enum1, account_type_enum2,
                                        Engagement_filters, last_influencer_id, page_size)

        elif name and post_engagement:
            results = query.get_name_postengagement_query(
                                        name, post_engagement,
                                        Engagement_filters, last_influencer_id, page_size)

        elif post_engagement and is_verified is not None:
            results = query.get_postengagement_isverified_query(
                                        post_engagement, is_verified,
                                        Engagement_filters, last_influencer_id, page_size)

        elif is_verified and account_type is not None:
            results = query.get_isverified_accountype_query(
                                        is_verified, account_type, account_type_enum1, account_type_enum2,
                                        Engagement_filters, last_influencer_id, page_size)

        elif is_verified and name is not None:
            results = query.get_isverified_name_query(
                                        is_verified, name,
                                        Engagement_filters, last_influencer_id, page_size)

        elif post_engagement:
            results = query.get_postengagement_query(
                                        post_engagement,
                                        Engagement_filters, last_influencer_id, page_size)

        elif name:
            results = query.get_name_query(
                                        name,
                                        Engagement_filters, last_influencer_id, page_size)

        elif account_type is not None:
            results = query.get_accounttype_query(
                                        account_type, account_type_enum1, account_type_enum2,
                                        Engagement_filters, last_influencer_id, page_size)

        elif is_verified:
            results = query.get_isverified_query(
                                        is_verified,
                                        Engagement_filters, last_influencer_id, page_size)

        else:
            results = query.get_default_query(
                                        Engagement_filters, last_influencer_id, page_size)

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
