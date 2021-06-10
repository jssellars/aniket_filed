import logging
from typing import Any

import flask_restful
import humps
from flask import request

from Core.flask_extensions import log_request
from Core.logging_config import request_as_log_dict
from Core.Web.Security.JWTTools import decode_jwt_from_headers
from FiledInfluencer.Api.Integrations.mail_sendgrid import SendGridMailer
from FiledInfluencer.Api.request_handlers import DocumentHandler, EmailTemplateHandler, InfluencerProfilesHandler
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
    #  Todo : Use parser here.

    @staticmethod
    def extract_param_or_default(request, param_name: str, default: Any) -> Any:
        """
        Extract params from request

        If parameter is not present,
        or a value for parameter is not provided
        return default
        """
        try:
            response = request.args.get(param_name) or default
            if param_name == "get_total_count":
                response = response == "true"
            elif param_name == "is_verified":
                if param_name == "true":
                    response = True
                elif param_name == "false":
                    response = False
            elif param_name != "name":
                response = int(response)
        except (TypeError, ValueError) as _:
            response = default
        finally:
            return response

    @staticmethod
    def range_checker(max_value, min_value, param_name):
        """
        Check if max value is not less than min value while filtering
        """
        if max_value is None and min_value is not None:
            return {"Message": f"Please provide max_value for {param_name}"}, False
        if min_value is None and max_value is not None:
            return {"Message": f"Please provide min_value for {param_name}"}, False
        if max_value < min_value:
            return {"Message": f"{param_name} range is out of bounds"}, False
        else:
            return None, True

    def get(self):
        page_size = self.extract_param_or_default(request, "page_size", 100)
        last_influencer_id = self.extract_param_or_default(request, "last_influencer_id", 0)
        name = self.extract_param_or_default(request, "name", None)
        get_total_count = self.extract_param_or_default(request, "get_total_count", False)
        followers_min_count = self.extract_param_or_default(request, "followers_min_count", 0)
        followers_max_count = self.extract_param_or_default(request, "followers_max_count", 100000000)
        engagements_per_post_min_count = self.extract_param_or_default(request, "engagements_per_post_min_count", None)
        engagements_per_post_max_count = self.extract_param_or_default(request, "engagements_per_post_max_count", None)
        engagement_rate_min_count = self.extract_param_or_default(request, "engagement_rate_min_count", 0)
        engagement_rate_max_count = self.extract_param_or_default(request, "engagement_rate_max_count", 100)
        account_type = self.extract_param_or_default(request, "account_type", None)
        is_verified = self.extract_param_or_default(request, "is_verified", None)

        if followers_min_count > 0:
            msg, followers_check = self.range_checker(followers_max_count, followers_min_count, "Followers")
            if not followers_check:
                return msg, 400

        followers = {"min_count": followers_min_count, "max_count": followers_max_count}

        engagement_per_post = None
        if engagements_per_post_min_count is not None or engagements_per_post_max_count is not None:
            msg, post_engagement_check = self.range_checker(
                engagements_per_post_max_count, engagements_per_post_min_count, "Engagements Per Post"
            )

            if not post_engagement_check:
                return msg, 400

            engagement_per_post = {
                "min_count": engagements_per_post_min_count,
                "max_count": engagements_per_post_max_count,
            }

        if engagement_rate_min_count > 0:
            msg, engagement_rate_check = self.range_checker(
                engagement_rate_max_count, engagement_rate_min_count, "Engagement Rate"
            )
            if not engagement_rate_check:
                return msg, 400

        engagement_rate = {"min_count": engagement_rate_min_count, "max_count": engagement_rate_max_count}

        if is_verified == "both":
            is_verified = None

        response = InfluencerProfilesHandler.get_profiles(
            name=name,
            last_influencer_id=last_influencer_id,
            engagement_rate=engagement_rate,
            page_size=page_size,
            get_total_count=get_total_count,
            engagement_per_post=engagement_per_post,
            account_type=account_type,
            is_verified=is_verified,
            followers=followers,
        )
        return response, 200


class EmailTemplates(Resource):
    parser = EmailTemplateHandler.email_template_parser()

    def get(self, user_id):
        response = EmailTemplateHandler.get_email_templates(user_id)
        if response:
            return response, 200
        return {"Message": "Not Found"}, 400

    def post(self, user_id):
        data = EmailTemplates.parser.parse_args()
        data["created_by"] = user_id
        try:
            email_template = EmailTemplateHandler.write_to_db(data)
        except:
            return {"message": "An error occurred while inserting the item."}, 500

        return email_template, 200


class Documents(Resource):
    parser = DocumentHandler.document_parser()

    def post(self):
        request_data = Documents.parser.parse_args()

        size_in_limit = DocumentHandler.max_document_size(request_data["documents"][0])
        if not size_in_limit:
            return "File size limit exceeds the max size", 413

        result = DocumentHandler.upload_document(request_data)
        if not result:
            return result, 400

        return result, 200

    def get(self):
        key = request.args.get("key")

        result = DocumentHandler.download_document(key)
        if not result:
            return result, 400

        return result, 200

    def delete(self):
        key = request.args.get("key")

        result = DocumentHandler.delete_document(key)
        if not result:
            return result, 400

        return result, 200


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
