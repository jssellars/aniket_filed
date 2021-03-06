from Core.mongo_adapter import MongoRepositoryBase


class DexterJournalMongoRepository(MongoRepositoryBase):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def get_last_two_entries(self, query, sort_query):
        self._database = self._client[self._config.journal_database_name]
        self.collection = self._config.journal_collection_name
        return self.get_sorted(query=query, sort_query=sort_query)[:2]

    def get_all_by_query(self, query):
        self._database = self._client[self._config.journal_database_name]
        self.collection = self._config.journal_collection_name
        return self.get(query=query)
