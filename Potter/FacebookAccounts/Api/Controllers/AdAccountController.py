import humps
from flask import request
from flask_jwt_simple import jwt_required, get_jwt
from flask_restful import Resource, abort

from Core.Web.Security.JWTTools import extract_business_owner_facebook_id
from Potter.FacebookAccounts.Api.Commands.AdAccountInsightsCommand import AdAccountInsightsCommand
from Potter.FacebookAccounts.Api.Mappings.AdAccountInsightsCommandMapping import AdAccountInsightsCommandMapping
from Potter.FacebookAccounts.Api.Queries.AdAccountInstagramQuery import AdAccountInstagramQuery
from Potter.FacebookAccounts.Api.Queries.AdAccountPageInstagramQuery import AdAccountPageInstagramQuery
from Potter.FacebookAccounts.Api.Queries.AdAccountPagesQuery import AdAccountPagesQuery
from Potter.FacebookAccounts.Api.Startup import startup
from Potter.FacebookAccounts.Infrastructure.GraphAPIHandlers.GraphAPIAdAccountInsightsHandler import GraphAPIAdAccountInsightsHandler


class AdAccountPagesEndpoint(Resource):

    @jwt_required
    def get(self, account_id):
        business_owner_id = extract_business_owner_facebook_id(get_jwt())
        try:
            response = AdAccountPagesQuery.handle(business_owner_id, account_id)
            return humps.camelize(response)
        except Exception as e:
            abort(400, message=f"Failed to retrieve pages for {account_id}. Error {str(e)}")


class AdAccountInstagramEndpoint(Resource):

    @jwt_required
    def get(self, account_id):
        business_owner_id = extract_business_owner_facebook_id(get_jwt())
        try:
            response = AdAccountInstagramQuery.handle(business_owner_id, account_id)
            return humps.camelize(response)
        except Exception as e:
            abort(400, message=f"Failed to retrieve pages for {account_id}. Error {str(e)}")


class AdAccountPageInstagramEndpoint(Resource):

    @jwt_required
    def get(self, page_id):
        business_owner_id = extract_business_owner_facebook_id(get_jwt())
        try:
            response = AdAccountPageInstagramQuery.handle(business_owner_id, page_id)
            return humps.camelize(response)
        except Exception as e:
            abort(400, message=f"Failed to retrieve pages for {page_id}. Error {str(e)}")
        # page_id?fields=instagram_business_account{id,username}
        pass


class AdAccountInsightsEndpoint(Resource):

    @jwt_required
    def post(self):
        business_owner_facebook_id = extract_business_owner_facebook_id(get_jwt())

        raw_request = humps.decamelize(request.get_json(force=True))

        mapping = AdAccountInsightsCommandMapping(AdAccountInsightsCommand)
        command = mapping.load(raw_request)
        command.business_owner_facebook_id = business_owner_facebook_id

        try:
            response = GraphAPIAdAccountInsightsHandler.handle(command, startup)
            response = humps.camelize(response)
            return response
        except Exception as e:
            abort(400, message=f"Failed to get insights. Error: {str(e)}")
