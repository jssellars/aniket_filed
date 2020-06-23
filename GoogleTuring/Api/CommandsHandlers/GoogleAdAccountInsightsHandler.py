from datetime import datetime

from flask import make_response, jsonify

from Core.Tools.MongoRepository.MongoConnectionHandler import MongoConnectionHandler
from GoogleTuring.Api.CommandsHandlers.GoogleTokenGetter import GoogleTokenGetter
from GoogleTuring.Api.Startup import startup
from GoogleTuring.Infrastructure.AdWordsAPIHandlers.AdWordsAPIAdAccountInsightsHandler import \
    AdWordsAPIAdAccountInsightsHandler
from GoogleTuring.Infrastructure.PersistenceLayer.GoogleBusinessOwnerMongoRepository import \
    GoogleBusinessOwnerMongoRepository


class GoogleAdAccountInsightsHandler(GoogleTokenGetter):
    @classmethod
    def __get_all_client_ids_for_business_owner(cls, business_owner_google_id):
        mongo_conn_handler = MongoConnectionHandler(startup.mongo_config)
        mongo_repository = GoogleBusinessOwnerMongoRepository(client=mongo_conn_handler.client,
                                                              database_name=startup.mongo_config[
                                                                  'google_accounts_database_name'],
                                                              collection_name=startup.mongo_config[
                                                                  'accounts_collection_name'])
        google_accounts = mongo_repository.get_active_google_accounts(business_owner_google_id)
        client_customer_ids = [google_account['client_customer_id']['google_id'] for google_account in google_accounts]
        return client_customer_ids

    @classmethod
    def handle(cls, config, command):
        business_owner_permanent_token = cls._get_permanent_token(command.business_owner_google_id)
        if business_owner_permanent_token:
            client_customer_ids = cls.__get_all_client_ids_for_business_owner(command.business_owner_google_id)
            start_date = datetime.strptime(command.from_date, '%Y-%m-%d')
            end_date = datetime.strptime(command.to_date, '%Y-%m-%d')
            response = AdWordsAPIAdAccountInsightsHandler.get_ad_account_insights(
                config=config,
                permanent_token=business_owner_permanent_token,
                client_customer_ids=client_customer_ids,
                start_date=start_date,
                end_date=end_date)
            return response
        else:
            return make_response(jsonify(error_message="Google account not found"), 404)
