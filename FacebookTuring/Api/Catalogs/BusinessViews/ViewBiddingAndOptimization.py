from FacebookTuring.Api.Catalogs.Views.ViewBase import View
from FacebookTuring.Api.Catalogs.Views.ViewColumnsMaster import ViewColumnsMaster


class ViewBiddingAndOptimizationBase(View):
    name = "Bidding and optimization"
    type = "Business"


class ViewCampaignBiddingAndOptimization(ViewBiddingAndOptimizationBase):
    tableName = "vCampaignInsights"
    columns = [
        ViewColumnsMaster.status,
        ViewColumnsMaster.campaign_name,
        ViewColumnsMaster.delivery,
        ViewColumnsMaster.results,
        ViewColumnsMaster.cost_per_result,
        ViewColumnsMaster.budget,
        ViewColumnsMaster.amount_spent
    ]


class ViewAdSetBiddingAndOptimization(ViewBiddingAndOptimizationBase):
    tableName = "vAdSetInsights"
    columns = [
        ViewColumnsMaster.status,
        ViewColumnsMaster.adset_name,
        ViewColumnsMaster.delivery,
        ViewColumnsMaster.results,
        ViewColumnsMaster.cost_per_result,
        # TODO: get facebook optimization events
        # TODO: get COST per optimization event
        ViewColumnsMaster.bid_strategy,
        ViewColumnsMaster.last_significant_edit,
        ViewColumnsMaster.budget,
        ViewColumnsMaster.amount_spent,
        ViewColumnsMaster.adset_schedule
    ]


class ViewAdBiddingAndOptimization(ViewBiddingAndOptimizationBase):
    tableName = "vAdInsights"
    columns = [
        ViewColumnsMaster.status,
        ViewColumnsMaster.ad_name,
        ViewColumnsMaster.delivery,
        ViewColumnsMaster.results,
        ViewColumnsMaster.cost_per_result,
        ViewColumnsMaster.bid_strategy,
        ViewColumnsMaster.last_significant_edit,
        ViewColumnsMaster.budget,
        ViewColumnsMaster.amount_spent
    ]
