from FacebookTuring.Api.Catalogs.Views.ViewBase import View
from FacebookTuring.Api.Catalogs.Views.ViewColumnsMaster import ViewColumnsMaster


class ViewEngagementBase(View):
    name = "Engagement"
    type = "Business"


class ViewCampaignEngagement(ViewEngagementBase):
    table_name = "vCampaignInsights"
    columns = [
        ViewColumnsMaster.status,
        ViewColumnsMaster.campaign_name,
        ViewColumnsMaster.delivery,
        ViewColumnsMaster.post_reactions,
        ViewColumnsMaster.post_comments,
        ViewColumnsMaster.post_saves,
        ViewColumnsMaster.post_shares,
        ViewColumnsMaster.link_clicks,
        ViewColumnsMaster.page_likes,
        ViewColumnsMaster.cost_per_unique_link_click
        # todo: effects share
    ]


class ViewAdSetEngagement(ViewEngagementBase):
    table_name = "vAdSetInsights"
    columns = [
        ViewColumnsMaster.status,
        ViewColumnsMaster.adset_name,
        ViewColumnsMaster.delivery,
        ViewColumnsMaster.post_reactions,
        ViewColumnsMaster.post_comments,
        ViewColumnsMaster.post_saves,
        ViewColumnsMaster.post_shares,
        ViewColumnsMaster.link_clicks,
        ViewColumnsMaster.page_likes,
        ViewColumnsMaster.cost_per_unique_link_click
        # ViewColumnsMaster.effectShare
    ]


class ViewAdEngagement(ViewEngagementBase):
    table_name = "vAdInsights"
    columns = [
        ViewColumnsMaster.status,
        ViewColumnsMaster.ad_name,
        ViewColumnsMaster.delivery,
        ViewColumnsMaster.post_reactions,
        ViewColumnsMaster.post_comments,
        ViewColumnsMaster.post_saves,
        ViewColumnsMaster.post_shares,
        ViewColumnsMaster.link_clicks,
        ViewColumnsMaster.page_likes,
        ViewColumnsMaster.cost_per_unique_link_click
        # ViewColumnsMaster.effectShare
    ]
