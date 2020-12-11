import sys
import typing
from datetime import datetime
from enum import Enum

from pymongo import MongoClient
from pymongo.errors import AutoReconnect
from retry import retry
from sshtunnel import SSHTunnelForwarder

from Core import type_extensions, settings
from Core.Tools.Misc.ObjectSerializers import object_to_json

import logging

logger = logging.getLogger(__name__)


class MongoProjectionState(Enum):
    ON = 1
    OFF = 0


class MongoRepositoryStatus(Enum):
    ACTIVE = 1
    REMOVED = 2
    DEPRECATED = 3


class MongoOperator(Enum):
    DOLLAR_SIGN = "$"
    IN = "$in"
    NOTIN = "$nin"
    AND = "$and"
    OR = "$or"
    EQUALS = "$eq"
    NOTEQUAL = "$ne"
    GREATERTHANEQUAL = "$gte"
    GREATERTHAN = "$gt"
    LESSTHANEQUAL = "$lte"
    LESSTHAN = "$lt"
    SET = "$set"
    GROUP = "$group"
    GROUP_KEY = "_id"
    SORT = "$sort"
    MATCH = "$match"
    SUM = "$sum"
    AVERAGE = "$avg"
    MIN = "$min"
    MAX = "$max"


class MongoRepositoryBase:
    RETRY_COUNT = 3

    def __init__(
        self,
        client: typing.Any = None,
        database_name: typing.AnyStr = None,
        collection_name: typing.AnyStr = None,
        config: typing.Any = None,
    ) -> None:
        self._client = client
        self._database_name = database_name
        self._collection_name = collection_name
        self._config = config

        self._connection_handler = None
        self._database = None
        self._collection = None

        if self._client is None and self._config is None:
            message = (
                "Cannot instantiate a Mongo Repository."
                " Please try again using either a Mongo client or a Mongo config."
            )
            logger.error(message)
            raise ValueError(message)

        if self._config is not None:
            self._connection_handler = MongoAdapter(self._config)
            self._client = self._connection_handler.client

    @property
    def config(self):
        return self._config

    @property
    def database(self):
        if self._database is None:
            self._database = self._client[self._database_name]

        return self._database

    @database.setter
    def database(self, database_name: typing.AnyStr = None):
        self._database_name = database_name
        self._database = self._client[self._database_name]

    @database.deleter
    def database(self):
        del self._database

    @property
    def collection(self):
        self._collection = self.database[self._collection_name]

        return self._collection

    @collection.setter
    def collection(self, collection_name: typing.AnyStr = None):
        self._collection_name = collection_name
        self._collection = self.database[self._collection_name]

    @collection.deleter
    def collection(self):
        del self._collection

    @retry(AutoReconnect, tries=RETRY_COUNT, delay=1)
    def add_one(self, document: typing.Any = None) -> typing.NoReturn:
        start = datetime.now()

        if not document:
            return

        try:
            self.collection.insert_one(self._convert_to_dict(document))
        except Exception as e:
            logger.error(
                f"Failed to add one document || {repr(e)}",
                extra=dict(data_size=sys.getsizeof(document), duration=(datetime.now() - start).total_seconds()),
            )
            raise e

    @retry(AutoReconnect, tries=RETRY_COUNT, delay=1)
    def add_many(self, documents: typing.List[typing.Any] = None) -> typing.NoReturn:
        start = datetime.now()

        if not documents:
            return

        try:
            documents = [self._convert_to_dict(document) for document in documents]
            result = self.collection.insert_many(documents)
            inserted_ids = result.inserted_ids

            if len(inserted_ids) == 0:
                logger.error(
                    "Failed to insert any document.",
                    extra=dict(data_size=sys.getsizeof(documents), duration=(datetime.now() - start).total_seconds()),
                )

            if len(inserted_ids) < len(documents):
                logger.warning(
                    f"Failed to insert all documents."
                    f" No of documents inserted {len(inserted_ids)} out of {len(documents)}",
                    extra=dict(data_size=sys.getsizeof(documents), duration=(datetime.now() - start).total_seconds()),
                )

        except Exception as e:
            logger.error(
                f"Failed to add many documents || {repr(e)}",
                extra=dict(data_size=sys.getsizeof(documents), duration=(datetime.now() - start).total_seconds()),
            )
            raise e

    @retry(AutoReconnect, tries=RETRY_COUNT, delay=1)
    def get_all(self) -> typing.List[typing.Dict]:
        start = datetime.now()

        try:
            results = self.collection.find({}, {MongoOperator.GROUP_KEY.value: MongoProjectionState.OFF.value})
            results = list(results)
        except Exception as e:
            logger.error(
                f"Failed to get all documents || {repr(e)}",
                extra=dict(duration=(datetime.now() - start).total_seconds()),
            )
            raise e

        return results

    @retry(AutoReconnect, tries=RETRY_COUNT, delay=1)
    def get_all_by_key(self, key_name: typing.AnyStr = None, key_value: typing.Any = None) -> typing.List[typing.Dict]:
        start = datetime.now()

        query = {key_name: {MongoOperator.EQUALS.value: key_value}}
        try:
            results = self.collection.find(query, {MongoOperator.GROUP_KEY.value: MongoProjectionState.OFF.value})
            results = list(results)
        except Exception as e:
            logger.error(
                f"Failed to get all documents by key: {key_name} with value: {key_value} || {repr(e)}",
                extra=dict(duration=(datetime.now() - start).total_seconds()),
            )
            raise e

        return results

    @retry(AutoReconnect, tries=RETRY_COUNT, delay=1)
    def get_first_by_key(self, key_name: typing.AnyStr = None, key_value: typing.Any = None) -> typing.Dict:
        start = datetime.now()

        try:
            results = self.get_all_by_key(key_name, key_value)
            results = results[0] if results else {}
        except Exception as e:
            logger.error(
                f"Failed to get first document by key: {key_name} with value: {key_value} || {repr(e)}",
                extra=dict(duration=(datetime.now() - start).total_seconds()),
            )
            raise e

        return results

    @retry(AutoReconnect, tries=RETRY_COUNT, delay=1)
    def get_last_updated(self, key_name: typing.AnyStr = None, key_value: datetime = None) -> typing.List[typing.Dict]:
        start = datetime.now()

        query = {key_name: {MongoOperator.GREATERTHANEQUAL.value: key_value}}
        try:
            results = self.collection.find(query, {MongoOperator.GROUP_KEY.value: MongoProjectionState.OFF.value})
            results = list(results)
        except Exception as e:
            logger.error(
                f"Failed to get last updated documents by key: {key_name} with value: {key_value} || {repr(e)}",
                extra=dict(duration=(datetime.now() - start).total_seconds()),
            )
            raise e

        return results

    @retry(AutoReconnect, tries=RETRY_COUNT, delay=1)
    def get(self, query: typing.Dict = None, projection: typing.Dict = None) -> typing.List[typing.Dict]:
        start = datetime.now()

        try:
            if not projection:
                results = list(self.collection.find(query))
            else:
                results = list(self.collection.find(query, projection))
        except Exception as e:
            logger.error(
                f"Failed to get documents || {repr(e)}",
                extra=dict(duration=(datetime.now() - start).total_seconds(), query=query, projection=projection),
            )
            raise e

        return results

    @retry(AutoReconnect, tries=RETRY_COUNT, delay=1)
    def get_sorted(
        self, query: typing.Dict = None, projection: typing.Dict = None, sort_query: typing.Dict = None
    ) -> typing.List[typing.Dict]:
        start = datetime.now()

        try:
            if not projection:
                results = list(self.collection.find(query).sort(sort_query))
            else:
                results = list(self.collection.find(query, projection).sort(sort_query))
        except Exception as e:
            logger.error(
                f"Failed to get sorted documents || {repr(e)}",
                extra=dict(
                    duration=(datetime.now() - start).total_seconds(),
                    query=query,
                    projection=projection,
                    query_filter=sort_query,
                ),
            )
            raise e

        return results

    @retry(AutoReconnect, tries=RETRY_COUNT, delay=1)
    def first_or_default(self, query: typing.Dict = None, projection: typing.Dict = None) -> typing.Dict:
        start = datetime.now()

        try:
            results = self.get(query, projection)
            results = results[0] if results else {}
        except Exception as e:
            logger.error(
                f"Failed to get first or default document || {repr(e)}",
                extra=dict(duration=(datetime.now() - start).total_seconds(), query=query, projection=projection),
            )
            raise e

        return results

    @retry(AutoReconnect, tries=RETRY_COUNT, delay=1)
    def update_one(self, query_filter: typing.Dict = None, query: typing.Dict = None) -> typing.NoReturn:
        start = datetime.now()

        try:
            self.collection.update(query_filter, query)
        except Exception as e:
            logger.error(
                f"Failed to update one document || {repr(e)}",
                extra=dict(duration=(datetime.now() - start).total_seconds(), query_filter=query_filter, query=query),
            )
            raise e

    @retry(AutoReconnect, tries=RETRY_COUNT, delay=1)
    def update_many(self, query_filter: typing.Dict = None, query: typing.Dict = None) -> typing.NoReturn:
        start = datetime.now()

        try:
            self.collection.update_many(query_filter, query)
        except Exception as e:
            logger.error(
                f"Failed to update many documents || {repr(e)}",
                extra=dict(duration=(datetime.now() - start).total_seconds(), query_filter=query_filter, query=query),
            )
            raise e

    @retry(AutoReconnect, tries=RETRY_COUNT, delay=1)
    def update_structure_status(
        self,
        structure_key: typing.Dict = None,
        structure_ids: typing.List = None,
        status_key: str = None,
        status_value: int = None,
    ) -> None:
        query_filter = ""
        query = ""
        start = datetime.now()

        try:
            query_filter = {structure_key: {MongoOperator.IN.value: structure_ids}}
            query = {MongoOperator.SET.value: {status_key: status_value}}
            self.update_many(query_filter, query)

        except Exception as e:
            logger.error(
                f"Failed to update many documents || {repr(e)}",
                extra=dict(duration=(datetime.now() - start).total_seconds(), query_filter=query_filter, query=query),
            )
            raise e

    @retry(AutoReconnect, tries=RETRY_COUNT, delay=1)
    def delete_many_older_than_date(self, date: typing.AnyStr = None) -> typing.NoReturn:
        start = datetime.now()
        query = {}

        try:
            query = {"date_start": {MongoOperator.LESSTHANEQUAL.value: date}}
            self.collection.delete_many(query)

        except Exception as e:
            logger.error(
                f"Failed to delete many documents || {repr(e)}",
                extra=dict(duration=(datetime.now() - start).total_seconds(), query=query),
            )
            raise e

    @retry(AutoReconnect, tries=RETRY_COUNT, delay=1)
    def get_collections(self) -> typing.List[str]:
        return self.database.collection_names() if self._database_name else []

    @retry(AutoReconnect, tries=RETRY_COUNT, delay=1)
    def delete_many(self, query_filter: typing.Dict = None) -> typing.NoReturn:
        start = datetime.now()

        try:
            self.collection.delete_many(query_filter)

        except Exception as e:
            logger.error(
                f"Failed to delete many documents || {repr(e)}",
                extra=dict(duration=(datetime.now() - start).total_seconds(), query_filter=query_filter),
            )
            raise e

    def close(self):
        self._client.close()

    @staticmethod
    def _convert_to_dict(data):
        return data if isinstance(data, typing.Mapping) else object_to_json(data)

    @classmethod
    def new_logs_repository(cls, config: settings.Mongo):
        return cls(
            config=config,
            database_name=config.logs_database,
            collection_name=config.logs_collection_name,
        )


class MongoAdapterException(Exception):
    pass


class MongoAdapter(metaclass=type_extensions.Singleton):
    LOCALHOST = "127.0.0.1"
    KEEP_ALIVE_INTERVAL_IN_SECONDS = 60 * 60 * 24  # 24h

    def __init__(self, config: settings.Mongo):
        self._config = config

        self._client = None
        self._ssh_tunnel = None

    @property
    def client(self):
        if not self._config.ssh_tunnel:
            self._client = MongoClient(self._config.connection_string_external)

            return self._client

        self._ssh_tunnel = SSHTunnelForwarder(
            ssh_address_or_host=(self._config.ssh_host, 22),
            ssh_username=self._config.ssh_username,
            ssh_password=self._config.ssh_password,
            remote_bind_address=(self._config.mongo_host_internal, self._config.mongo_port),
            set_keepalive=MongoAdapter.KEEP_ALIVE_INTERVAL_IN_SECONDS,
        )
        self._ssh_tunnel.start()
        self._client = MongoClient(
            host=MongoAdapter.LOCALHOST,
            port=self._ssh_tunnel.local_bind_port,
            username=self._config.mongo_username,
            password=self._config.mongo_password,
            retryWrites=self._config.retry_writes,
            maxIdleTimeMS=1000,
            serverSelectionTimeoutMS=60000,
            maxPoolSize=None,
        )

        return self._client

    def close(self):
        self._client.close()
        self._ssh_tunnel.close()


def filter_null_values_from_documents(documents):
    return [{k: v for k, v in document.items() if v is not None} for document in documents]
