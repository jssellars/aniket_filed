import json
import logging

import flask_restful
from flask import Response, jsonify, request

from Core.flask_extensions import log_request
from Core.logging_config import request_as_log_dict
from FiledEcommerce.Api.Dtos.ImportIntegrationMappingDto import ImportIntegrationMappingDto
from FiledEcommerce.Api.Dtos.ImportIntegrationModelDto import ImportIntegrationModelDto

logger = logging.getLogger(__name__)


class Resource(flask_restful.Resource):
    method_decorators = [log_request(logger)]


class ImportIntegrationModel(Resource):
    def get(self, platform):
        try:
            return ImportIntegrationModelDto.get(platform=platform), 200
        except Exception as e:
            logger.exception(repr(e), extra=request_as_log_dict(request))
            return {"message": "Failed to retrieve model."}, 400


class ImportIntegrationMapping(Resource):
    def get(self, platform):
        try:
            return ImportIntegrationMappingDto.get(platform=platform)
        except Exception as e:
            logger.exception(repr(e), extra=request_as_log_dict(request))
            return {"message": "Failed to retrieve mapping."}, 400


class OAuth(Resource):
    def get(self):
        pass
