import typing

from Core.Metadata.Columns.ColumnMetadata import ColumnMetadata


class ViewColumn:

    def __init__(self,
                 id: typing.Union[typing.AnyStr, int] = None,
                 display_name: typing.AnyStr = None,
                 primary_value: ColumnMetadata = None,
                 secondary_value: ColumnMetadata = None,
                 type_id: int = None,  # ViewColumnTypeEnum
                 actions: typing.List[typing.Any] = None,
                 category_id: id = None,  # ViewColumnCategoryEnum
                 width: int = 50,
                 is_fixed: bool = False,
                 group_display_name: typing.AnyStr = None,  # ViewColumnGroupEnum
                 hidden: bool = False,
                 no_of_decimals: int = 0,
                 ):
        self.id = id
        self.display_name = display_name  # string
        self.primary_value = primary_value  # ColumnMetadata
        self.secondary_value = secondary_value  # ColumnMetadata
        self.type_id = type_id  # ViewColumnTypeEnum
        self.actions = actions  # List of ActionEnum.id
        self.category_id = category_id  # ViewColumnCategoryEnum -> id
        self.width = width
        self.is_fixed = is_fixed
        self.group_display_name = group_display_name
        self.hidden = hidden
        self.no_of_decimals = no_of_decimals
