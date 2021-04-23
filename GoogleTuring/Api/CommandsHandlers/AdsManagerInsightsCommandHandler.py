import logging

from flask import jsonify, make_response
from google.ads.googleads.errors import GoogleAdsException

from Core.Tools.QueryBuilder.QueryBuilder import AgGridInsightsRequest, QueryBuilderRequestMapper
from Core.Tools.QueryBuilder.QueryBuilderGoogleRequestParser import QueryBuilderGoogleRequestParser
from GoogleTuring.Api.CommandsHandlers.GoogleTokenGetter import GoogleTokenGetter
from GoogleTuring.Infrastructure.AdsAPIHandlers.AdsAPIPerformanceInsightsHandler import AdsAPIPerformanceInsightsHandler
from GoogleTuring.Infrastructure.AdWordsAPIHandlers.AdWordsAPIInsightsHandler import AdWordsAPIInsightsHandler
from GoogleTuring.Infrastructure.Domain.Enums.FiledGoogleInsightsTableEnum import FiledGoogleInsightsTableEnum

logger = logging.getLogger(__name__)


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
            response = AdWordsAPIInsightsHandler.get_insights(
                config=config,
                permanent_token=business_owner_permanent_token,
                query_builder_request_parser=query_builder_request_parser,
            )
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
                query_builder_request_parser=query_builder_request_parser,
            )
            return response
        else:
            return make_response(jsonify(error_message="Google account not found"), 404)


class AdsManagerInsightsPerformance:
    @classmethod
    def __map_query(cls, query_builder_request_parser, level, has_breakdowns=True):
        query_builder_request = AgGridInsightsRequest(query_builder_request_parser)
        query_builder_request_parser = QueryBuilderGoogleRequestParser()
        query_builder_request_parser.parse_ag_grid_insights_query(query_builder_request, level)
        return query_builder_request_parser

    @classmethod
    def get_performance_insights(cls, refresh_token, config, query_json, level):
        try:
            query_builder_request_parser = cls.__map_query(query_json, level)
            return AdsAPIPerformanceInsightsHandler.get_performance_insights(
                config=config, refresh_token=refresh_token, query_builder_request_parser=query_builder_request_parser
            )
        except GoogleAdsException as ex:
            logger.exception(f"Request with ID '{ex.request_id}' failed with status {ex.error.code().name}")
