import humps
import typing
from flask import request
from flask_jwt_simple import jwt_required, get_jwt
from flask_restful import Resource, abort

from Core.Web.Security.JWTTools import extract_business_owner_facebook_id
from Turing.Api.CommandsHandlers.AdsManagerInsightsCommandHandler import AdsManagerInsightsCommandHandler


class AdsManagerInsightsEndpoint(Resource):

    @jwt_required
    def post(self, level: typing.AnyStr = None):
        requestJson = request.get_json(force=True)
        business_owner_facebook_id = extract_business_owner_facebook_id(get_jwt())

        try:
            response = AdsManagerInsightsCommandHandler.get_insights(requestJson["level"], requestJson["query"], business_owner_facebook_id)
            return response
        except Exception as e:
            abort(400, message="Failed to process your insights request. %s" % str(e))


class AdsManagerInsightsWithTotalsEndpoint(Resource):

    @jwt_required
    def post(self):
        requestJson = request.get_json(force=True)
        business_owner_facebook_id = extract_business_owner_facebook_id(get_jwt())

        try:
            response = AdsManagerInsightsCommandHandler.get_insights_with_totals(requestJson["query"], business_owner_facebook_id)
            return response
        except Exception as e:
            abort(400, message="Failed to process your insights request. %s" % str(e))
