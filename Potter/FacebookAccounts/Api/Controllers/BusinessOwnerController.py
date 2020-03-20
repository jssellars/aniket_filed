import humps
from flask import request
from flask_jwt_simple import jwt_required, get_jwt
from flask_restful import Resource, abort

from Core.Web.Security.JWTTools import extract_business_owner_facebook_id
from Potter.FacebookAccounts.Api.Commands.BusinessOwnerCommands import BusinessOwnerCreateCommand, BusinessOwnerUpdateCommand
from Potter.FacebookAccounts.Api.CommandsHandlers.BusinessOwnerCommandHandler import BusinessOwnerCreateCommandHandler, BusinessOwnerUpdateCommandHandler
from Potter.FacebookAccounts.Api.Mappings import BusinessOwnerCommandsMappings


class BusinessOwnerEndpoint(Resource):

    @jwt_required
    def post(self):
        # business_owner_facebook_id = extract_business_owner_facebook_id(get_jwt())
        raw_request = humps.decamelize(request.get_json(force=True))

        mapping = BusinessOwnerCommandsMappings.BusinessOwnerCreateCommandMapping(BusinessOwnerCreateCommand)
        command = mapping.load(raw_request)

        # generate and store permanent token
        try:
            BusinessOwnerCreateCommandHandler.handle(command)
        except Exception as e:
            abort(400, message=f"Failed to add new business owner. Error {str(e)}")

        return 200

    @jwt_required
    def put(self):
        business_owner_facebook_id = extract_business_owner_facebook_id(get_jwt())
        raw_request = humps.decamelize(request.get_json(force=True))

        mapping = BusinessOwnerCommandsMappings.BusinessOwnerUpdateCommandMapping(BusinessOwnerUpdateCommand)
        command = mapping.load(raw_request)

        # generate and store permanent token
        BusinessOwnerUpdateCommandHandler.handle(command)

        return 200