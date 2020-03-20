from Core.Tools.QueryBuilder.QueryBuilder import QueryBuilderRequestMapper
from Core.Tools.QueryBuilder.QueryBuilderRequestParser import QueryBuilderRequestParser
from Core.Web.BusinessOwnerRepository.BusinessOwnerRepository import BusinessOwnerRepository
from Turing.Api.Startup import startup
from Turing.Infrastructure.GraphAPIHandlers.GraphAPIInsightsHandler import GraphAPIInsightsHandler


class AdsManagerInsightsCommandHandler:

    @classmethod
    def map_query(cls, query, has_breakdowns=True):
        query_builder_request = QueryBuilderRequestMapper(query)
        query = QueryBuilderRequestParser()
        query.from_query(query_builder_request, parse_breakdowns=has_breakdowns)
        return query

    @classmethod
    def get_insights(cls, query_json, business_owner_facebook_id):
        business_owner_permanent_token = BusinessOwnerRepository(startup.Session).get_permanent_token(business_owner_facebook_id)
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
    def get_insights_with_totals(cls, query_json, business_owner_facebook_id):
        business_owner_permanent_token = BusinessOwnerRepository(startup.Session).get_permanent_token(business_owner_facebook_id)
        query = cls.map_query(query_json, has_breakdowns=True)

        response = GraphAPIInsightsHandler.get_insights_with_totals(permanent_token=business_owner_permanent_token,
                                                                    level=query.level,
                                                                    ad_account_id=query.facebook_id,
                                                                    fields=query.fields,
                                                                    parameters=query.parameters,
                                                                    structure_fields=query.structure_fields,
                                                                    requested_fields=query.requested_columns)
        return response