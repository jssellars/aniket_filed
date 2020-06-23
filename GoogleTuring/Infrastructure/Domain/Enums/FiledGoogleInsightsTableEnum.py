from Core.Tools.Misc.EnumerationBase import EnumerationBase
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


REPORT_TO_STATUS_FIELD = {
    FiledGoogleInsightsTableEnum.CAMPAIGN: GoogleFieldsMetadata.campaign_status,
    FiledGoogleInsightsTableEnum.AD_GROUP: GoogleFieldsMetadata.ad_group_status,
    FiledGoogleInsightsTableEnum.AD: GoogleFieldsMetadata.status,
    FiledGoogleInsightsTableEnum.GENDER: GoogleFieldsMetadata.status,
    FiledGoogleInsightsTableEnum.AGE_RANGE: GoogleFieldsMetadata.status,
    FiledGoogleInsightsTableEnum.GEO: GoogleFieldsMetadata.campaign_status,  # TODO: check if this is true
    FiledGoogleInsightsTableEnum.KEYWORDS: GoogleFieldsMetadata.status
}
