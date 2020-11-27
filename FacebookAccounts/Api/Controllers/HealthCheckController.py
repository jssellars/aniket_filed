import json

from flask import request, Response
from flask_restful import Resource

from Core.logging_legacy import request_as_log_dict_nested
from FacebookAccounts.Api.Startup import startup


import logging

logger = logging.getLogger(__name__)


class VersionEndpoint(Resource):
    def get(self):
        logger.info(request_as_log_dict_nested(request))

        response = {"api_name": startup.api_name,
                    "api_version": startup.api_version,
                    "service_name": startup.service_name,
                    "service_version": startup.service_version,
                    "environment": startup.environment}
        response = json.dumps(response)
        return Response(response=response, status=200, mimetype='application/json')


class HealthCheckEndpoint(Resource):
    def get(self):
        logger.info(request_as_log_dict_nested(request))
        return Response(status=200, mimetype='application/json')
