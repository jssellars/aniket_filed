import json
import typing

import humps
from flask import request, Response
from flask_jwt_simple import jwt_required, get_jwt
from flask_restful import Resource, abort

from Core.Tools.Logger.LoggerAPIRequestMessageBase import LoggerAPIRequestMessageBase
from Core.Tools.Logger.LoggerMessageBase import LoggerMessageBase, LoggerMessageTypeEnum
from Core.Web.Misc import snake_to_camelcase
from Core.Web.Security.JWTTools import extract_business_owner_google_id
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
from GoogleTuring.Api.Startup import logger, startup
from GoogleTuring.Infrastructure.Domain.Enums.Level import Level
from GoogleTuring.Infrastructure.Domain.Structures.StructureType import StructureType


class AdsManagerEndpoint(Resource):
    @jwt_required
    def put(self, account_id, level, structure_id):
        try:
            business_owner_google_id = extract_business_owner_google_id(get_jwt())
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

    @jwt_required
    def delete(self, account_id, level, structure_id):
        try:
            level = StructureType.get_enum_by_value(level)
            business_owner_google_id = extract_business_owner_google_id(get_jwt())
            AdsManagerDeleteStructureCommandHandler.handle(config=startup.google_config,
                                                           account_id=account_id,
                                                           level=level,
                                                           structure_id=structure_id,
                                                           business_owner_google_id=business_owner_google_id)
        except Exception as e:
            abort(400, message=f"Could not process your request. Error: {str(e)}")

        return 204


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


class AdsManagerGetAdGroupsEndpoint(Resource):

    @jwt_required
    def get(self, account_id):
        logger.logger.info(LoggerAPIRequestMessageBase(request).to_dict())
        level = Level.AD_GROUP.value
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


class AdsManagerGetKeywordsEndpoint(Resource):

    @jwt_required
    def get(self, account_id):
        logger.logger.info(LoggerAPIRequestMessageBase(request).to_dict())
        level = Level.KEYWORDS.value
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
        if level == 'adset':
            level = 'adgroup'
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
            response = humps.camelize(response)
            response = json.dumps(response)
            return Response(response=response, status=200, mimetype="application/json")
        except Exception as e:
            log = LoggerMessageBase(mtype=LoggerMessageTypeEnum.ERROR,
                                    name="AdsManagerFilteredStructuresEndpoint",
                                    description=str(e),
                                    extra_data=LoggerAPIRequestMessageBase(request).request_details)
            logger.logger.exception(log.to_dict())
            error = str(e)
            return Response(response=json.dumps(error), status=400, mimetype='application/json')
