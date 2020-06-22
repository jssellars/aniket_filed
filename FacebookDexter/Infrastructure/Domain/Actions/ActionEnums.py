from enum import Enum


class ActionEnum(Enum):
    NONE = None
    REMOVE = "remove"
    PAUSE = "pause"
    CREATE = "create"
    DECREASE_BUDGET = "decrease_budget"
    INCREASE_BUDGET = "increase_budget"
    GENERAL = "general"
    DUPLICATE = "duplicate"


class BudgetTypeEnum(Enum):
    LIFETIME = "lifetime_budget"
    DAILY = "daily_budget"


class GenderEnum(Enum):
    UNKNOWN = ("unknown", 0)
    MALE = ("male", 1)
    FEMALE = ("female", 2)


class PlacementPositionEnum(Enum):
    FACEBOOK = "facebook_positions"
    INSTAGRAM = "instagram_positions"
    AUDIENCE_NETWORK = "audience_network_positions"
    MESSENGER = "messenger_positions"


class PlacementEnum(Enum):
    PUBLISHER_PLATFORMS = "publisher_platforms"
    DEVICE_PLATFORMS = "device_platforms"
    PLACEMENT_POSITIONS = PlacementPositionEnum


class ImpressionDeviceEnum(Enum):
    USER_DEVICE = "user_device"
