from Turing.Api.Catalogs.Views.ViewBase import View
from Turing.Api.Catalogs.Views.ViewColumnsMaster import ViewColumnsMaster


class ViewEngagementBase(View):
    name = "Engagement"
    type = "Business"


class ViewCampaignEngagement(ViewEngagementBase):
    table_name = "vCampaignInsights"
    columns = [
        ViewColumnsMaster.effective_status,
        ViewColumnsMaster.campaign_name,
        ViewColumnsMaster.delivery,
        ViewColumnsMaster.post_reaction,
        ViewColumnsMaster.comment,
        # TODO: Add post save column
        ViewColumnsMaster.post_share,
        ViewColumnsMaster.link_click,
        ViewColumnsMaster.like,
        # ViewColumnsMaster.costPerUniqueInlineLinkClick,
        # ViewColumnsMaster.effectShare
    ]


class ViewAdSetEngagement(ViewEngagementBase):
    table_name = "vAdSetInsights"
    columns = [
        ViewColumnsMaster.effective_status,
        ViewColumnsMaster.adset_name,
        ViewColumnsMaster.delivery,
        ViewColumnsMaster.post_reaction,
        ViewColumnsMaster.comment,
        # TODO: Add post save column
        ViewColumnsMaster.post_share,
        ViewColumnsMaster.link_click,
        ViewColumnsMaster.like,
        # ViewColumnsMaster.costPerUniqueInlineLinkClick,
        # ViewColumnsMaster.effectShare
    ]


class ViewAdEngagement(ViewEngagementBase):
    table_name = "vAdInsights"
    columns = [
        ViewColumnsMaster.effective_status,
        ViewColumnsMaster.ad_name,
        ViewColumnsMaster.delivery,
        ViewColumnsMaster.post_reaction,
        ViewColumnsMaster.comment,
        # TODO: Add post save column
        ViewColumnsMaster.post_share,
        ViewColumnsMaster.link_click,
        ViewColumnsMaster.like,
        # ViewColumnsMaster.costPerUniqueInlineLinkClick,
        # ViewColumnsMaster.effectShare
    ]
