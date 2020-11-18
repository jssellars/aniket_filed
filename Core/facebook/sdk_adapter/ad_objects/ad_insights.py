from enum import Enum

from facebook_business.adobjects.adsinsights import AdsInsights

from Core.facebook.sdk_adapter.catalog_models import Cat, cat_enum, Contexts

# https://developers.facebook.com/docs/marketing-api/attribution#reference_attribution_windows
# https://developers.facebook.com/docs/marketing-api/insights/#sample
# https://developers.facebook.com/docs/marketing-api/reference/ad-campaign-group#attribution_spec
# https://www.facebook.com/business/help/304909959680406?locale=en_GB

_attribution_windows = AdsInsights.ActionAttributionWindows


@cat_enum
class ActionAttributionWindows(Enum):
    VALUE_1D_CLICK = Cat(_attribution_windows.value_1d_click, display_name="1 day after clicking")
    VALUE_1D_VIEW = Cat(_attribution_windows.value_1d_view, display_name="1 day after viewing")
    VALUE_28D_CLICK = Cat(_attribution_windows.value_28d_click, display_name="7 days after clicking")
    VALUE_28D_VIEW = Cat(_attribution_windows.value_28d_view, display_name="7 days after viewing")
    VALUE_7D_CLICK = Cat(_attribution_windows.value_7d_click, display_name="28 days after clicking")
    VALUE_7D_VIEW = Cat(_attribution_windows.value_7d_view, display_name="28 days after viewing")

    contexts = Contexts.all_with_items(
        VALUE_1D_CLICK,
        VALUE_7D_CLICK,
        VALUE_28D_CLICK,
        VALUE_1D_VIEW,
        VALUE_7D_VIEW,
        VALUE_28D_VIEW,
        default_item=VALUE_1D_CLICK,
    )


@cat_enum
class ActionAttributionWindowClick(Enum):
    VALUE_1D = Cat(_attribution_windows.value_1d_click, display_name="1 day after clicking")
    VALUE_28D = Cat(_attribution_windows.value_28d_click, display_name="7 days after clicking")
    VALUE_7D = Cat(_attribution_windows.value_7d_click, display_name="28 days after clicking")
    NONE = Cat(None, display_name="Not using click")

    contexts = Contexts.all_with_items(VALUE_1D, VALUE_7D, VALUE_28D, NONE, default_item=VALUE_1D,)


@cat_enum
class ActionAttributionWindowView(Enum):
    VALUE_1D = Cat(_attribution_windows.value_1d_view, display_name="1 day after viewing")
    VALUE_28D = Cat(_attribution_windows.value_28d_view, display_name="7 days after viewing")
    VALUE_7D = Cat(_attribution_windows.value_7d_view, display_name="28 days after viewing")
    NONE = Cat(None, display_name="Not using view")

    contexts = Contexts.all_with_items(VALUE_1D, VALUE_7D, VALUE_28D, NONE, default_item=NONE,)
