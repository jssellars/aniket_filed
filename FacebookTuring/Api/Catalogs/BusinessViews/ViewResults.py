from FacebookTuring.Api.Catalogs.Views.ViewsAdsManager.ViewBase import View
from FacebookTuring.Api.Catalogs.Views.ViewsAdsManager.ViewColumnsMaster import ViewColumnsMaster


class ViewCampaignResults(View):
    name = "Results"
    table_name = "vCampaignInsights"
    type = "Business"
    columns = [
        ViewColumnsMaster.status,
        ViewColumnsMaster.campaign_name,
        ViewColumnsMaster.delivery,
        ViewColumnsMaster.bid_strategy,
        ViewColumnsMaster.budget,
        ViewColumnsMaster.results,
        ViewColumnsMaster.reach,
        ViewColumnsMaster.impressions,
        ViewColumnsMaster.cost_per_result,
        ViewColumnsMaster.amount_spent,
        ViewColumnsMaster.stop_time,
        ViewColumnsMaster.video_plays_3s,
        ViewColumnsMaster.video_average_play_time,
    ]


class ViewAdsetResults(ViewCampaignResults):
    table_name = "vAdSetInsights"
    columns = [
        ViewColumnsMaster.status,
        ViewColumnsMaster.adset_name,
        ViewColumnsMaster.delivery,
        ViewColumnsMaster.bid_strategy,
        ViewColumnsMaster.budget,
        ViewColumnsMaster.last_significant_edit,
        ViewColumnsMaster.results,
        ViewColumnsMaster.reach,
        ViewColumnsMaster.impressions,
        ViewColumnsMaster.cost_per_result,
        ViewColumnsMaster.amount_spent,
        ViewColumnsMaster.stop_time,
        ViewColumnsMaster.adset_schedule,
        ViewColumnsMaster.video_plays_3s,
        ViewColumnsMaster.video_average_play_time,
    ]


class ViewAdResults(ViewCampaignResults):
    table_name = "vAdInsights"
    columns = [
        ViewColumnsMaster.status,
        ViewColumnsMaster.ad_name,
        ViewColumnsMaster.delivery,
        ViewColumnsMaster.bid_strategy,
        ViewColumnsMaster.budget,
        ViewColumnsMaster.last_significant_edit,
        ViewColumnsMaster.results,
        ViewColumnsMaster.reach,
        ViewColumnsMaster.impressions,
        ViewColumnsMaster.cost_per_result,
        ViewColumnsMaster.amount_spent,
        ViewColumnsMaster.adset_schedule,
        ViewColumnsMaster.video_plays_3s,
        ViewColumnsMaster.video_average_play_time,
    ]


