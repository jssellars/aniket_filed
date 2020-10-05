from Core.Tools.Misc.ObjectSerializers import object_to_json
from FacebookTuring.Api.Catalogs.ReportColumns.Breakdowns.BreakdownsColumns import REPORTS_BREAKDOWNS


class AdsManagerCatalogsReportsBreakdownsDto:
    json_encoder = object_to_json

    @classmethod
    def get(cls):
        return cls.json_encoder(REPORTS_BREAKDOWNS)
