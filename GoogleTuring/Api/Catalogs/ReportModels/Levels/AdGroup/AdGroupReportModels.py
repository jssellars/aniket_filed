from GoogleTuring.Api.Catalogs.ReportModels.Levels.AdGroup.AdGroupReportEnum import AdGroupReportEnum
from GoogleTuring.Api.Catalogs.ReportModels.ReportModel import ReportModel


class AdGroupPerformanceReportModel(ReportModel):
    report_key = AdGroupReportEnum.AD_GROUP_PERFORMANCE_REPORT.value
    display_name = "Ad Group Performance Report"


class AdGroupAgeRangePerformanceReportModel(ReportModel):
    report_key = AdGroupReportEnum.AD_GROUP_AGE_RANGE_PERFORMANCE_REPORT.value
    display_name = "Ad Group Age Range Performance Report"


class AdGroupGenderPerformanceReportModel(ReportModel):
    report_key = AdGroupReportEnum.AD_GROUP_GENDER_PERFORMANCE_REPORT.value
    display_name = "Ad Group Gender Performance Report"


class AdGroupGeoPerformanceReportModel(ReportModel):
    report_key = AdGroupReportEnum.AD_GROUP_GEO_PERFORMANCE_REPORT.value
    display_name = "Ad Group Geo Performance Report"


class AdGroupKeywordsPerformanceReportModel(ReportModel):
    report_key = AdGroupReportEnum.AD_GROUP_KEYWORDS_PERFORMANCE_REPORT.value
    display_name = "Ad Group Keywords Performance Report"
