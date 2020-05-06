from flask import jsonify, make_response

from Core.Tools.MongoRepository.MongoConnectionHandler import MongoConnectionHandler
from Core.Tools.QueryBuilder.QueryBuilder import QueryBuilderRequestMapper
from Core.Tools.QueryBuilder.QueryBuilderGoogleRequestParser import QueryBuilderGoogleRequestParser
from GoogleTuring.Api.Startup import startup
from GoogleTuring.Infrastructure.AdwordsAPIHandlers.AdWordsAPIInsightsHandler import AdWordsAPIInsightsHandler
from GoogleTuring.Infrastructure.Domain.Enums.FiledGoogleInsightsTableEnum import FiledGoogleInsightsTableEnum
from GoogleTuring.Infrastructure.PersistanceLayer.GoogleBusinessOwnerMongoRepository import GoogleBusinessOwnerMongoRepository


class AdsManagerInsightsCommandHandler:

    @classmethod
    def __map_query(cls, query):
        query_builder_request = QueryBuilderRequestMapper(query, FiledGoogleInsightsTableEnum)
        query = QueryBuilderGoogleRequestParser()
        query.from_query(query_builder_request)
        return query

    @classmethod
    def get_insights(cls, query_json, business_owner_google_id):
        business_owner_permanent_token = cls.__get_permanent_token(business_owner_google_id)
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
    def __get_permanent_token(cls, business_owner_google_id):
        mongo_conn_handler = MongoConnectionHandler(startup.mongo_config)
        mongo_repository = GoogleBusinessOwnerMongoRepository(client=mongo_conn_handler.client, database_name=startup.mongo_config['google_accounts_database_name'],
                                                              collection_name=startup.mongo_config['accounts_collection_name'])
        business_owner_permanent_token = mongo_repository.get_permanent_token(business_owner_google_id)
        mongo_conn_handler.close()
        return business_owner_permanent_token

    @classmethod
    def get_insights_with_totals(cls, query_json, business_owner_google_id):
        business_owner_permanent_token = cls.__get_permanent_token(business_owner_google_id)
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
