from facebook_business.adobjects.adsinsights import AdsInsights

from FacebookCampaignsBuilder.Api.catalogs.base import Base
from FacebookCampaignsBuilder.Api.catalogs.node import Node

# https://developers.facebook.com/docs/marketing-api/insights/#sample
# https://www.facebook.com/business/help/304909959680406?locale=en_GB

_attribution_windows = AdsInsights.ActionAttributionWindows


class ActionAttributionWindows(Base):
    value_1d_click = Node(_attribution_windows.value_1d_click)
    value_1d_view = Node(_attribution_windows.value_1d_view)
    value_28d_click = Node(_attribution_windows.value_28d_click)
    value_28d_view = Node(_attribution_windows.value_28d_view)
    value_7d_click = Node(_attribution_windows.value_7d_click)
    value_7d_view = Node(_attribution_windows.value_7d_view)
