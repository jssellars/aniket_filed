from GoogleTuring.Api.Catalogs.ReportModels.Levels.Campaign.CampaignReportEnum import CampaignReportEnum
from GoogleTuring.Api.Catalogs.ReportModels.ReportModel import ReportModel


class CampaignPerformanceReportModel(ReportModel):
    report_key = CampaignReportEnum.CAMPAIGN_PERFORMANCE_REPORT.value
    display_name = "Campaign Performance Report"


class CampaignAgeRangePerformanceReportModel(ReportModel):
    report_key = CampaignReportEnum.CAMPAIGN_AGE_RANGE_PERFORMANCE_REPORT.value
    display_name = "Campaign Age Range Performance Report"


class CampaignGenderPerformanceReportModel(ReportModel):
    report_key = CampaignReportEnum.CAMPAIGN_GENDER_PERFORMANCE_REPORT.value
    display_name = "Campaign Gender Performance Report"


class CampaignGeoPerformanceReportModel(ReportModel):
    report_key = CampaignReportEnum.CAMPAIGN_GEO_PERFORMANCE_REPORT.value
    display_name = "Campaign Geo Performance Report"


class CampaignKeywordsPerformanceReportModel(ReportModel):
    report_key = CampaignReportEnum.CAMPAIGN_KEYWORDS_PERFORMANCE_REPORT.value
    display_name = "Campaign Keywords Performance Report"
