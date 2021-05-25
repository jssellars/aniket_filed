from GoogleTuring.Api.Catalogs.Views.ViewsAdsManager.ViewBase import View
from GoogleTuring.Api.Catalogs.Views.ViewsAdsManager.ViewColumnsMaster import ViewColumnsMaster


class ViewCampaignPerformance(View):
    name = "Performance"
    table_name = "vCampaignInsights"
    type = "Business"
    columns = [
        ViewColumnsMaster.campaign_name,
        ViewColumnsMaster.campaign_budget,
        ViewColumnsMaster.clicks,
        ViewColumnsMaster.cost,
        ViewColumnsMaster.impressions,
        ViewColumnsMaster.ctr,
        ViewColumnsMaster.interactions,
        ViewColumnsMaster.interaction_rate,
        ViewColumnsMaster.engagements,
        ViewColumnsMaster.engagement_rate,
        ViewColumnsMaster.invalid_clicks,
        ViewColumnsMaster.invalid_click_rate,
        ViewColumnsMaster.average_cpc,
        ViewColumnsMaster.average_cost,
        ViewColumnsMaster.average_cpe,
        ViewColumnsMaster.average_cpm,
        ViewColumnsMaster.average_cpv,
        ViewColumnsMaster.average_target_cpa,
        ViewColumnsMaster.average_target_roas,
        ViewColumnsMaster.views,
        ViewColumnsMaster.view_rate,
        ViewColumnsMaster.video_p_25,
        ViewColumnsMaster.video_p_50,
        ViewColumnsMaster.video_p_75,
        ViewColumnsMaster.video_p_100,
        ViewColumnsMaster.absolute_top_impression_percentage,
        ViewColumnsMaster.top_impression_percentage,
    ]


class ViewAdGroupPerformance(ViewCampaignPerformance):
    table_name = "vAdGroupInsights"
    columns = [
        ViewColumnsMaster.adgroup_name,
        ViewColumnsMaster.clicks,
        ViewColumnsMaster.cost,
        ViewColumnsMaster.impressions,
        ViewColumnsMaster.ctr,
        ViewColumnsMaster.interactions,
        ViewColumnsMaster.interaction_rate,
        ViewColumnsMaster.engagements,
        ViewColumnsMaster.engagement_rate,
        ViewColumnsMaster.average_cpc,
        ViewColumnsMaster.average_cost,
        ViewColumnsMaster.average_cpe,
        ViewColumnsMaster.average_cpm,
        ViewColumnsMaster.average_cpv,
        ViewColumnsMaster.views,
        ViewColumnsMaster.view_rate,
        ViewColumnsMaster.watch_time,
        ViewColumnsMaster.average_watch_time,
        ViewColumnsMaster.video_p_25,
        ViewColumnsMaster.video_p_50,
        ViewColumnsMaster.video_p_75,
        ViewColumnsMaster.video_p_100,
        ViewColumnsMaster.absolute_top_impression_percentage,
        ViewColumnsMaster.top_impression_percentage,
    ]


class ViewAdPerformance(View):
    name = "Performance"
    table_name = "vAdInsights"
    type = "Business"
    columns = [
        ViewColumnsMaster.ad_name,
        ViewColumnsMaster.clicks,
        ViewColumnsMaster.cost,
        ViewColumnsMaster.impressions,
        ViewColumnsMaster.ctr,
        ViewColumnsMaster.interactions,
        ViewColumnsMaster.interaction_rate,
        ViewColumnsMaster.engagements,
        ViewColumnsMaster.engagement_rate,
        ViewColumnsMaster.average_cpc,
        ViewColumnsMaster.average_cost,
        ViewColumnsMaster.average_cpe,
        ViewColumnsMaster.average_cpm,
        ViewColumnsMaster.average_cpv,
        ViewColumnsMaster.views,
        ViewColumnsMaster.view_rate,
        ViewColumnsMaster.watch_time,
        ViewColumnsMaster.average_watch_time,
        ViewColumnsMaster.video_p_25,
        ViewColumnsMaster.video_p_50,
        ViewColumnsMaster.video_p_75,
        ViewColumnsMaster.video_p_100,
        ViewColumnsMaster.absolute_top_impression_percentage,
        ViewColumnsMaster.top_impression_percentage,
    ]


class ViewKeywordPerformance(View):
    name = "Performance"
    table_name = "vKeywordInsights"
    type = "Business"
    columns = [
        ViewColumnsMaster.keyword_text,
        ViewColumnsMaster.keyword_match_type,
        ViewColumnsMaster.clicks,
        ViewColumnsMaster.cost,
        ViewColumnsMaster.impressions,
        ViewColumnsMaster.ctr,
        ViewColumnsMaster.interactions,
        ViewColumnsMaster.interaction_rate,
        ViewColumnsMaster.engagements,
        ViewColumnsMaster.engagement_rate,
        ViewColumnsMaster.average_cpc,
        ViewColumnsMaster.average_cost,
        ViewColumnsMaster.average_cpe,
        ViewColumnsMaster.average_cpm,
        ViewColumnsMaster.average_cpv,
        ViewColumnsMaster.average_target_cpa,
        ViewColumnsMaster.average_target_roas,
        ViewColumnsMaster.views,
        ViewColumnsMaster.view_rate,
        ViewColumnsMaster.video_p_25,
        ViewColumnsMaster.video_p_50,
        ViewColumnsMaster.video_p_75,
        ViewColumnsMaster.video_p_100,
        ViewColumnsMaster.absolute_top_impression_percentage,
        ViewColumnsMaster.top_impression_percentage,
    ]


class ViewAudiencePerformance(View):
    name = "Performance"
    table_name = "vAudienceInsights"
    type = "Business"
    columns = [
        ViewColumnsMaster.audience_id,
        ViewColumnsMaster.audience,
        ViewColumnsMaster.audience_category,
        ViewColumnsMaster.audience_type,
        ViewColumnsMaster.campaign_id,
        ViewColumnsMaster.campaign_name,
        ViewColumnsMaster.adgroup_id,
        ViewColumnsMaster.adgroup_name,
        ViewColumnsMaster.clicks,
        ViewColumnsMaster.cost,
        ViewColumnsMaster.impressions,
        ViewColumnsMaster.ctr,
        ViewColumnsMaster.interactions,
        ViewColumnsMaster.interaction_rate,
        ViewColumnsMaster.engagements,
        ViewColumnsMaster.engagement_rate,
        ViewColumnsMaster.average_cpc,
        ViewColumnsMaster.average_cost,
        ViewColumnsMaster.average_cpe,
        ViewColumnsMaster.average_cpm,
        ViewColumnsMaster.average_cpv,
        ViewColumnsMaster.average_target_cpa,
        ViewColumnsMaster.average_target_roas,
        ViewColumnsMaster.views,
        ViewColumnsMaster.view_rate,
        ViewColumnsMaster.video_p_25,
        ViewColumnsMaster.video_p_50,
        ViewColumnsMaster.video_p_75,
        ViewColumnsMaster.video_p_100,
    ]


class ViewCampaignFallback(ViewCampaignPerformance):
    name = "Filed default view"
    type = "Fallback"


class ViewAdSetFallback(ViewAdGroupPerformance):
    name = "Filed default view"
    type = "Fallback"


class ViewAdFallback(ViewAdPerformance):
    name = "Filed default view"
    type = "Fallback"
