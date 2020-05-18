from GoogleTuring.Api.Catalogs.BusinessViews.TableEnum import TableEnum
from GoogleTuring.Api.Catalogs.Views.GoogleView import GoogleView
from GoogleTuring.Api.Catalogs.Views.ViewColumnsMaster.Levels.AdGroupColumnsMaster import AdGroupColumnsMaster
from GoogleTuring.Api.Catalogs.Views.ViewColumnsMaster.Levels.Breakdowns.AgeRange.AdGroupAgeRangeColumnsMaster import \
    AdGroupAgeRangeColumnsMaster
from GoogleTuring.Api.Catalogs.Views.ViewColumnsMaster.Levels.Breakdowns.Gender.AdGroupGenderColumnsMaster import \
    AdGroupGenderColumnsMaster
from GoogleTuring.Api.Catalogs.Views.ViewColumnsMaster.Levels.Breakdowns.Keywords.AdGroupKeywordsColumnsMaster import \
    AdGroupKeywordsColumnsMaster
from GoogleTuring.Api.Catalogs.Views.ViewTypeEnum import ViewTypeEnum
from GoogleTuring.Infrastructure.Domain.Enums.FiledGoogleInsightsTableEnum import FiledGoogleInsightsTableEnum


class ViewAdGroupBase(GoogleView):
    table_name = TableEnum.AD_GROUP_PERFORMANCES.value


class ViewAdGroup(ViewAdGroupBase):
    view_name = "Ad Groups"
    data_source_name = FiledGoogleInsightsTableEnum.AD_GROUP.value
    type = ViewTypeEnum.BUSINESS.value
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
    view_name = "Demographics - Gender"
    data_source_name = FiledGoogleInsightsTableEnum.GENDER.value
    type = ViewTypeEnum.BUSINESS.value
    columns = [
        AdGroupGenderColumnsMaster.enable_pause_ad_group.id,
        AdGroupGenderColumnsMaster.gender.id,
        AdGroupGenderColumnsMaster.campaign_name.id,
        AdGroupGenderColumnsMaster.ad_group_name.id,
        AdGroupGenderColumnsMaster.status.id,
        AdGroupGenderColumnsMaster.average_cpv.id,
        AdGroupGenderColumnsMaster.bid_modifier.id,
        AdGroupGenderColumnsMaster.impressions.id,
        AdGroupGenderColumnsMaster.interactions.id,
        AdGroupGenderColumnsMaster.interaction_rate.id,
        AdGroupGenderColumnsMaster.average_cost.id,
        AdGroupGenderColumnsMaster.cost.id,
        AdGroupGenderColumnsMaster.conversion_rate.id,
        AdGroupGenderColumnsMaster.conversions.id,
        AdGroupGenderColumnsMaster.cost_per_conversion.id
    ]


class ViewAdGroupKeywords(GoogleView):
    table_name = TableEnum.AD_PERFORMANCES.value
    view_name = "Search Keywords"
    data_source_name = FiledGoogleInsightsTableEnum.KEYWORDS.value
    type = ViewTypeEnum.BUSINESS.value
    columns = [
        AdGroupKeywordsColumnsMaster.enable_pause_keyword.id,
        AdGroupKeywordsColumnsMaster.keyword.id,
        AdGroupKeywordsColumnsMaster.campaign_name.id,
        AdGroupKeywordsColumnsMaster.ad_group_name.id,
        AdGroupKeywordsColumnsMaster.status.id,
        AdGroupKeywordsColumnsMaster.max_cpc.id,
        AdGroupKeywordsColumnsMaster.approval_status.id,
        AdGroupKeywordsColumnsMaster.final_urls.id,
        AdGroupKeywordsColumnsMaster.impressions.id,
        AdGroupKeywordsColumnsMaster.interactions.id,
        AdGroupKeywordsColumnsMaster.interaction_rate.id,
        AdGroupKeywordsColumnsMaster.average_cost.id,
        AdGroupKeywordsColumnsMaster.cost.id,
        AdGroupKeywordsColumnsMaster.conversion_rate.id,
        AdGroupKeywordsColumnsMaster.conversions.id,
        AdGroupKeywordsColumnsMaster.cost_per_conversion.id
    ]


class ViewAdGroupAge(GoogleView):
    table_name = TableEnum.AD_PERFORMANCES.value
    view_name = "Demographics - Age"
    data_source_name = FiledGoogleInsightsTableEnum.AGE_RANGE.value
    type = ViewTypeEnum.BUSINESS.value
    columns = [
        AdGroupAgeRangeColumnsMaster.enable_pause_ad_group.id,
        AdGroupAgeRangeColumnsMaster.age_range.id,
        AdGroupAgeRangeColumnsMaster.campaign_name.id,
        AdGroupAgeRangeColumnsMaster.ad_group_name.id,
        AdGroupAgeRangeColumnsMaster.status.id,
        AdGroupAgeRangeColumnsMaster.average_cpv.id,
        AdGroupAgeRangeColumnsMaster.bid_modifier.id,
        AdGroupAgeRangeColumnsMaster.impressions.id,
        AdGroupAgeRangeColumnsMaster.interactions.id,
        AdGroupAgeRangeColumnsMaster.interaction_rate.id,
        AdGroupAgeRangeColumnsMaster.average_cost.id,
        AdGroupAgeRangeColumnsMaster.cost.id,
        AdGroupAgeRangeColumnsMaster.conversion_rate.id,
        AdGroupAgeRangeColumnsMaster.conversions.id,
        AdGroupAgeRangeColumnsMaster.cost_per_conversion.id
    ]
