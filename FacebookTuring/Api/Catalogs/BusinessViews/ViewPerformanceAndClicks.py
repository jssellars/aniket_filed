from FacebookTuring.Api.Catalogs.Views.ViewBase import View
from FacebookTuring.Api.Catalogs.Views.ViewColumnsMaster import ViewColumnsMaster


class ViewPerformanceAndClicksBase(View):
    name = "Performance and clicks"
    type = "Business"


class ViewCampaignPerformanceAndClicks(ViewPerformanceAndClicksBase):
    table_name = "vCampaignInsights"
    columns = [
        ViewColumnsMaster.effective_status,
        ViewColumnsMaster.campaign_name,
        ViewColumnsMaster.delivery,
        ViewColumnsMaster.results,
        ViewColumnsMaster.cost_per_result,
        ViewColumnsMaster.spend,
        ViewColumnsMaster.impressions,
        ViewColumnsMaster.cpm,
        ViewColumnsMaster.link_click,
        # ViewColumnsMaster.costPerUniqueInlineLinkClick,
        ViewColumnsMaster.link_click_website_ctr,
        ViewColumnsMaster.clicks,
        ViewColumnsMaster.ctr,
        ViewColumnsMaster.cpc,
        ViewColumnsMaster.unique_clicks
    ]


class ViewAdSetPerformanceAndClicks(ViewPerformanceAndClicksBase):
    table_name = "vAdSetInsights"
    columns = [
        ViewColumnsMaster.effective_status,
        ViewColumnsMaster.adset_name,
        ViewColumnsMaster.delivery,
        ViewColumnsMaster.results,
        ViewColumnsMaster.cost_per_result,
        ViewColumnsMaster.spend,
        ViewColumnsMaster.impressions,
        ViewColumnsMaster.cpm,
        ViewColumnsMaster.link_click,
        # ViewColumnsMaster.costPerUniqueInlineLinkClick,
        ViewColumnsMaster.link_click_website_ctr,
        ViewColumnsMaster.clicks,
        ViewColumnsMaster.ctr,
        ViewColumnsMaster.cpc,
        ViewColumnsMaster.unique_clicks
    ]


class ViewAdPerformanceAndClicks(ViewPerformanceAndClicksBase):
    table_name = "vAdInsights"
    columns = [
        ViewColumnsMaster.effective_status,
        ViewColumnsMaster.ad_name,
        ViewColumnsMaster.delivery,
        ViewColumnsMaster.results,
        ViewColumnsMaster.cost_per_result,
        ViewColumnsMaster.spend,
        ViewColumnsMaster.impressions,
        ViewColumnsMaster.cpm,
        ViewColumnsMaster.link_click,
        # ViewColumnsMaster.costPerUniqueInlineLinkClick,
        ViewColumnsMaster.link_click_website_ctr,
        ViewColumnsMaster.clicks,
        ViewColumnsMaster.ctr,
        ViewColumnsMaster.cpc,
        ViewColumnsMaster.unique_clicks
    ]