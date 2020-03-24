class MongoRepositoryBaseException(Exception):
    pass


class MongoRepositoryBase:

    def __init__(self, client=None, database_name=None, collection_name=None):
        self._client = client
        self._database_name = database_name
        self._collection_name = collection_name

        self._database = None
        self._collection = None

    @property
    def database(self):
        if not self._client:
            raise MongoRepositoryBaseException('Invalid connection.')

        if self._database is None:
            self._database = self._get_database(self._database_name)

        return self._database

    @database.setter
    def database(self, database_name):
        self._database_name = database_name
        self._database = self._get_database(self._database_name)

    @database.deleter
    def database(self):
        del self._database

    @property
    def collection(self):
        if not self._client:
            raise MongoRepositoryBaseException('Invalid connection.')

        if self._collection is None:
            self._collection = self._get_collection(self._collection_name)

        return self._collection

    @collection.setter
    def collection(self, collection_name):
        self._collection_name = collection_name
        self._collection = self._get_collection(self._collection_name)

    @collection.deleter
    def collection(self):
        del self._collection

    def _get_database(self, database_name):
        available_databases = self._client.list_database_names()
        if database_name not in available_databases:
            # Log warning that database does not exist, will be created
            pass

        return self._client[database_name]

    def _get_collection(self, collection_name):
        available_collections = self.database.list_collection_names()
        if collection_name not in available_collections:
            # Log warning that collection does not exist, will be created
            pass

        return self.database[collection_name]

    def get_distinct_by_key(self, key):
        return self._collection.distinct(key)

    def get_all_collections(self):
        return self.database.list_collection_names()

    def add_one(self, document):
        try:
            self.collection.insert_one(document)
        except Exception as e:
            raise MongoRepositoryBaseException(e)

    def add_many(self, documents):
        try:
            self.collection.insert_many(documents)
        except Exception as e:
            raise MongoRepositoryBaseException(e)

    def get_all(self):
        try:
            results = self.collection.find({}, {"_id": 0})
        except Exception as e:
            raise MongoRepositoryBaseException(e)

        return list(results)

    def get_all_by_key(self, key, values):
        query = {
            key: {
                "$in": values
            }
        }

        try:
            results = self.collection.find(query, {"_id": 0})
        except Exception as e:
            raise MongoRepositoryBaseException(e)

        return list(results)

    def get_first_by_key(self, key, values):
        results = self.get_all_by_key(key, values)
        if results:
            return results[0]
        else:
            raise MongoRepositoryBaseException(NotImplementedError)

    def get_last_updated_structures(self, last_updated_date_time):
        query = {
            "last_updated": {
                "$gt": last_updated_date_time.strftime("%Y-%m-%dT%H:%M:%s")
            }
        }

        try:
            results = self.collection.find(query, {"_id": 0})
        except Exception as e:
            raise MongoRepositoryBaseException(e)

        return list(results)

    def find(self, query):
        try:
            results = self.collection.find(query)
        except Exception as e:
            raise MongoRepositoryBaseException(e)

        return list(results)

    def first_or_default(self, query):
        try:
            results = self.find(query)
            if results:
                return results[0]
            else:
                return {}
        except Exception as e:
            raise MongoRepositoryBaseException(e)

    def update(self, query_filter, query):
        try:
            result = self.collection.update(query_filter, query)
            return result['nModified']
        except Exception as e:
            raise MongoRepositoryBaseException(e)

    def update_many(self, query_filter, query):
        try:
            result = self.collection.update_many(query_filter, query)
            return result['nModified']
        except Exception as e:
            raise MongoRepositoryBaseException(e)
