import json

from flask import request, Response
from flask_restful import Resource

from Core.logging_config import request_as_log_dict
from FacebookPixels.Api.startup import config, fixtures

import logging

logger = logging.getLogger(__name__)


class VersionEndpoint(Resource):

    def get(self):
        logger.info(request_as_log_dict(request))
        response = {"app_name": config.name, "app_version": config.version, "environment": config.environment}
        response = json.dumps(response)
        return Response(response=response, status=200, mimetype='application/json')


class HealthCheckEndpoint(Resource):
    def get(self):
        logger.info(request_as_log_dict(request))
        return Response(status=200, mimetype='application/json')
