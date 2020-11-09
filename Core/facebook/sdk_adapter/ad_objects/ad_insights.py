from enum import Enum

from facebook_business.adobjects.adsinsights import AdsInsights

from Core.facebook.sdk_adapter.catalog_models import Cat, cat_enum

# https://developers.facebook.com/docs/marketing-api/insights/#sample
# https://www.facebook.com/business/help/304909959680406?locale=en_GB

_attribution_windows = AdsInsights.ActionAttributionWindows


@cat_enum
class ActionAttributionWindows(Enum):
    VALUE_1D_CLICK = Cat(_attribution_windows.value_1d_click)
    VALUE_1D_VIEW = Cat(_attribution_windows.value_1d_view)
    VALUE_28D_CLICK = Cat(_attribution_windows.value_28d_click)
    VALUE_28D_VIEW = Cat(_attribution_windows.value_28d_view)
    VALUE_7D_CLICK = Cat(_attribution_windows.value_7d_click)
    VALUE_7D_VIEW = Cat(_attribution_windows.value_7d_view)
