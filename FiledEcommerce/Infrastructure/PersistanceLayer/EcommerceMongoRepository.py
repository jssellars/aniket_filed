from Core.mongo_adapter import MongoRepositoryBase
from FiledEcommerce.Api.startup import config


class EcommerceMongoRepository(MongoRepositoryBase):
    def __init__(self):
        super(EcommerceMongoRepository, self).__init__(
            config=config.mongo, database_name=config.mongo.ecommerce_database_name, collection_name="oauth"
        )

    def add_oauth_creds(self, data):
        self.add_one(document=data)

    def read_oauth_creds(self, key, value):
        return self.get_first_by_key(key_name=key, key_value=value)
