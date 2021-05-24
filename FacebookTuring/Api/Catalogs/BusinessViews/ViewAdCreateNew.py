from FacebookTuring.Api.Catalogs.Views.ViewsAdsManager.ViewBase import View
from FacebookTuring.Api.Catalogs.Views.ViewsAdsManager.ViewColumnsMaster import ViewColumnsMaster

class ViewAdCreateNew(View):
    name = "Create New Ad"
    table_name = "vAdInsights"
    type = "Business"
    columns = [
        ViewColumnsMaster.status,
        ViewColumnsMaster.ad_name,
        ViewColumnsMaster.ad_image,
        ViewColumnsMaster.reach,
        ViewColumnsMaster.impressions,
        ViewColumnsMaster.results,
        ViewColumnsMaster.cost_per_result,
        ViewColumnsMaster.cost_per_unique_click_all,
        ViewColumnsMaster.unique_ctr_all,
    ]