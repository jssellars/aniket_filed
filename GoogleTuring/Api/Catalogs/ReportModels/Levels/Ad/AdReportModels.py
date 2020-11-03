from GoogleTuring.Api.Catalogs.ReportModels.ReportModel import ReportModel
from GoogleTuring.Infrastructure.Domain.Enums.AdReportEnum import AdReportEnum


class AdPerformanceReportModel(ReportModel):
    key = AdReportEnum.AD_PERFORMANCE_REPORT.value
    display_name = "Ad Performance Report"
