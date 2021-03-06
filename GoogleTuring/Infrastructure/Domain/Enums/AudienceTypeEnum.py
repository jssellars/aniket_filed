from enum import Enum


class AudienceTypeEnum(Enum):
    UNKNOWN_AUDIENCE = 0
    UNSPECIFIED_AUDIENCE = 1
    AFFINITY_AUDIENCE = 2
    IN_MARKET_AUDIENCE = 3
    MOBILE_APP_INSTALL_USER_AUDIENCE = 4
    VERTICAL_GEO_AUDIENCE = 5
    NEW_SMART_PHONE_USER_AUDIENCE = 6
    CUSTOM_INTENT = 7
    USER_INTEREST = 8
    CUSTOM_AFFINITY = 9
