import json
from datetime import datetime

import humps
from flask_restful import reqparse
from typing import Dict, List

from FiledInfluencer.Api.EmailTemplate.models import EmailTemplates
from FiledInfluencer.Api.EmailTemplate.schemas import EmailTemplateResponse
from FiledInfluencer.Api.startup import session_scope


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
        """
        This will fetch the templates based on user_Id
        @param user_id: The id of the user whose templates have to be fetched
        @return: Dict containing templates
        """
        with session_scope() as session:
            # for infinite scrolling
            # offset queries are inefficient
            results = session.query(EmailTemplates).filter(EmailTemplates.CreatedById == user_id)

        return [cls.convert_to_json(result) for result in results]

    @classmethod
    def populate_model(cls, data):
        """
        This is used to Populate the Email Templates dataclass
        @param data: All the data in the form of Dictionary
        @return: EmailTemplate object
        """
        email_template = EmailTemplates(
            Name=data["name"],
            Subject=data["subject"],
            Body=data["body"],
            CampaignId=data["campaign"],
            CreatedById=data["created_by"],
            CreatedAt=datetime.utcnow(),
            # TODO: extract from JWT
            CreatedByFirstName="",
            CreatedByLastName="",
        )
        return email_template

    @classmethod
    def write_to_db(cls, data):
        """
        This will save the Email Template data into the database
        @param data: Contains all the details of Email template
        @return: Saved email template in JSON Format
        """
        value = cls.populate_model(data)
        with session_scope() as session:
            session.add(value)
        value = cls.convert_to_json(value)
        return value
