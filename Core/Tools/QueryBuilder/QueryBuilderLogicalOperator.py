from enum import Enum
from Core.Tools.Misc.EnumerationBase import EnumerationBase


class QueryBuilderLogicalOperator(Enum):
    EQUAL = 0
    GREATER_THAN = 1
    GREATER_THAN_OR_EQUAL = 2
    LESS_THAN = 3
    LESS_THAN_OR_EQUAL = 4
    NOT_EQUAL = 5
    IN = 6


class AgGridFacebookOperator(Enum):
    CONTAIN = "contains"
    NOT_CONTAIN = "notContains"
    EQUAL = "equals"
    NOT_EQUAL = "notEqual"
    STARTS_WITH = "startsWith"
    LESS_THAN = "lessThan"
    LESS_THAN_OR_EQUAL = "lessThanOrEqual"
    GREATER_THAN = "greaterThan"
    GREATER_THAN_OR_EQUAL = "greaterThanOrEqual"
    IN_RANGE = "inRange"
    NOT_IN_RANGE = "notInRange"
    IN = "inValues"
    NOT_IN = "notIn"
