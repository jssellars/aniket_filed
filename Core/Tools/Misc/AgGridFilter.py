from enum import Enum


class AgGridFilter(Enum):
    TEXT = "agTextColumnFilter"
    NUMBER = "agNumberColumnFilter"
    CURRENCY = "agNumberColumnFilter"
    TOGGLE = ""
    LINK = "agTextColumnFilter"
    PERCENTAGE = "agNumberColumnFilter"
    BUTTON = ""
    DATE = "agDateColumnFilter"
    BUDGET = "agNumberColumnFilter"
