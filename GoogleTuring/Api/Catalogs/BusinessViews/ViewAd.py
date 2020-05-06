from GoogleTuring.Api.Catalogs.Views.ViewTypeEnum import ViewTypeEnum
from GoogleTuring.Infrastructure.Domain.Enums.FiledGoogleInsightsTableEnum import FiledGoogleInsightsTableEnum
from GoogleTuring.Api.Catalogs.BusinessViews.TableEnum import TableEnum
from GoogleTuring.Api.Catalogs.Views.GoogleView import GoogleView
from GoogleTuring.Api.Catalogs.Views.ViewColumnsMaster.Levels.AdColumnsMaster import AdColumnsMaster


class ViewAd(GoogleView):
    table_name = TableEnum.AD_PERFORMANCES.value
    view_name = "Ads"
    data_source_name = FiledGoogleInsightsTableEnum.AD.value
    type = ViewTypeEnum.BUSINESS.value
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
