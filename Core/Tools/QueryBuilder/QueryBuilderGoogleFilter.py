from dataclasses import dataclass
from typing import Any, List, Union

from Core.Tools.QueryBuilder.QueryBuilderLogicalOperator import AgGridGoogleOperator, QueryBuilderLogicalOperator


class QueryBuilderGoogleFilter:
    def __init__(self, condition, entry):
        self.field = condition.field_name
        self.operator = QueryBuilderLogicalOperator(entry.Operator)
        self.value = entry.Value


@dataclass
class QueryBuilderGoogleFilters:
    name: str
    operator: AgGridGoogleOperator
    value: Union[Any, List[Any]]


@dataclass
class QueryBuilderGoogleSort:
    field: str
    ascending: bool = True
