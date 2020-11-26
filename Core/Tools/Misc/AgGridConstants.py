from enum import Enum, auto

COLUMN_ID = "col_id"
FIELD = "field"
NUMBER_OF_DECIMALS = "number_of_decimals"
HEADER_NAME = "header_name"
FILTER = "filter"
EDITABLE = "editable"
SORTABLE = "sortable"
SUPPRESS_COLUMNS_TOOL_PANEL = "suppress_columns_tool_panel"
PINNED = "pinned"
LOCK_POSITION = "lock_position"
DESCRIPTION = "description"
COLUMN_TYPE = "column_type"
IS_TOGGLE = "is_toggle"
IS_NAME_CLICKABLE = "is_name_clickable"

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
