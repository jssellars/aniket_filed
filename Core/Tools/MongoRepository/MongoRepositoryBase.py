import typing
from datetime import datetime
from enum import Enum

from Core.Tools.Misc.ObjectSerializers import object_to_json
from Core.Tools.MongoRepository.MongoConnectionHandler import MongoConnectionHandler
from Core.Tools.MongoRepository.MongoOperator import MongoOperator


class MongoProjectionState(Enum):
    ON = 1
    OFF = 0


class MongoRepositoryBase:

    def __init__(self, client: typing.Any = None, database_name: typing.AnyStr = None,
                 collection_name: typing.AnyStr = None, config: typing.Any = None):
        if client is None and config is None:
            raise ValueError(
                "Cannot instantiate a Mongo Repository. Please try again using either a Mongo client or a Mongo config.")

        if config is None:
            self._client = client
            self.connection_handler = None

        if config is not None:
            self._config = config
            self.connection_handler = MongoConnectionHandler(self._config)
            self._client = self.connection_handler.client

        self._database_name = database_name
        self._collection_name = collection_name

        self._database = None
        self._collection = None

    @property
    def config(self):
        return self._config

    @property
    def database(self):
        if not self._client:
            raise Exception('Invalid connection.')
        if self._database is None:
            self._database = self._get_database(self._database_name)
        return self._database

    @database.setter
    def database(self, database_name: typing.AnyStr = None):
        self._database_name = database_name
        self._database = self._get_database(self._database_name)

    @database.deleter
    def database(self):
        del self._database

    @property
    def collection(self):
        if not self._client:
            raise Exception('Invalid connection.')
        self._collection = self._get_collection(self._collection_name)
        return self._collection

    @collection.setter
    def collection(self, collection_name: typing.AnyStr = None):
        self._collection_name = collection_name
        self._collection = self._get_collection(self._collection_name)

    @collection.deleter
    def collection(self):
        del self._collection

    def _get_database(self, database_name: typing.AnyStr = None):
        return self._client[database_name]

    def _get_collection(self, collection_name: typing.AnyStr = None):
        return self.database[collection_name]

    def set_database(self, database_name: typing.AnyStr = None):
        self._database_name = database_name
        self._database = self._client[self._database_name]

    def set_collection(self, collection_name: typing.AnyStr = None):
        self._collection = collection_name
        self._collection_name = collection_name

    def add_one(self, document: typing.Any = None) -> typing.NoReturn:
        if not document:
            return
        try:
            self.collection.insert_one(self._convert_to_dict(document))
        except Exception as e:
            raise e

    def add_many(self, documents: typing.List[typing.Any] = None) -> typing.NoReturn:
        if not documents:
            return
        try:
            documents = [self._convert_to_dict(document) for document in documents]
            self.collection.insert_many(documents)
        except Exception as e:
            raise e

    def get_all(self) -> typing.List[typing.Dict]:
        try:
            results = self.collection.find({}, {MongoOperator.GROUP_KEY.value: MongoProjectionState.OFF.value})
        except Exception as e:
            raise e
        return list(results)

    def get_all_by_key(self, key_name: typing.AnyStr = None, key_value: typing.Any = None) -> typing.List[typing.Dict]:
        query = {
            key_name: {
                MongoOperator.EQUALS.value: key_value
            }
        }
        try:
            results = self.collection.find(query, {MongoOperator.GROUP_KEY.value: MongoProjectionState.OFF.value})
        except Exception as e:
            raise e
        return list(results)

    def get_first_by_key(self, key_name: typing.AnyStr = None, key_value: typing.Any = None) -> typing.Dict:
        results = self.get_all_by_key(key_name, key_value)
        if results:
            return results[0]
        else:
            raise NotImplementedError

    def get_last_updated(self, key_name: typing.AnyStr = None, key_value: datetime = None) -> typing.List[typing.Dict]:
        query = {
            key_name: {
                MongoOperator.GREATERTHANEQUAL.value: key_value
            }
        }
        try:
            results = self.collection.find(query, {MongoOperator.GROUP_KEY.value: MongoProjectionState.OFF.value})
        except Exception as e:
            raise e
        return list(results)

    def get(self, query: typing.Dict = None, projection: typing.Dict = None) -> typing.List[typing.Dict]:
        try:
            if not projection:
                results = self.collection.find(query)
            else:
                results = self.collection.find(query, projection)
        except Exception as e:
            raise e
        return list(results)

    def first_or_default(self, query: typing.Dict = None, projection: typing.Dict = None) -> typing.Dict:
        try:
            results = self.get(query, projection)
            if results:
                return results[0]
            else:
                return {}
        except Exception as e:
            raise e

    def update_one(self, query_filter: typing.Dict = None, query: typing.Dict = None) -> typing.NoReturn:
        try:
            self.collection.update(query_filter, query)
        except Exception as e:
            raise e

    def update_many(self, query_filter: typing.Dict = None, query: typing.Dict = None) -> typing.NoReturn:
        try:
            self.collection.update_many(query_filter, query)
        except Exception as e:
            raise e

    def close(self):
        self._client.close()

    @staticmethod
    def _convert_to_dict(data):
        if isinstance(data, typing.Mapping):
            return data
        return object_to_json(data)

    def new_repository(self):
        repository = MongoRepositoryBase(config=self.config, database_name=self.config.logs_database)
        return repository
