from Core.Web.GoogleAdWordsAPI.Enums.AdWordsPerformanceReportType import AdWordsPerformanceReportType
from GoogleTuring.Api.Catalogs.Views.GoogleView import GoogleView
from GoogleTuring.Api.Catalogs.Views.ViewColumnsMaster.AdGroupColumnsMaster import AdGroupColumnsMaster
from GoogleTuring.Api.Catalogs.Views.ViewColumnsMaster.GenderColumnsMaster import GenderColumnsMaster


class ViewAdGroupBase(GoogleView):
    table_name = "Ad Group Performances"


class ViewAdGroup(ViewAdGroupBase):
    view_name = "Ad Groups"
    data_source_name = AdWordsPerformanceReportType.AD_GROUP.value
    type = 1  # Fallback
    columns = [
        AdGroupColumnsMaster.enable_pause_ad_group.id,
        AdGroupColumnsMaster.ad_group_name.id,
        AdGroupColumnsMaster.campaign_name.id,
        AdGroupColumnsMaster.ad_group_status.id,
        AdGroupColumnsMaster.cpc_bid.id,
        AdGroupColumnsMaster.cpv_bid.id,
        AdGroupColumnsMaster.ad_group_type.id,
        AdGroupColumnsMaster.impressions.id,
        AdGroupColumnsMaster.interactions.id,
        AdGroupColumnsMaster.interaction_rate.id,
        AdGroupColumnsMaster.average_cost.id,
        AdGroupColumnsMaster.cost.id,
        AdGroupColumnsMaster.conversion_rate.id,
        AdGroupColumnsMaster.conversions.id,
        AdGroupColumnsMaster.cost_per_conversion.id
    ]


class ViewAdGroupGender(ViewAdGroupBase):
    view_name = "Ad Groups - Gender"
    data_source_name = AdWordsPerformanceReportType.GENDER.value
    type = 2  # Business
    columns = [
        GenderColumnsMaster.campaign_name.id,
        GenderColumnsMaster.ad_group_name.id,
        GenderColumnsMaster.status.id,
        GenderColumnsMaster.average_cpv.id,
        GenderColumnsMaster.bid_modifier.id,
        GenderColumnsMaster.impressions.id,
        GenderColumnsMaster.interactions.id,
        GenderColumnsMaster.interaction_rate.id,
        GenderColumnsMaster.average_cost.id,
        GenderColumnsMaster.cost.id,
        GenderColumnsMaster.conversion_rate.id,
        GenderColumnsMaster.conversions.id,
        GenderColumnsMaster.cost_per_conversion.id
    ]
