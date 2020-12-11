import json

from flask import Response
from flask_restful import Resource

from GoogleTuring.Api.startup import config, fixtures


class VersionEndpoint(Resource):
    def get(self):
        response = {"app_name": config.name, "app_version": config.version, "environment": config.environment}
        return Response(response=json.dumps(response), status=200, mimetype='application/json')


class HealthCheckEndpoint(Resource):
    def get(self):
        return Response(status=200, mimetype='application/json')
