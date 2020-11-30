import sys
import typing
from datetime import datetime
from enum import Enum

from pymongo.errors import AutoReconnect
from retry import retry

from Core.Tools.Misc.ObjectSerializers import object_to_json
from Core.Tools.MongoRepository.MongoConnectionHandler import MongoConnectionHandler
from Core.Tools.MongoRepository.MongoOperator import MongoOperator


import logging

logger = logging.getLogger(__name__)


class MongoProjectionState(Enum):
    ON = 1
    OFF = 0


class MongoRepositoryBase:
    __RETRY_LIMIT__ = 3

    def __init__(
            self,
            client: typing.Any = None,
            database_name: typing.AnyStr = None,
            collection_name: typing.AnyStr = None,
            config: typing.Any = None,
    ):
        if client is None and config is None:
            message = (
                "Cannot instantiate a Mongo Repository."
                " Please try again using either a Mongo client or a Mongo config."
            )
            logger.error(message)
            raise ValueError(message)

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
            raise Exception("Invalid connection.")
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
            raise Exception("Invalid connection.")
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

    @retry(AutoReconnect, tries=__RETRY_LIMIT__, delay=1)
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

    @retry(AutoReconnect, tries=__RETRY_LIMIT__, delay=1)
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

    @retry(AutoReconnect, tries=__RETRY_LIMIT__, delay=1)
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

    @retry(AutoReconnect, tries=__RETRY_LIMIT__, delay=1)
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

    @retry(AutoReconnect, tries=__RETRY_LIMIT__, delay=1)
    def get_first_by_key(self, key_name: typing.AnyStr = None, key_value: typing.Any = None) -> typing.Dict:
        start = datetime.now()

        try:
            results = self.get_all_by_key(key_name, key_value)
            if results:
                results = results[0]
            else:
                results = {}
        except Exception as e:
            logger.error(
                f"Failed to get first document by key: {key_name} with value: {key_value} || {repr(e)}",
                extra=dict(duration=(datetime.now() - start).total_seconds()),
            )
            raise e

        return results

    @retry(AutoReconnect, tries=__RETRY_LIMIT__, delay=1)
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

    @retry(AutoReconnect, tries=__RETRY_LIMIT__, delay=1)
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

    @retry(AutoReconnect, tries=__RETRY_LIMIT__, delay=1)
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

    @retry(AutoReconnect, tries=__RETRY_LIMIT__, delay=1)
    def first_or_default(self, query: typing.Dict = None, projection: typing.Dict = None) -> typing.Dict:
        start = datetime.now()

        try:
            results = self.get(query, projection)
            if results:
                results = results[0]
            else:
                results = {}
        except Exception as e:
            logger.error(
                f"Failed to get first or default document || {repr(e)}",
                extra=dict(duration=(datetime.now() - start).total_seconds(), query=query, projection=projection),
            )
            raise e

        return results

    @retry(AutoReconnect, tries=__RETRY_LIMIT__, delay=1)
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

    @retry(AutoReconnect, tries=__RETRY_LIMIT__, delay=1)
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

    @retry(AutoReconnect, tries=__RETRY_LIMIT__, delay=1)
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

    @retry(AutoReconnect, tries=__RETRY_LIMIT__, delay=1)
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

    @retry(AutoReconnect, tries=__RETRY_LIMIT__, delay=1)
    def get_collections(self) -> typing.List[str]:
        if self._database_name:
            return self.database.collection_names()
        return []

    @retry(AutoReconnect, tries=__RETRY_LIMIT__, delay=1)
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
        if isinstance(data, typing.Mapping):
            return data
        return object_to_json(data)

    def new_repository(self):
        repository = MongoRepositoryBase(config=self.config, database_name=self.config.logs_database)
        return repository
