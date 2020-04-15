from Core.Web.GoogleAdWordsAPI.Enums.AdWordsPerformanceReportType import AdWordsPerformanceReportType
from GoogleTuring.Api.Catalogs.Views.GoogleView import GoogleView
from GoogleTuring.Api.Catalogs.Views.ViewColumnsMaster.CampaignColumnsMaster import CampaignColumnsMaster
from GoogleTuring.Api.Catalogs.Views.ViewColumnsMaster.GenderColumnsMaster import GenderColumnsMaster


class ViewCampaignBase(GoogleView):
    table_name = "CampaignPerformances"


class ViewCampaignPerformances(ViewCampaignBase):
    view_name = "Campaigns"
    data_source_name = AdWordsPerformanceReportType.CAMPAIGN.value
    type = 1  # Fallback
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
    view_name = "Campaigns - Gender"
    data_source_name = AdWordsPerformanceReportType.GENDER.value
    type = 2  # Business
    columns = [
        GenderColumnsMaster.campaign_name.id,
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
