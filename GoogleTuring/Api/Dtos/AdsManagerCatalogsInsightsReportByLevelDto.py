from Core.Tools.Misc.ObjectSerializers import object_to_json, object_to_attribute_values_list
from GoogleTuring.Api.Catalogs.ReportModels.Levels.AdGroupPerformanceReport import AdGroupPerformanceReport
from GoogleTuring.Api.Catalogs.ReportModels.Levels.AdPerformanceReport import AdPerformanceReport
from GoogleTuring.Api.Catalogs.ReportModels.Levels.Breakdowns.AgeRange.AdGroupAgeRangePerformanceReport import \
    AdGroupAgeRangePerformanceReport
from GoogleTuring.Api.Catalogs.ReportModels.Levels.Breakdowns.AgeRange.CampaignAgeRangePerformanceReport import \
    CampaignAgeRangePerformanceReport
from GoogleTuring.Api.Catalogs.ReportModels.Levels.Breakdowns.Gender.AdGroupGenderPerformanceReport import \
    AdGroupGenderPerformanceReport
from GoogleTuring.Api.Catalogs.ReportModels.Levels.Breakdowns.Gender.CampaignGenderPerformanceReport import \
    CampaignGenderPerformanceReport
from GoogleTuring.Api.Catalogs.ReportModels.Levels.Breakdowns.Geo.AdGroupGeoPerformanceReport import \
    AdGroupGeoPerformanceReport
from GoogleTuring.Api.Catalogs.ReportModels.Levels.Breakdowns.Geo.CampaignGeoPerformanceReport import \
    CampaignGeoPerformanceReport
from GoogleTuring.Api.Catalogs.ReportModels.Levels.Breakdowns.Keywords.AdGroupKeywordsPerformanceReport import \
    AdGroupKeywordsPerformanceReport
from GoogleTuring.Api.Catalogs.ReportModels.Levels.Breakdowns.Keywords.CampaignKeywordsPerformanceReport import \
    CampaignKeywordsPerformanceReport
from GoogleTuring.Api.Catalogs.ReportModels.Levels.CampaignPerformanceReport import CampaignPerformanceReport


class AdsManagerCatalogsInsightsReportByLevelDto:
    json_encoder = object_to_json
    json_list_encoder = object_to_attribute_values_list

    campaign = [
        CampaignPerformanceReport,
        CampaignGenderPerformanceReport,
        CampaignAgeRangePerformanceReport,
        CampaignGeoPerformanceReport,
        CampaignKeywordsPerformanceReport
    ]

    ad_group = [
        AdGroupPerformanceReport,
        AdGroupGenderPerformanceReport,
        AdGroupAgeRangePerformanceReport,
        AdGroupGeoPerformanceReport,
        AdGroupKeywordsPerformanceReport
    ]
    ad = [
        AdPerformanceReport
    ]

    @classmethod
    def get(cls, level):
        return cls.json_encoder(getattr(cls, level))
