import typing

from Core.Tools.MongoRepository.MongoRepositoryBase import MongoRepositoryBase


class MongoLogger:
    _instance = None

    class Logger:
        COLLECTION_NAME = 'logs'

        def __init__(self, repository: MongoRepositoryBase = None, database_name: typing.AnyStr = None):
            self.__repository = repository.new_repository()
            self.__repository.set_database(database_name)
            self.__repository.set_collection(self.COLLECTION_NAME)

        def info(self, message: typing.Dict = None):
            self.__repository.add_one(message)

    def __new__(self, repository: MongoRepositoryBase = None, database_name: typing.AnyStr = None):
        if self._instance is None:
            self._instance = super(MongoLogger, self).__new__(self)

        self.logger = MongoLogger.Logger(repository, database_name)

        return self._instance