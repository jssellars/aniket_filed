import json
import typing

import humps
from flask import request, Response
from flask_jwt_simple import jwt_required, get_jwt
from flask_restful import Resource

from Core.Tools.Logger.LoggerAPIRequestMessageBase import LoggerAPIRequestMessageBase
from Core.Tools.Logger.LoggerMessageBase import LoggerMessageBase, LoggerMessageTypeEnum
from Core.Web.Security.JWTTools import extract_business_owner_facebook_id
from FacebookAccounts.Api.Commands.BusinessOwnerCommands import BusinessOwnerCreateCommand
from FacebookAccounts.Api.CommandsHandlers.BusinessOwnerCommandHandler import BusinessOwnerCreateCommandHandler
from FacebookAccounts.Api.CommandsHandlers.BusinessOwnerDeletePermissionsCommandHandler import \
    BusinessOwnerDeletePermissionsCommandHandler
from FacebookAccounts.Api.Mappings import BusinessOwnerCommandsMappings
from FacebookAccounts.Api.Startup import logger


class BusinessOwnerEndpoint(Resource):

    @jwt_required
    def post(self):
        #  log request information
        logger.logger.info(LoggerAPIRequestMessageBase(request).to_dict())
        try:
            raw_request = humps.decamelize(request.get_json(force=True))
            mapping = BusinessOwnerCommandsMappings.BusinessOwnerCreateCommandMapping(BusinessOwnerCreateCommand)
            command = mapping.load(raw_request)
        except Exception as e:
            log = LoggerMessageBase(mtype=LoggerMessageTypeEnum.ERROR,
                                    name="BusinessOwnerEndpoint",
                                    description=str(e),
                                    extra_data=LoggerAPIRequestMessageBase(request).request_details)
            logger.logger.exception(log.to_dict())
            response = json.dumps({"message": f"Failed to process request. Error {str(e)}"})
            return Response(response=response, status=400, mimetype='application/json')

        # generate and store permanent token
        try:
            BusinessOwnerCreateCommandHandler.handle(command)
            return Response(status=200, mimetype='application/json')
        except Exception as e:
            log = LoggerMessageBase(mtype=LoggerMessageTypeEnum.ERROR,
                                    name="BusinessOwnerEndpoint",
                                    description=str(e),
                                    extra_data=LoggerAPIRequestMessageBase(request).request_details)
            logger.logger.exception(log.to_dict())
            response = json.dumps({"message": f"Failed to add new business owner. Error {str(e)}"})
            return Response(response=response, status=400, mimetype='application/json')


class BusinessOwnerDeletePermissionsEndpoint(Resource):

    @jwt_required
    def delete(self, permissions: typing.List[typing.AnyStr] = None):
        #  log request information
        logger.logger.info(LoggerAPIRequestMessageBase(request).to_dict())

        try:
            business_owner_facebook_id = extract_business_owner_facebook_id(get_jwt())

            response = BusinessOwnerDeletePermissionsCommandHandler.handle(business_owner_facebook_id, permissions)
            response = humps.camelize(response)
            response = json.dumps(response)
            return Response(response=response, status=200, mimetype='application/json')
        except Exception as e:
            log = LoggerMessageBase(mtype=LoggerMessageTypeEnum.ERROR,
                                    name="BusinessOwnerEndpoint",
                                    description=str(e),
                                    extra_data=LoggerAPIRequestMessageBase(request).request_details)
            logger.logger.exception(log.to_dict())

            response = json.dumps({"message": f"Failed to delete permissions. Error {str(e)}"})
            return Response(response=response, status=400, mimetype='application/json')
