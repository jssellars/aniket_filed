from Core.Tools.Misc.ObjectSerializers import object_to_json
from FacebookTuring.Api.Catalogs.ReportColumns.Metrics.MetricsColumns import METRICS_COLUMNS


class AdsManagerCatalogsReportsMetricsDto:
    json_encoder = object_to_json

    @classmethod
    def get(cls):
        return cls.json_encoder(METRICS_COLUMNS)
