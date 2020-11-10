from enum import Enum

from facebook_business.adobjects.targeting import Targeting

from Core.facebook.sdk_adapter.catalog_models import Cat, cat_enum

# TODO: add documentation link(s)

_device_platforms = Targeting.DevicePlatforms


@cat_enum
class DevicePlatform(Enum):
    CONNECTED_TV = Cat(_device_platforms.connected_tv)
    DESKTOP = Cat(_device_platforms.desktop)
    MOBILE = Cat(_device_platforms.mobile)