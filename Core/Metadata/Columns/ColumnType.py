from Core.Tools.Misc.Enumeration import Enumeration


class ColumnType:
    text = Enumeration(1, "text", "text")
    number = Enumeration(2, "number", "number")
    date = Enumeration(3, "date", "date")
    categorical = Enumeration(4, "categorical", "categorical")
