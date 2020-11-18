from enum import Enum, auto

column_id = "col_id"
field = "field"
number_of_decimals = "number_of_decimals"
header_name = "header_name"
filter = "filter"
editable = "editable"
sortable = "sortable"
suppress_columns_tool_panel = "suppress_columns_tool_panel"
pinned = "pinned"
lock_position = "lock_position"
is_toggle = "is_toggle"


class PinnedDirection(Enum):
    LEFT = "left"
    RIGHT = "right"


class PositiveEffectTrendDirection(Enum):
    INCREASING = auto()
    DECREASING = auto()


class Trend(Enum):
    POSITIVE = auto()
    NEGATIVE = auto()
    UNDEFINED = auto()
