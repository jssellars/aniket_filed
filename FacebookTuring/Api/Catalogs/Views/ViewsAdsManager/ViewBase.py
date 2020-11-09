from dataclasses import dataclass, field
from typing import List, Optional


class View:
    name = None
    table_name = None
    type = None
    filters = None
    breakdowns = None
    columns = []


@dataclass
class AgGridView:
    name: str
    id: int = 0
    is_default: bool = False
    is_selected: bool = False
    columns: List = field(default_factory=list)
