from FacebookTuring.Api.Catalogs.Views.ViewsAdsManager.ViewBase import View
from FacebookTuring.Api.Catalogs.Views.ViewsAdsManager.ViewColumnsMaster import ViewColumnsMaster


class ViewTargetingAndCreativeBase(View):
    name = "Targeting and creative"
    type = "Business"


class ViewCampaignTargetingAndCreative(ViewTargetingAndCreativeBase):
    table_name = "vCampaignInsights"
    columns = [
        ViewColumnsMaster.status,
        ViewColumnsMaster.campaign_name,
        ViewColumnsMaster.delivery,
        ViewColumnsMaster.results,
        ViewColumnsMaster.reach,
        ViewColumnsMaster.frequency,
        ViewColumnsMaster.cost_per_result,
        ViewColumnsMaster.budget,
        ViewColumnsMaster.amount_spent,
        ViewColumnsMaster.stop_time,
        ViewColumnsMaster.impressions,
        ViewColumnsMaster.cpm,
        ViewColumnsMaster.link_clicks,
        ViewColumnsMaster.cost_per_link_click,
        ViewColumnsMaster.link_click_through_rate,
        ViewColumnsMaster.clicks_all,
        ViewColumnsMaster.ctr_all,
        ViewColumnsMaster.cpc_all,
    ]


class ViewAdSetTargetingAndCreative(ViewTargetingAndCreativeBase):
    table_name = "vAdSetInsights"
    columns = [
        ViewColumnsMaster.status,
        ViewColumnsMaster.adset_name,
        ViewColumnsMaster.delivery,
        ViewColumnsMaster.results,
        ViewColumnsMaster.reach,
        ViewColumnsMaster.frequency,
        ViewColumnsMaster.cost_per_result,
        ViewColumnsMaster.budget,
        ViewColumnsMaster.amount_spent,
        ViewColumnsMaster.stop_time,
        ViewColumnsMaster.adset_schedule,
        ViewColumnsMaster.impressions,
        ViewColumnsMaster.cpm,
        ViewColumnsMaster.link_clicks,
        ViewColumnsMaster.cost_per_link_click,
        ViewColumnsMaster.link_click_through_rate,
        ViewColumnsMaster.clicks_all,
        ViewColumnsMaster.ctr_all,
        ViewColumnsMaster.cpc_all,
    ]


class ViewAdTargetingAndCreative(ViewTargetingAndCreativeBase):
    table_name = "vAdInsights"
    columns = [
        ViewColumnsMaster.status,
        ViewColumnsMaster.ad_name,
        ViewColumnsMaster.delivery,
        ViewColumnsMaster.results,
        ViewColumnsMaster.reach,
        ViewColumnsMaster.frequency,
        ViewColumnsMaster.cost_per_result,
        ViewColumnsMaster.budget,
        ViewColumnsMaster.amount_spent,
        ViewColumnsMaster.impressions,
        ViewColumnsMaster.cpm,
        ViewColumnsMaster.link_clicks,
        ViewColumnsMaster.cost_per_link_click,
        ViewColumnsMaster.link_click_through_rate,
        ViewColumnsMaster.clicks_all,
        ViewColumnsMaster.ctr_all,
        ViewColumnsMaster.cpc_all,
    ]
