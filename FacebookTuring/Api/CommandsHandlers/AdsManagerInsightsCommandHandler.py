import typing

from Core.Tools.QueryBuilder.QueryBuilder import QueryBuilderRequestMapper, QueryBuilderAgGridRequest
from Core.Tools.QueryBuilder.QueryBuilderFacebookRequestParser import QueryBuilderFacebookRequestParser
from Core.Web.BusinessOwnerRepository.BusinessOwnerRepository import BusinessOwnerRepository
from FacebookTuring.Api.Commands.AdsManagerInsightsCommand import AdsManagerInsightsCommandEnum
from FacebookTuring.Api.Startup import startup, logger
from FacebookTuring.Infrastructure.Domain.FiledFacebookInsightsTableEnum import \
    FiledFacebookInsightsTableEnum
from FacebookTuring.Infrastructure.GraphAPIHandlers.GraphAPIInsightsHandler import GraphAPIInsightsHandler


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
            AdsManagerInsightsCommandEnum.AG_GRID_INSIGHTS: cls.get_ag_grid_insights
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
    def map_ag_grid_query(cls, query: typing.Dict = None,
                          level: typing.AnyStr = None,
                          has_breakdowns: bool = True) -> QueryBuilderFacebookRequestParser:
        query_builder_request = QueryBuilderAgGridRequest(
            query_builder_request=query,
            table_name=FiledFacebookInsightsTableEnum.get_enum_by_name(level.upper())
        )
        query = QueryBuilderFacebookRequestParser()
        query.parse_ag_grid(query_builder_request, level, parse_breakdowns=has_breakdowns)
        return query

    @classmethod
    def get_insights(cls,
                     query_json: typing.Dict = None,
                     business_owner_id: typing.AnyStr = None,
                     level: typing.AnyStr = None) -> typing.Dict:
        permanent_token = (BusinessOwnerRepository(startup.session).
                           get_permanent_token(business_owner_id))
        query = cls.map_query(query_json, has_breakdowns=True)
        response = GraphAPIInsightsHandler.set_logger(logger).get_insights(permanent_token=permanent_token,
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
        response = GraphAPIInsightsHandler.set_logger(logger).get_insights_with_totals(
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
                             query_json: typing.Dict = None,
                             business_owner_id: typing.AnyStr = None,
                             level: typing.AnyStr = None) -> typing.Dict:
        permanent_token = BusinessOwnerRepository(startup.session).get_permanent_token(business_owner_id)
        query = cls.map_ag_grid_query(query_json, level, has_breakdowns=True)

        return GraphAPIInsightsHandler.set_logger(logger).get_ag_grid_insights(
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
    def get_reports_insights(cls,
                             query_json: typing.Dict = None,
                             business_owner_id: typing.AnyStr = None,
                             level: typing.AnyStr = None) -> typing.List[typing.Dict]:
        permanent_token = BusinessOwnerRepository(startup.session).get_permanent_token(business_owner_id)
        query = cls.map_query(query_json, has_breakdowns=True)
        response = GraphAPIInsightsHandler.set_logger(logger).get_reports_insights(permanent_token=permanent_token,
                                                                                   ad_account_id=query.facebook_id,
                                                                                   fields=query.fields,
                                                                                   parameters=query.parameters,
                                                                                   requested_fields=query.requested_columns)
        return response
