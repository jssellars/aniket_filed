from enum import Enum


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
