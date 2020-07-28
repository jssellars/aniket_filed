from FacebookTuring.Api.Catalogs.ReportModels.Levels.AdSet.AdSetReportEnum import AdSetReportEnum
from FacebookTuring.Api.Catalogs.ReportModels.ReportModel import ReportModel


class AdSetPerformanceReportModel(ReportModel):
    key = AdSetReportEnum.AD_SET_PERFORMANCE_REPORT.value
    display_name = "Ad Set Performance Report"
