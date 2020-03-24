from enum import Enum

class TrendTypes(Enum):

    Ascending = "Ascending"
    StableIncrease = "StableIncrease"
    StableDecrease = "StableDecrease"
    DescendingStop = "Descending"


UpDownTrendThreshHolds = {
    0.7: TrendTypes.Ascending,
    0.5: TrendTypes.StableIncrease,
    0.3: TrendTypes.StableDecrease,
    0.0: TrendTypes.DescendingStop
    }

PercentileChangeTrendTreshHolds = {
    50.0: TrendTypes.Ascending,
    0.0: TrendTypes.StableIncrease,
    -10.0: TrendTypes.StableDecrease,
    -50.0: TrendTypes.DescendingStop
    }


def GetUpDownTrendType(score):
    for threshold in UpDownTrendThreshHolds.keys():
        if score >= threshold:
            return UpDownTrendThreshHolds.get(threshold).value
        return UpDownTrendThreshHolds.get(0.0).value


def GetPercentileChangeTrendType(score):
    for threshold in PercentileChangeTrendTreshHolds.keys():
        if score >= threshold:
            return PercentileChangeTrendTreshHolds.get(threshold).value
        return PercentileChangeTrendTreshHolds.get(-50.0).value





    







