from datetime import datetime

from Core.logging_legacy import log_operation_mongo
from Core.Tools.MongoRepository.MongoOperator import MongoOperator
from Core.Tools.MongoRepository.MongoRepositoryBase import MongoProjectionState
from GoogleTuring.Infrastructure.Domain.Enums.GoogleAccountStatus import GoogleAccountStatus
from GoogleTuring.Infrastructure.PersistenceLayer.StatusChangerMongoRepository import StatusChangerMongoRepository


import logging

logger_native = logging.getLogger(__name__)


class GoogleBusinessOwnerMongoRepository(StatusChangerMongoRepository):
    def __init__(self, client=None, database_name=None, collection_name=None, config=None, **kwargs):
        super().__init__(client=client, database_name=database_name, collection_name=collection_name, config=config,
                         **kwargs)

    def get_permanent_token(self, business_owner_id):
        google_accounts = self.get_active_google_accounts(business_owner_id)
        if len(google_accounts) != 0:
            return google_accounts[0]['refresh_token']
        else:
            return None

    def get_active_google_accounts(self, business_owner_id):
        query = {
            "business_owner_google_id": {
                MongoOperator.EQUALS.value: business_owner_id
            },
            "status": {
                MongoOperator.EQUALS.value: GoogleAccountStatus.ACTIVE.value
            }
        }
        operation_start_time = datetime.now()
        try:
            active_google_accounts = self.collection.find(query, {"_id": MongoProjectionState.OFF.value})
        except Exception as e:
            operation_end_time = datetime.now()
            duration = (operation_end_time - operation_start_time).total_seconds()
            log_operation_mongo(logger=self._logger,
                                log_level=logging.ERROR,
                                timestamp=datetime.now(),
                                duration=duration,
                                query=query)
            raise e
        return list(active_google_accounts)

    def get_all_active_google_accounts(self):
        query = {
            "status": {
                MongoOperator.EQUALS.value: GoogleAccountStatus.ACTIVE.value
            }
        }
        operation_start_time = datetime.now()

        try:
            active_google_accounts = self.collection.find(query, {"_id": MongoProjectionState.OFF.value})
        except Exception as e:
            operation_end_time = datetime.now()
            duration = (operation_end_time - operation_start_time).total_seconds()
            log_operation_mongo(logger=self._logger,
                                log_level=logging.ERROR,
                                timestamp=datetime.now(),
                                duration=duration,
                                query=query)
            raise e
        return active_google_accounts
