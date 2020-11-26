from FacebookTuring.Api.Catalogs.Views.ViewsAdsManager.ViewBase import View
from FacebookTuring.Api.Catalogs.Views.ViewsAdsManager.ViewColumnsMaster import ViewColumnsMaster


class ViewCampaignSetup(View):
    name = "Setup"
    table_name = "vCampaignInsights"
    type = "Business"
    columns = [
        ViewColumnsMaster.status,
        ViewColumnsMaster.campaign_name,
        ViewColumnsMaster.bid_strategy,
        ViewColumnsMaster.spend_cap,
        ViewColumnsMaster.objective,
        ViewColumnsMaster.buying_type,
        ViewColumnsMaster.campaign_id,
    ]


class ViewAdsetSetup(ViewCampaignSetup):
    table_name = "vAdSetInsights"
    columns = [
        ViewColumnsMaster.status,
        ViewColumnsMaster.adset_name,
        ViewColumnsMaster.included_custom_audiences,
        ViewColumnsMaster.excluded_custom_audiences,
        ViewColumnsMaster.location,
        ViewColumnsMaster.bid_strategy,
        ViewColumnsMaster.budget,
        ViewColumnsMaster.adset_schedule,
        ViewColumnsMaster.adset_id,
    ]


class ViewAdSetup(ViewCampaignSetup):
    table_name = "vAdInsights"
    columns = [
        ViewColumnsMaster.status,
        ViewColumnsMaster.ad_name,
        ViewColumnsMaster.link,
        ViewColumnsMaster.url_parameters,
        ViewColumnsMaster.pixel,
        ViewColumnsMaster.app_event,
        ViewColumnsMaster.bid_strategy,
        ViewColumnsMaster.budget,
        ViewColumnsMaster.objective,
        ViewColumnsMaster.ad_id,
    ]


