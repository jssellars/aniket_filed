from Core.Metadata.Insights.InsightsReportModel import InsightsReportModel
from Core.Tools.Misc.ObjectSerializers import object_to_attribute_values_list
from GoogleTuring.Api.Catalogs.Breakdowns.SegmentIds import SegmentIds
from GoogleTuring.Api.Catalogs.BusinessViews.TableEnum import TableEnum
from GoogleTuring.Api.Catalogs.Views.ViewColumnsMaster.Levels.CampaignColumnsMaster import CampaignColumnsMaster


class CampaignPerformanceReport(InsightsReportModel):
    table_name = TableEnum.CAMPAIGN_PERFORMANCES.value
    report_breakdowns = [TableEnum.CAMPAIGN_GENDER_PERFORMANCES.value, TableEnum.CAMPAIGN_AGE_RANGE_PERFORMANCES.value,
                         TableEnum.CAMPAIGN_GEO_PERFORMANCES.value, TableEnum.CAMPAIGN_KEYWORDS_PERFORMANCES.value]
    display_name = "Campaign Report"
    json_list_encoder = object_to_attribute_values_list

    breakdowns = {
        "segments": [
            SegmentIds.ad_network_type_1,
            SegmentIds.ad_network_type_2,
            SegmentIds.click_type,
            SegmentIds.conversion_adjustment_lag_bucket,
            SegmentIds.conversion_attribution_event_type,
            SegmentIds.conversion_category_name,
            SegmentIds.conversion_lag_bucket,
            SegmentIds.conversion_tracker_id,
            SegmentIds.conversion_type_name,
            SegmentIds.date,
            SegmentIds.day_of_week,
            SegmentIds.device,
            SegmentIds.external_conversion_source,
            SegmentIds.hour_of_day,
            SegmentIds.month,
            SegmentIds.month_of_year,
            SegmentIds.quarter,
            SegmentIds.slot,
            SegmentIds.week,
            SegmentIds.year
        ]}

    columns = json_list_encoder(CampaignColumnsMaster)