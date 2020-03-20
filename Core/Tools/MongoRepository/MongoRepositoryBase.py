# todo: make this work with arbitrary objects that extend JsonType or dataclass
from dataclasses import asdict
from datetime import datetime
from enum import Enum

import typing

from Core.Tools.Misc.ObjectSerializers import object_to_json
from Core.Tools.MongoRepository.MongoConnectionHandler import MongoConnectionHandler
from Core.Tools.MongoRepository.MongoOperator import MongoOperator
from Core.Tools.MongoRepository.MongoRepositoryStatusBase import MongoRepositoryStatusBase


class MongoProjectionState(Enum):
    ON = 1
    OFF = 0


class MongoRepositoryBase:

    def __init__(self, client=None, database_name=None, collection_name=None, config=None):
        if client is None and config is None:
            raise ValueError("Cannot instantiate a Mongo Repository. Please try again using either a Mongo client or a Mongo config.")

        if config is None:
            self._client = client
            self.connection_handler = None

        if config is not None:
            self.connection_handler = MongoConnectionHandler(config)
            self._client = self.connection_handler.client

        self._database_name = database_name
        self._collection_name = collection_name

        self._database = None
        self._collection = None

    @property
    def database(self):
        if not self._client:
            raise Exception('Invalid connection.')
        
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
            raise Exception('Invalid connection.')

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

    def set_collection(self, collection_name):
        self._collection = collection_name
        self._collection_name = collection_name

    def add_one(self, document=None):
        if not document:
            return

        try:
            self.collection.insert_one(self._convert_to_dict(document))
        except Exception as e:
            raise e

    def add_many(self, documents=None):
        if not documents:
            return

        try:
            documents = [self._convert_to_dict(document) for document in documents]
            self.collection.insert_many(documents)
        except Exception as e:
            raise e

    def get_all(self):
        try:
            results = self.collection.find({}, {"_id": MongoProjectionState.OFF.value})
        except Exception as e:
            raise e

        return list(results)

    def get_all_by_key(self, key=None, values=None):
        query = {
            key: {
                MongoOperator.IN.value: values
            }
        }

        try:
            results = self.collection.find(query, {"_id": MongoProjectionState.OFF.value})
        except Exception as e:
            raise e

        return list(results)

    def get_first_by_key(self, key=None, values=None):
        results = self.get_all_by_key(key, values)
        if results:
            return results[0]
        else:
            raise NotImplementedError

    def get_last_updated(self, last_updated_datetime=None):
        query = {
            "last_updated": {
                MongoOperator.GREATERTHANEQUAL.value: last_updated_datetime.strftime("%Y-%m-%dT%H:%M:%s")
            }
        }

        try:
            results = self.collection.find(query, {"_id": MongoProjectionState.OFF.value})
        except Exception as e:
            raise e

        return list(results)

    def get(self, query=None):
        try:
            results = self.collection.find(query)
        except Exception as e:
            raise e

        return list(results)

    def get_id_and_name_by_key(self, key=None, values=None, id_key="id", name_key="name"):
        query = {
            key: {
                MongoOperator.IN.value: values
            }
        }
        projection = {
            "_id": MongoProjectionState.OFF.value,
            id_key: MongoProjectionState.ON.value,
            name_key: MongoProjectionState.ON.value
        }

        try:
            results = self.collection.find(query, projection)
        except Exception as e:
            raise e

        return list(results)

    def first_or_default(self, query=None):
        try:
            results = self.get(query)
            if results:
                return results[0]
            else:
                return {}
        except Exception as e:
            raise e

    def update_one(self, query_filter=None, query=None):
        try:
            result = self.collection.update(query_filter, query)
            return result['nModified']
        except Exception as e:
            raise e

    def update_many(self, query_filter=None, query=None):
        try:
            result = self.collection.update_many(query_filter, query)
            return result['nModified']
        except Exception as e:
            raise e

    def change_status(self, id=None, new_status=None, id_key="facebook_id"):
        query_filter = {
            id_key: {
                MongoOperator.EQUALS.value: id
            },
            "status": {
                MongoOperator.EQUALS.value: MongoRepositoryStatusBase.ACTIVE.value
            }
        }
        query = {
            MongoOperator.SET.value: {
                "status": new_status,
                "last_updated_at": datetime.now()
            }
        }
        return self.update_one(query_filter, query)

    def change_status_to_match_facebook(self, id=None, facebook_last_updated_at=None, new_status=None, id_key="facebook_id"):
        query_filter = {
            MongoOperator.AND.value: [{
                id_key: {
                    MongoOperator.EQUALS.value: id
                }
            },
                {
                    "last_updated_at": {
                        MongoOperator.LESSTHAN.value: facebook_last_updated_at

                    }
                }]
        }

        query = {
            MongoOperator.SET.value: {
                "status": new_status,
                "last_updated_at": datetime.now()
            }
        }

        return self.update_many(query_filter, query)

    def change_status_many(self, ids=None, new_status=None, id_key="facebook_id"):
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

    def add_updated_structure(self, document=None, id_key="facebook_id"):
        query_filter = {
            id_key: {
                MongoOperator.EQUALS.value: getattr(document, id_key)
            }
        }

        query = {
            MongoOperator.SET.value: {
                "status": MongoRepositoryStatusBase.DEPRECATED.value,
                "last_updated_on": datetime.now()
            }
        }

        self.update_one(query_filter, query)

        try:
            self.add_one(self._convert_to_dict(document))
        except Exception as e:
            raise e

    def _convert_to_dict(self, data):
        if isinstance(data, typing.Mapping):
            return data

        return object_to_json(data)