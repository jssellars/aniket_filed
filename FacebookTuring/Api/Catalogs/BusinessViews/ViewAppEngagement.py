from FacebookTuring.Api.Catalogs.Views.ViewBase import View
from FacebookTuring.Api.Catalogs.Views.ViewColumnsMaster import ViewColumnsMaster


class ViewAppEngagementBase(View):
    name = "App engagement"
    type = "Business"


class ViewCampaignAppEngagement(ViewAppEngagementBase):
    tableName = "vCampaignInsights"
    columns = [
        ViewColumnsMaster.status,
        ViewColumnsMaster.campaign_name,
        ViewColumnsMaster.delivery,
        ViewColumnsMaster.mobile_app_installs_total,
        ViewColumnsMaster.website_app_installs_total,
        ViewColumnsMaster.app_install_cost,
        # TODO: get COST per desktop mobile app install column
        ViewColumnsMaster.amount_spent
    ]


class ViewAdSetAppEngagement(ViewAppEngagementBase):
    tableName = "vAdSetInsights"
    columns = [
        ViewColumnsMaster.status,
        ViewColumnsMaster.adset_name,
        ViewColumnsMaster.delivery,
        ViewColumnsMaster.mobile_app_installs_total,
        ViewColumnsMaster.website_app_installs_total,
        ViewColumnsMaster.app_install_cost,
        # TODO: get COST per desktop mobile app install column
        ViewColumnsMaster.amount_spent
    ]


class ViewAdAppEngagement(ViewAppEngagementBase):
    tableName = "vAdInsights"
    columns = [
        ViewColumnsMaster.status,
        ViewColumnsMaster.ad_name,
        ViewColumnsMaster.delivery,
        ViewColumnsMaster.mobile_app_installs_total,
        ViewColumnsMaster.website_app_installs_total,
        ViewColumnsMaster.app_install_cost,
        # TODO: get COST per desktop mobile app install column
        ViewColumnsMaster.amount_spent
    ]
