from Core.Metadata.Insights.InsightsReportModel import InsightsReportModel
from Core.Tools.Misc.ObjectSerializers import object_to_attribute_values_list
from GoogleTuring.Api.Catalogs.Breakdowns.SegmentIds import SegmentIds
from GoogleTuring.Api.Catalogs.Views.ViewColumnsMaster.GeoColumnsMaster import GeoColumnsMaster


class GeoPerformanceReport(InsightsReportModel):
    json_list_encoder = object_to_attribute_values_list

    breakdowns = {
        "segments": [
            SegmentIds.ad_format,
            SegmentIds.ad_group_id_segment,
            SegmentIds.ad_group_name_segment,
            SegmentIds.ad_group_status_segment,
            SegmentIds.ad_network_type_1,
            SegmentIds.ad_network_type_2,
            SegmentIds.conversion_category_name,
            SegmentIds.conversion_tracker_id,
            SegmentIds.conversion_type_name,
            SegmentIds.date,
            SegmentIds.day_of_week,
            SegmentIds.device,
            SegmentIds.external_conversion_source,
            SegmentIds.location_type,
            SegmentIds.month,
            SegmentIds.month_of_year,
            SegmentIds.quarter,
            SegmentIds.week,
            SegmentIds.year
        ]}

    table_name = 'GeoPerformances'
    report_breakdowns = ['CampaignPerformances', 'AdGroupPerformances']
    columns = json_list_encoder(GeoColumnsMaster)
