import logging

import flask_restful

from Core.flask_extensions import log_request
from FacebookCampaignsBuilder.BackgroundTasks.startup import config

logger = logging.getLogger(__name__)


class Resource(flask_restful.Resource):
    method_decorators = [log_request(logger)]


class HealthCheck(Resource):
    def get(self):
        return None, 200


class Version(Resource):
    def get(self):
        return config.version_endpoint_payload, 200
