from enum import Enum


class MongoOperator(Enum):
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