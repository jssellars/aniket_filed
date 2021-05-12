from dataclasses import dataclass
from typing import Any, List, Optional, Union

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


@dataclass
class QueryBuilderGoogleUpdateInfo:
    field: str
    value: Any
    campaign_id: Optional[str] = None
    ad_group_id: Optional[str] = None
    keyword_id: Optional[str] = None
