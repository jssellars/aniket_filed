import logging

import flask_restful
from flask_restful import reqparse, inputs
from flask import request

from Core.flask_extensions import log_request
from FiledInfluencer.Api.request_handlers import InfluencerProfilesHandler, EmailTemplateHandler
from FiledInfluencer.Api.startup import config

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
    @staticmethod
    def extract_param_or_default(request, param_name: str, default: int) -> int:
        """
        Extract params from request

        If parameter is not present,
        or a value for parameter is not provided
        return default
        """
        try:
            response = request.args.get(param_name) or default
            response = int(response)
        except (TypeError, ValueError) as _:
            response = default
        finally:
            return response

    def get(self):
        last_influencer_id = self.extract_param_or_default(request, "last_influencer_id", 0)
        page_size = self.extract_param_or_default(request, "page_size", 100)
        response = InfluencerProfilesHandler.get_profiles(
            last_influencer_id=last_influencer_id,
            page_size=page_size,
        )
        return response, 200


class EmailTemplates(Resource):
    parser = EmailTemplateHandler.email_template_parser()

    def get(self, user_id):
        response = EmailTemplateHandler.get_email_templates(user_id)
        if response:
            return response, 200
        return {'Message': 'Not Found'}, 400

    def post(self, user_id):
        data = EmailTemplates.parser.parse_args()
        data["created_by"] = user_id
        try:
            email_template = EmailTemplateHandler.write_to_db(data)
        except:
            return {"message": "An error occurred while inserting the item."}, 500

        return email_template, 200
