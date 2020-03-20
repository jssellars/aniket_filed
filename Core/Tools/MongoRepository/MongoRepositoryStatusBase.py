from enum import Enum


class MongoRepositoryStatusBase(Enum):
    ACTIVE = 1
    REMOVED = 2
    DEPRECATED = 3
