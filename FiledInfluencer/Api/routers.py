import logging

import flask_restful
from flask import request

from Core.flask_extensions import log_request
from FiledInfluencer.Api.request_handlers import InfluencerProfilesHandler
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
    def get(self):
        last_influencer_id = int(request.args.get("last_influencer_id", 0))
        page_size = int(request.args.get("page_size", 100))
        response = InfluencerProfilesHandler.get_profiles(
            last_influencer_id=last_influencer_id,
            page_size=page_size,
        )
        return response, 200
