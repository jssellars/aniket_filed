import json
import typing

import humps
from flask import request, Response
from flask_restful import Resource

from Core.logging_config import request_as_log_dict
from Core.Web.FacebookGraphAPI.Tools import Tools
from Core.Web.Misc import snake_to_camelcase
from Core.Web.Security.JWTTools import extract_business_owner_facebook_id
from Core.Web.Security.Permissions import AdsManagerPermissions, OptimizePermissions, ReportsPermissions
from FacebookTuring.Api.Commands.AdsManagerDuplicateStructureCommand import AdsManagerDuplicateStructureCommand
from FacebookTuring.Api.Commands.AdsManagerFilteredStructuresCommand import AdsManagerFilteredStructuresCommand
from FacebookTuring.Api.Commands.AdsManagerSaveDraftCommand import AdsManagerSaveDraftCommand
from FacebookTuring.Api.Commands.AdsManagerUpdateStructureCommand import AdsManagerUpdateStructureCommand
from FacebookTuring.Api.CommandsHandlers.AdsManagerDeleteStructureCommandHandler import \
    AdsManagerDeleteStructureCommandHandler
from FacebookTuring.Api.CommandsHandlers.AdsManagerDiscardDraftCommandHandler import \
    AdsManagerDiscardDraftCommandHandler
from FacebookTuring.Api.CommandsHandlers.AdsManagerDuplicateStructureCommandHandler import \
    AdsManagerDuplicateStructureCommandHandler, AdsManagerDuplicateStructureCommandHandlerException
from FacebookTuring.Api.CommandsHandlers.AdsManagerFilteredStructuresCommandHandler import \
    AdsManagerFilteredStructuresCommandHandler
from FacebookTuring.Api.CommandsHandlers.AdsManagerSaveDraftCommandHandler import AdsManagerSaveDraftCommandHandler
from FacebookTuring.Api.CommandsHandlers.AdsManagerUpdateStructureCommandHandler import \
    AdsManagerUpdateStructureCommandHandler
from FacebookTuring.Api.Mappings.AdsManagerDuplicateStructureCommandMapping import \
    AdsManagerDuplicateStructureCommandMapping
from FacebookTuring.Api.Mappings.AdsManagerFilteredStructuresCommandMapping import \
    AdsManagerFilteredStructuresCommandMapping
from FacebookTuring.Api.Mappings.AdsManagerSaveDraftCommandMapping import AdsManagerSaveDraftCommandMapping
from FacebookTuring.Api.Mappings.AdsManagerUpdateStructureCommandMapping import AdsManagerUpdateStructureCommandMapping
from FacebookTuring.Api.Queries.AdsManagerCampaignTreeStructureQuery import AdsManagerCampaignTreeStructureQuery
from FacebookTuring.Api.Queries.AdsManagerGetStructuresQuery import AdsManagerGetStructuresQuery
from FacebookTuring.Api.Startup import startup


import logging

logger = logging.getLogger(__name__)


class AdsManagerCampaignTreeStructureEndpoint(Resource):
    @startup.authorize_permission(permission=AdsManagerPermissions.ADS_MANAGER_EDIT)
    def get(self, level, facebook_id):
        logger.info(request_as_log_dict(request))
        try:
            response = AdsManagerCampaignTreeStructureQuery.get(level, facebook_id)
            response = humps.camelize(response)
            response = json.dumps(response)
            return Response(response=response, status=200, mimetype='application/json')
        except Exception as e:
            logger.exception(repr(e), extra=request_as_log_dict(request))
            return Response(response=json.dumps({"message": f"Could not retrieve tree for {facebook_id}"}), status=400,
                            mimetype='application/json')


class GetStructuresHandler:
    @staticmethod
    def handle(level, account_id):
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
        logger.info(request_as_log_dict(request))
        try:
            raw_request = humps.decamelize(request.get_json(force=True))
            mapping = AdsManagerFilteredStructuresCommandMapping(target=AdsManagerFilteredStructuresCommand)
            command = mapping.load(raw_request)
        except Exception as e:
            logger.exception(repr(e), extra=request_as_log_dict(request))
            return Response(response=json.dumps({"message": str(e)}), status=400, mimetype='application/json')

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
            error = Tools.create_error(e)
            return Response(response=json.dumps(error), status=400, mimetype='application/json')


class AdsManagerEndpoint(Resource):
    @startup.authorize_permission(permission=AdsManagerPermissions.ADS_MANAGER_EDIT)
    def get(self, level, facebook_id):
        logger.info(request_as_log_dict(request))
        try:
            response = AdsManagerGetStructuresQuery.get_structure_details(level, facebook_id)
            response = snake_to_camelcase(response)
            response = json.dumps(response)
            return Response(response=response, status=200, mimetype='application/json')
        except Exception as e:
            logger.exception(repr(e), extra=request_as_log_dict(request))
            return Response(response=json.dumps({"message": f"Could not retrieve {level} for {facebook_id}"}),
                            status=400, mimetype='application/json')

    @startup.authorize_permission(permission=AdsManagerPermissions.ADS_MANAGER_EDIT)
    def put(self, level, facebook_id):
        logger.info(request_as_log_dict(request))
        try:
            raw_request = humps.decamelize(request.get_json(force=True))
            mapping = AdsManagerUpdateStructureCommandMapping(target=AdsManagerUpdateStructureCommand)
            command = mapping.load(raw_request)
            business_owner_facebook_id = extract_business_owner_facebook_id()
        except Exception as e:
            logger.exception(repr(e), extra=request_as_log_dict(request))
            return Response(response=json.dumps({"message": "Failed to process request."}), status=400,
                            mimetype='application/json')

        try:
            response = AdsManagerUpdateStructureCommandHandler.handle(
                command=command,
                level=level,
                facebook_id=facebook_id,
                business_owner_facebook_id=business_owner_facebook_id
            )
            # TODO: this will be returned once FE finishes their side as well to avoid crashes
            response = json.dumps(response)
            return Response(status=200, mimetype="application/json")

        except Exception as e:
            logger.exception(repr(e), extra=request_as_log_dict(request))
            error = Tools.create_error(e)
            return Response(response=json.dumps(error), status=400,
                            mimetype='application/json')

    @startup.authorize_permission(permission=AdsManagerPermissions.ADS_MANAGER_DELETE)
    def delete(self, level, facebook_id):
        logger.info(request_as_log_dict(request))
        business_owner_facebook_id = extract_business_owner_facebook_id()
        try:
            response = AdsManagerDeleteStructureCommandHandler.handle(level, facebook_id, business_owner_facebook_id)
            if response:
                return Response(status=204, mimetype="application/json")
            else:
                return Response(response=json.dumps({"message": f"Missing structure {facebook_id}."}), status=404,
                                mimetype='application/json')
        except Exception as e:
            logger.exception(repr(e), extra=request_as_log_dict(request))
            return Response(response=json.dumps({"message": f"Failed to delete structure {facebook_id}."}), status=400,
                            mimetype='application/json')


class AdsManagerUpdateStructureDraftEndpoint(Resource):
    @startup.authorize_permission(permission=AdsManagerPermissions.ADS_MANAGER_EDIT)
    def put(self, level, facebook_id):
        logger.info(request_as_log_dict(request))
        try:
            raw_request = humps.decamelize(request.get_json(force=True))
            mapping = AdsManagerSaveDraftCommandMapping(target=AdsManagerSaveDraftCommand)
            command = mapping.load(raw_request)
        except Exception as e:
            logger.exception(repr(e), extra=request_as_log_dict(request))
            return Response(response=json.dumps({"message": "Failed to process request."}), status=400,
                            mimetype='application/json')

        try:
            AdsManagerSaveDraftCommandHandler.handle(command, level, facebook_id)
            return Response(status=204, mimetype="application/json")
        except Exception as e:
            logger.exception(repr(e), extra=request_as_log_dict(request))
            return Response(response=json.dumps({"message": f"Failed to save draft for {facebook_id}."}), status=400,
                            mimetype='application/json')

    @startup.authorize_permission(permission=AdsManagerPermissions.ADS_MANAGER_EDIT)
    def delete(self, level, facebook_id):
        logger.info(request_as_log_dict(request))
        try:
            AdsManagerDiscardDraftCommandHandler.handle(level, facebook_id)
            return Response(status=204, mimetype="application/json")
        except Exception as e:
            logger.exception(repr(e), extra=request_as_log_dict(request))
            return Response(response=json.dumps({"message": f"Failed to delete draft for {facebook_id}."}), status=400,
                            mimetype='application/json')


class AdsManagerDuplicateStructureEndpoint(Resource):
    @startup.authorize_permission(permission=AdsManagerPermissions.ADS_MANAGER_EDIT)
    def post(self, level, facebook_id):
        logger.info(request_as_log_dict(request))
        try:
            raw_request = humps.decamelize(request.get_json(force=True))
            mapping = AdsManagerDuplicateStructureCommandMapping(target=AdsManagerDuplicateStructureCommand)
            command = mapping.load(raw_request)
            business_owner_facebook_id = extract_business_owner_facebook_id()
        except Exception as e:
            logger.exception(repr(e), extra=request_as_log_dict(request))
            return Response(response=json.dumps({"message": "Failed to process request."}), status=400,
                            mimetype='application/json')
        try:
            command_handler = AdsManagerDuplicateStructureCommandHandler()
            command_handler.handle(command, level, facebook_id, business_owner_facebook_id)
            return Response(status=204, mimetype="application/json")
        except AdsManagerDuplicateStructureCommandHandlerException as e:
            logger.exception(repr(e), extra=request_as_log_dict(request))
            return Response(response=json.dumps({"message": f"Could not find structure {facebook_id} tree."}),
                            status=404, mimetype='application/json')
        except Exception as e:
            logger.exception(repr(e), extra=request_as_log_dict(request))
            return Response(response=json.dumps({"message": f"Failed to duplicate structure {facebook_id}."}),
                            status=400, mimetype='application/json')
