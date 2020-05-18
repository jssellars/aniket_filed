from Core.Metadata.Insights.InsightsReportModel import InsightsReportModel
from Core.Tools.Misc.ObjectSerializers import object_to_attribute_values_list
from GoogleTuring.Api.Catalogs.Breakdowns.SegmentIds import SegmentIds
from GoogleTuring.Api.Catalogs.BusinessViews.TableEnum import TableEnum
from GoogleTuring.Api.Catalogs.Views.ViewColumnsMaster.Levels.Breakdowns.AgeRange.CampaignAgeRangeColumnsMaster import \
    CampaignAgeRangeColumnsMaster


class CampaignAgeRangePerformanceReport(InsightsReportModel):
    table_name = TableEnum.CAMPAIGN_AGE_RANGE_PERFORMANCES.value
    report_breakdowns = []
    display_name = "Campaign - Age Report"
    json_list_encoder = object_to_attribute_values_list

    breakdowns = {
        "segments": [
            SegmentIds.ad_network_type_1,
            SegmentIds.ad_network_type_2,
            SegmentIds.click_type,
            SegmentIds.conversion_category_name,
            SegmentIds.conversion_tracker_id,
            SegmentIds.conversion_type_name,
            SegmentIds.date,
            SegmentIds.day_of_week,
            SegmentIds.device,
            SegmentIds.external_conversion_source,
            SegmentIds.month,
            SegmentIds.month_of_year,
            SegmentIds.quarter,
            SegmentIds.week,
            SegmentIds.year
        ]}

    columns = json_list_encoder(CampaignAgeRangeColumnsMaster)
