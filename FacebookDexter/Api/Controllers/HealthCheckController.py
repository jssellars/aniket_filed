import json

from flask import request, Response
from flask_restful import Resource

from Core.logging_legacy import request_as_log_dict_nested
from FacebookDexter.Api.Startup import logger, startup


class DexterApiHealthCheck(Resource):
    def get(self):
        logger.logger.info(request_as_log_dict_nested(request))
        return Response(status=200, mimetype='application/json')


class DexterApiVersion(Resource):
    def get(self):
        logger.logger.info(request_as_log_dict_nested(request))
        response = {"api_name": startup.api_name,
                    "api_version": startup.api_version,
                    "environment": startup.environment}
        return Response(response=json.dumps(response), status=200, mimetype='application/json')
