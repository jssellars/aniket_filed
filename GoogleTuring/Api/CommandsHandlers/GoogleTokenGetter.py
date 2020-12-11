from GoogleTuring.Api.startup import config, fixtures
from GoogleTuring.Infrastructure.PersistenceLayer.GoogleBusinessOwnerMongoRepository import \
    GoogleBusinessOwnerMongoRepository


class GoogleTokenGetter:
    @classmethod
    def _get_permanent_token(cls, business_owner_google_id):
        mongo_adapter = fixtures.mongo_adapter
        mongo_repository = GoogleBusinessOwnerMongoRepository(client=mongo_adapter.client,
                                                              database_name=config.mongo.google_accounts_database_name,
                                                              collection_name=config.mongo.accounts_collection_name)
        business_owner_permanent_token = mongo_repository.get_permanent_token(business_owner_google_id)
        return business_owner_permanent_token
