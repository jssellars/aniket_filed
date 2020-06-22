import typing
from dataclasses import dataclass
from enum import Enum

from Core.Tools.Misc.EnumerationBase import EnumerationBase


@dataclass
class QueryBuilderColumn:
    Name: typing.AnyStr = None
    Aggregator: int = None


@dataclass
class QueryBuilderDimension:
    GroupColumnName: typing.AnyStr = None


@dataclass
class QueryBuilderCondition:
    ColumnName: typing.AnyStr = None
    Operator: typing.AnyStr = None
    Value: typing.Union[typing.AnyStr, int, float] = None

    __keys = ['ColumnName', 'Operator', 'Value']

    @classmethod
    def has_same_parameters(cls, other: typing.Any) -> bool:
        if not isinstance(other, dict):
            return False
        return list(other.keys()) == cls.__keys


class QueryBuilderSortEnum(Enum):
    ASCENDING = 1
    DESCENDING = 2


@dataclass
class QueryBuilderSortCondition:
    Dimension: typing.AnyStr = None
    Order: QueryBuilderSortEnum = None


class QueryBuilderRequestMapper:
    TableName = None
    Columns = None
    Dimensions = None
    Where = None
    Sort = None

    table_name = None

    def __init__(self, query_builder_request: typing.Dict = None, table_name: EnumerationBase = None):
        # get table name
        self.TableName = query_builder_request['TableName']

        # get requested columns
        self.Columns = [QueryBuilderColumn(**column) for column in query_builder_request['Columns']]

        # get requested dimensions
        self.Dimensions = [QueryBuilderDimension(**dimension) for dimension in query_builder_request['Dimensions']]

        # get request conditions and filters
        self.Conditions = self.find_all_where_conditions(query_builder_request['Where'])

        # get sort parameters
        if 'Sort' in query_builder_request:
            self.Sort = QueryBuilderSortCondition(Dimension=query_builder_request['Sort']['Dimension'],
                                                  Order=QueryBuilderSortEnum(query_builder_request['Sort']['Order']))
        else:
            self.Sort = QueryBuilderSortCondition()

        self.table_name = table_name

    def get_level(self):
        return self.table_name.get_by_value(self.TableName).lower()

    def get_report(self):
        return self.table_name.get_enum_by_value(self.TableName)

    @staticmethod
    def is_list(x: typing.Any = None) -> bool:
        return isinstance(x, list)

    @staticmethod
    def is_dict(x: typing.Any = None) -> bool:
        return isinstance(x, dict)

    @staticmethod
    def is_leaf(x: typing.Any = None) -> bool:
        return QueryBuilderCondition.has_same_parameters(x)

    # todo: map condition operator to QueryBuilderLogicalOperator
    @classmethod
    def find_all_where_conditions(cls, entry):
        leaves = []

        def find_all_conditions(entry):
            if cls.is_leaf(entry):
                leaves.append(QueryBuilderCondition(**entry))
            elif cls.is_dict(entry):
                for key, value in entry.items():
                    if (cls.is_list(value) or cls.is_dict(value)) and not cls.is_leaf(value):
                        find_all_conditions(value)
                    elif cls.is_leaf(value):
                        leaves.append(QueryBuilderCondition(**value))
                    else:
                        continue
            elif cls.is_list(entry):
                for element in entry:
                    if (cls.is_list(element) or cls.is_dict(element)) and not cls.is_leaf(element):
                        find_all_conditions(element)
                    elif cls.is_leaf(element):
                        leaves.append(QueryBuilderCondition(**element))
                    else:
                        continue

        find_all_conditions(entry)
        return leaves
