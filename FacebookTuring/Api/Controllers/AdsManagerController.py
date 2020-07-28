import json
import typing

import humps
from flask import request, Response
from flask_jwt_simple import jwt_required, get_jwt
from flask_restful import Resource

from Core.Tools.Logger.LoggerAPIRequestMessageBase import LoggerAPIRequestMessageBase
from Core.Tools.Logger.LoggerMessageBase import LoggerMessageBase, LoggerMessageTypeEnum
from Core.Web.FacebookGraphAPI.Tools import Tools
from Core.Web.Misc import snake_to_camelcase
from Core.Web.Security.JWTTools import extract_business_owner_facebook_id
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
from FacebookTuring.Api.Startup import logger
from FacebookTuring.Infrastructure.Mappings.LevelMapping import Level


class AdsManagerCampaignTreeStructureEndpoint(Resource):

    @jwt_required
    def get(self, level, facebook_id):
        logger.logger.info(LoggerAPIRequestMessageBase(request).to_dict())
        try:
            response = AdsManagerCampaignTreeStructureQuery.get(level, facebook_id)
            response = humps.camelize(response)
            response = json.dumps(response)
            return Response(response=response, status=200, mimetype='application/json')
        except Exception as e:
            log = LoggerMessageBase(mtype=LoggerMessageTypeEnum.ERROR,
                                    name="AdsManagerCampaignTreeStructureEndpoint",
                                    description=str(e),
                                    extra_data=LoggerAPIRequestMessageBase(request).request_details)
            logger.logger.exception(log.to_dict())
            return Response(response=json.dumps({"message": f"Could not retrieve tree for {facebook_id}"}), status=400,
                            mimetype='application/json')


class AdsManagerGetCampaignsEndpoint(Resource):

    @jwt_required
    def get(self, account_id):
        logger.logger.info(LoggerAPIRequestMessageBase(request).to_dict())
        level = Level.CAMPAIGN.value
        try:
            response = AdsManagerGetStructuresQuery.get_structures(level, account_id)
            response = snake_to_camelcase(response)
            response = json.dumps(response)
            return Response(response=response, status=200, mimetype='application/json')
        except Exception as e:
            log = LoggerMessageBase(mtype=LoggerMessageTypeEnum.ERROR,
                                    name="AdsManagerGetCampaignsEndpoint",
                                    description=str(e),
                                    extra_data=LoggerAPIRequestMessageBase(request).request_details)
            logger.logger.exception(log.to_dict())
            return Response(response=json.dumps({"message": f"Could not retrieve {level} for {account_id}"}),
                            status=400, mimetype='application/json')


class AdsManagerGetAdSetsEndpoint(Resource):

    @jwt_required
    def get(self, account_id):
        logger.logger.info(LoggerAPIRequestMessageBase(request).to_dict())
        level = Level.ADSET.value
        try:
            response = AdsManagerGetStructuresQuery.get_structures(level, account_id)
            response = snake_to_camelcase(response)
            response = json.dumps(response)
            return Response(response=response, status=200, mimetype='application/json')
        except Exception as e:
            log = LoggerMessageBase(mtype=LoggerMessageTypeEnum.ERROR,
                                    name="AdsManagerGetAdSetsEndpoint",
                                    description=str(e),
                                    extra_data=LoggerAPIRequestMessageBase(request).request_details)
            logger.logger.exception(log.to_dict())
            return Response(response=json.dumps({"message": f"Could not retrieve {level} for {account_id}"}),
                            status=400, mimetype='application/json')


class AdsManagerGetAdsEndpoint(Resource):

    @jwt_required
    def get(self, account_id):
        logger.logger.info(LoggerAPIRequestMessageBase(request).to_dict())
        level = Level.AD.value
        try:
            response = AdsManagerGetStructuresQuery.get_structures(level, account_id)
            response = snake_to_camelcase(response)
            response = json.dumps(response)
            return Response(response=response, status=200, mimetype='application/json')
        except Exception as e:
            log = LoggerMessageBase(mtype=LoggerMessageTypeEnum.ERROR,
                                    name="AdsManagerGetAdsEndpoint",
                                    description=str(e),
                                    extra_data=LoggerAPIRequestMessageBase(request).request_details)
            logger.logger.exception(log.to_dict())
            return Response(response=json.dumps({"message": f"Could not retrieve {level} for {account_id}"}),
                            status=400, mimetype='application/json')


class AdsManagerFilteredStructuresEndpoint(Resource):

    @jwt_required
    def post(self, level: typing.AnyStr = None):
        logger.logger.info(LoggerAPIRequestMessageBase(request).to_dict())
        try:
            raw_request = humps.decamelize(request.get_json(force=True))
            mapping = AdsManagerFilteredStructuresCommandMapping(target=AdsManagerFilteredStructuresCommand)
            command = mapping.load(raw_request)
        except Exception as e:
            log = LoggerMessageBase(mtype=LoggerMessageTypeEnum.ERROR,
                                    name="AdsManagerFilteredStructuresEndpoint",
                                    description=str(e),
                                    extra_data=LoggerAPIRequestMessageBase(request).request_details)
            logger.logger.exception(log.to_dict())
            return Response(response=json.dumps({"message": str(e)}), status=400,
                            mimetype='application/json')

        try:
            response = AdsManagerFilteredStructuresCommandHandler.handle(level=level, command=command)
            if not response:
                return Response(response=json.dumps({'error_message': 'Structures not found!'}), status=404,
                                mimetype='application/json')

            response = snake_to_camelcase(response)
            response = json.dumps(response)
            return Response(response=response, status=200, mimetype="application/json")
        except Exception as e:
            log = LoggerMessageBase(mtype=LoggerMessageTypeEnum.ERROR,
                                    name="AdsManagerFilteredStructuresEndpoint",
                                    description=str(e),
                                    extra_data=LoggerAPIRequestMessageBase(request).request_details)
            logger.logger.exception(log.to_dict())
            error = Tools.create_error(e)
            return Response(response=json.dumps(error), status=400, mimetype='application/json')


class AdsManagerEndpoint(Resource):

    @jwt_required
    def get(self, level, facebook_id):
        logger.logger.info(LoggerAPIRequestMessageBase(request).to_dict())
        try:
            response = AdsManagerGetStructuresQuery.get_structure_details(level, facebook_id)
            response = snake_to_camelcase(response)
            response = json.dumps(response)
            return Response(response=response, status=200, mimetype='application/json')
        except Exception as e:
            log = LoggerMessageBase(mtype=LoggerMessageTypeEnum.ERROR,
                                    name="AdsManagerEndpoint",
                                    description=str(e),
                                    extra_data=LoggerAPIRequestMessageBase(request).request_details)
            logger.logger.exception(log.to_dict())
            return Response(response=json.dumps({"message": f"Could not retrieve {level} for {facebook_id}"}),
                            status=400, mimetype='application/json')

    @jwt_required
    def put(self, level, facebook_id):
        logger.logger.info(LoggerAPIRequestMessageBase(request).to_dict())
        try:
            raw_request = humps.decamelize(request.get_json(force=True))
            mapping = AdsManagerUpdateStructureCommandMapping(target=AdsManagerUpdateStructureCommand)
            command = mapping.load(raw_request)
            business_owner_facebook_id = extract_business_owner_facebook_id(get_jwt())
        except Exception as e:
            log = LoggerMessageBase(mtype=LoggerMessageTypeEnum.ERROR,
                                    name="AdsManagerEndpoint",
                                    description=str(e),
                                    extra_data=LoggerAPIRequestMessageBase(request).request_details)
            logger.logger.exception(log.to_dict())
            return Response(response=json.dumps({"message": "Failed to process request."}), status=400,
                            mimetype='application/json')

        try:
            AdsManagerUpdateStructureCommandHandler.handle(command=command,
                                                           level=level,
                                                           facebook_id=facebook_id,
                                                           business_owner_facebook_id=business_owner_facebook_id)
            return Response(status=200, mimetype="application/json")
        except Exception as e:
            log = LoggerMessageBase(mtype=LoggerMessageTypeEnum.ERROR,
                                    name="AdsManagerEndpoint",
                                    description=str(e),
                                    extra_data=LoggerAPIRequestMessageBase(request).request_details)
            logger.logger.exception(log.to_dict())
            error = Tools.create_error(e)
            return Response(response=json.dumps(error), status=400,
                            mimetype='application/json')

    @jwt_required
    def delete(self, level, facebook_id):
        logger.logger.info(LoggerAPIRequestMessageBase(request).to_dict())
        business_owner_facebook_id = extract_business_owner_facebook_id(get_jwt())
        try:
            response = AdsManagerDeleteStructureCommandHandler.handle(level, facebook_id, business_owner_facebook_id)
            if response:
                return Response(status=204, mimetype="application/json")
            else:
                return Response(response=json.dumps({"message": f"Missing structure {facebook_id}."}), status=404,
                                mimetype='application/json')
        except Exception as e:
            log = LoggerMessageBase(mtype=LoggerMessageTypeEnum.ERROR,
                                    name="AdsManagerEndpoint",
                                    description=str(e),
                                    extra_data=LoggerAPIRequestMessageBase(request).request_details)
            logger.logger.exception(log.to_dict())
            return Response(response=json.dumps({"message": f"Failed to delete structure {facebook_id}."}), status=400,
                            mimetype='application/json')


class AdsManagerUpdateStructureDraftEndpoint(Resource):

    @jwt_required
    def put(self, level, facebook_id):
        logger.logger.info(LoggerAPIRequestMessageBase(request).to_dict())
        try:
            raw_request = humps.decamelize(request.get_json(force=True))
            mapping = AdsManagerSaveDraftCommandMapping(target=AdsManagerSaveDraftCommand)
            command = mapping.load(raw_request)
        except Exception as e:
            log = LoggerMessageBase(mtype=LoggerMessageTypeEnum.ERROR,
                                    name="AdsManagerUpdateStructureDraftEndpoint",
                                    description=str(e),
                                    extra_data=LoggerAPIRequestMessageBase(request).request_details)
            logger.logger.exception(log.to_dict())
            return Response(response=json.dumps({"message": "Failed to process request."}), status=400,
                            mimetype='application/json')

        try:
            AdsManagerSaveDraftCommandHandler.handle(command, level, facebook_id)
            return Response(status=204, mimetype="application/json")
        except Exception as e:
            log = LoggerMessageBase(mtype=LoggerMessageTypeEnum.ERROR,
                                    name="AdsManagerUpdateStructureDraftEndpoint",
                                    description=str(e),
                                    extra_data=LoggerAPIRequestMessageBase(request).request_details)
            logger.logger.exception(log.to_dict())
            return Response(response=json.dumps({"message": f"Failed to save draft for {facebook_id}."}), status=400,
                            mimetype='application/json')

    @jwt_required
    def delete(self, level, facebook_id):
        logger.logger.info(LoggerAPIRequestMessageBase(request).to_dict())
        try:
            AdsManagerDiscardDraftCommandHandler.handle(level, facebook_id)
            return Response(status=204, mimetype="application/json")
        except Exception as e:
            log = LoggerMessageBase(mtype=LoggerMessageTypeEnum.ERROR,
                                    name="AdsManagerUpdateStructureDraftEndpoint",
                                    description=str(e),
                                    extra_data=LoggerAPIRequestMessageBase(request).request_details)
            logger.logger.exception(log.to_dict())
            return Response(response=json.dumps({"message": f"Failed to delete draft for {facebook_id}."}), status=400,
                            mimetype='application/json')


class AdsManagerDuplicateStructureEndpoint(Resource):

    @jwt_required
    def post(self, level, facebook_id):
        logger.logger.info(LoggerAPIRequestMessageBase(request).to_dict())
        try:
            raw_request = humps.decamelize(request.get_json(force=True))
            mapping = AdsManagerDuplicateStructureCommandMapping(target=AdsManagerDuplicateStructureCommand)
            command = mapping.load(raw_request)
            business_owner_facebook_id = extract_business_owner_facebook_id(get_jwt())
        except Exception as e:
            log = LoggerMessageBase(mtype=LoggerMessageTypeEnum.ERROR,
                                    name="AdsManagerDuplicateStructureEndpoint",
                                    description=str(e),
                                    extra_data=LoggerAPIRequestMessageBase(request).request_details)
            logger.logger.exception(log.to_dict())
            return Response(response=json.dumps({"message": "Failed to process request."}), status=400,
                            mimetype='application/json')
        try:
            command_handler = AdsManagerDuplicateStructureCommandHandler()
            command_handler.handle(command, level, facebook_id, business_owner_facebook_id)
            return Response(status=204, mimetype="application/json")
        except AdsManagerDuplicateStructureCommandHandlerException as ex:
            log = LoggerMessageBase(mtype=LoggerMessageTypeEnum.ERROR,
                                    name="AdsManagerUpdateStructureDraftEndpoint",
                                    description=str(ex),
                                    extra_data=LoggerAPIRequestMessageBase(request).request_details)
            logger.logger.exception(log.to_dict())
            return Response(response=json.dumps({"message": f"Could not find structure {facebook_id} tree."}),
                            status=404, mimetype='application/json')
        except Exception as e:
            log = LoggerMessageBase(mtype=LoggerMessageTypeEnum.ERROR,
                                    name="AdsManagerUpdateStructureDraftEndpoint",
                                    description=str(e),
                                    extra_data=LoggerAPIRequestMessageBase(request).request_details)
            logger.logger.exception(log.to_dict())
            return Response(response=json.dumps({"message": f"Failed to duplicate structure {facebook_id}."}),
                            status=400, mimetype='application/json')
