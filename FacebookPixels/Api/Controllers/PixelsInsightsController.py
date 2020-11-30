import json
import typing

import humps
from flask import request, Response
from flask_restful import Resource

from Core.logging_config import request_as_log_dict
from Core.Tools.Misc.ObjectSerializers import object_to_json
from Core.Web.FacebookGraphAPI.Tools import Tools
from Core.Web.Security.JWTTools import extract_business_owner_facebook_id
from Core.Web.Security.Permissions import PixelPermissions
from FacebookPixels.Api.Commands.PixelsInsightsCommand import PixelsInsightsCommand
from FacebookPixels.Api.CommandsHandlers.PixelsInsightsCommandHandlers import PixelsInsightsCommandHandler
from FacebookPixels.Api.Mappings.PixelsInsightsCommandMapping import PixelsInsightsCommandMapping
from FacebookPixels.Api.Startup import startup


import logging

logger = logging.getLogger(__name__)


class PixelsInsightsEndpoint(Resource):
    @startup.authorize_permission(permission=PixelPermissions.CAN_ACCESS_PIXELS)
    def post(self, level: typing.AnyStr = None) -> typing.Union[typing.List[typing.NoReturn], typing.Dict]:
        logger.info(request_as_log_dict(request))
        try:
            business_owner_facebook_id = extract_business_owner_facebook_id()
            raw_request = humps.decamelize(request.get_json(force=True))
            mapping = PixelsInsightsCommandMapping(target=PixelsInsightsCommand)
            command = mapping.load(raw_request)
            command.level = level
            command.business_owner_facebook_id = business_owner_facebook_id
        except Exception as e:
            logger.exception(repr(e), extra=request_as_log_dict(request))
            response = json.dumps({"message": "Failed to process request."})
            return Response(response=response, status=400, mimetype='application/json')

        try:
            response = PixelsInsightsCommandHandler.handle(command)
            response = object_to_json(response)
            response = json.dumps(response)
            return Response(response=response, status=200, mimetype="application/json")
        except Exception as e:
            logger.exception(repr(e), extra=request_as_log_dict(request))
            response = Tools.create_error(e, code='POTTER_BAD_REQUEST')
            response = json.dumps(response)
            return Response(response=response, status=400, mimetype='application/json')
