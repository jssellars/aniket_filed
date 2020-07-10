from Core.Tools.Misc.ObjectSerializers import object_to_json, object_to_attribute_values_list
from GoogleTuring.Api.Catalogs.ReportModels.Levels.Ad.AdReportEnum import AdReportEnum
from GoogleTuring.Api.Catalogs.ReportModels.Levels.AdGroup.AdGroupReportEnum import AdGroupReportEnum
from GoogleTuring.Api.Catalogs.ReportModels.Levels.Campaign.CampaignReportEnum import CampaignReportEnum
from GoogleTuring.Api.Catalogs.ReportModels.ReportMappings import REPORT_TO_DIMENSIONS


class AdsManagerCatalogsDimensionsDto:
    __available_enums = [CampaignReportEnum, AdGroupReportEnum, AdReportEnum]
    json_encoder = object_to_json
    json_list_encoder = object_to_attribute_values_list

    @classmethod
    def __find_enum_value_from_report(cls, report):
        for enum in cls.__available_enums:
            enum_value = enum.get_enum_by_value(report)
            if enum_value:
                return enum_value

        return None

    @classmethod
    def get(cls, report):
        enum_value = cls.__find_enum_value_from_report(report)
        return cls.json_encoder(REPORT_TO_DIMENSIONS.get(enum_value))