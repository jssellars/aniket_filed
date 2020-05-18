import typing

from Core.Tools.QueryBuilder.QueryBuilder import QueryBuilderRequestMapper
from Core.Tools.QueryBuilder.QueryBuilderFacebookRequestParser import QueryBuilderFacebookRequestParser
from Core.Web.BusinessOwnerRepository.BusinessOwnerRepository import BusinessOwnerRepository
from FacebookTuring.Api.Startup import startup
from FacebookTuring.Infrastructure.GraphAPIHandlers.GraphAPIInsightsHandler import GraphAPIInsightsHandler


class AdsManagerInsightsCommandHandler:

    @classmethod
    def map_query(cls, query: typing.Dict = None, has_breakdowns: bool = True):
        query_builder_request = QueryBuilderRequestMapper(query)
        query = QueryBuilderFacebookRequestParser()
        query.parse(query_builder_request, parse_breakdowns=has_breakdowns)
        return query

    @classmethod
    def get_insights(cls, query_json: typing.Dict = None, business_owner_facebook_id: typing.AnyStr = None) -> \
            typing.List[typing.Dict]:
        business_owner_permanent_token = BusinessOwnerRepository(startup.session).get_permanent_token(
            business_owner_facebook_id)
        query = cls.map_query(query_json, has_breakdowns=True)
        response = GraphAPIInsightsHandler.get_insights(permanent_token=business_owner_permanent_token,
                                                        level=query.level,
                                                        ad_account_id=query.facebook_id,
                                                        fields=query.fields,
                                                        parameters=query.parameters,
                                                        structure_fields=query.structure_fields,
                                                        requested_fields=query.requested_columns)
        return response

    @classmethod
    def get_insights_with_totals(cls,
                                 query_json: typing.Dict = None,
                                 business_owner_facebook_id: typing.AnyStr = None) -> typing.Dict:
        business_owner_permanent_token = BusinessOwnerRepository(startup.session).get_permanent_token(
            business_owner_facebook_id)
        query = cls.map_query(query_json, has_breakdowns=True)
        response = GraphAPIInsightsHandler.get_insights_with_totals(permanent_token=business_owner_permanent_token,
                                                                    level=query.level,
                                                                    ad_account_id=query.facebook_id,
                                                                    fields=query.fields,
                                                                    parameters=query.parameters,
                                                                    structure_fields=query.structure_fields,
                                                                    requested_fields=query.requested_columns)
        return response

    @classmethod
    def get_reports_insights(cls, query_json: typing.Dict = None, business_owner_facebook_id: typing.AnyStr = None) -> \
            typing.List[typing.Dict]:
        business_owner_permanent_token = BusinessOwnerRepository(startup.session).get_permanent_token(
            business_owner_facebook_id)
        query = cls.map_query(query_json, has_breakdowns=True)
        response = GraphAPIInsightsHandler.get_reports_insights(permanent_token=business_owner_permanent_token,
                                                                ad_account_id=query.facebook_id,
                                                                fields=query.fields,
                                                                parameters=query.parameters,
                                                                requested_fields=query.requested_columns)
        return response
