import typing
from enum import Enum


def equals(x, y):
    return x == y


def not_equals(x, y):
    return not equals(x, y)


def is_in(x, y):
    return x in y


def not_is_in(x, y):
    return not is_in(x, y)


def is_like(x, y):
    return y.find(x) > -1


class ActionFieldConditionOperatorEnum(Enum):
    EQUALS = equals
    NOT_EQUALS = not_equals
    IN = is_in
    NOT_IN = not_is_in
    LIKE = is_like


FieldValueType = typing.Union[typing.AnyStr, typing.List[typing.AnyStr]]


class ActionFieldCondition:

    def __init__(self,
                 field_name: typing.AnyStr = None,
                 operator: ActionFieldConditionOperatorEnum = ActionFieldConditionOperatorEnum.EQUALS,
                 field_value: FieldValueType = None,
                 field_value_map: typing.Callable = None):
        self.field_name = field_name
        self.filter_operator = operator
        self.field_value = field_value
        self.field_value_map = field_value_map

    def evaluate(self, data: typing.Dict = None) -> bool:
        if self.field_value_map:
            self.field_value = self.field_value_map(data)
        try:
            return self.filter_operator(data[self.field_name], self.field_value)
        except Exception as e:
            raise NotImplementedError(str(e))
