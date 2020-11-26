from FacebookTuring.Api.Catalogs.Views.ViewsAdsManager.ViewBase import View
from FacebookTuring.Api.Catalogs.Views.ViewsAdsManager.ViewColumnsMaster import ViewColumnsMaster


class ViewCampaignPerformance(View):
    name = "Performance"
    table_name = "vCampaignInsights"
    type = "Business"
    columns = [
        ViewColumnsMaster.status,
        ViewColumnsMaster.campaign_name,
        ViewColumnsMaster.delivery,
        ViewColumnsMaster.budget,
        ViewColumnsMaster.amount_spent,
        ViewColumnsMaster.impressions,
        ViewColumnsMaster.cpm,
        ViewColumnsMaster.unique_clicks_all,
        ViewColumnsMaster.cost_per_unique_click_all,
        ViewColumnsMaster.unique_ctr_all,
        ViewColumnsMaster.results,
        ViewColumnsMaster.cost_per_result,
        ViewColumnsMaster.result_rate,
        ViewColumnsMaster.landing_page_views_total,
        ViewColumnsMaster.landing_page_views_unique,
        ViewColumnsMaster.purchases_value,
        ViewColumnsMaster.purchase_roas,
        ViewColumnsMaster.stop_time,
    ]


class ViewAdSetPerformance(ViewCampaignPerformance):
    table_name = "vAdSetInsights"
    columns = [
        ViewColumnsMaster.status,
        ViewColumnsMaster.adset_name,
        ViewColumnsMaster.delivery,
        ViewColumnsMaster.budget,
        ViewColumnsMaster.amount_spent,
        ViewColumnsMaster.impressions,
        ViewColumnsMaster.cpm,
        ViewColumnsMaster.frequency,
        ViewColumnsMaster.unique_clicks_all,
        ViewColumnsMaster.cost_per_unique_click_all,
        ViewColumnsMaster.unique_ctr_all,
        ViewColumnsMaster.results,
        ViewColumnsMaster.cost_per_result,
        ViewColumnsMaster.result_rate,
        ViewColumnsMaster.landing_page_views_total,
        ViewColumnsMaster.landing_page_views_unique,
        ViewColumnsMaster.purchases_value,
        ViewColumnsMaster.purchase_roas,
        ViewColumnsMaster.stop_time,
    ]


class ViewAdPerformance(View):
    name = "Performance"
    table_name = "vAdInsights"
    type = "Business"
    columns = [
        ViewColumnsMaster.status,
        ViewColumnsMaster.ad_name,
        ViewColumnsMaster.delivery,
        ViewColumnsMaster.budget,
        ViewColumnsMaster.amount_spent,
        ViewColumnsMaster.impressions,
        ViewColumnsMaster.cpm,
        ViewColumnsMaster.frequency,
        ViewColumnsMaster.unique_clicks_all,
        ViewColumnsMaster.cost_per_unique_click_all,
        ViewColumnsMaster.unique_ctr_all,
        ViewColumnsMaster.results,
        ViewColumnsMaster.cost_per_result,
        ViewColumnsMaster.result_rate,
        ViewColumnsMaster.landing_page_views_total,
        ViewColumnsMaster.landing_page_views_unique,
        ViewColumnsMaster.purchases_value,
        ViewColumnsMaster.purchase_roas,
        ViewColumnsMaster.quality_ranking,
        ViewColumnsMaster.engagement_rate_ranking,
        ViewColumnsMaster.conversion_rate_ranking,
        ViewColumnsMaster.stop_time,
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
