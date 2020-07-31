from enum import Enum

from Core.Dexter.Infrastructure.Domain.Actions.ActionEnumBase import ActionEnumBase


class FacebookActionEnum(ActionEnumBase):
    NONE = None
    REMOVE = "remove"
    PAUSE = "pause"
    CREATE = "create"
    DECREASE_BUDGET = "decrease_budget"
    INCREASE_BUDGET = "increase_budget"
    GENERAL = "general"
    DUPLICATE = "duplicate"


class FacebookBudgetTypeEnum(Enum):
    LIFETIME = "lifetime_budget"
    DAILY = "daily_budget"


class FacebookGenderEnum(Enum):
    UNKNOWN = ("unknown", 0)
    MALE = ("male", 1)
    FEMALE = ("female", 2)


class FacebookPlacementPositionEnum(Enum):
    FACEBOOK = "facebook_positions"
    INSTAGRAM = "instagram_positions"
    AUDIENCE_NETWORK = "audience_network_positions"
    MESSENGER = "messenger_positions"


class FacebookPlacementEnum(Enum):
    PUBLISHER_PLATFORMS = "publisher_platforms"
    DEVICE_PLATFORMS = "device_platforms"
    PLACEMENT_POSITIONS = FacebookPlacementPositionEnum


class FacebookImpressionDeviceEnum(Enum):
    USER_DEVICE = "user_device"
