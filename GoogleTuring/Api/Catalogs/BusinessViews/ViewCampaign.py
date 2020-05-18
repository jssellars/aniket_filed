from GoogleTuring.Api.Catalogs.BusinessViews.TableEnum import TableEnum
from GoogleTuring.Api.Catalogs.Views.GoogleView import GoogleView
from GoogleTuring.Api.Catalogs.Views.ViewColumnsMaster.Levels.Breakdowns.AgeRange.CampaignAgeRangeColumnsMaster import \
    CampaignAgeRangeColumnsMaster
from GoogleTuring.Api.Catalogs.Views.ViewColumnsMaster.Levels.Breakdowns.Gender.CampaignGenderColumnsMaster import \
    CampaignGenderColumnsMaster
from GoogleTuring.Api.Catalogs.Views.ViewColumnsMaster.Levels.Breakdowns.Keywords.CampaignKeywordsColumnsMaster import \
    CampaignKeywordsColumnsMaster
from GoogleTuring.Api.Catalogs.Views.ViewColumnsMaster.Levels.CampaignColumnsMaster import CampaignColumnsMaster
from GoogleTuring.Api.Catalogs.Views.ViewTypeEnum import ViewTypeEnum
from GoogleTuring.Infrastructure.Domain.Enums.FiledGoogleInsightsTableEnum import FiledGoogleInsightsTableEnum


class ViewCampaignBase(GoogleView):
    table_name = TableEnum.CAMPAIGN_PERFORMANCES.value


class ViewCampaign(ViewCampaignBase):
    view_name = "Campaigns"
    data_source_name = FiledGoogleInsightsTableEnum.CAMPAIGN.value
    type = ViewTypeEnum.BUSINESS.value
    columns = [
        CampaignColumnsMaster.enable_pause_campaign.id,
        CampaignColumnsMaster.campaign_name.id,
        CampaignColumnsMaster.amount.id,
        CampaignColumnsMaster.campaign_status.id,
        CampaignColumnsMaster.cost.id,
        CampaignColumnsMaster.impressions.id,
        CampaignColumnsMaster.average_cpm.id,
        CampaignColumnsMaster.clicks.id,
        CampaignColumnsMaster.average_cpc.id,
        CampaignColumnsMaster.ctr.id,
        CampaignColumnsMaster.conversions.id,
        CampaignColumnsMaster.conversion_rate.id,
        CampaignColumnsMaster.cost_per_conversion.id
    ]


class ViewCampaignGender(ViewCampaignBase):
    view_name = "Demographics - Gender"
    data_source_name = FiledGoogleInsightsTableEnum.GENDER.value
    type = ViewTypeEnum.BUSINESS.value
    columns = [
        CampaignGenderColumnsMaster.enable_pause_campaign.id,
        CampaignGenderColumnsMaster.gender.id,
        CampaignGenderColumnsMaster.campaign_name.id,
        CampaignGenderColumnsMaster.status.id,
        CampaignGenderColumnsMaster.average_cpv.id,
        CampaignGenderColumnsMaster.bid_modifier.id,
        CampaignGenderColumnsMaster.impressions.id,
        CampaignGenderColumnsMaster.interactions.id,
        CampaignGenderColumnsMaster.interaction_rate.id,
        CampaignGenderColumnsMaster.average_cost.id,
        CampaignGenderColumnsMaster.cost.id,
        CampaignGenderColumnsMaster.conversion_rate.id,
        CampaignGenderColumnsMaster.conversions.id,
        CampaignGenderColumnsMaster.cost_per_conversion.id
    ]


class ViewCampaignKeywords(ViewCampaignBase):
    table_name = TableEnum.CAMPAIGN_PERFORMANCES.value
    view_name = "Search Keywords"
    data_source_name = FiledGoogleInsightsTableEnum.KEYWORDS.value
    type = ViewTypeEnum.BUSINESS.value
    columns = [
        CampaignKeywordsColumnsMaster.enable_pause_keyword.id,
        CampaignKeywordsColumnsMaster.keyword.id,
        CampaignKeywordsColumnsMaster.campaign_name.id,
        CampaignKeywordsColumnsMaster.status.id,
        CampaignKeywordsColumnsMaster.max_cpc.id,
        CampaignKeywordsColumnsMaster.approval_status.id,
        CampaignKeywordsColumnsMaster.final_urls.id,
        CampaignKeywordsColumnsMaster.impressions.id,
        CampaignKeywordsColumnsMaster.interactions.id,
        CampaignKeywordsColumnsMaster.interaction_rate.id,
        CampaignKeywordsColumnsMaster.average_cost.id,
        CampaignKeywordsColumnsMaster.cost.id,
        CampaignKeywordsColumnsMaster.conversion_rate.id,
        CampaignKeywordsColumnsMaster.conversions.id,
        CampaignKeywordsColumnsMaster.cost_per_conversion.id
    ]


class ViewCampaignAge(ViewCampaignBase):
    view_name = "Demographics - Age"
    data_source_name = FiledGoogleInsightsTableEnum.AGE_RANGE.value
    type = ViewTypeEnum.BUSINESS.value
    columns = [
        CampaignAgeRangeColumnsMaster.enable_pause_campaign.id,
        CampaignAgeRangeColumnsMaster.age_range.id,
        CampaignAgeRangeColumnsMaster.campaign_name.id,
        CampaignAgeRangeColumnsMaster.status.id,
        CampaignAgeRangeColumnsMaster.average_cpv.id,
        CampaignAgeRangeColumnsMaster.bid_modifier.id,
        CampaignAgeRangeColumnsMaster.impressions.id,
        CampaignAgeRangeColumnsMaster.interactions.id,
        CampaignAgeRangeColumnsMaster.interaction_rate.id,
        CampaignAgeRangeColumnsMaster.average_cost.id,
        CampaignAgeRangeColumnsMaster.cost.id,
        CampaignAgeRangeColumnsMaster.conversion_rate.id,
        CampaignAgeRangeColumnsMaster.conversions.id,
        CampaignAgeRangeColumnsMaster.cost_per_conversion.id
    ]
