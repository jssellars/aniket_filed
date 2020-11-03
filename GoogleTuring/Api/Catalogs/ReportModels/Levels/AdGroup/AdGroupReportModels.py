from GoogleTuring.Api.Catalogs.ReportModels.ReportModel import ReportModel
from GoogleTuring.Infrastructure.Domain.Enums.AdGroupReportEnum import AdGroupReportEnum


class AdGroupPerformanceReportModel(ReportModel):
    key = AdGroupReportEnum.AD_GROUP_PERFORMANCE_REPORT.value
    display_name = "Ad Group Performance Report"


class AdGroupAgeRangePerformanceReportModel(ReportModel):
    key = AdGroupReportEnum.AD_GROUP_AGE_RANGE_PERFORMANCE_REPORT.value
    display_name = "Ad Group Age Range Performance Report"


class AdGroupGenderPerformanceReportModel(ReportModel):
    key = AdGroupReportEnum.AD_GROUP_GENDER_PERFORMANCE_REPORT.value
    display_name = "Ad Group Gender Performance Report"


class AdGroupGeoPerformanceReportModel(ReportModel):
    key = AdGroupReportEnum.AD_GROUP_GEO_PERFORMANCE_REPORT.value
    display_name = "Ad Group Geo Performance Report"


class AdGroupKeywordsPerformanceReportModel(ReportModel):
    key = AdGroupReportEnum.AD_GROUP_KEYWORDS_PERFORMANCE_REPORT.value
    display_name = "Ad Group Keywords Performance Report"
