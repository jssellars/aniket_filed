from Core.Tools.Misc.Enumeration import Enumeration


class AggregationType:
    null = Enumeration(0, "None", "")
    sum = Enumeration(1, "Sum", "SUM")
    avg = Enumeration(2, "Average", "AVG")
    max = Enumeration(3, "Maximum", "MAX")
    min = Enumeration(4, "Minimum", "MIN")
