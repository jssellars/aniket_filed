from FacebookTuring.Api.Catalogs.Views.ViewBase import View
from FacebookTuring.Api.Catalogs.Views.ViewColumnsMaster import ViewColumnsMaster


class ViewDeliveryBase(View):
    name = "Delivery"
    type = "Business"


class ViewCampaignDelivery(ViewDeliveryBase):
    table_name = "vCampaignInsights"
    columns = [
        ViewColumnsMaster.effective_status,
        ViewColumnsMaster.campaign_name,
        ViewColumnsMaster.delivery,
        ViewColumnsMaster.reach,
        ViewColumnsMaster.cost_per_1000_people_reached,
        ViewColumnsMaster.impressions,
        ViewColumnsMaster.cpm,
        ViewColumnsMaster.frequency
    ]


class ViewAdSetDelivery(ViewDeliveryBase):
    table_name = "vAdSetInsights"
    columns = [
        ViewColumnsMaster.effective_status,
        ViewColumnsMaster.adset_name,
        ViewColumnsMaster.delivery,
        ViewColumnsMaster.reach,
        ViewColumnsMaster.cost_per_1000_people_reached,
        ViewColumnsMaster.impressions,
        ViewColumnsMaster.cpm,
        ViewColumnsMaster.frequency
    ]


class ViewAdDelivery(ViewDeliveryBase):
    table_name = "vAdInsights"
    columns = [
        ViewColumnsMaster.effective_status,
        ViewColumnsMaster.ad_name,
        ViewColumnsMaster.delivery,
        ViewColumnsMaster.reach,
        ViewColumnsMaster.cost_per_1000_people_reached,
        ViewColumnsMaster.impressions,
        ViewColumnsMaster.cpm,
        ViewColumnsMaster.frequency
    ]