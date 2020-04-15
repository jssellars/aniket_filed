from Core.Metadata.Insights.InsightsReportModel import InsightsReportModel
from Core.Tools.Misc.ObjectSerializers import object_to_attribute_values_list
from GoogleTuring.Api.Catalogs.Breakdowns.SegmentIds import SegmentIds
from GoogleTuring.Api.Catalogs.Views.ViewColumnsMaster.AdColumnsMaster import AdColumnsMaster


class AdPerformanceReport(InsightsReportModel):
    json_list_encoder = object_to_attribute_values_list

    breakdowns = {
        "segments": [
            SegmentIds.ad_network_type_1,
            SegmentIds.ad_network_type_2,
            SegmentIds.click_type,
            SegmentIds.conversion_adjustment_lag_bucket,
            SegmentIds.conversion_category_name,
            SegmentIds.conversion_lag_bucket,
            SegmentIds.conversion_tracker_id,
            SegmentIds.conversion_type_name,
            SegmentIds.criterion_id,
            SegmentIds.criterion_type,
            SegmentIds.date,
            SegmentIds.day_of_week,
            SegmentIds.device,
            SegmentIds.external_conversion_source,
            SegmentIds.month,
            SegmentIds.month_of_year,
            SegmentIds.quarter,
            SegmentIds.slot,
            SegmentIds.week,
            SegmentIds.year
        ]}

    level = 'AdPerformances'
    report_breakdowns = []
    columns = json_list_encoder(AdColumnsMaster)
