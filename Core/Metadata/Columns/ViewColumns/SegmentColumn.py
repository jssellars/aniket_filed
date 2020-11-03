from Core.Metadata.Columns.ViewColumns.BreakdownsEnumeration import BreakdownsEnumeration


class SegmentColumn:
    def __init__(self,
                 id=None, column_name=None,
                 display_name=None,
                 not_supported_dimensions=None,
                 not_supported_metrics=None):
        self.breakdowns_enumeration = BreakdownsEnumeration(id=id, column_name=column_name, display_name=display_name)
        self.not_supported_dimensions = not_supported_dimensions
        self.not_supported_metrics = not_supported_metrics
