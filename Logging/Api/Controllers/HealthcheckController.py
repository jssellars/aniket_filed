import json

from flask import request, Response
from flask_restful import Resource

from Core.Tools.Logger.LoggerAPIRequestMessageBase import LoggerAPIRequestMessageBase
from Logging.Api.Startup import logger, startup


class VersionEndpoint(Resource):
    def get(self):
        logger.logger.info(LoggerAPIRequestMessageBase(request).to_dict())
        response = {"api_name": startup.api_name,
                    "api_version": startup.api_version,
                    "service_name": startup.service_name,
                    "service_version": startup.service_version,
                    "environment": startup.environment}
        return Response(response=json.dumps(response), status=200, mimetype='application/json')


class HealthCheckEndpoint(Resource):
    def get(self):
        logger.logger.info(LoggerAPIRequestMessageBase(request).to_dict())
        return Response(status=200, mimetype='application/json')
