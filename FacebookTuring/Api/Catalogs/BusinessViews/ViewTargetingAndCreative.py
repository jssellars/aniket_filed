from FacebookTuring.Api.Catalogs.Views.ViewBase import View
from FacebookTuring.Api.Catalogs.Views.ViewColumnsMaster import ViewColumnsMaster


class ViewTargetingAndCreativeBase(View):
    name = "Bidding and optimization"
    type = "Business"


class ViewCampaignTargetingAndCreative(ViewTargetingAndCreativeBase):
    table_name = "vCampaignInsights"
    columns = [
        ViewColumnsMaster.effective_status,
        ViewColumnsMaster.campaign_name,
        ViewColumnsMaster.results,
        ViewColumnsMaster.cost_per_result,
        ViewColumnsMaster.budget,
        ViewColumnsMaster.spend,
        ViewColumnsMaster.end_date,
        ViewColumnsMaster.reach,
        ViewColumnsMaster.cost_per_1000_people_reached,
        ViewColumnsMaster.link_click,
        # TODO: get COST per link click column
        # TODO: get ctr per link click
        ViewColumnsMaster.cpc,
        ViewColumnsMaster.ctr,
        ViewColumnsMaster.clicks
    ]


class ViewAdSetTargetingAndCreative(ViewTargetingAndCreativeBase):
    table_name = "vAdSetInsights"
    columns = [
        ViewColumnsMaster.effective_status,
        ViewColumnsMaster.adset_name,
        ViewColumnsMaster.delivery,
        ViewColumnsMaster.results,
        ViewColumnsMaster.reach,
        ViewColumnsMaster.frequency,
        ViewColumnsMaster.cost_per_result,
        ViewColumnsMaster.budget,
        ViewColumnsMaster.spend,
        ViewColumnsMaster.end_date,
        # TODO: get ad set schedule
        ViewColumnsMaster.location,
        ViewColumnsMaster.age,
        ViewColumnsMaster.gender,
        ViewColumnsMaster.impressions,
        ViewColumnsMaster.cpm,
        ViewColumnsMaster.link_click,
        # TODO: get COST per link click column
        # TODO: get ctr per link click
        ViewColumnsMaster.clicks,
        ViewColumnsMaster.ctr,
        ViewColumnsMaster.cpc
    ]


class ViewAdTargetingAndCreative(ViewTargetingAndCreativeBase):
    table_name = "vAdInsights"
    columns = [
        ViewColumnsMaster.effective_status,
        ViewColumnsMaster.ad_name,
        ViewColumnsMaster.delivery,
        ViewColumnsMaster.results,
        ViewColumnsMaster.reach,
        ViewColumnsMaster.frequency,
        ViewColumnsMaster.cost_per_result,
        ViewColumnsMaster.budget,
        ViewColumnsMaster.spend,
        ViewColumnsMaster.end_date,
        # TODO: get ad schedule
        ViewColumnsMaster.quality_ranking,
        ViewColumnsMaster.engagement_rate_ranking,
        ViewColumnsMaster.conversion_rate_ranking,
        ViewColumnsMaster.headline,
        ViewColumnsMaster.body,
        ViewColumnsMaster.destination,
        ViewColumnsMaster.link,
        ViewColumnsMaster.page_name,
        # TODO: get preview link
        ViewColumnsMaster.impressions,
        ViewColumnsMaster.cpm,
        ViewColumnsMaster.link_click,
        # TODO: get COST per link click column
        # TODO: get ctr per link click
        ViewColumnsMaster.clicks,
        ViewColumnsMaster.ctr,
        ViewColumnsMaster.cpc
    ]