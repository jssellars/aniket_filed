from facebook_business.adobjects.producteventstat import ProductEventStat

from PotterFacebookCampaignsBuilder.Api.catalogs.base import Base
from PotterFacebookCampaignsBuilder.Api.catalogs.node import Node

_device_type = ProductEventStat.DeviceType


class DeviceType(Base):
    desktop = Node(_device_type.desktop)
    mobile_android_phone = Node(_device_type.mobile_android_phone)
    mobile_android_tablet = Node(_device_type.mobile_android_tablet)
    mobile_ipad = Node(_device_type.mobile_ipad)
    mobile_iphone = Node(_device_type.mobile_iphone)
    mobile_ipod = Node(_device_type.mobile_ipod)
    mobile_phone = Node(_device_type.mobile_phone)
    mobile_tablet = Node(_device_type.mobile_tablet)
    mobile_windows_phone = Node(_device_type.mobile_windows_phone)
