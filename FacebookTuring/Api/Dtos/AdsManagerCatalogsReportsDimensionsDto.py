from Core.Tools.Misc.ObjectSerializers import object_to_json, object_to_attribute_values_list
from FacebookTuring.Api.Catalogs.ReportColumns.Dimensions.AdLevelDimensions import AD_PERFORMANCE_REPORT_DIMENSIONS
from FacebookTuring.Api.Catalogs.ReportColumns.Dimensions.AdSetLevelDimensions import \
    ADSET_PERFORMANCE_REPORT_DIMENSIONS
from FacebookTuring.Api.Catalogs.ReportColumns.Dimensions.CampaignLevelDimensions import \
    CAMPAIGN_PERFORMANCE_REPORT_DIMENSIONS
from FacebookTuring.Api.Catalogs.ReportModels.Levels.Ad.AdReportEnum import AdReportEnum
from FacebookTuring.Api.Catalogs.ReportModels.Levels.AdSet.AdSetReportEnum import AdSetReportEnum
from FacebookTuring.Api.Catalogs.ReportModels.Levels.Campaign.CampaignReportEnum import CampaignReportEnum


class AdsManagerCatalogsReportsDimensionsDto:
    json_encoder = object_to_json
    json_list_encoder = object_to_attribute_values_list

    DIMENSIONS = {
        AdReportEnum.AD_PERFORMANCE_REPORT.value: AD_PERFORMANCE_REPORT_DIMENSIONS,
        AdSetReportEnum.AD_SET_PERFORMANCE_REPORT.value: ADSET_PERFORMANCE_REPORT_DIMENSIONS,
        CampaignReportEnum.CAMPAIGN_PERFORMANCE_REPORT.value: CAMPAIGN_PERFORMANCE_REPORT_DIMENSIONS
    }

    @classmethod
    def get(cls, report_type=None):
        return cls.json_encoder(cls.DIMENSIONS.get(report_type))
