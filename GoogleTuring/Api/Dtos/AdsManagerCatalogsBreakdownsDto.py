from Core.Tools.Misc.ObjectSerializers import object_to_json, object_to_attribute_values_list
from GoogleTuring.Api.Catalogs.ReportModels.ReportMappings import REPORT_TO_BREAKDOWNS
from GoogleTuring.Infrastructure.Domain.Enums.AdGroupReportEnum import AdGroupReportEnum
from GoogleTuring.Infrastructure.Domain.Enums.AdReportEnum import AdReportEnum
from GoogleTuring.Infrastructure.Domain.Enums.CampaignReportEnum import CampaignReportEnum


class AdsManagerCatalogsBreakdownsDto:
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
    def get(cls, report, dimension, metrics):
        enum_value = cls.__find_enum_value_from_report(report)
        dimension_to_metric_to_segments = REPORT_TO_BREAKDOWNS.get(enum_value)
        if dimension_to_metric_to_segments:
            metrics = metrics.split(',')
            segments = set()

            for metric in metrics:
                segments |= set(dimension_to_metric_to_segments[dimension][metric])

            segments_list = list(segments)
            return cls.json_encoder(segments_list)
