import json
import typing

import humps
from flask import request, Response
from flask_restful import Resource, abort

from Core.logging_config import request_as_log_dict
from Core.Web.Misc import snake_to_camelcase
from Core.Web.Security.JWTTools import extract_business_owner_google_id
from Core.Web.Security.Permissions import AdsManagerPermissions, OptimizePermissions, ReportsPermissions
from GoogleTuring.Api.Commands.AdsManagerFilteredStructuresCommand import AdsManagerFilteredStructuresCommand
from GoogleTuring.Api.Commands.AdsManagerUpdateStructureCommand import AdsManagerUpdateStructureCommand
from GoogleTuring.Api.CommandsHandlers.AdsManagerDeleteStructureCommandHandler import \
    AdsManagerDeleteStructureCommandHandler
from GoogleTuring.Api.CommandsHandlers.AdsManagerFilteredStructuresCommandHandler import \
    AdsManagerFilteredStructuresCommandHandler
from GoogleTuring.Api.CommandsHandlers.AdsManagerUpdateStructureCommandHandler import \
    AdsManagerUpdateStructureCommandHandler
from GoogleTuring.Api.Mappings.AdsManagerFilteredStructuresCommandMapping import \
    AdsManagerFilteredStructuresCommandMapping
from GoogleTuring.Api.Mappings.AdsManagerUpdateStructureCommandMapping import AdsManagerUpdateStructureCommandMapping
from GoogleTuring.Api.Queries.AdsManagerGetStructuresQuery import AdsManagerGetStructuresQuery
from GoogleTuring.Api.Startup import startup
from GoogleTuring.Infrastructure.Domain.Structures.StructureType import StructureType


import logging

logger = logging.getLogger(__name__)


class AdsManagerEndpoint(Resource):
    @startup.authorize_permission(permission=AdsManagerPermissions.ADS_MANAGER_EDIT)
    def put(self, account_id, level, structure_id):
        try:
            business_owner_google_id = extract_business_owner_google_id()
            raw_request = request.get_json(force=True)
            mapping = AdsManagerUpdateStructureCommandMapping(target=AdsManagerUpdateStructureCommand)
            command = mapping.load(raw_request)
            AdsManagerUpdateStructureCommandHandler.handle(config=startup.google_config,
                                                           command=command,
                                                           account_id=account_id,
                                                           level=level,
                                                           structure_id=structure_id,
                                                           business_owner_google_id=business_owner_google_id)
        except Exception as e:
            abort(400, message=f"Could not process your request. Error: {str(e)}")

        return 204

    @startup.authorize_permission(permission=AdsManagerPermissions.ADS_MANAGER_DELETE)
    def delete(self, account_id, level, structure_id):
        try:
            level = StructureType.get_enum_by_value(level)
            business_owner_google_id = extract_business_owner_google_id()
            AdsManagerDeleteStructureCommandHandler.handle(config=startup.google_config,
                                                           account_id=account_id,
                                                           level=level,
                                                           structure_id=structure_id,
                                                           business_owner_google_id=business_owner_google_id)
        except Exception as e:
            abort(400, message=f"Could not process your request. Error: {str(e)}")

        return 204


class GetStructuresHandler:
    @staticmethod
    def handle(level, account_id):
        if level == 'adset':
            level = 'adgroup'

        logger.info(request_as_log_dict(request))
        try:
            response = AdsManagerGetStructuresQuery.get_structures(level, account_id)
            response = snake_to_camelcase(response)
            response = json.dumps(response)
            return Response(response=response, status=200, mimetype='application/json')
        except Exception as e:
            logger.exception(repr(e), extra=request_as_log_dict(request))
            return Response(response=json.dumps({"message": f"Could not retrieve {level} for {account_id}"}),
                            status=400, mimetype='application/json')


# TODO: keywords level should be renamed to keyword
class AdsManagerGetStructuresEndpoint(Resource):
    @startup.authorize_permission(permission=AdsManagerPermissions.ADS_MANAGER_CAN_ACCESS_REPORTS_DATA)
    def get(self, level, account_id):
        return GetStructuresHandler.handle(level, account_id)


class OptimizeGetStructuresEndpoint(Resource):
    @startup.authorize_permission(permission=OptimizePermissions.CAN_ACCESS_OPTIMIZE)
    def get(self, level, account_id):
        return GetStructuresHandler.handle(level, account_id)


class AdsManagerFilteredStructuresEndpoint(Resource):
    @startup.authorize_permission(permission=ReportsPermissions.FILTERED_STRUCTURES_PERMISSION)
    def post(self, level: typing.AnyStr = None):
        if level == 'adset':
            level = 'adgroup'
        logger.info(request_as_log_dict(request))
        try:
            raw_request = humps.decamelize(request.get_json(force=True))
            mapping = AdsManagerFilteredStructuresCommandMapping(target=AdsManagerFilteredStructuresCommand)
            command = mapping.load(raw_request)
        except Exception as e:
            logger.exception(repr(e), extra=request_as_log_dict(request))
            return Response(response=json.dumps({"message": str(e)}), status=400,
                            mimetype='application/json')

        try:
            response = AdsManagerFilteredStructuresCommandHandler.handle(level=level, command=command)
            if not response:
                return Response(response=json.dumps({'error_message': 'Structures not found!'}), status=404,
                                mimetype='application/json')

            response = humps.camelize(response)
            response = json.dumps(response)
            return Response(response=response, status=200, mimetype="application/json")
        except Exception as e:
            logger.exception(repr(e), extra=request_as_log_dict(request))
            error = str(e)
            return Response(response=json.dumps(error), status=400, mimetype='application/json')
