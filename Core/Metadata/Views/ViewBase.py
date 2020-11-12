from dataclasses import dataclass, field
from typing import List


class BaseView:
    view_name = None
    table_name = None
    type = None
    # filters = None
    # breakdowns = None
    columns = None


@dataclass
class AgGridView:
    name: str
    id: int = 0
    is_default: bool = False
    is_selected: bool = False
    columns: List = field(default_factory=list)


@dataclass
class AgGridAccountsView:
    name: str
    id: int = 0
    account_structure_columns: List = field(default_factory=list)
    account_insight_columns: List = field(default_factory=list)
