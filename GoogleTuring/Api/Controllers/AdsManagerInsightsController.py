from flask import request
from flask_jwt_simple import jwt_required, get_jwt
from flask_restful import Resource, abort

from Core.Web.Security.JWTTools import extract_business_owner_google_id
from GoogleTuring.Api.CommandsHandlers.AdsManagerInsightsCommandHandler import AdsManagerInsightsCommandHandler
from GoogleTuring.Api.Startup import startup


class AdsManagerInsightsEndpoint(Resource):

    @jwt_required
    def post(self):
        request_json = request.get_json(force=True)

        try:
            business_owner_google_id = extract_business_owner_google_id(get_jwt())
            response = AdsManagerInsightsCommandHandler.get_insights(config=startup.google_config,
                                                                     query_json=request_json["query"],
                                                                     business_owner_google_id=business_owner_google_id)
            return response
        except Exception as e:
            abort(400, message="Failed to process your insights request. %s" % str(e))


class AdsManagerInsightsWithTotalsEndpoint(Resource):

    @jwt_required
    def post(self):
        request_json = request.get_json(force=True)

        try:
            business_owner_google_id = extract_business_owner_google_id(get_jwt())
            response = AdsManagerInsightsCommandHandler.get_insights_with_totals(config=startup.google_config,
                                                                                 query_json=request_json["query"],
                                                                                 business_owner_google_id=business_owner_google_id)
            return response
        except Exception as e:
            abort(400, message="Failed to process your insights request. %s" % str(e))
