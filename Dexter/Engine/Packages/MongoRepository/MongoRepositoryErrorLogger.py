from Packages.MongoRepository.MongoRepositoryBase import MongoRepositoryBase
import datetime

class MongoRepositoryErrorLogger(MongoRepositoryBase):
    def __init__(self, client, database_name, collection_name=None):
        super().__init__(client=client, database_name=database_name, collection_name=collection_name)

    def send_log_error(self, error):
        pass
