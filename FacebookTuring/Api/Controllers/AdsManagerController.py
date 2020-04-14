import humps
from flask import request
from flask_jwt_simple import jwt_required, get_jwt
from flask_restful import Resource, abort

from Core.Web.Misc import snake_to_camelcase
from Core.Web.Security.JWTTools import extract_business_owner_facebook_id
from FacebookTuring.Api.Commands.AdsManagerDuplicateStructureCommand import AdsManagerDuplicateStructureCommand
from FacebookTuring.Api.Commands.AdsManagerSaveDraftCommand import AdsManagerSaveDraftCommand
from FacebookTuring.Api.Commands.AdsManagerUpdateStructureCommand import AdsManagerUpdateStructureCommand
from FacebookTuring.Api.CommandsHandlers.AdsManagerDeleteStructureCommandHandler import AdsManagerDeleteStructureCommandHandler
from FacebookTuring.Api.CommandsHandlers.AdsManagerDiscardDraftCommandHandler import AdsManagerDiscardDraftCommandHandler
from FacebookTuring.Api.CommandsHandlers.AdsManagerSaveDraftCommandHandler import AdsManagerSaveDraftCommandHandler
from FacebookTuring.Api.CommandsHandlers.AdsManagerUpdateStructureCommandHandler import AdsManagerUpdateStructureCommandHandler
from FacebookTuring.Api.Mappings.AdsManagerDuplicateStructureCommandMapping import AdsManagerDuplicateStructureCommandMapping
from FacebookTuring.Api.Mappings.AdsManagerSaveDraftCommandMapping import AdsManagerSaveDraftCommandMapping
from FacebookTuring.Api.Mappings.AdsManagerUpdateStructureCommandMapping import AdsManagerUpdateStructureCommandMapping
from FacebookTuring.Api.Queries.AdsManagerCampaignTreeStructureQuery import AdsManagerCampaignTreeStructureQuery
from FacebookTuring.Api.Queries.AdsManagerGetStructuresQuery import AdsManagerGetStructuresQuery
from FacebookTuring.Infrastructure.Mappings.LevelMapping import Level


class AdsManagerCampaignTreeStructureEndpoint(Resource):

    @jwt_required
    def get(self, level, facebook_id):
        try:
            response = AdsManagerCampaignTreeStructureQuery.get(level, facebook_id)
            return humps.camelize(response)
        except Exception as e:
            abort(400, message=f"Could not retrieve tree for {facebook_id}. Error: {str(e)}")


class AdsManagerGetCampaignsEndpoint(Resource):

    @jwt_required
    def get(self, account_id):
        level = Level.CAMPAIGN.value
        try:
            response = AdsManagerGetStructuresQuery.get_structures(level, account_id)
            return snake_to_camelcase(response)
        except Exception as e:
            abort(400, message=f"Could not retrieve {level} for {account_id}. Error: {str(e)}")


class AdsManagerGetAdSetsEndpoint(Resource):

    @jwt_required
    def get(self, account_id):
        level = Level.ADSET.value
        try:
            response = AdsManagerGetStructuresQuery.get_structures(level, account_id)
            return snake_to_camelcase(response)
        except Exception as e:
            abort(400, message=f"Could not retrieve {level} for {account_id}. Error: {str(e)}")


class AdsManagerGetAdsEndpoint(Resource):

    @jwt_required
    def get(self, account_id):
        level = Level.AD.value
        try:
            response = AdsManagerGetStructuresQuery.get_structures(level, account_id)
            return snake_to_camelcase(response)
        except Exception as e:
            abort(400, message=f"Could not retrieve {level} for {account_id}. Error: {str(e)}")


class AdsManagerEndpoint(Resource):

    @jwt_required
    def get(self, level, facebook_id):
        try:
            response = AdsManagerGetStructuresQuery.get_structure_details(level, facebook_id)
            return snake_to_camelcase(response)
        except Exception as e:
            abort(400, message=f"Could not retrieve {level} for {facebook_id}. Error: {str(e)}")

    @jwt_required
    def put(self, level, facebook_id):
        try:
            raw_request = humps.decamelize(request.get_json(force=True))
            mapping = AdsManagerUpdateStructureCommandMapping(target=AdsManagerUpdateStructureCommand)
            command = mapping.load(raw_request)
            business_owner_facebook_id = extract_business_owner_facebook_id(get_jwt())
        except Exception as e:
            abort(400, message=f"Could not process your request. Error: {str(e)}")

        try:
            AdsManagerUpdateStructureCommandHandler.handle(command=command,
                                                           level=level,
                                                           facebook_id=facebook_id,
                                                           business_owner_facebook_id=business_owner_facebook_id)
        except Exception as e:
            abort(400, message=f"Could not process your request. Error: {str(e)}")

        return 204

    @jwt_required
    def delete(self, level, facebook_id):
        business_owner_facebook_id = extract_business_owner_facebook_id(get_jwt())
        try:
            response = AdsManagerDeleteStructureCommandHandler.handle(level, facebook_id, business_owner_facebook_id)
            if response:
                return "", 204
            else:
                abort(404, message=f"Could not find {level} with id: {facebook_id}")
        except Exception as e:
            abort(400, message=f"Could not process your request. Error: {str(e)}")

        return 204


class AdsManagerUpdateStructureDraftEndpoint(Resource):

    @jwt_required
    def put(self, level, facebook_id):
        try:
            raw_request = humps.decamelize(request.get_json(force=True))
            mapping = AdsManagerSaveDraftCommandMapping(target=AdsManagerSaveDraftCommand)
            command = mapping.load(raw_request)
        except Exception as e:
            abort(400, message=f"Could not process your request. Error: {str(e)}")

        try:
            AdsManagerSaveDraftCommandHandler.handle(command, level, facebook_id)
        except Exception as e:
            abort(400, message=f"Could not process your request. Error: {str(e)}")

        return 204

    @jwt_required
    def delete(self, level, facebook_id):
        try:
            AdsManagerDiscardDraftCommandHandler.handle(level, facebook_id)
        except Exception as e:
            abort(400, message=f"Could not retrieve {level} for {facebook_id}. Error: {str(e)}")

        return 204


class AdsManagerDuplicateStructureEndpoint(Resource):

    @jwt_required
    def post(self, level, facebook_id):
        try:
            raw_request = humps.decamelize(request.get_json(force=True))
            mapping = AdsManagerDuplicateStructureCommandMapping(target=AdsManagerDuplicateStructureCommand)
            command = mapping.load(raw_request)
            business_owner_facebook_id = extract_business_owner_facebook_id(get_jwt())
        except Exception as e:
            abort(400, message=f"Could not process your request. Error: {str(e)}")

        try:
            AdsManagerUpdateStructureCommandHandler.handle(command, level, facebook_id, business_owner_facebook_id)
        except Exception as e:
            abort(400, message=f"Could not process your request. Error: {str(e)}")

        return 204
