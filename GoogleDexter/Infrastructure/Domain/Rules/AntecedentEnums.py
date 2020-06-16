from enum import Enum


class AntecedentTypeEnum(Enum):
    VALUE = 1
    VALUE_LIST = 2
    TREND = 3
    FUZZY_VALUE = 4
    FUZZY_TREND = 5
    CURRENT_VALUE = 6
    DIFFERENCE = 7
    PERCENTAGE_DIFFERENCE = 8
    WEIGHTED_FUZZY_TREND = 9
    WEIGHTED_TREND = 10
