from datetime import datetime

from Core.mongo_adapter import MongoRepositoryBase, MongoOperator


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
