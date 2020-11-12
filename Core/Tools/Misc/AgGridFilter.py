from enum import Enum


class AgGridFilter(Enum):
    TEXT = "agTextColumnFilter"
    NUMBER = "agNumberColumnFilter"
    DATE = "agDateColumnFilter"
    CATEGORICAL = ""

