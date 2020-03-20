from Turing.Api.Catalogs.Views.ViewBase import View
from Turing.Api.Catalogs.Views.ViewColumnsMaster import ViewColumnsMaster


class ViewVideoEngagementBase(View):
    name = "Video engagement"
    type = "Business"


class ViewCampaignVideoEngagement(ViewVideoEngagementBase):
    table_name = "vCampaignInsights"
    columns = [
        ViewColumnsMaster.effective_status,
        ViewColumnsMaster.campaign_name,
        ViewColumnsMaster.delivery,
        ViewColumnsMaster.total_video_thruplay_watched_actions,
        ViewColumnsMaster.cost_per_total_video_thruplay_watched_actions,
        ViewColumnsMaster.spend,
        ViewColumnsMaster.total_video_p25_watched_actions,
        ViewColumnsMaster.total_video_p50_watched_actions,
        ViewColumnsMaster.total_video_p100_watched_actions
    ]


class ViewAdSetVideoEngagement(ViewVideoEngagementBase):
    table_name = "vAdSetInsights"
    columns = [
        ViewColumnsMaster.effective_status,
        ViewColumnsMaster.adset_name,
        ViewColumnsMaster.delivery,
        ViewColumnsMaster.total_video_thruplay_watched_actions,
        ViewColumnsMaster.cost_per_total_video_thruplay_watched_actions,
        ViewColumnsMaster.spend,
        ViewColumnsMaster.total_video_p25_watched_actions,
        ViewColumnsMaster.total_video_p50_watched_actions,
        ViewColumnsMaster.total_video_p100_watched_actions
    ]


class ViewAdVideoEngagement(ViewVideoEngagementBase):
    table_name = "vAdInsights"
    columns = [
        ViewColumnsMaster.effective_status,
        ViewColumnsMaster.ad_name,
        ViewColumnsMaster.delivery,
        ViewColumnsMaster.total_video_thruplay_watched_actions,
        ViewColumnsMaster.cost_per_total_video_thruplay_watched_actions,
        ViewColumnsMaster.spend,
        ViewColumnsMaster.total_video_p25_watched_actions,
        ViewColumnsMaster.total_video_p50_watched_actions,
        ViewColumnsMaster.total_video_p100_watched_actions
    ]