
from FacebookTuring.Api.Catalogs.Views.ViewsAdsManager.ViewBase import View
from FacebookTuring.Api.Catalogs.Views.ViewsAdsManager.ViewColumnsMaster import ViewColumnsMaster


class ViewOfflineConversionsBase(View):
    name = "Offline conversions"
    type = "Business"


class ViewCampaignOfflineConversions(ViewOfflineConversionsBase):
    table_name = "vCampaignInsights"
    columns = [
        ViewColumnsMaster.status,
        ViewColumnsMaster.campaign_name,
        ViewColumnsMaster.results,
        ViewColumnsMaster.reach,
        ViewColumnsMaster.amount_spent,
        ViewColumnsMaster.offline_purchases_total,
        ViewColumnsMaster.purchases_cost,
        ViewColumnsMaster.offline_leads_total,
        ViewColumnsMaster.leads_cost,
        ViewColumnsMaster.other_offline_conversions_total,
        ViewColumnsMaster.other_offline_conversions_cost,
    ]


class ViewAdSetOfflineConversions(ViewOfflineConversionsBase):
    table_name = "vAdSetInsights"
    columns = [
        ViewColumnsMaster.status,
        ViewColumnsMaster.adset_name,
        ViewColumnsMaster.results,
        ViewColumnsMaster.reach,
        ViewColumnsMaster.amount_spent,
        ViewColumnsMaster.offline_purchases_total,
        ViewColumnsMaster.purchases_cost,
        ViewColumnsMaster.offline_leads_total,
        ViewColumnsMaster.leads_cost,
        ViewColumnsMaster.other_offline_conversions_total,
        ViewColumnsMaster.other_offline_conversions_cost,
    ]


class ViewAdOfflineConversions(ViewOfflineConversionsBase):
    table_name = "vAdInsights"
    columns = [
        ViewColumnsMaster.status,
        ViewColumnsMaster.ad_name,
        ViewColumnsMaster.results,
        ViewColumnsMaster.reach,
        ViewColumnsMaster.amount_spent,
        ViewColumnsMaster.offline_purchases_total,
        ViewColumnsMaster.purchases_cost,
        ViewColumnsMaster.offline_leads_total,
        ViewColumnsMaster.leads_cost,
        ViewColumnsMaster.other_offline_conversions_total,
        ViewColumnsMaster.other_offline_conversions_cost,
    ]
