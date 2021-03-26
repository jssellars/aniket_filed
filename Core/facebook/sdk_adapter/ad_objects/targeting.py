from enum import Enum

from facebook_business.adobjects.targeting import Targeting

from Core.facebook.sdk_adapter.catalog_models import Cat, Contexts, cat_enum

# TODO: add documentation link(s)

_device_platforms = Targeting.DevicePlatforms


@cat_enum
class DevicePlatform(Enum):
    DESKTOP = Cat(_device_platforms.desktop)
    MOBILE = Cat(_device_platforms.mobile)

    contexts = Contexts.all_with_items(DESKTOP, MOBILE)
