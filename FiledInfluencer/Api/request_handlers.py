import json

from datetime import datetime
from flask_restful import reqparse, inputs

import humps
from typing import Dict, List, Union

from FiledInfluencer.Api.models import Influencers, EmailTemplates
from FiledInfluencer.Api.schemas import InfluencersResponse, EmailTemplateResponse
from FiledInfluencer.Api.startup import session_scope


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
        )
        return humps.camelize(pydantic_influencer.dict())

    @classmethod
    def get_profiles(
        cls,
        name: str,
        engagement: Dict,
        last_influencer_id: int,
        page_size: int,
        total_count: bool,
    ) -> Union[List[Dict[str, str]], Dict[str, str]]:
        # last_influencer_id was already sent in previous request
        last_influencer_id += 1

        Engagement_filters = (
            Influencers.Engagement > engagement["min_count"],
            Influencers.Engagement < engagement["max_count"],
        )

        with session_scope() as session:
            # for infinite scrolling
            # offset queries are inefficient
            if total_count is True:
                count = session.query(Influencers).count()
                results = {"count": count}

            elif name:
                search = f"%{name}%"
                results = (
                    session.query(Influencers)
                    .filter(Influencers.Id >= last_influencer_id, Influencers.Name.like(search), *Engagement_filters)
                    .limit(page_size)
                )

            else:
                results = (
                    session.query(Influencers)
                    .filter(Influencers.Id >= last_influencer_id, *Engagement_filters)
                    .limit(page_size)
                )

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
