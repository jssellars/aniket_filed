from typing import List

from Core.Tools.Misc.Enumeration import Enumeration
from FacebookTuring.Api.Catalogs.Columns.ColumnType import ColumnType


class ColumnMetadata:
    def __init__(self, column_name, aggregation_type, column_type, categorical_values_list: List[Enumeration] = ()):
        self.name = column_name
        self.aggregation_id = aggregation_type.id
        self.type_id = column_type.id

        # Optional parameter
        self.categorical_values = [enumeration.name for enumeration in categorical_values_list] if self.type_id == ColumnType.categorical.id else None


