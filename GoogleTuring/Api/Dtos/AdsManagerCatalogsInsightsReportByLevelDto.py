from Core.Tools.Misc.ObjectSerializers import object_to_json, object_to_attribute_values_list
from GoogleTuring.Api.Catalogs.ReportModels.AdGroupPerformanceReport import AdGroupPerformanceReport
from GoogleTuring.Api.Catalogs.ReportModels.AdPerformanceReport import AdPerformanceReport
from GoogleTuring.Api.Catalogs.ReportModels.AgeRangePerformanceReport import AgeRangePerformanceReport
from GoogleTuring.Api.Catalogs.ReportModels.CampaignPerformanceReport import CampaignPerformanceReport
from GoogleTuring.Api.Catalogs.ReportModels.GenderPerformanceReport import GenderPerformanceReport
from GoogleTuring.Api.Catalogs.ReportModels.GeoPerformanceReport import GeoPerformanceReport
from GoogleTuring.Api.Catalogs.ReportModels.KeywordsPerformanceReport import KeywordsPerformanceReport


class AdsManagerCatalogsInsightsReportByLevelDto:
    json_encoder = object_to_json
    json_list_encoder = object_to_attribute_values_list

    campaign = [
        CampaignPerformanceReport,
        GenderPerformanceReport,
        AgeRangePerformanceReport,
        GeoPerformanceReport,
        KeywordsPerformanceReport
    ]

    ad_group = [
        AdGroupPerformanceReport,
        GenderPerformanceReport,
        AgeRangePerformanceReport,
        GeoPerformanceReport,
        KeywordsPerformanceReport
    ]
    ad = [
        AdPerformanceReport
    ]

    @classmethod
    def get(cls, level):
        return cls.json_encoder(getattr(cls, level))
