import logging

import flask_restful
import humps
from flask import request

import GoogleAccounts.Api.mappings
from Core.flask_extensions import log_request
from Core.logging_config import request_as_log_dict
from GoogleAccounts.Api import dtos
from GoogleAccounts.Api.command_handlers import GetAccountsTreeCommandHandler
from GoogleAccounts.Api.commands import AdAccountInsightsCommand, GetAccountsCommand
from GoogleAccounts.Api.startup import config
from GoogleAccounts.CommandsHandlers.AdAccountInsightsCommandHandler import AdAccountInsightsCommandHandler

logger = logging.getLogger(__name__)


class Resource(flask_restful.Resource):
    method_decorators = [log_request(logger)]


class HealthCheck(Resource):
    def get(self):
        return None, 200


class Version(Resource):
    def get(self):
        return config.version_endpoint_payload, 200


class GetAccountsTree(Resource):
    def post(self):
        try:
            raw_request = humps.decamelize(request.get_json(force=True))
            mapping = GoogleAccounts.Api.mappings.GetAccountsCommandMapping(GetAccountsCommand)
            command = mapping.load(raw_request)
        except Exception as e:
            logger.exception(repr(e), extra=request_as_log_dict(request))

            return {"message": f"Failed to process request. Error {repr(e)}"}, 400

        try:
            response = GetAccountsTreeCommandHandler.handle(command)
            return response, 200

        except Exception as e:
            logger.exception(repr(e), extra=request_as_log_dict(request))

            return {"message": f"Failed to get account tree. Error {repr(e)}"}, 400


class AdAccountsView(Resource):
    def get(self):
        try:
            response = dtos.get_view()
            response = humps.camelize(response)

            return response, 200

        except Exception as e:
            logger.exception(repr(e), extra=request_as_log_dict(request))

            return {"message": "Failed to retrieve ag grid views on Accounts."}, 400


class AdAccountInsights(Resource):
    def post(self, manager_id):
        try:
            raw_request = humps.decamelize(request.get_json(force=True))
            mapping = GoogleAccounts.Api.mappings.AdAccountInsightsCommandMapping(AdAccountInsightsCommand)
            command = mapping.load(raw_request)
        except Exception as e:
            logger.exception(repr(e), extra=request_as_log_dict(request))

            return {"message": f"Failed to process request. Error {repr(e)}"}, 400

        try:
            response = AdAccountInsightsCommandHandler.handle(config.google, command, manager_id)
            return response, 200

        except Exception as e:
            logger.exception(repr(e), extra=request_as_log_dict(request))

            return {"message": f"Failed to get account tree. Error {repr(e)}"}, 400
