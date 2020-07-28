from Core.Tools.Misc.ObjectSerializers import object_to_json
from FacebookTuring.Api.Catalogs.ReportColumns.Breakdowns.BreakdownsColumns import extract_breakdown_columns


class AdsManagerCatalogsReportsBreakdownsDto:
    json_encoder = object_to_json

    @classmethod
    def get(cls, metrics=None):
        return cls.json_encoder(extract_breakdown_columns(metrics))
