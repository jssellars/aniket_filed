from datetime import datetime

from Core.Tools.MongoRepository.MongoOperator import MongoOperator
from Core.Tools.MongoRepository.MongoRepositoryBase import MongoRepositoryBase


class StatusChangerMongoRepository(MongoRepositoryBase):
    def change_status_many(self, ids, new_status, id_key):
        query_filter = {
            id_key: {
                MongoOperator.IN.value: ids
            }
        }
        query = {
            MongoOperator.SET.value: {
                "status": new_status,
                "last_updated_at": datetime.now()
            }
        }

        return self.update_many(query_filter, query)
