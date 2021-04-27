import typing
from dataclasses import dataclass
from typing import Optional

from Core.Tools.Misc.AgGridConstants import PinnedDirection
from Core.Web.GoogleAdsAPI.Models.GoogleField import GoogleField


@dataclass
class ViewColumn:
    id_: str = None
    display_name: typing.AnyStr = None
    primary_value: GoogleField = None
    secondary_value: GoogleField = None
    type_id: int = None  # ViewColumnTypeEnum
    actions: typing.List[typing.Any] = None
    category_id: id = None  # ViewColumnCategoryEnum
    width: int = 50
    is_fixed: bool = False
    group_display_name: typing.AnyStr = None  # ViewColumnGroupEnum
    hidden: bool = False
    is_filterable: bool = False
    is_editable: bool = False
    is_sortable: bool = False
    no_of_decimals: int = 0
    pinned: Optional[PinnedDirection] = None
    description: Optional[str] = None
    is_toggle: Optional[bool] = False
    objective_filtering: Optional[bool] = False
