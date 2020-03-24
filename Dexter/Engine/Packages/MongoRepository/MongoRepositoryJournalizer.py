from Packages.MongoRepository.MongoRepositoryBase import MongoRepositoryBase

class MongoRepositoryJournalizer(MongoRepositoryBase):
    def __init__(self, client, database_name, collection_name=None):
        super().__init__(client=client, database_name=database_name, collection_name=collection_name)

    def get_last_two_entries(self, query, sort_query):

        return self.collection.find(query).sort(sort_query).limit(2)
