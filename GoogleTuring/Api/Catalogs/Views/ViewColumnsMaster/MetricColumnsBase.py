from collections import defaultdict


class MetricColumnsBase:
    METRICS = []
    AVAILABLE_DIMENSIONS = []

    def __init__(self):
        self.DIMENSION_TO_METRICS = defaultdict(list)
        for dimension in self.AVAILABLE_DIMENSIONS:
            for metric in self.METRICS:
                if dimension not in metric.not_supported_dimensions:
                    self.DIMENSION_TO_METRICS[dimension.primary_value.name].append(metric.view_column)
