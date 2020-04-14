from enum import Enum


class LogicOperatorEnum(Enum):
    AND = 1
    OR = 2
    NOT = 3
    EQUALS = 4
    NOT_EQUAL = 5
    EQUAL_OR_GREATER_THAN = 6
    EQUAL_OR_LESS_THAN = 7
    GREATER_THAN = 8
    LESS_THAN = 9
    IN = 10
    NOT_IN = 11