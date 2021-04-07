import logging

import flask_restful
import humps
from flask import request

import FacebookAccounts.Api.mappings
import GoogleAccounts.Api.mappings
from Core.flask_extensions import log_request
from Core.logging_config import request_as_log_dict
from Core.Web.Security.JWTTools import extract_business_owner_facebook_id
from Core.Web.Security.Permissions import (
    AccountsPermissions,
    CampaignBuilderPermissions,
    MiscellaneousPermissions,
    SettingsPermissions,
)
from GoogleAccounts.Api.command_handlers import GetAccountsTreeCommandHandler
from GoogleAccounts.Api.commands import GetAccountsCommand
from GoogleAccounts.Api.startup import config

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
