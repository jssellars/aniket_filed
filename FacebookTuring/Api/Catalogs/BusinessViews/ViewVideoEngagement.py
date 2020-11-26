from FacebookTuring.Api.Catalogs.Views.ViewsAdsManager.ViewBase import View
from FacebookTuring.Api.Catalogs.Views.ViewsAdsManager.ViewColumnsMaster import ViewColumnsMaster


class ViewVideoEngagementBase(View):
    name = "Video engagement"
    type = "Business"


class ViewCampaignVideoEngagement(ViewVideoEngagementBase):
    table_name = "vCampaignInsights"
    columns = [
        ViewColumnsMaster.status,
        ViewColumnsMaster.campaign_name,
        ViewColumnsMaster.delivery,
        ViewColumnsMaster.impressions,
        ViewColumnsMaster.continuous_video_plays_2s,
        ViewColumnsMaster.cost_per_continuous_video_play_2s,
        ViewColumnsMaster.video_plays_3s,
        ViewColumnsMaster.thru_plays,
        ViewColumnsMaster.cost_per_thru_play,
        ViewColumnsMaster.reach,
        ViewColumnsMaster.amount_spent,
        ViewColumnsMaster.video_plays_25p,
        ViewColumnsMaster.video_plays_50p,
        ViewColumnsMaster.video_plays_75p,
        ViewColumnsMaster.video_plays_95p,
        ViewColumnsMaster.video_plays_100p,
        ViewColumnsMaster.video_plays,
    ]


class ViewAdSetVideoEngagement(ViewVideoEngagementBase):
    table_name = "vAdSetInsights"
    columns = [
        ViewColumnsMaster.status,
        ViewColumnsMaster.adset_name,
        ViewColumnsMaster.delivery,
        ViewColumnsMaster.impressions,
        ViewColumnsMaster.continuous_video_plays_2s,
        ViewColumnsMaster.cost_per_continuous_video_play_2s,
        ViewColumnsMaster.video_plays_3s,
        ViewColumnsMaster.thru_plays,
        ViewColumnsMaster.cost_per_thru_play,
        ViewColumnsMaster.reach,
        ViewColumnsMaster.amount_spent,
        ViewColumnsMaster.video_plays_25p,
        ViewColumnsMaster.video_plays_50p,
        ViewColumnsMaster.video_plays_75p,
        ViewColumnsMaster.video_plays_95p,
        ViewColumnsMaster.video_plays_100p,
        ViewColumnsMaster.video_plays,
    ]


class ViewAdVideoEngagement(ViewVideoEngagementBase):
    table_name = "vAdInsights"
    columns = [
        ViewColumnsMaster.status,
        ViewColumnsMaster.ad_name,
        ViewColumnsMaster.delivery,
        ViewColumnsMaster.impressions,
        ViewColumnsMaster.continuous_video_plays_2s,
        ViewColumnsMaster.cost_per_continuous_video_play_2s,
        ViewColumnsMaster.video_plays_3s,
        ViewColumnsMaster.thru_plays,
        ViewColumnsMaster.cost_per_thru_play,
        ViewColumnsMaster.reach,
        ViewColumnsMaster.amount_spent,
        ViewColumnsMaster.video_plays_25p,
        ViewColumnsMaster.video_plays_50p,
        ViewColumnsMaster.video_plays_75p,
        ViewColumnsMaster.video_plays_95p,
        ViewColumnsMaster.video_plays_100p,
        ViewColumnsMaster.video_plays,
    ]
