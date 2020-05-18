from enum import Enum


class QueryBuilderLogicalOperator(Enum):
    EQUAL = 0
    GREATER_THAN = 1
    GREATER_THAN_OR_EQUAL = 2
    LESS_THAN = 3
    LESS_THAN_OR_EQUAL = 4
    NOT_EQUAL = 5
    IN = 6
