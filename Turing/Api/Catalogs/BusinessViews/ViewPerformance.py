from Turing.Api.Catalogs.Views.ViewBase import View
from Turing.Api.Catalogs.Views.ViewColumnsMaster import ViewColumnsMaster


class ViewCampaignPerformance(View):
    name = "Performance"
    table_name = "vCampaignInsights"
    type = "Business"
    columns = [
        ViewColumnsMaster.effective_status,
        ViewColumnsMaster.campaign_name,
        ViewColumnsMaster.budget,
        ViewColumnsMaster.spend,
        ViewColumnsMaster.reach,
        ViewColumnsMaster.impressions,
        ViewColumnsMaster.cpm,
        ViewColumnsMaster.unique_link_click,
        ViewColumnsMaster.results,
        ViewColumnsMaster.cost_per_result,
        ViewColumnsMaster.conversions,
        ViewColumnsMaster.cost_per_conversion
    ]


class ViewAdSetPerformance(ViewCampaignPerformance):
    table_name = "vAdSetInsights"
    columns = [
        ViewColumnsMaster.effective_status,
        ViewColumnsMaster.adset_name,
        ViewColumnsMaster.budget,
        ViewColumnsMaster.spend,
        ViewColumnsMaster.reach,
        ViewColumnsMaster.impressions,
        ViewColumnsMaster.cpm,
        ViewColumnsMaster.unique_link_click,
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
        ViewColumnsMaster.effective_status,
        ViewColumnsMaster.ad_name,
        ViewColumnsMaster.spend,
        ViewColumnsMaster.reach,
        ViewColumnsMaster.impressions,
        ViewColumnsMaster.results,
        ViewColumnsMaster.cost_per_result,
        ViewColumnsMaster.quality_ranking,
        ViewColumnsMaster.conversions,
        ViewColumnsMaster.cost_per_conversion
    ]


class ViewCampaignFallback(ViewCampaignPerformance):
    name = "Cristian's requested changed name"
    type = "Fallback"


class ViewAdSetFallback(ViewAdSetPerformance):
    name = "Cristian's requested changed name"
    type = "Fallback"


class ViewAdFallback(ViewAdPerformance):
    name = "Cristian's requested changed name"
    type = "Fallback"