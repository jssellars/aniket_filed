import typing
from typing import Optional

from Core.Tools.Misc.AgGridConstants import PinnedDirection
from Core.Web.FacebookGraphAPI.Models.Field import Field


class ViewColumn:

    def __init__(self,
                 id: typing.Union[typing.AnyStr, int] = None,
                 display_name: typing.AnyStr = None,
                 primary_value: Field = None,
                 secondary_value: Field = None,
                 type_id: int = None,  # ViewColumnTypeEnum
                 actions: typing.List[typing.Any] = None,
                 category_id: id = None,  # ViewColumnCategoryEnum
                 width: int = 50,
                 is_fixed: bool = False,
                 group_display_name: typing.AnyStr = None,  # ViewColumnGroupEnum
                 hidden: bool = False,
                 is_filterable: bool = False,
                 is_editable: bool = False,
                 is_sortable: bool = False,
                 no_of_decimals: int = 0,
                 pinned: Optional[PinnedDirection] = None):
        self.id = id
        self.display_name = display_name
        self.primary_value = primary_value
        self.secondary_value = secondary_value
        self.type_id = type_id
        self.actions = actions
        self.category_id = category_id
        self.width = width
        self.is_fixed = is_fixed
        self.group_display_name = group_display_name
        self.hidden = hidden
        self.is_filterable = is_filterable
        self.is_editable = is_editable
        self.is_sortable = is_sortable
        self.no_of_decimals = no_of_decimals
        self.pinned = pinned
