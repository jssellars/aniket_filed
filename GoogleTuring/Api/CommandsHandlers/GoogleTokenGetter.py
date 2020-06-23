from Core.Tools.MongoRepository.MongoConnectionHandler import MongoConnectionHandler
from GoogleTuring.Api.Startup import startup
from GoogleTuring.Infrastructure.PersistenceLayer.GoogleBusinessOwnerMongoRepository import \
    GoogleBusinessOwnerMongoRepository


class GoogleTokenGetter:
    @classmethod
    def _get_permanent_token(cls, business_owner_google_id):
        mongo_conn_handler = MongoConnectionHandler(startup.mongo_config)
        mongo_repository = GoogleBusinessOwnerMongoRepository(client=mongo_conn_handler.client,
                                                              database_name=startup.mongo_config[
                                                                  'google_accounts_database_name'],
                                                              collection_name=startup.mongo_config[
                                                                  'accounts_collection_name'])
        business_owner_permanent_token = mongo_repository.get_permanent_token(business_owner_google_id)
        return business_owner_permanent_token
