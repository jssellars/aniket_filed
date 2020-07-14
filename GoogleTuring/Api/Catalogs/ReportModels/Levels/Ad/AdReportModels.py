from GoogleTuring.Api.Catalogs.ReportModels.Levels.Ad.AdReportEnum import AdReportEnum
from GoogleTuring.Api.Catalogs.ReportModels.ReportModel import ReportModel


class AdPerformanceReportModel(ReportModel):
    key = AdReportEnum.AD_PERFORMANCE_REPORT.value
    display_name = "Ad Performance Report"
