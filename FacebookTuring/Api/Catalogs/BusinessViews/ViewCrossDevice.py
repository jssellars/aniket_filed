from FacebookTuring.Api.Catalogs.Views.ViewsAdsManager.ViewBase import View
from FacebookTuring.Api.Catalogs.Views.ViewsAdsManager.ViewColumnsMaster import ViewColumnsMaster


class ViewCrossDeviceBase(View):
    name = "Cross-Device"
    type = "Business"


class ViewCampaignCrossDevice(ViewCrossDeviceBase):
    table_name = "vCampaignInsights"
    columns = [
        ViewColumnsMaster.status,
        ViewColumnsMaster.campaign_name,
        ViewColumnsMaster.delivery,
        ViewColumnsMaster.reach,
        ViewColumnsMaster.impressions,
        # TODO: get desktop impressions
        # TODO: get mobile impressions
        ViewColumnsMaster.link_clicks,
        # TODO: get desktop link clicks
        # TODO: get mobile link clicks
        ViewColumnsMaster.unique_link_click_through_rate,
        # TODO: get desktop link click ctr
        # TODO: get mobile link click ctr
        ViewColumnsMaster.results
        # TODO: get desktop results
        # TODO: get mobile results
    ]


class ViewAdSetCrossDevice(ViewCrossDeviceBase):
    table_name = "vAdSetInsights"
    columns = [
        ViewColumnsMaster.status,
        ViewColumnsMaster.adset_name,
        ViewColumnsMaster.delivery,
        ViewColumnsMaster.reach,
        ViewColumnsMaster.impressions,
        # TODO: get desktop impressions
        # TODO: get mobile impressions
        ViewColumnsMaster.link_clicks,
        # TODO: get desktop link clicks
        # TODO: get mobile link clicks
        ViewColumnsMaster.unique_link_click_through_rate,
        # TODO: get desktop link click ctr
        # TODO: get mobile link click ctr
        ViewColumnsMaster.results
        # TODO: get desktop results
        # TODO: get mobile results
    ]


class ViewAdCrossDevice(ViewCrossDeviceBase):
    table_name = "vAdInsights"
    columns = [
        ViewColumnsMaster.status,
        ViewColumnsMaster.ad_name,
        ViewColumnsMaster.delivery,
        ViewColumnsMaster.reach,
        ViewColumnsMaster.impressions,
        # TODO: get desktop impressions
        # TODO: get mobile impressions
        ViewColumnsMaster.link_clicks,
        # TODO: get desktop link clicks
        # TODO: get mobile link clicks
        ViewColumnsMaster.unique_link_click_through_rate,
        # TODO: get desktop link click ctr
        # TODO: get mobile link click ctr
        ViewColumnsMaster.results
        # TODO: get desktop results
        # TODO: get mobile results
    ]
