import json
from enum import Enum


class ActorStates(Enum):
    Off = "Off"
    On = "On"
    Deleted = "Deleted"


state_id_to_state_mapping = {
    0: ActorStates.Off,
    1: ActorStates.On,
    2: ActorStates.Deleted
}


class Levels(Enum):
    Campaign = 1
    AdSet = 2
    Ad = 4
    Interest = 8
    Breakdown = 16


class LevelNames(Enum):
    Campaign = "campaign"
    AdSet = "adset"
    Ad = "ad"
    Interest = "interest"
    Breakdown = "breakdown"


class RecommendationVerdicts(Enum):
    IncreaseBudget = "IncreaseBudget"
    LeaveAsIs = "Leave as is"
    DecreaseBudget = "DecreaseBudget"
    Stop = "Stop"
    Start = "Start"
    Remove = "Remove"
    Split = "SplitStructure"


# TODO refactor levels and parents to a more generic less code duplicate way that abstracts their types into function calls


class OptimizationType:

    def __init__(self, name, levels=[], breakdown='None'):
        self.name = name
        self.levelSetter(levels)
        self.breakdown = breakdown  # TODO plus superior containing type based on previous level

    # LEVELS REGION
    def addLevel(self, level):
        self.level = self.level | level.value

    def hasLevel(self, level):
        return self.level & level.value

    def getLevels(self):
        levels = []
        for level in Levels:
            if self.hasLevel(level):
                levels.append(level.name)

        return levels

    def levelSetter(self, levels):
        bitMaskedLevels = 0
        for level in levels:
            if not isinstance(level, Levels):
                raise ValueError("Please try and set levels to actual Levels")
            bitMaskedLevels = bitMaskedLevels | level.value
        self.level = bitMaskedLevels

    def getJson(self):
        return json.dumps(self.__dict__)

    def getExpandedTuples(self):
        expandedTuples = []
        levels = self.getLevels()
        for level in levels:
            optimizationTuple = OptimizationTuple(self.name, level, self.breakdown)
            expandedTuples.append(optimizationTuple)

        return expandedTuples


class OptimizationTuple(dict):
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

    def __init__(self, level, breakdown, action_breakdown):
        self.level = level
        self.breakdown = breakdown
        self.action_breakdown = action_breakdown
