from FacebookTuring.Api.Catalogs.Views.ViewsAdsManager.ViewBase import View
from FacebookTuring.Api.Catalogs.Views.ViewsAdsManager.ViewColumnsMaster import ViewColumnsMaster


class ViewCampaignPerformance(View):
    name = "Performance"
    table_name = "vCampaignInsights"
    type = "Business"
    columns = [
        ViewColumnsMaster.status,
        ViewColumnsMaster.campaign_name,
        ViewColumnsMaster.budget,
        ViewColumnsMaster.amount_spent,
        ViewColumnsMaster.reach,
        ViewColumnsMaster.impressions,
        ViewColumnsMaster.cpm,
        ViewColumnsMaster.unique_link_clicks,
        ViewColumnsMaster.results,
        ViewColumnsMaster.cost_per_result,
        ViewColumnsMaster.conversions,
        ViewColumnsMaster.cost_per_conversion
    ]


class ViewAdSetPerformance(ViewCampaignPerformance):
    table_name = "vAdSetInsights"
    columns = [
        ViewColumnsMaster.status,
        ViewColumnsMaster.adset_name,
        ViewColumnsMaster.budget,
        ViewColumnsMaster.amount_spent,
        ViewColumnsMaster.reach,
        ViewColumnsMaster.impressions,
        ViewColumnsMaster.cpm,
        ViewColumnsMaster.unique_link_clicks,
        ViewColumnsMaster.results,
        ViewColumnsMaster.cost_per_result,
        ViewColumnsMaster.conversions,
        ViewColumnsMaster.cost_per_conversion
    ]


class ViewAdPerformance(View):
    name = "Performance"
    table_name = "vAdInsights"
    type = "Business"
    columns = [
        ViewColumnsMaster.status,
        ViewColumnsMaster.ad_name,
        ViewColumnsMaster.amount_spent,
        ViewColumnsMaster.reach,
        ViewColumnsMaster.impressions,
        ViewColumnsMaster.results,
        ViewColumnsMaster.cost_per_result,
        ViewColumnsMaster.quality_ranking,
        ViewColumnsMaster.conversions,
        ViewColumnsMaster.cost_per_conversion
    ]


class ViewCampaignFallback(ViewCampaignPerformance):
    name = "Filed default view"
    type = "Fallback"


class ViewAdSetFallback(ViewAdSetPerformance):
    name = "Filed default view"
    type = "Fallback"


class ViewAdFallback(ViewAdPerformance):
    name = "Filed default view"
    type = "Fallback"
