from typing import List

from Core.Metadata.Columns.ColumnType import ColumnType
from Core.Tools.Misc.Enumeration import Enumeration


class ColumnMetadata:
    def __init__(self, column_name, column_type, categorical_values_list: List[Enumeration] = ()):
        self.name = column_name
        self.type_id = column_type.id

        # Optional parameter
        self.categorical_values = [enumeration.name for enumeration in
                                   categorical_values_list] if self.type_id == ColumnType.categorical.id else None
