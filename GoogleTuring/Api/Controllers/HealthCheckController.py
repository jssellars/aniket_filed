import json

from flask import Response
from flask_restful import Resource

from GoogleTuring.Api.Startup import startup


class VersionEndpoint(Resource):
    def get(self):
        response = {"api_name": startup.api_name,
                    "api_version": startup.api_version,
                    "service_name": startup.service_name,
                    "service_version": startup.service_version,
                    "environment": startup.environment}
        return Response(response=json.dumps(response), status=200, mimetype='application/json')


class HealthCheckEndpoint(Resource):
    def get(self):
        return Response(status=200, mimetype='application/json')
