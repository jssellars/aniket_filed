from collections import defaultdict


class SegmentColumnsBase:
    AVAILABLE_DIMENSIONS = []
    AVAILABLE_METRICS = []
    SEGMENTS = []

    def __init__(self):
        self.DIMENSION_TO_METRIC_TO_SEGMENTS = defaultdict(lambda: defaultdict(list))
        for dimension in self.AVAILABLE_DIMENSIONS:
            for metric in self.AVAILABLE_METRICS:
                for segment in self.SEGMENTS:
                    if dimension not in segment.not_supported_dimensions and \
                            metric not in segment.not_supported_metrics:
                        self.DIMENSION_TO_METRIC_TO_SEGMENTS[dimension.primary_value.name][
                            metric.view_column.primary_value.name].append(segment.breakdowns_enumeration)
