from Core.mongo_adapter import MongoRepositoryBase


class LoggingMongoRepository(MongoRepositoryBase):

    def __init__(self, *args, **kwargs):
        super(LoggingMongoRepository, self).__init__(*args, **kwargs)
