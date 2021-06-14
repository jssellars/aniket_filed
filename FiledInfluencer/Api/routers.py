import logging

import flask_restful
import humps
from flask import request
from typing import Dict

from Core.Web.Security.JWTTools import decode_jwt_from_headers
from Core.flask_extensions import log_request
from Core.logging_config import request_as_log_dict
from FiledInfluencer.Api.AWSDocuments.request_handler import DocumentHandler, DocumentParser
from FiledInfluencer.Api.EmailTemplate.request_handler import EmailTemplateHandler
from FiledInfluencer.Api.InfluencerProfile.request_handler import (
    InfluencerProfilesHandler,
    InfluencerParser,
)
from FiledInfluencer.Api.Integrations.mail_sendgrid import SendGridMailer
from FiledInfluencer.Api.startup import config, fixtures

logger = logging.getLogger(__name__)


class Resource(flask_restful.Resource):
    method_decorators = [log_request(logger)]


class HealthCheck(Resource):
    def get(self):
        return None, 200


class Version(Resource):
    def get(self):
        return config.version_endpoint_payload, 200


class InfluencerProfiles(Resource):

    @fixtures.authorize_jwt
    def get(self):
        """
        This GET request will fetch the profiles based on what filters have been provided by the client
        @return:  Profiles in Json Format
        """

        try:
            # Get the data from the parser
            parser = InfluencerParser.influencer_profile_parser()
            data = parser.parse_args()

            # Populate InfluencerProfile object
            profile = InfluencerProfilesHandler.populate_profiles(data)

            if isinstance(profile, Dict):
                return profile, 400

            # Get profiles based on filters
            response = InfluencerProfilesHandler.get_profiles(
                profile
            )
            return response, 200
        except Exception as e:
            logger.exception(repr(e), extra=request_as_log_dict(request))
            return "error occurred", 400


class EmailTemplates(Resource):
    parser = EmailTemplateHandler.email_template_parser()

    @fixtures.authorize_jwt
    def get(self, user_id):
        """
        This GET request will fetch the saved templates of the user.
        @param user_id: User requesting the templates
        @return: Dict containing templates
        """
        try:
            #  Retrieve email templates for the user_id
            response = EmailTemplateHandler.get_email_templates(user_id)
            if response:
                return response, 200
            return {"Message": "Not Found"}, 400
        except Exception as e:
            logger.exception(repr(e), extra=request_as_log_dict(request))
            return "error occurred", 400

    @fixtures.authorize_jwt
    def post(self, user_id):
        """
        This POST request saves template of the user to the database.
        @param user_id: User requesting the templates
        @return: Save template in JSON format
        """

        try:
            # Get the data from the parser
            data = EmailTemplates.parser.parse_args()
            data["created_by"] = user_id
            try:
                # Save the email template to the database
                email_template = EmailTemplateHandler.write_to_db(data)
            except:
                return {"message": "An error occurred while inserting the item."}, 500

            return email_template, 200
        except Exception as e:
            logger.exception(repr(e), extra=request_as_log_dict(request))
            return "error occurred", 400


class Documents(Resource):

    @fixtures.authorize_jwt
    def post(self):
        """
        The POST request will upload the document on the S3 bucket, If the upload is successful then we will save the
        Details in the database
        @return: Saved Document details in Json Format
        """

        try:
            # Get the data from the parser
            parser = DocumentParser.post_parser()
            request_data = parser.parse_args()

            # Check if size of document is within limits
            size_in_limit = DocumentHandler.max_document_size(request_data["documents"][0])
            if not size_in_limit:
                return "File size limit exceeds the max size", 413

            # Upload the document to S3 and Save it to the Database
            result = DocumentHandler.upload_document(request_data)
            if not result:
                return result, 400

            return result, 200
        except Exception as e:
            logger.exception(repr(e), extra=request_as_log_dict(request))
            return "error occurred", 400

    @fixtures.authorize_jwt
    def get(self):
        """
        This GET request will fetch the document from the S3.
        @return: DICT containing the downloadable URL
        """
        try:
            # Get the data from the parser
            parser = DocumentParser.get_parser()
            request_data = parser.parse_args()
            key = request_data["key"]

            # Download the document from the S3
            result = DocumentHandler.download_document(key)
            if not result:
                return result, 400

            return result, 200
        except Exception as e:
            logger.exception(repr(e), extra=request_as_log_dict(request))
            return "error occurred", 400

    @fixtures.authorize_jwt
    def delete(self):
        """
        This DELETE request will delete the document from the S3 and also delete the entry of that document from the
        database.
        @return: True
        """
        try:
            # Get the data from the parser
            parser = DocumentParser.delete_parser()
            request_data = parser.parse_args()
            key = request_data["key"]

            #  Delete the Document from the S3 and remove entry from database
            result = DocumentHandler.delete_document(key)
            if not result:
                return result, 400

            return result, 200
        except Exception as e:
            logger.exception(repr(e), extra=request_as_log_dict(request))
            return "error occurred", 400


class MailSender(Resource):
    @fixtures.authorize_jwt
    def post(self):
        try:
            token_data = decode_jwt_from_headers()
            user_id = token_data["user_filed_id"]
            # TODO: jwt verified but may need added checking and permissions

            message_json = humps.depascalize(request.get_json(force=True))
            if (
                isinstance(message_json["to_emails"], list)
                and isinstance(message_json["subject"], str)
                and isinstance(message_json["text_body"], str)
            ):
                response = SendGridMailer.send_mail(
                    to_emails=message_json["to_emails"],
                    subject=message_json["subject"],
                    plain_text_content=message_json["text_body"],
                    cc_emails=message_json["cc_emails"] if isinstance(message_json["cc_emails"], list) else None,
                )
                if response["status_code"] == 202:
                    return response["x_message_id"], 200
                else:
                    return response["body"], response["status_code"]
        except Exception as e:
            logger.exception(repr(e), extra=request_as_log_dict(request))
            return "error occurred", 400
