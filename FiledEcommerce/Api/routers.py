import logging

import flask_restful
import humps
from flask import redirect, request

from Core.flask_extensions import log_request
from Core.logging_config import request_as_log_dict
from FiledEcommerce.Api.Dtos.ImportIntegrationMappingDto import ImportIntegrationMappingDto
from FiledEcommerce.Api.Dtos.ImportIntegrationModelDto import ImportIntegrationModelDto
from FiledEcommerce.Api.ImportIntegration.interface.ImportIntegrationProvider import ImportIntegrationProvider
from FiledEcommerce.Api.services.reciever.main import receiver_lambda
from FiledEcommerce.Api.utils.tools.json_serializer import RequestSerializer

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
    def get(self, platform, action):
        store = ImportIntegrationProvider.get_instance(platform)
        if action == "preinstall":
            url = store.pre_install()
        elif action == "install":
            url = store.app_install()
        elif action == "load":
            url = store.app_load()
        elif action == "uninstall":
            url = store.app_uninstall()
        else:
            url = "Invalid action"  # Redirect to error page

        if action == "preinstall":
            return {"url": url}
        else:
            return redirect(url)

    def post(self, platform, action):
        return self.get(platform, action)


class Receiver(Resource):
    def post(self, platform):
        if platform == 'csv':
            json_data = RequestSerializer(event=request)
            request_json = json_data.get_body()
        else:
            request_json = humps.depascalize(request.get_json(force=True))
        try:
            response = receiver_lambda(request_json, platform)
        except Exception as e:
            logger.exception(repr(e), extra=request_as_log_dict(request))
            return {"message": "Failed to save products to db."}, 400
        else:
            return response, 200
