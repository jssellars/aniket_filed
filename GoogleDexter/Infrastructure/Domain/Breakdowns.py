import typing
from dataclasses import dataclass
from enum import Enum

from Core.Tools.Misc.ObjectSerializers import object_to_json


@dataclass
class BreakdownBase:
    name: typing.AnyStr = None
    display_name: typing.AnyStr = None

    def to_dict(self):
        return object_to_json(self)

    def __eq__(self, other):
        if not isinstance(other, BreakdownBase):
            return False

        if self.name == other.name:
            return True

        return False

    def __ne__(self, other):
        return not self.__eq__(other)


class BreakdownEnum(Enum):
    NONE = BreakdownBase(name="none", display_name="")
    AGE = BreakdownBase(name="age_range", display_name="Age")
    GENDER = BreakdownBase(name="gender", display_name="Gender")
    # PLACEMENT = BreakdownBase(name="placement", display_name="Placement")
    # DEVICE = BreakdownBase(name="impression_device", display_name="Device")
    # PLATFORM = BreakdownBase(name="platform_position", display_name="Publisher platform")


class ActionBreakdownEnum(Enum):
    NONE = BreakdownBase(name="none", display_name="")


@dataclass
class BreakdownMetadata:
    breakdown: BreakdownEnum = None
    breakdown_value: typing.Any = None
    action_breakdown: ActionBreakdownEnum = None
    action_breakdown_value: typing.Any = None

    def equals(self, other):
        is_equal = (self.breakdown == other.breakdown and
                    self.breakdown_value == other.breakdown_value and
                    self.action_breakdown == other.action_breakdown and
                    self.action_breakdown_value == other.action_breakdown_value)
        return is_equal
