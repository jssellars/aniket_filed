from FacebookTuring.Api.Catalogs.Views.ViewsAdsManager.ViewBase import View
from FacebookTuring.Api.Catalogs.Views.ViewsAdsManager.ViewColumnsMaster import ViewColumnsMaster


class ViewPerformanceAndClicksBase(View):
    name = "Performance and clicks"
    type = "Business"


class ViewCampaignPerformanceAndClicks(ViewPerformanceAndClicksBase):
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
        ViewColumnsMaster.video_plays_3s,
        ViewColumnsMaster.video_average_play_time,
    ]


class ViewAdSetPerformanceAndClicks(ViewPerformanceAndClicksBase):
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
        ViewColumnsMaster.impressions,
        ViewColumnsMaster.cpm,
        ViewColumnsMaster.link_clicks,
        ViewColumnsMaster.cost_per_link_click,
        ViewColumnsMaster.link_click_through_rate,
        ViewColumnsMaster.clicks_all,
        ViewColumnsMaster.ctr_all,
        ViewColumnsMaster.cpc_all,
        ViewColumnsMaster.video_plays_3s,
        ViewColumnsMaster.video_average_play_time,
    ]


class ViewAdPerformanceAndClicks(ViewPerformanceAndClicksBase):
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
        ViewColumnsMaster.video_plays_3s,
        ViewColumnsMaster.video_average_play_time,
    ]
