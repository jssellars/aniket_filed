from flask import request
from flask_jwt_simple import jwt_required, get_jwt
from flask_restful import Resource, abort

from Core.Web.Security.JWTTools import extract_business_owner_google_id
from GoogleTuring.Api.Commands.AdsManagerUpdateStructureCommand import AdsManagerUpdateStructureCommand
from GoogleTuring.Api.CommandsHandlers.AdsManagerDeleteStructureCommandHandler import AdsManagerDeleteStructureCommandHandler
from GoogleTuring.Api.CommandsHandlers.AdsManagerUpdateStructureCommandHandler import AdsManagerUpdateStructureCommandHandler
from GoogleTuring.Api.Mappings.AdsManagerUpdateStructureCommandMapping import AdsManagerUpdateStructureCommandMapping
from GoogleTuring.Infrastructure.Domain.Structures.StructureType import StructureType


class AdsManagerEndpoint(Resource):
    @jwt_required
    def put(self, account_id, level, structure_id):
        try:
            business_owner_google_id = extract_business_owner_google_id(get_jwt())
            raw_request = request.get_json(force=True)
            mapping = AdsManagerUpdateStructureCommandMapping(target=AdsManagerUpdateStructureCommand)
            command = mapping.load(raw_request)
            AdsManagerUpdateStructureCommandHandler.handle(command=command,
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
            AdsManagerDeleteStructureCommandHandler.handle(account_id=account_id,
                                                           level=level,
                                                           structure_id=structure_id,
                                                           business_owner_google_id=business_owner_google_id)
        except Exception as e:
            abort(400, message=f"Could not process your request. Error: {str(e)}")

        return 204
