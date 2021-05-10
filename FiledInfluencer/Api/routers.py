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
        influencer_id = request.args.get("influencer_id")
        response = InfluencerProfilesHandler.get_profiles(
            influencer_id=influencer_id,
        )
        return response, 200
