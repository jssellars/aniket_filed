import typing
from dataclasses import dataclass
from enum import Enum
from typing import Dict

from Core.Tools.Misc.EnumerationBase import EnumerationBase


@dataclass
class QueryBuilderColumn:
    Name: typing.AnyStr = None
    Aggregator: int = None


@dataclass
class QueryBuilderDimension:
    GroupColumnName: typing.AnyStr = None
    Name: typing.AnyStr = None


@dataclass
class QueryBuilderCondition:
    ColumnName: typing.AnyStr = None
    Operator: typing.AnyStr = None
    Value: typing.Union[typing.AnyStr, int, float] = None

    __keys = ["ColumnName", "Operator", "Value"]

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

    __structure_columns = []

    def __init__(self, query_builder_request, table_name):
        # get table name
        self.TableName = query_builder_request["TableName"]

        # get requested columns
        self.Columns = [QueryBuilderColumn(**column) for column in query_builder_request["Columns"]]

        # get requested dimensions
        self.Dimensions = [QueryBuilderDimension(**dimension) for dimension in query_builder_request["Dimensions"]]

        # get request conditions and filters
        self.Conditions = self.find_all_where_conditions(query_builder_request["Where"])

        # get sort parameters
        if "Sort" in query_builder_request:
            self.Sort = QueryBuilderSortCondition(
                Dimension=query_builder_request["Sort"]["Dimension"],
                Order=QueryBuilderSortEnum(query_builder_request["Sort"]["Order"]),
            )
        else:
            self.Sort = QueryBuilderSortCondition()

        self.table_name = table_name

        self.Google_breakdown = query_builder_request.get("Breakdown")

    def set_structure_columns(self, structure_columns: typing.List[typing.AnyStr] = None):
        self.__structure_columns = structure_columns
        return self

    def get_level(self):
        level = self.table_name.get_by_value(self.TableName).lower()
        if self.__structure_columns:
            has_structure_field = self.__has_structure_fields()
            if not has_structure_field:
                # this string literal should be removed and extracted into a generic level enum
                level = "account"
        return level

    def __has_structure_fields(self):
        # determine if it has a campaign structure filed. Stop searching for columns if a structure field is found
        # in the query.
        for column in self.Columns:
            if column.Name in self.__structure_columns:
                return True
        for column in self.Dimensions:
            if column.GroupColumnName in self.__structure_columns:
                return True
        return False

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


class AgGridInsightsRequest:

    __structure_columns = []

    def __init__(self, query_builder_request: Dict):
        self.ag_columns = query_builder_request["agColumns"].split(", ")
        self.next_page_cursor = query_builder_request["nextPageCursor"]
        self.filter_model = query_builder_request["filterModel"]
        self.filter_objective = query_builder_request.get("filterObjective")
        self.sort_model = query_builder_request["sortModel"]
        self.time_range = query_builder_request["timeRange"]
        self.facebook_account_id = query_builder_request.get("facebookAccountId")
        self.google_account_id = query_builder_request.get("googleAccountId")
        self.google_manager_id = query_builder_request.get("googleManagerId")
        self.page_size = query_builder_request["pageSize"]
        self.has_delivery = query_builder_request.get("hasDelivery", True)
        self.start_row = query_builder_request["startRow"]
        self.end_row = query_builder_request["endRow"]


class AgGridTrendRequest:

    __structure_columns = []

    def __init__(self, query_builder_request: Dict):
        self.ag_columns = query_builder_request["agColumns"].split(", ")
        self.filter_model = query_builder_request["filterModel"]
        self.time_range = query_builder_request["timeRange"]
        self.facebook_account_id = query_builder_request["facebookAccountId"]
