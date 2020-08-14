import json
import typing
import humps

from flask import request, Response
from flask_jwt_simple import jwt_required, get_jwt
from flask_restful import Resource

from Core.Tools.Logger.LoggerAPIRequestMessageBase import LoggerAPIRequestMessageBase
from Core.Tools.Logger.LoggerMessageBase import LoggerMessageTypeEnum, LoggerMessageBase
from Core.Tools.Misc.ObjectSerializers import object_to_json
from Core.Web.FacebookGraphAPI.Tools import Tools
from Core.Web.Security.JWTTools import extract_business_owner_facebook_id
from Potter.FacebookPixels.Api.Commands.PixelsInsightsCommand import PixelsInsightsCommand
from Potter.FacebookPixels.Api.CommandsHandlers.PixelsInsightsCommandHandlers import PixelsInsightsCommandHandler
from Potter.FacebookPixels.Api.Mappings.PixelsInsightsCommandMapping import PixelsInsightsCommandMapping
from Potter.FacebookPixels.Api.Startup import logger


class PixelsInsightsEndpoint(Resource):

    @jwt_required
    def post(self, level: typing.AnyStr = None) -> typing.Union[typing.List[typing.NoReturn], typing.Dict]:
        logger.logger.info(LoggerAPIRequestMessageBase(request).to_dict())
        try:
            business_owner_facebook_id = extract_business_owner_facebook_id(get_jwt())
            raw_request = humps.decamelize(request.get_json(force=True))
            mapping = PixelsInsightsCommandMapping(target=PixelsInsightsCommand)
            command = mapping.load(raw_request)
            command.level = level
            command.business_owner_facebook_id = business_owner_facebook_id
        except Exception as e:
            log = LoggerMessageBase(mtype=LoggerMessageTypeEnum.ERROR,
                                    name="PixelsInsightsEndpoint",
                                    description=str(e),
                                    extra_data=LoggerAPIRequestMessageBase(request).request_details)
            logger.logger.exception(log.to_dict())
            response = json.dumps({"message": "Failed to process request."})
            return Response(response=response, status=400, mimetype='application/json')

        try:
            response = PixelsInsightsCommandHandler.handle(command)
            response = object_to_json(response)
            response = json.dumps(response)
            return Response(response=response, status=200, mimetype="application/json")
        except Exception as e:
            log = LoggerMessageBase(mtype=LoggerMessageTypeEnum.ERROR,
                                    name="PixelsInsightsEndpoint",
                                    description=str(e),
                                    extra_data=LoggerAPIRequestMessageBase(request).request_details)
            logger.logger.exception(log.to_dict())
            response = Tools.create_error(e, code='POTTER_BAD_REQUEST')
            response = json.dumps(response)
            return Response(response=response, status=400, mimetype='application/json')
