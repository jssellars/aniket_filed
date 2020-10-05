from Core.Tools.Misc.ObjectSerializers import object_to_json, object_to_attribute_values_list
from FacebookTuring.Api.Catalogs.ReportModels.Levels.Ad.AdReportModels import AdPerformanceReportModel
from FacebookTuring.Api.Catalogs.ReportModels.Levels.AdSet.AdSetReportModels import AdSetPerformanceReportModel
from FacebookTuring.Api.Catalogs.ReportModels.Levels.Campaign.CampaignReportModels import \
    CampaignPerformanceReportModel


class AdsManagerCatalogsReportsDto:
    json_encoder = object_to_json
    json_list_encoder = object_to_attribute_values_list

    catalogs = {
        "campaign": [CampaignPerformanceReportModel],
        "adset": [AdSetPerformanceReportModel],
        "ad": [AdPerformanceReportModel]
    }

    @classmethod
    def get(cls):
        return cls.json_encoder(cls.catalogs)
