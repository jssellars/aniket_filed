from enum import Enum

from Core.Dexter.Infrastructure.Domain.Actions.ActionEnumBase import ActionEnumBase


class GoogleActionEnum(ActionEnumBase):
    NONE = None
    REMOVE = "remove"
    PAUSE = "pause"
    CREATE = "create"
    DECREASE_BUDGET = "decrease_budget"
    INCREASE_BUDGET = "increase_budget"
    GENERAL = "general"


class GoogleBudgetTypeEnum(Enum):
    LIFETIME = "lifetime_budget"
    DAILY = "daily_budget"


class GoogleGenderEnum(Enum):
    UNKNOWN = ("unknown", 0)
    MALE = ("male", 1)
    FEMALE = ("female", 2)


class GooglePlacementPositionEnum(Enum):
    FACEBOOK = "facebook_positions"
    INSTAGRAM = "instagram_positions"
    AUDIENCE_NETWORK = "audience_network_positions"
    MESSENGER = "messenger_positions"


class GooglePlacementEnum(Enum):
    PUBLISHER_PLATFORMS = "publisher_platforms"
    DEVICE_PLATFORMS = "device_platforms"
    PLACEMENT_POSITIONS = GooglePlacementPositionEnum


class GoogleImpressionDeviceEnum(Enum):
    USER_DEVICE = "user_device"
