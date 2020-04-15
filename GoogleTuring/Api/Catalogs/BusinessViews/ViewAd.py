from Core.Web.GoogleAdWordsAPI.Enums.AdWordsPerformanceReportType import AdWordsPerformanceReportType
from GoogleTuring.Api.Catalogs.Views.GoogleView import GoogleView
from GoogleTuring.Api.Catalogs.Views.ViewColumnsMaster.AdColumnsMaster import AdColumnsMaster


class ViewAd(GoogleView):
    table_name = "Ad Performances"
    view_name = "Ads"
    data_source_name = AdWordsPerformanceReportType.AD.value
    type = 1  # Fallback
    columns = [
        AdColumnsMaster.enable_pause_ad.id,
        AdColumnsMaster.headline.id,
        AdColumnsMaster.campaign_name.id,
        AdColumnsMaster.ad_group_name.id,
        AdColumnsMaster.status.id,
        AdColumnsMaster.ad_type.id,
        AdColumnsMaster.impressions.id,
        AdColumnsMaster.interactions.id,
        AdColumnsMaster.interaction_rate.id,
        AdColumnsMaster.average_cost.id,
        AdColumnsMaster.cost.id,
        # Video ?
        AdColumnsMaster.conversion_rate.id,
        AdColumnsMaster.conversions.id,
        AdColumnsMaster.cost_per_conversion.id
    ]
