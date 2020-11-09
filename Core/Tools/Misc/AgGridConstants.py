from enum import Enum

column_id = "col_id"
field = "field"
number_of_decimals = "number_of_decimals"
header_name = "header_name"
filter = "filter"
editable = "editable"
sortable = "sortable"
suppress_columns_tool_panel = "suppress_columns_tool_panel"
pinned = "pinned"


class PinnedDirection(Enum):
    LEFT = "left"
    RIGHT = "right"
