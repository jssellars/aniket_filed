import typing

import humps
from flask import request
from flask_jwt_simple import jwt_required, get_jwt
from flask_restful import Resource, abort

from Core.Tools.Misc.ObjectSerializers import object_to_json
from Core.Web.Security.JWTTools import extract_business_owner_facebook_id
from Potter.FacebookPixels.Api.Commands.PixelsInsightsCommand import PixelsInsightsCommand
from Potter.FacebookPixels.Api.CommandsHandlers.PixelsInsightsCommandHandlers import PixelsInsightsCommandHandler
from Potter.FacebookPixels.Api.Mappings.PixelsInsightsCommandMapping import PixelsInsightsCommandMapping


class PixelsInsightsEndpoint(Resource):

    @jwt_required
    def post(self, level: typing.AnyStr = None) -> typing.List[typing.Dict]:
        business_owner_facebook_id = extract_business_owner_facebook_id(get_jwt())
        raw_request = humps.decamelize(request.get_json(force=True))
        mapping = PixelsInsightsCommandMapping(target=PixelsInsightsCommand)
        command = mapping.load(raw_request)
        command.level = level
        command.business_owner_facebook_id = business_owner_facebook_id

        try:
            response = PixelsInsightsCommandHandler.handle(command)
            response = object_to_json(response)
            return response
        except Exception as e:
            abort(400, message=f"Failed to get insights. Error: {str(e)}")

