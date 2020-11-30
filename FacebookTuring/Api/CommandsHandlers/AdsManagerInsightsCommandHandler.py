import typing
from datetime import datetime, timedelta
from typing import Dict

from Core.Tools.Misc.AgGridConstants import PositiveEffectTrendDirection, Trend
from Core.Tools.Misc.Constants import DEFAULT_DATETIME
from Core.Tools.QueryBuilder.QueryBuilder import QueryBuilderRequestMapper, AgGridInsightsRequest, AgGridTrendRequest
from Core.Tools.QueryBuilder.QueryBuilderFacebookRequestParser import QueryBuilderFacebookRequestParser
from Core.Web.BusinessOwnerRepository.BusinessOwnerRepository import BusinessOwnerRepository
from FacebookTuring.Api.Commands.AdsManagerInsightsCommand import AdsManagerInsightsCommandEnum
from FacebookTuring.Api.Startup import startup
from FacebookTuring.Infrastructure.Domain.FiledFacebookInsightsTableEnum import \
    FiledFacebookInsightsTableEnum
from FacebookTuring.Infrastructure.GraphAPIHandlers.GraphAPIInsightsHandler import GraphAPIInsightsHandler

import logging

logger = logging.getLogger(__name__)


PERCENTAGE_DIFFERENCE_KEY = "percentage_difference"
TREND_KEY = "trend"


class AdsManagerInsightsCommandHandler:

    @classmethod
    def handle(cls,
               handler_type: AdsManagerInsightsCommandEnum = None,
               query_json: typing.Dict = None,
               business_owner_id: typing.AnyStr = None,
               level: typing.AnyStr = None) -> typing.List[typing.Dict]:
        handlers = {
            AdsManagerInsightsCommandEnum.INSIGHTS: cls.get_insights,
            AdsManagerInsightsCommandEnum.INSIGHTS_WITH_TOTALS: cls.get_insights_with_totals,
            AdsManagerInsightsCommandEnum.REPORTS: cls.get_reports_insights,
            AdsManagerInsightsCommandEnum.AG_GRID_INSIGHTS: cls.get_ag_grid_insights,
            AdsManagerInsightsCommandEnum.AG_GRID_INSIGHTS_TREND: cls.get_ag_grid_trend,
        }
        handler = handlers.get(handler_type, None)
        if handler is None:
            raise ValueError('Invalid insights handler: %s' % handler_type.value)

        return handler(query_json=query_json, business_owner_id=business_owner_id, level=level)

    @classmethod
    def map_query(cls, query: typing.Dict = None, has_breakdowns: bool = True) -> QueryBuilderFacebookRequestParser:
        query_builder_request = QueryBuilderRequestMapper(query, FiledFacebookInsightsTableEnum)
        query = QueryBuilderFacebookRequestParser()
        query.parse(query_builder_request, parse_breakdowns=has_breakdowns)
        return query

    @classmethod
    def map_ag_grid_insights_query(cls, query: typing.Dict = None,
                                   level: typing.AnyStr = None,
                                   has_breakdowns: bool = True) -> QueryBuilderFacebookRequestParser:
        query_builder_request = AgGridInsightsRequest(query_builder_request=query)
        query = QueryBuilderFacebookRequestParser()
        query.parse_ag_grid_insights_query(query_builder_request, level, parse_breakdowns=has_breakdowns)
        return query

    @classmethod
    def map_ag_grid_trend_query(cls, query: typing.Dict = None,
                                level: typing.AnyStr = None,
                                has_breakdowns: bool = True) -> QueryBuilderFacebookRequestParser:
        query_builder_request = AgGridTrendRequest(query)
        query = QueryBuilderFacebookRequestParser()
        query.parse_ag_grid_trend_query(query_builder_request, level, parse_breakdowns=has_breakdowns)
        return query

    @classmethod
    def get_insights(cls,
                     query_json: typing.Dict = None,
                     business_owner_id: typing.AnyStr = None,
                     level: typing.AnyStr = None) -> typing.Dict:
        permanent_token = (BusinessOwnerRepository(startup.session).
                           get_permanent_token(business_owner_id))
        query = cls.map_query(query_json, has_breakdowns=True)
        response = GraphAPIInsightsHandler.get_insights(permanent_token=permanent_token,
                                                                           level=query.level,
                                                                           ad_account_id=query.facebook_id,
                                                                           fields=query.fields,
                                                                           parameters=query.parameters,
                                                                           structure_fields=query.structure_fields,
                                                                           requested_fields=query.requested_columns,
                                                                           filter_params=query.filtering)
        return response

    @classmethod
    def get_insights_with_totals(cls,
                                 query_json: typing.Dict = None,
                                 business_owner_id: typing.AnyStr = None,
                                 level: typing.AnyStr = None) -> typing.Dict:
        permanent_token = BusinessOwnerRepository(startup.session).get_permanent_token(business_owner_id)
        query = cls.map_query(query_json, has_breakdowns=True)
        response = GraphAPIInsightsHandler.get_insights_with_totals(
            permanent_token=permanent_token,
            level=query.level,
            ad_account_id=query.facebook_id,
            fields=query.fields,
            parameters=query.parameters,
            structure_fields=query.structure_fields,
            requested_fields=query.requested_columns,
            filter_params=query.filtering
        )
        return response

    @classmethod
    def get_ag_grid_insights(cls,
                             query_json: Dict = None,
                             business_owner_id: str = None,
                             level: str = None) -> Dict:
        permanent_token = BusinessOwnerRepository(startup.session).get_permanent_token(business_owner_id)
        query = cls.map_ag_grid_insights_query(query_json, level, has_breakdowns=True)

        return GraphAPIInsightsHandler.get_ag_grid_insights(
            permanent_token=permanent_token,
            level=level,
            ad_account_id=query.facebook_id,
            fields=query.fields,
            parameters=query.parameters,
            structure_fields=query.structure_fields,
            requested_fields=query.requested_columns,
            next_page_cursor=query.next_page_cursor,
            page_size=query.page_size,
        )

    @classmethod
    def get_ag_grid_trend(cls,
                          query_json: typing.Dict = None,
                          business_owner_id: typing.AnyStr = None,
                          level: typing.AnyStr = None) -> Dict:

        permanent_token = BusinessOwnerRepository(startup.session).get_permanent_token(business_owner_id)
        query = cls.map_ag_grid_trend_query(query_json, level, has_breakdowns=True)

        requested_columns = query.requested_columns
        if len(requested_columns) > 1:
            logger.exception("The ag grid trend endpoint should receive only one column.")
            raise Exception("The ag grid trend endpoint should receive only one column.")

        _, _, result = GraphAPIInsightsHandler.get_insights_page(
            permanent_token=permanent_token,
            level=level,
            ad_account_id=query.facebook_id,
            fields=query.fields,
            parameters=query.parameters,
            add_totals=True,
            requested_fields=requested_columns,
            next_page_cursor=query.next_page_cursor,
            page_size=1,
        )

        since_date = datetime.strptime(query.time_range["since"], DEFAULT_DATETIME)
        until_date = datetime.strptime(query.time_range["until"], DEFAULT_DATETIME)
        time_interval_in_days = (until_date - since_date).days + 1

        query.time_range["since"] = (since_date - timedelta(days=time_interval_in_days)).date().isoformat()
        query.time_range["until"] = (until_date - timedelta(days=time_interval_in_days)).date().isoformat()

        _, _, past_period_result = GraphAPIInsightsHandler.get_insights_page(
            permanent_token=permanent_token,
            level=level,
            ad_account_id=query.facebook_id,
            fields=query.fields,
            parameters=query.parameters,
            add_totals=True,
            requested_fields=requested_columns,
            next_page_cursor=query.next_page_cursor,
            page_size=1,
        )

        required_metric = requested_columns[0].name
        positive_effect_trend_direction = requested_columns[0].positive_effect_trend_direction

        # TODO think of a way to redefine the contract and make some fields optional
        if not result or not result[0] or required_metric not in result[0]:
            return {required_metric: None, PERCENTAGE_DIFFERENCE_KEY: None, TREND_KEY: Trend.UNDEFINED.name}

        metric_result = result[0][required_metric]

        if not past_period_result or not past_period_result[0] or required_metric not in past_period_result[0]:
            return {required_metric: metric_result, PERCENTAGE_DIFFERENCE_KEY: None, TREND_KEY: Trend.UNDEFINED.name}

        previous_period_metric_result = past_period_result[0][required_metric]
        percentage_difference = (metric_result / previous_period_metric_result - 1) * 100

        trend = Trend.NEGATIVE.name if positive_effect_trend_direction else Trend.UNDEFINED.name
        if percentage_difference < 0 and positive_effect_trend_direction == PositiveEffectTrendDirection.DECREASING:
            trend = Trend.POSITIVE.name
        elif percentage_difference > 0 and positive_effect_trend_direction == PositiveEffectTrendDirection.INCREASING:
            trend = Trend.POSITIVE.name

        return {required_metric: metric_result, PERCENTAGE_DIFFERENCE_KEY: percentage_difference, TREND_KEY: trend}

    @classmethod
    def get_reports_insights(cls,
                             query_json: typing.Dict = None,
                             business_owner_id: typing.AnyStr = None,
                             level: typing.AnyStr = None) -> typing.List[typing.Dict]:
        permanent_token = BusinessOwnerRepository(startup.session).get_permanent_token(business_owner_id)
        query = cls.map_query(query_json, has_breakdowns=True)
        response = GraphAPIInsightsHandler.get_reports_insights(permanent_token=permanent_token,
                                                                                   ad_account_id=query.facebook_id,
                                                                                   fields=query.fields,
                                                                                   parameters=query.parameters,
                                                                                   requested_fields=query.requested_columns,
                                                                                   level=level)
        return response
