import typing

from Core.Tools.MongoRepository.MongoRepositoryBase import MongoRepositoryBase


class MongoLogger:
    class Logger:
        COLLECTION_NAME = 'logs'

        def __init__(self, repository: MongoRepositoryBase = None, database_name: typing.AnyStr = None):
            self.__repository = repository
            self.__repository.set_database(database_name)
            self.__repository.set_collection(self.COLLECTION_NAME)

        def info(self, message: typing.Dict = None):
            self.__repository.add_one(message)

    def __init__(self, repository: MongoRepositoryBase = None, database_name: typing.AnyStr = None):
        self.logger = self.Logger(repository, database_name)
