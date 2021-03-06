from FacebookTuring.Api.Catalogs.Views.ViewsAdsManager.ViewBase import View
from FacebookTuring.Api.Catalogs.Views.ViewsAdsManager.ViewColumnsMaster import ViewColumnsMaster


class ViewDeliveryBase(View):
    name = "Delivery"
    type = "Business"


class ViewCampaignDelivery(ViewDeliveryBase):
    table_name = "vCampaignInsights"
    columns = [
        ViewColumnsMaster.status,
        ViewColumnsMaster.campaign_name,
        ViewColumnsMaster.delivery,
        ViewColumnsMaster.reach,
        ViewColumnsMaster.frequency,
        ViewColumnsMaster.cost_per_1000_people_reached,
        ViewColumnsMaster.impressions,
        ViewColumnsMaster.cpm,
    ]


class ViewAdSetDelivery(ViewDeliveryBase):
    table_name = "vAdSetInsights"
    columns = [
        ViewColumnsMaster.status,
        ViewColumnsMaster.adset_name,
        ViewColumnsMaster.delivery,
        ViewColumnsMaster.reach,
        ViewColumnsMaster.frequency,
        ViewColumnsMaster.cost_per_1000_people_reached,
        ViewColumnsMaster.impressions,
        ViewColumnsMaster.cpm,
    ]


class ViewAdDelivery(ViewDeliveryBase):
    table_name = "vAdInsights"
    columns = [
        ViewColumnsMaster.status,
        ViewColumnsMaster.ad_name,
        ViewColumnsMaster.delivery,
        ViewColumnsMaster.reach,
        ViewColumnsMaster.frequency,
        ViewColumnsMaster.cost_per_1000_people_reached,
        ViewColumnsMaster.impressions,
        ViewColumnsMaster.cpm,
    ]
