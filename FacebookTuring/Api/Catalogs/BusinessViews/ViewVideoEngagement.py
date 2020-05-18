from FacebookTuring.Api.Catalogs.Views.ViewBase import View
from FacebookTuring.Api.Catalogs.Views.ViewColumnsMaster import ViewColumnsMaster


class ViewVideoEngagementBase(View):
    name = "Video engagement"
    type = "Business"


class ViewCampaignVideoEngagement(ViewVideoEngagementBase):
    table_name = "vCampaignInsights"
    columns = [
        ViewColumnsMaster.status,
        ViewColumnsMaster.campaign_name,
        ViewColumnsMaster.delivery,
        ViewColumnsMaster.thru_plays,
        ViewColumnsMaster.cost_per_thru_play,
        ViewColumnsMaster.amount_spent,
        ViewColumnsMaster.video_plays_25p,
        ViewColumnsMaster.video_plays_50p,
        ViewColumnsMaster.video_plays_100p
    ]


class ViewAdSetVideoEngagement(ViewVideoEngagementBase):
    table_name = "vAdSetInsights"
    columns = [
        ViewColumnsMaster.status,
        ViewColumnsMaster.adset_name,
        ViewColumnsMaster.delivery,
        ViewColumnsMaster.thru_plays,
        ViewColumnsMaster.cost_per_thru_play,
        ViewColumnsMaster.amount_spent,
        ViewColumnsMaster.video_plays_25p,
        ViewColumnsMaster.video_plays_50p,
        ViewColumnsMaster.video_plays_100p
    ]


class ViewAdVideoEngagement(ViewVideoEngagementBase):
    table_name = "vAdInsights"
    columns = [
        ViewColumnsMaster.status,
        ViewColumnsMaster.ad_name,
        ViewColumnsMaster.delivery,
        ViewColumnsMaster.thru_plays,
        ViewColumnsMaster.cost_per_thru_play,
        ViewColumnsMaster.amount_spent,
        ViewColumnsMaster.video_plays_25p,
        ViewColumnsMaster.video_plays_50p,
        ViewColumnsMaster.video_plays_100p
    ]
