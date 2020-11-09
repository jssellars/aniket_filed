from enum import Enum

from facebook_business.adobjects.producteventstat import ProductEventStat

from Core.facebook.sdk_adapter.catalog_models import Cat, cat_enum

# https://developers.facebook.com/docs/marketing-api/reference/product-event-stat

_device_type = ProductEventStat.DeviceType


@cat_enum
class DeviceType(Enum):
    DESKTOP = Cat(_device_type.desktop)
    MOBILE_ANDROID_PHONE = Cat(_device_type.mobile_android_phone)
    MOBILE_ANDROID_TABLET = Cat(_device_type.mobile_android_tablet)
    MOBILE_IPAD = Cat(_device_type.mobile_ipad)
    MOBILE_IPHONE = Cat(_device_type.mobile_iphone)
    MOBILE_IPOD = Cat(_device_type.mobile_ipod)
    MOBILE_PHONE = Cat(_device_type.mobile_phone)
    MOBILE_TABLET = Cat(_device_type.mobile_tablet)
    MOBILE_WINDOWS_PHONE = Cat(_device_type.mobile_windows_phone)
