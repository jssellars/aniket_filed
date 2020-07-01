from Core.Tools.Misc.EnumerationBase import EnumerationBase
from GoogleTuring.Api.Catalogs.ReportModels.Levels.Ad.AdReportEnum import AdReportEnum
from GoogleTuring.Api.Catalogs.ReportModels.Levels.AdGroup.AdGroupReportEnum import AdGroupReportEnum
from GoogleTuring.Api.Catalogs.ReportModels.Levels.Campaign.CampaignReportEnum import CampaignReportEnum
from GoogleTuring.Infrastructure.Domain.Enums.Level import Level
from GoogleTuring.Infrastructure.Domain.GoogleFieldsMetadata import GoogleFieldsMetadata


class FiledGoogleInsightsTableEnum(EnumerationBase):
    CAMPAIGN = "CAMPAIGN_PERFORMANCE_REPORT"
    AD_GROUP = "ADGROUP_PERFORMANCE_REPORT"
    AD = "AD_PERFORMANCE_REPORT"
    GENDER = "GENDER_PERFORMANCE_REPORT"
    AGE_RANGE = "AGE_RANGE_PERFORMANCE_REPORT"
    GEO = "GEO_PERFORMANCE_REPORT"
    KEYWORDS = "KEYWORDS_PERFORMANCE_REPORT"
    ACCOUNT = "ACCOUNT_PERFORMANCE_REPORT"


PERFORMANCE_REPORT_TO_INFO = {
    CampaignReportEnum.CAMPAIGN_PERFORMANCE_REPORT.value: (FiledGoogleInsightsTableEnum.CAMPAIGN, Level.CAMPAIGN),
    CampaignReportEnum.CAMPAIGN_GENDER_PERFORMANCE_REPORT.value: (FiledGoogleInsightsTableEnum.GENDER, Level.CAMPAIGN),
    CampaignReportEnum.CAMPAIGN_AGE_RANGE_PERFORMANCE_REPORT.value: (
        FiledGoogleInsightsTableEnum.AGE_RANGE, Level.CAMPAIGN),
    CampaignReportEnum.CAMPAIGN_GEO_PERFORMANCE_REPORT.value: (FiledGoogleInsightsTableEnum.GEO, Level.CAMPAIGN),
    CampaignReportEnum.CAMPAIGN_KEYWORDS_PERFORMANCE_REPORT.value: (
        FiledGoogleInsightsTableEnum.KEYWORDS, Level.CAMPAIGN),
    AdGroupReportEnum.AD_GROUP_PERFORMANCE_REPORT.value: (FiledGoogleInsightsTableEnum.AD_GROUP, Level.AD_GROUP),
    AdGroupReportEnum.AD_GROUP_GENDER_PERFORMANCE_REPORT.value: (FiledGoogleInsightsTableEnum.GENDER, Level.AD_GROUP),
    AdGroupReportEnum.AD_GROUP_AGE_RANGE_PERFORMANCE_REPORT.value: (
        FiledGoogleInsightsTableEnum.AGE_RANGE, Level.AD_GROUP),
    AdGroupReportEnum.AD_GROUP_GEO_PERFORMANCE_REPORT.value: (FiledGoogleInsightsTableEnum.GEO, Level.AD_GROUP),
    AdGroupReportEnum.AD_GROUP_KEYWORDS_PERFORMANCE_REPORT.value: (
        FiledGoogleInsightsTableEnum.KEYWORDS, Level.CAMPAIGN.AD_GROUP),
    AdReportEnum.AD_PERFORMANCE_REPORT.value: (FiledGoogleInsightsTableEnum.AD, Level.AD_GROUP)
}

REPORT_TO_STATUS_FIELD = {
    FiledGoogleInsightsTableEnum.CAMPAIGN: GoogleFieldsMetadata.campaign_status,
    FiledGoogleInsightsTableEnum.AD_GROUP: GoogleFieldsMetadata.ad_group_status,
    FiledGoogleInsightsTableEnum.AD: GoogleFieldsMetadata.status,
    FiledGoogleInsightsTableEnum.GENDER: GoogleFieldsMetadata.status,
    FiledGoogleInsightsTableEnum.AGE_RANGE: GoogleFieldsMetadata.status,
    FiledGoogleInsightsTableEnum.GEO: GoogleFieldsMetadata.campaign_status,  # TODO: check if this is true
    FiledGoogleInsightsTableEnum.KEYWORDS: GoogleFieldsMetadata.status
}

REPORT_TO_LEVEL = {
    FiledGoogleInsightsTableEnum.CAMPAIGN: Level.CAMPAIGN,
    FiledGoogleInsightsTableEnum.AD_GROUP: Level.AD_GROUP,
    FiledGoogleInsightsTableEnum.AD: Level.AD,
    FiledGoogleInsightsTableEnum.GENDER: Level.AD_GROUP,
    FiledGoogleInsightsTableEnum.AGE_RANGE: Level.AD_GROUP,
    FiledGoogleInsightsTableEnum.GEO: Level.AD_GROUP,
    FiledGoogleInsightsTableEnum.KEYWORDS: Level.KEYWORDS
}
