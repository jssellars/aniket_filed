from Core.Tools.Misc.Enumeration import Enumeration


class ViewColumnType:
    masterCheckbox = Enumeration(0, "masterCheckbox", "masterCheckbox")
    text = Enumeration(1, "text", "text")
    number = Enumeration(2, "number", "number")
    currency = Enumeration(3, "currency", "currency")
    toggle = Enumeration(4, "toggle", "toggle")
    link = Enumeration(5, "link", "link")
    percentage = Enumeration(6, "percentage", "percentage")
    button = Enumeration(7, "button", "button")
    date = Enumeration(8, "date", "date")
