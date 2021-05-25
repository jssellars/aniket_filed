import logging
from typing import Any

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
            if param_name == 'get_total_count':
                response = response == 'true'
            elif param_name != 'name':
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
            return {'Message': f'Please provide max_value for {param_name}'}, False
        if min_value is None and max_value is not None:
            return {'Message': f'Please provide min_value for {param_name}'}, False
        if max_value < min_value:
            return {'Message': f'{param_name} range is out of bounds'}, False
        else:
            return None, True

    def get(self):
        page_size = self.extract_param_or_default(request, "page_size", 100)
        last_influencer_id = self.extract_param_or_default(request, "last_influencer_id", 0)
        name = self.extract_param_or_default(request, "name", None)
        get_total_count = self.extract_param_or_default(request, "get_total_count", False)
        engagement_min_count = self.extract_param_or_default(request, "followers_min_count", 0)
        engagement_max_count = self.extract_param_or_default(request, "followers_max_count", 100000000)
        post_engagement_min_count = self.extract_param_or_default(request, "engagements_min_count", None)
        #  Todo: define default Max value for engagements
        post_engagement_max_count = self.extract_param_or_default(request, "engagements_max_count", None)

        if engagement_min_count > 0:
            msg, engagement_check = self.range_checker(engagement_max_count, engagement_min_count, "Followers")
            if not engagement_check:
                return msg, 400

        post_engagement = None
        if post_engagement_min_count is not None or post_engagement_max_count is not None:
            msg, post_engagement_check = self.range_checker(post_engagement_max_count, post_engagement_min_count, "Engagements")

            if not post_engagement_check:
                return msg, 400

            post_engagement = {
                'min_count': post_engagement_min_count,
                'max_count': post_engagement_max_count
            }

        engagement = {
            'min_count': engagement_min_count,
            'max_count': engagement_max_count
        }

        response = InfluencerProfilesHandler.get_profiles(
            name=name,
            engagement=engagement,
            last_influencer_id=last_influencer_id,
            page_size=page_size,
            get_total_count=get_total_count,
            post_engagement=post_engagement,
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
