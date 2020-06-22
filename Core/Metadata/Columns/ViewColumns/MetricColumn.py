import typing

from Core.Metadata.Columns.ColumnMetadata import ColumnMetadata
from Core.Metadata.Columns.ViewColumns.ViewColumn import ViewColumn


class MetricColumn:
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
                 not_supported_dimensions: typing.List[ViewColumn] = None):
        self.view_column = ViewColumn(id=id,
                                      display_name=display_name,
                                      primary_value=primary_value,
                                      secondary_value=secondary_value,
                                      type_id=type_id,
                                      actions=actions,
                                      category_id=category_id,
                                      width=width,
                                      is_fixed=is_fixed,
                                      group_display_name=group_display_name,
                                      hidden=hidden)
        self.not_supported_dimensions = not_supported_dimensions
