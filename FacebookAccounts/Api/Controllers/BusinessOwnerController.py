import json
import typing

import humps
from flask import request, Response
from flask_restful import Resource

from Core.logging_config import request_as_log_dict
from Core.Web.Security.JWTTools import extract_business_owner_facebook_id
from Core.Web.Security.Permissions import MiscellaneousPermissions, SettingsPermissions
from FacebookAccounts.Api.Commands.BusinessOwnerCommands import BusinessOwnerCreateCommand
from FacebookAccounts.Api.CommandsHandlers.BusinessOwnerCommandHandler import BusinessOwnerCreateCommandHandler
from FacebookAccounts.Api.CommandsHandlers.BusinessOwnerDeletePermissionsCommandHandler import \
    BusinessOwnerDeletePermissionsCommandHandler
from FacebookAccounts.Api.Mappings import BusinessOwnerCommandsMappings
from FacebookAccounts.Api.startup import config, fixtures


import logging

logger = logging.getLogger(__name__)


class BusinessOwnerEndpoint(Resource):
    @fixtures.authorize_permission(permission=MiscellaneousPermissions.MISCELLANEOUS_FACEBOOK_ACCESS)
    def post(self):
        # log request information
        logger.info(request_as_log_dict(request))
        try:
            raw_request = humps.decamelize(request.get_json(force=True))
            mapping = BusinessOwnerCommandsMappings.BusinessOwnerCreateCommandMapping(BusinessOwnerCreateCommand)
            command = mapping.load(raw_request)
        except Exception as e:
            logger.exception(repr(e), extra=request_as_log_dict(request))
            response = json.dumps({"message": f"Failed to process request. Error {str(e)}"})
            return Response(response=response, status=400, mimetype='application/json')

        # generate and store permanent token
        try:
            BusinessOwnerCreateCommandHandler.handle(command)
            return Response(status=200, mimetype='application/json')
        except Exception as e:
            logger.exception(repr(e), extra=request_as_log_dict(request))
            response = json.dumps({"message": f"Failed to add new business owner. Error {str(e)}"})
            return Response(response=response, status=400, mimetype='application/json')


class BusinessOwnerDeletePermissionsEndpoint(Resource):
    @fixtures.authorize_permission(permission=SettingsPermissions.SETTINGS_MANAGE_PERMISSIONS_EDIT)
    def delete(self, permissions: typing.List[typing.AnyStr] = None):
        # log request information
        logger.info(request_as_log_dict(request))

        try:
            business_owner_facebook_id = extract_business_owner_facebook_id()

            response = BusinessOwnerDeletePermissionsCommandHandler.handle(business_owner_facebook_id, permissions)
            response = humps.camelize(response)
            response = json.dumps(response)
            return Response(response=response, status=200, mimetype='application/json')
        except Exception as e:
            logger.exception(repr(e), extra=request_as_log_dict(request))

            response = json.dumps({"message": f"Failed to delete permissions. Error {str(e)}"})
            return Response(response=response, status=400, mimetype='application/json')
