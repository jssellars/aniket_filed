from Core.Tools.Misc.ObjectSerializers import object_to_json, object_to_attribute_values_list
from GoogleTuring.Api.Catalogs.ReportModels.Levels.Ad.AdReportModels import AdPerformanceReportModel
from GoogleTuring.Api.Catalogs.ReportModels.Levels.AdGroup.AdGroupReportModels import AdGroupPerformanceReportModel, \
    AdGroupGenderPerformanceReportModel, AdGroupAgeRangePerformanceReportModel, AdGroupGeoPerformanceReportModel, \
    AdGroupKeywordsPerformanceReportModel
from GoogleTuring.Api.Catalogs.ReportModels.Levels.Campaign.CampaignReportModels import CampaignPerformanceReportModel, \
    CampaignGenderPerformanceReportModel, CampaignKeywordsPerformanceReportModel, CampaignGeoPerformanceReportModel, \
    CampaignAgeRangePerformanceReportModel


class AdsManagerCatalogReportsDto:
    json_encoder = object_to_json
    json_list_encoder = object_to_attribute_values_list

    campaign = [
        CampaignPerformanceReportModel,
        CampaignGenderPerformanceReportModel,
        CampaignAgeRangePerformanceReportModel,
        CampaignGeoPerformanceReportModel,
        CampaignKeywordsPerformanceReportModel
    ]

    adset = [
        AdGroupPerformanceReportModel,
        AdGroupGenderPerformanceReportModel,
        AdGroupAgeRangePerformanceReportModel,
        AdGroupGeoPerformanceReportModel,
        AdGroupKeywordsPerformanceReportModel
    ]
    ad = [
        AdPerformanceReportModel
    ]

    @classmethod
    def get(cls, level):
        return cls.json_encoder(getattr(cls, level))
