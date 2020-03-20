from Turing.Api.Catalogs.Views.ViewBase import View
from Turing.Api.Catalogs.Views.ViewColumnsMaster import ViewColumnsMaster


class ViewCrossDeviceBase(View):
    name = "Cross-Device"
    type = "Business"


class ViewCampaignCrossDevice(ViewCrossDeviceBase):
    table_name = "vCampaignInsights"
    columns = [
        ViewColumnsMaster.effective_status,
        ViewColumnsMaster.campaign_name,
        ViewColumnsMaster.delivery,
        ViewColumnsMaster.reach,
        ViewColumnsMaster.impressions,
        # TODO: get desktop impressions
        # TODO: get mobile impressions
        ViewColumnsMaster.link_click,
        # TODO: get desktop link clicks
        # TODO: get mobile link clicks
        ViewColumnsMaster.unique_link_clicks_ctr,
        # TODO: get desktop link click ctr
        # TODO: get mobile link click ctr
        ViewColumnsMaster.results
        # TODO: get desktop results
        # TODO: get mobile results
    ]


class ViewAdSetCrossDevice(ViewCrossDeviceBase):
    table_name = "vAdSetInsights"
    columns = [
        ViewColumnsMaster.effective_status,
        ViewColumnsMaster.adset_name,
        ViewColumnsMaster.delivery,
        ViewColumnsMaster.reach,
        ViewColumnsMaster.impressions,
        # TODO: get desktop impressions
        # TODO: get mobile impressions
        ViewColumnsMaster.link_click,
        # TODO: get desktop link clicks
        # TODO: get mobile link clicks
        ViewColumnsMaster.unique_link_clicks_ctr,
        # TODO: get desktop link click ctr
        # TODO: get mobile link click ctr
        ViewColumnsMaster.results
        # TODO: get desktop results
        # TODO: get mobile results
    ]


class ViewAdCrossDevice(ViewCrossDeviceBase):
    table_name = "vAdInsights"
    columns = [
        ViewColumnsMaster.effective_status,
        ViewColumnsMaster.ad_name,
        ViewColumnsMaster.delivery,
        ViewColumnsMaster.reach,
        ViewColumnsMaster.impressions,
        # TODO: get desktop impressions
        # TODO: get mobile impressions
        ViewColumnsMaster.link_click,
        # TODO: get desktop link clicks
        # TODO: get mobile link clicks
        ViewColumnsMaster.unique_link_clicks_ctr,
        # TODO: get desktop link click ctr
        # TODO: get mobile link click ctr
        ViewColumnsMaster.results
        # TODO: get desktop results
        # TODO: get mobile results
    ]