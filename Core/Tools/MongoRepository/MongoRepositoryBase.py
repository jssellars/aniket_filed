import typing
from datetime import datetime
from enum import Enum

from Core.Tools.Logger.Helpers import log_operation_mongo
from Core.Tools.Logger.LoggerMessageBase import LoggerMessageTypeEnum
from Core.Tools.Logger.LoggingLevelEnum import LoggingLevelEnum
from Core.Tools.Misc.ObjectSerializers import object_to_json
from Core.Tools.MongoRepository.MongoConnectionHandler import MongoConnectionHandler
from Core.Tools.MongoRepository.MongoOperator import MongoOperator
from FacebookTuring.Infrastructure.Domain.MiscFieldsEnum import MiscFieldsEnum
from FacebookTuring.Infrastructure.Domain.StructureStatusEnum import StructureStatusEnum
from pymongo.errors import AutoReconnect
from retry import retry


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
            logger=None,
    ):
        self._logger = logger

        if client is None and config is None:
            log_operation_mongo(
                logger=self._logger,
                log_level=LoggerMessageTypeEnum.ERROR,
                description="Cannot instantiate a Mongo Repository. Please try again using "
                            "either a Mongo client or a Mongo config.",
            )
            raise ValueError(
                "Cannot instantiate a Mongo Repository. Please try again using "
                "either a Mongo client or a Mongo config."
            )

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
        operation_start_time = datetime.now()

        if not document:
            return

        try:
            self.collection.insert_one(self._convert_to_dict(document))
        except Exception as e:
            operation_end_time = datetime.now()
            duration = (operation_end_time - operation_start_time).total_seconds()
            log_operation_mongo(
                logger=self._logger,
                log_level=LoggerMessageTypeEnum.ERROR,
                data=document,
                description="Failed to add one document. Reason %s" % str(e),
                timestamp=operation_end_time,
                duration=duration,
            )
            raise e

        if self._logger.level == LoggingLevelEnum.DEBUG.value:
            operation_end_time = datetime.now()
            duration = (operation_end_time - operation_start_time).total_seconds()
            log_operation_mongo(
                logger=self._logger,
                log_level=LoggerMessageTypeEnum.EXEC_DETAILS,
                data=document,
                description="Add one document.",
                timestamp=operation_end_time,
                duration=duration,
            )

    @retry(AutoReconnect, tries=__RETRY_LIMIT__, delay=1)
    def add_many(self, documents: typing.List[typing.Any] = None) -> typing.NoReturn:
        operation_start_time = datetime.now()

        if not documents:
            return
        try:
            documents = [self._convert_to_dict(document) for document in documents]
            result = self.collection.insert_many(documents)
            inserted_ids = result.inserted_ids

            operation_end_time = datetime.now()
            duration = (operation_end_time - operation_start_time).total_seconds()
            description_message = "All documents were successfully inserted."
            log_level = LoggerMessageTypeEnum.INFO

            if len(inserted_ids) == 0:
                description_message = "Failed to insert any document."
                log_level = LoggerMessageTypeEnum.ERROR

            if len(inserted_ids) < len(documents):
                description_message = "Failed to insert all documents. No of documents inserted %d out of %d" % (len(inserted_ids), len(documents))
                log_level = LoggerMessageTypeEnum.WARNING

            log_operation_mongo(
                logger=self._logger,
                log_level=log_level,
                data=documents,
                description=description_message,
                timestamp=operation_end_time,
                duration=duration,
            )

        except Exception as e:
            operation_end_time = datetime.now()
            duration = (operation_end_time - operation_start_time).total_seconds()
            log_operation_mongo(
                logger=self._logger,
                log_level=LoggerMessageTypeEnum.ERROR,
                data=documents,
                description="Failed to add many documents. Reason %s" % str(e),
                timestamp=operation_end_time,
                duration=duration,
            )
            raise e

        if self._logger.level == LoggingLevelEnum.DEBUG.value:
            operation_end_time = datetime.now()
            duration = (operation_end_time - operation_start_time).total_seconds()
            log_operation_mongo(
                logger=self._logger,
                log_level=LoggerMessageTypeEnum.EXEC_DETAILS,
                data=documents,
                description="Add one document.",
                timestamp=operation_end_time,
                duration=duration,
            )

    @retry(AutoReconnect, tries=__RETRY_LIMIT__, delay=1)
    def get_all(self) -> typing.List[typing.Dict]:
        operation_start_time = datetime.now()

        try:
            results = self.collection.find({}, {MongoOperator.GROUP_KEY.value: MongoProjectionState.OFF.value})
            results = list(results)
        except Exception as e:
            operation_end_time = datetime.now()
            duration = (operation_end_time - operation_start_time).total_seconds()
            log_operation_mongo(
                logger=self._logger,
                log_level=LoggerMessageTypeEnum.ERROR,
                description="Failed to get all documents. Reason %s" % str(e),
                timestamp=operation_end_time,
                duration=duration,
            )
            raise e

        if self._logger.level == LoggingLevelEnum.DEBUG.value:
            operation_end_time = datetime.now()
            duration = (operation_end_time - operation_start_time).total_seconds()
            log_operation_mongo(
                logger=self._logger,
                log_level=LoggerMessageTypeEnum.EXEC_DETAILS,
                data=results,
                description="Get all documents.",
                timestamp=operation_end_time,
                duration=duration,
            )

        return results

    @retry(AutoReconnect, tries=__RETRY_LIMIT__, delay=1)
    def get_all_by_key(self, key_name: typing.AnyStr = None, key_value: typing.Any = None) -> typing.List[typing.Dict]:
        operation_start_time = datetime.now()

        query = {key_name: {MongoOperator.EQUALS.value: key_value}}
        try:
            results = self.collection.find(query, {MongoOperator.GROUP_KEY.value: MongoProjectionState.OFF.value})
            results = list(results)
        except Exception as e:
            operation_end_time = datetime.now()
            duration = (operation_end_time - operation_start_time).total_seconds()
            log_operation_mongo(
                logger=self._logger,
                log_level=LoggerMessageTypeEnum.ERROR,
                description="Failed to get all documents "
                            "by key: %s with value: %s. Reason: %s" % (key_name, key_value, str(e)),
                timestamp=operation_end_time,
                duration=duration,
            )
            raise e

        if self._logger.level == LoggingLevelEnum.DEBUG.value:
            operation_end_time = datetime.now()
            duration = (operation_end_time - operation_start_time).total_seconds()
            log_operation_mongo(
                logger=self._logger,
                log_level=LoggerMessageTypeEnum.EXEC_DETAILS,
                data=results,
                description="Get all documents by key: %s with value: %s." % (key_name, key_value),
                timestamp=operation_end_time,
                duration=duration,
            )

        return results

    @retry(AutoReconnect, tries=__RETRY_LIMIT__, delay=1)
    def get_first_by_key(self, key_name: typing.AnyStr = None, key_value: typing.Any = None) -> typing.Dict:
        operation_start_time = datetime.now()

        try:
            results = self.get_all_by_key(key_name, key_value)
            if results:
                results = results[0]
            else:
                results = {}
        except Exception as e:
            operation_end_time = datetime.now()
            duration = (operation_end_time - operation_start_time).total_seconds()
            log_operation_mongo(
                logger=self._logger,
                log_level=LoggerMessageTypeEnum.ERROR,
                description="Failed to get first document "
                            "by key: %s with value: %s. Reason: %s" % (key_name, key_value, str(e)),
                timestamp=operation_end_time,
                duration=duration,
            )
            raise e

        if self._logger.level == LoggingLevelEnum.DEBUG.value:
            operation_end_time = datetime.now()
            duration = (operation_end_time - operation_start_time).total_seconds()
            log_operation_mongo(
                logger=self._logger,
                log_level=LoggerMessageTypeEnum.EXEC_DETAILS,
                data=results,
                description="Get first document by key: %s with value: %s." % (key_name, key_value),
                timestamp=operation_end_time,
                duration=duration,
            )

        return results

    @retry(AutoReconnect, tries=__RETRY_LIMIT__, delay=1)
    def get_last_updated(self, key_name: typing.AnyStr = None, key_value: datetime = None) -> typing.List[typing.Dict]:
        operation_start_time = datetime.now()

        query = {key_name: {MongoOperator.GREATERTHANEQUAL.value: key_value}}
        try:
            results = self.collection.find(query, {MongoOperator.GROUP_KEY.value: MongoProjectionState.OFF.value})
            results = list(results)
        except Exception as e:
            operation_end_time = datetime.now()
            duration = (operation_end_time - operation_start_time).total_seconds()
            log_operation_mongo(
                logger=self._logger,
                log_level=LoggerMessageTypeEnum.ERROR,
                description="Failed to get last updated documents "
                            "by key: %s with value: %s. Reason: %s" % (key_name, key_value, str(e)),
                timestamp=operation_end_time,
                duration=duration,
            )
            raise e

        if self._logger.level == LoggingLevelEnum.DEBUG.value:
            operation_end_time = datetime.now()
            duration = (operation_end_time - operation_start_time).total_seconds()
            log_operation_mongo(
                logger=self._logger,
                log_level=LoggerMessageTypeEnum.EXEC_DETAILS,
                data=results,
                description="Get last updated documents by key: %s with value: %s." % (key_name, key_value),
                timestamp=operation_end_time,
                duration=duration,
            )

        return results

    @retry(AutoReconnect, tries=__RETRY_LIMIT__, delay=1)
    def get(self, query: typing.Dict = None, projection: typing.Dict = None) -> typing.List[typing.Dict]:
        operation_start_time = datetime.now()

        try:
            if not projection:
                results = list(self.collection.find(query))
            else:
                results = list(self.collection.find(query, projection))
        except Exception as e:
            operation_end_time = datetime.now()
            duration = (operation_end_time - operation_start_time).total_seconds()
            log_operation_mongo(
                logger=self._logger,
                log_level=LoggerMessageTypeEnum.ERROR,
                description="Failed to get documents. Reason: %s" % str(e),
                timestamp=operation_end_time,
                duration=duration,
                query=query,
                projection=projection,
            )
            raise e

        if self._logger.level == LoggingLevelEnum.DEBUG.value:
            operation_end_time = datetime.now()
            duration = (operation_end_time - operation_start_time).total_seconds()
            log_operation_mongo(
                logger=self._logger,
                log_level=LoggerMessageTypeEnum.EXEC_DETAILS,
                data=results,
                description="Get documents",
                timestamp=operation_end_time,
                duration=duration,
                query=query,
                projection=projection,
            )

        return results

    @retry(AutoReconnect, tries=__RETRY_LIMIT__, delay=1)
    def get_sorted(
            self, query: typing.Dict = None, projection: typing.Dict = None, sort_query: typing.Dict = None
    ) -> typing.List[typing.Dict]:
        operation_start_time = datetime.now()

        try:
            if not projection:
                results = list(self.collection.find(query).sort(sort_query))
            else:
                results = list(self.collection.find(query, projection).sort(sort_query))
        except Exception as e:
            operation_end_time = datetime.now()
            duration = (operation_end_time - operation_start_time).total_seconds()
            log_operation_mongo(
                logger=self._logger,
                log_level=LoggerMessageTypeEnum.ERROR,
                description="Failed to get sorted documents. Reason: %s" % str(e),
                timestamp=operation_end_time,
                duration=duration,
                query=query,
                projection=projection,
                query_filter=sort_query,
            )
            raise e

        if self._logger.level == LoggingLevelEnum.DEBUG.value:
            operation_end_time = datetime.now()
            duration = (operation_end_time - operation_start_time).total_seconds()
            log_operation_mongo(
                logger=self._logger,
                log_level=LoggerMessageTypeEnum.EXEC_DETAILS,
                data=results,
                description="Get sorted documents",
                timestamp=operation_end_time,
                duration=duration,
                query=query,
                projection=projection,
                query_filter=sort_query,
            )

        return results

    @retry(AutoReconnect, tries=__RETRY_LIMIT__, delay=1)
    def first_or_default(self, query: typing.Dict = None, projection: typing.Dict = None) -> typing.Dict:
        operation_start_time = datetime.now()

        try:
            results = self.get(query, projection)
            if results:
                results = results[0]
            else:
                results = {}
        except Exception as e:
            operation_end_time = datetime.now()
            duration = (operation_end_time - operation_start_time).total_seconds()
            log_operation_mongo(
                logger=self._logger,
                log_level=LoggerMessageTypeEnum.ERROR,
                description="Failed to get first or default document. Reason: %s" % str(e),
                timestamp=operation_end_time,
                duration=duration,
                query=query,
                projection=projection,
            )
            raise e

        if self._logger.level == LoggingLevelEnum.DEBUG.value:
            operation_end_time = datetime.now()
            duration = (operation_end_time - operation_start_time).total_seconds()
            log_operation_mongo(
                logger=self._logger,
                log_level=LoggerMessageTypeEnum.EXEC_DETAILS,
                data=results,
                description="Get first or default.",
                timestamp=operation_end_time,
                duration=duration,
                query=query,
                projection=projection,
            )

        return results

    @retry(AutoReconnect, tries=__RETRY_LIMIT__, delay=1)
    def update_one(self, query_filter: typing.Dict = None, query: typing.Dict = None) -> typing.NoReturn:
        operation_start_time = datetime.now()

        try:
            self.collection.update(query_filter, query)
        except Exception as e:
            operation_end_time = datetime.now()
            duration = (operation_end_time - operation_start_time).total_seconds()
            log_operation_mongo(
                logger=self._logger,
                log_level=LoggerMessageTypeEnum.ERROR,
                description="Failed to update one document. Reason: %s" % str(e),
                timestamp=operation_end_time,
                duration=duration,
                query_filter=query_filter,
                query=query,
            )
            raise e

        if self._logger.level == LoggingLevelEnum.DEBUG.value:
            operation_end_time = datetime.now()
            duration = (operation_end_time - operation_start_time).total_seconds()
            log_operation_mongo(
                logger=self._logger,
                log_level=LoggerMessageTypeEnum.EXEC_DETAILS,
                description="Update one document",
                timestamp=operation_end_time,
                duration=duration,
                query_filter=query_filter,
                query=query,
            )

    @retry(AutoReconnect, tries=__RETRY_LIMIT__, delay=1)
    def update_many(self, query_filter: typing.Dict = None, query: typing.Dict = None) -> typing.NoReturn:
        operation_start_time = datetime.now()

        try:
            self.collection.update_many(query_filter, query)
        except Exception as e:
            operation_end_time = datetime.now()
            duration = (operation_end_time - operation_start_time).total_seconds()
            log_operation_mongo(
                logger=self._logger,
                log_level=LoggerMessageTypeEnum.ERROR,
                description="Failed to update many documents. Reason: %s" % str(e),
                timestamp=operation_end_time,
                duration=duration,
                query_filter=query_filter,
                query=query,
            )
            raise e

        if self._logger.level == LoggingLevelEnum.DEBUG.value:
            operation_end_time = datetime.now()
            duration = (operation_end_time - operation_start_time).total_seconds()
            log_operation_mongo(
                logger=self._logger,
                log_level=LoggerMessageTypeEnum.EXEC_DETAILS,
                description="Update one document",
                timestamp=operation_end_time,
                duration=duration,
                query_filter=query_filter,
                query=query,
            )

    @retry(AutoReconnect, tries=__RETRY_LIMIT__, delay=1)
    def update_structure_status(self, structure_key: typing.Dict = None, structure_ids: typing.List = None) -> None:
        query_filter = ""
        query = ""
        operation_start_time = datetime.now()

        try:
            query_filter = {structure_key: {MongoOperator.IN.value: structure_ids}}
            query = {MongoOperator.SET.value: {MiscFieldsEnum.status: StructureStatusEnum.COMPLETED.value}}
            self.update_many(query_filter, query)

        except Exception as e:
            operation_end_time = datetime.now()
            duration = (operation_end_time - operation_start_time).total_seconds()
            log_operation_mongo(
                logger=self._logger,
                log_level=LoggerMessageTypeEnum.ERROR,
                description="Failed to update many documents. Reason: %s" % str(e),
                timestamp=operation_end_time,
                duration=duration,
                query_filter=query_filter,
                query=query,
            )
            raise e

        if self._logger.level == LoggingLevelEnum.DEBUG.value:
            operation_end_time = datetime.now()
            duration = (operation_end_time - operation_start_time).total_seconds()
            log_operation_mongo(
                logger=self._logger,
                log_level=LoggerMessageTypeEnum.EXEC_DETAILS,
                description="Update one document",
                timestamp=operation_end_time,
                duration=duration,
                query_filter=query_filter,
                query=query,
            )

    @retry(AutoReconnect, tries=__RETRY_LIMIT__, delay=1)
    def delete_many_older_than_date(self, date: typing.AnyStr = None) -> typing.NoReturn:
        operation_start_time = datetime.now()
        query = {}

        try:
            query = {"date_start": {MongoOperator.LESSTHANEQUAL.value: date}}
            self.collection.delete_many(query)

        except Exception as e:
            operation_end_time = datetime.now()
            duration = (operation_end_time - operation_start_time).total_seconds()
            log_operation_mongo(
                logger=self._logger,
                log_level=LoggerMessageTypeEnum.ERROR,
                description="Failed to delete many documents. Reason: %s" % str(e),
                timestamp=operation_end_time,
                duration=duration,
                query=query,
            )
            raise e

        if self._logger.level == LoggingLevelEnum.DEBUG.value:
            operation_end_time = datetime.now()
            duration = (operation_end_time - operation_start_time).total_seconds()
            log_operation_mongo(
                logger=self._logger,
                log_level=LoggerMessageTypeEnum.EXEC_DETAILS,
                description="Delete many documents",
                timestamp=operation_end_time,
                duration=duration,
                query=query,
            )

    @retry(AutoReconnect, tries=__RETRY_LIMIT__, delay=1)
    def get_collections(self) -> typing.List[str]:
        if self._database_name:
            return self.database.collection_names()
        return []

    @retry(AutoReconnect, tries=__RETRY_LIMIT__, delay=1)
    def delete_many(self, query_filter: typing.Dict = None) -> typing.NoReturn:
        operation_start_time = datetime.now()

        try:
            self.collection.delete_many(query_filter)

        except Exception as e:
            operation_end_time = datetime.now()
            duration = (operation_end_time - operation_start_time).total_seconds()
            log_operation_mongo(
                logger=self._logger,
                log_level=LoggerMessageTypeEnum.ERROR,
                description="Failed to delete many documents. Reason: %s" % str(e),
                timestamp=operation_end_time,
                duration=duration,
                query_filter=query_filter,
            )
            raise e

        if self._logger.level == LoggingLevelEnum.DEBUG.value:
            operation_end_time = datetime.now()
            duration = (operation_end_time - operation_start_time).total_seconds()
            log_operation_mongo(
                logger=self._logger,
                log_level=LoggerMessageTypeEnum.EXEC_DETAILS,
                description="Delete many documents",
                timestamp=operation_end_time,
                duration=duration,
                query_filter=query_filter,
            )

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
