from Turing.Api.Catalogs.Views.ViewBase import View
from Turing.Api.Catalogs.Views.ViewColumnsMaster import ViewColumnsMaster


class ViewAppEngagementBase(View):
    name = "App engagement"
    type = "Business"


class ViewCampaignAppEngagement(ViewAppEngagementBase):
    tableName = "vCampaignInsights"
    columns = [
        ViewColumnsMaster.effective_status,
        ViewColumnsMaster.campaign_name,
        ViewColumnsMaster.delivery,
        # ViewColumnsMaster.omniMobileAppInstall,
        # ViewColumnsMaster.mobileAppInstall,
        # TODO: get desktop mobile app install column
        # ViewColumnsMaster.costPerUniqueMobileAppInstall,
        # TODO: get COST per desktop mobile app install column
        ViewColumnsMaster.spend
    ]


class ViewAdSetAppEngagement(ViewAppEngagementBase):
    tableName = "vAdSetInsights"
    columns = [
        ViewColumnsMaster.effective_status,
        ViewColumnsMaster.adset_name,
        ViewColumnsMaster.delivery,
        # ViewColumnsMaster.omniMobileAppInstall,
        # ViewColumnsMaster.mobileAppInstall,
        # TODO: get desktop mobile app install column
        # ViewColumnsMaster.costPerUniqueMobileAppInstall,
        # TODO: get COST per desktop mobile app install column
        ViewColumnsMaster.spend
    ]


class ViewAdAppEngagement(ViewAppEngagementBase):
    tableName = "vAdInsights"
    columns = [
        ViewColumnsMaster.effective_status,
        ViewColumnsMaster.ad_name,
        ViewColumnsMaster.delivery,
        # ViewColumnsMaster.omniMobileAppInstall,
        # ViewColumnsMaster.mobileAppInstall,
        # TODO: get desktop mobile app install column
        # ViewColumnsMaster.costPerUniqueMobileAppInstall,
        # TODO: get COST per desktop mobile app install column
        ViewColumnsMaster.spend
    ]