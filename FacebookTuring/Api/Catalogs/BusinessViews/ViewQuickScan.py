from FacebookTuring.Api.Catalogs.Views.ViewsAdsManager.ViewBase import View
from FacebookTuring.Api.Catalogs.Views.ViewsAdsManager.ViewColumnsMaster import ViewColumnsMaster


class ViewQuickScanBase(View):
    name = "Quick Scan"
    type = "Business"


class ViewCampaignQuickScan(ViewQuickScanBase):
    tableName = "vCampaignInsights"
    columns = [
        ViewColumnsMaster.status,
        ViewColumnsMaster.campaign_name,
        ViewColumnsMaster.frequency,
        ViewColumnsMaster.amount_spent,
        ViewColumnsMaster.budget,
        ViewColumnsMaster.cpm,
        ViewColumnsMaster.link_clicks,
        ViewColumnsMaster.results,
        ViewColumnsMaster.link_click_through_rate,
        ViewColumnsMaster.cost_per_link_click,
        ViewColumnsMaster.cost_per_result,
        ViewColumnsMaster.impressions,
    ]


class ViewAdSetQuickScan(ViewQuickScanBase):
    tableName = "vAdSetInsights"
    columns = [
        ViewColumnsMaster.status,
        ViewColumnsMaster.adset_name,
        ViewColumnsMaster.frequency,
        ViewColumnsMaster.amount_spent,
        ViewColumnsMaster.budget,
        ViewColumnsMaster.cpm,
        ViewColumnsMaster.link_clicks,
        ViewColumnsMaster.results,
        ViewColumnsMaster.link_click_through_rate,
        ViewColumnsMaster.cost_per_link_click,
        ViewColumnsMaster.cost_per_result,
        ViewColumnsMaster.impressions,
    ]


class ViewAdQuickScan(ViewQuickScanBase):
    tableName = "vAdInsights"
    columns = [
        ViewColumnsMaster.status,
        ViewColumnsMaster.ad_name,
        ViewColumnsMaster.frequency,
        ViewColumnsMaster.amount_spent,
        ViewColumnsMaster.budget,
        ViewColumnsMaster.cpm,
        ViewColumnsMaster.link_clicks,
        ViewColumnsMaster.results,
        ViewColumnsMaster.link_click_through_rate,
        ViewColumnsMaster.cost_per_link_click,
        ViewColumnsMaster.cost_per_result,
        ViewColumnsMaster.impressions,
    ]
