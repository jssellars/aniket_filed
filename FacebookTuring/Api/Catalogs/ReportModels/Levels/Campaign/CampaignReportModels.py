from FacebookTuring.Api.Catalogs.ReportModels.Levels.Campaign.CampaignReportEnum import CampaignReportEnum
from FacebookTuring.Api.Catalogs.ReportModels.ReportModel import ReportModel


class CampaignPerformanceReportModel(ReportModel):
    key = CampaignReportEnum.CAMPAIGN_PERFORMANCE_REPORT.value
    display_name = "Campaign Performance Report"
