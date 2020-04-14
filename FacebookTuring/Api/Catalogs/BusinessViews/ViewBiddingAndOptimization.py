from FacebookTuring.Api.Catalogs.Views.ViewBase import View
from FacebookTuring.Api.Catalogs.Views.ViewColumnsMaster import ViewColumnsMaster


class ViewBiddingAndOptimizationBase(View):
    name = "Bidding and optimization"
    type = "Business"


class ViewCampaignBiddingAndOptimization(ViewBiddingAndOptimizationBase):
    tableName = "vCampaignInsights"
    columns = [
        ViewColumnsMaster.effective_status,
        ViewColumnsMaster.campaign_name,
        ViewColumnsMaster.delivery,
        ViewColumnsMaster.results,
        ViewColumnsMaster.cost_per_result,
        ViewColumnsMaster.budget,
        ViewColumnsMaster.spend
    ]


class ViewAdSetBiddingAndOptimization(ViewBiddingAndOptimizationBase):
    tableName = "vAdSetInsights"
    columns = [
        ViewColumnsMaster.effective_status,
        ViewColumnsMaster.adset_name,
        ViewColumnsMaster.delivery,
        ViewColumnsMaster.results,
        ViewColumnsMaster.cost_per_result,
        # TODO: get facebook optimization events
        # TODO: get COST per optimization event
        ViewColumnsMaster.bid_strategy,
        ViewColumnsMaster.last_significant_edit,
        ViewColumnsMaster.budget,
        ViewColumnsMaster.spend,
        # TODO: add adset schedule column
    ]


class ViewAdBiddingAndOptimization(ViewBiddingAndOptimizationBase):
    tableName = "vAdInsights"
    columns = [
        ViewColumnsMaster.effective_status,
        ViewColumnsMaster.ad_name,
        ViewColumnsMaster.delivery,
        ViewColumnsMaster.results,
        ViewColumnsMaster.cost_per_result,
        ViewColumnsMaster.bid_strategy,
        ViewColumnsMaster.last_significant_edit,
        ViewColumnsMaster.budget,
        ViewColumnsMaster.spend
    ]

