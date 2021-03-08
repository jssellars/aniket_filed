from flask import jsonify, make_response

from Core.Tools.QueryBuilder.QueryBuilder import QueryBuilderRequestMapper
from Core.Tools.QueryBuilder.QueryBuilderGoogleRequestParser import QueryBuilderGoogleRequestParser
from GoogleTuring.Api.CommandsHandlers.GoogleTokenGetter import GoogleTokenGetter
from GoogleTuring.Infrastructure.AdWordsAPIHandlers.AdWordsAPIInsightsHandler import AdWordsAPIInsightsHandler
from GoogleTuring.Infrastructure.Domain.Enums.FiledGoogleInsightsTableEnum import FiledGoogleInsightsTableEnum


class AdsManagerInsightsCommandHandler(GoogleTokenGetter):

    @classmethod
    def __map_query(cls, query_builder_request_parser):
        query_builder_request = QueryBuilderRequestMapper(query_builder_request_parser, FiledGoogleInsightsTableEnum)
        query_builder_request_parser = QueryBuilderGoogleRequestParser()
        query_builder_request_parser.from_query(query_builder_request)
        return query_builder_request_parser

    @classmethod
    def get_insights(cls, config, query_json, business_owner_google_id):
        business_owner_permanent_token = cls._get_permanent_token(business_owner_google_id)
        if business_owner_permanent_token:
            query_builder_request_parser = cls.__map_query(query_json)
            response = AdWordsAPIInsightsHandler.get_insights(config=config,
                                                              permanent_token=business_owner_permanent_token,
                                                              query_builder_request_parser=query_builder_request_parser)
            return response
        else:
            return make_response(jsonify(error_message="Google account not found"), 404)

    @classmethod
    def get_insights_with_totals(cls, config, query_json, business_owner_google_id):
        business_owner_permanent_token = cls._get_permanent_token(business_owner_google_id)
        if business_owner_permanent_token:
            query_builder_request_parser = cls.__map_query(query_json)
            response = AdWordsAPIInsightsHandler.get_insights_with_totals(
                config=config,
                permanent_token=business_owner_permanent_token,
                query_builder_request_parser=query_builder_request_parser)
            return response
        else:
            return make_response(jsonify(error_message="Google account not found"), 404)
