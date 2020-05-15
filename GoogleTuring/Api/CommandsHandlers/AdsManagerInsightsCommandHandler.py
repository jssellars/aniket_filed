from flask import jsonify, make_response

from Core.Tools.QueryBuilder.QueryBuilder import QueryBuilderRequestMapper
from Core.Tools.QueryBuilder.QueryBuilderGoogleRequestParser import QueryBuilderGoogleRequestParser
from GoogleTuring.Api.CommandsHandlers.AdsManagerBaseCommandHandler import AdsManagerBaseCommandHandler
from GoogleTuring.Infrastructure.AdWordsAPIHandlers.AdWordsAPIInsightsHandler import AdWordsAPIInsightsHandler
from GoogleTuring.Infrastructure.Domain.Enums.FiledGoogleInsightsTableEnum import FiledGoogleInsightsTableEnum


class AdsManagerInsightsCommandHandler(AdsManagerBaseCommandHandler):

    @classmethod
    def __map_query(cls, query):
        query_builder_request = QueryBuilderRequestMapper(query, FiledGoogleInsightsTableEnum)
        query = QueryBuilderGoogleRequestParser()
        query.from_query(query_builder_request)
        return query

    @classmethod
    def get_insights(cls, query_json, business_owner_google_id):
        business_owner_permanent_token = cls._get_permanent_token(business_owner_google_id)
        if business_owner_permanent_token:
            query = cls.__map_query(query_json)
            response = AdWordsAPIInsightsHandler.get_insights(permanent_token=business_owner_permanent_token,
                                                              client_customer_id=query.google_id,
                                                              report=query.report,
                                                              fields=query.google_fields,
                                                              time_range=query.time_range)
            return response, 200
        else:
            return make_response(jsonify(error_message="Google account not found"), 404)

    @classmethod
    def get_insights_with_totals(cls, query_json, business_owner_google_id):
        business_owner_permanent_token = cls._get_permanent_token(business_owner_google_id)
        if business_owner_permanent_token:
            query = cls.__map_query(query_json)
            response = AdWordsAPIInsightsHandler.get_insights_with_totals(permanent_token=business_owner_permanent_token,
                                                                          client_customer_id=query.google_id,
                                                                          report=query.report,
                                                                          fields=query.google_fields,
                                                                          time_range=query.time_range)
            return response, 200
        else:
            return make_response(jsonify(error_message="Google account not found"), 404)
