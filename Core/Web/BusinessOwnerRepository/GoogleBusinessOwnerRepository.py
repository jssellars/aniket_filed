import logging
from datetime import datetime

from Core.mongo_adapter import MongoOperator, MongoProjectionState, MongoRepositoryBase

logger = logging.getLogger(__name__)


class GoogleBusinessOwnerRepository(MongoRepositoryBase):
    def __init__(self, client=None, database_name=None, collection_name=None, config=None, **kwargs):
        super().__init__(
            client=client, database_name=database_name, collection_name=collection_name, config=config, **kwargs
        )

    def get_refresh_token(self, business_owner_id):
        google_accounts = self.get_active_google_accounts(business_owner_id)
        if len(google_accounts) != 0:
            return google_accounts[0]["refresh_token"]
        else:
            return None

    def get_active_google_accounts(self, business_owner_id):
        query = {"business_owner_google_id": {MongoOperator.EQUALS.value: business_owner_id}}
        start = datetime.now()
        try:
            active_google_accounts = self.collection.find(query, {"_id": MongoProjectionState.OFF.value})
        except Exception as e:
            logger.error(dict(duration=(datetime.now() - start).total_seconds(), query=query))
            raise e
        return list(active_google_accounts)
