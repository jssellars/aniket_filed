from Core.Metadata.Columns.ColumnMetadata import ColumnMetadata
from Core.Metadata.Columns.ColumnType import ColumnType

from GoogleTuring.Infrastructure.Domain.GoogleSegmentFieldsMetadata import GoogleSegmentFieldsMetadata


class GoogleSegmentMetadataColumnsPool:
    #  Structure fields and parameters
    #  Object names, IDs, statuses, and dates
    ad_network_type_1 = ColumnMetadata(GoogleSegmentFieldsMetadata.ad_network_type_1.field_name, ColumnType.text)

    ad_network_type_2 = ColumnMetadata(GoogleSegmentFieldsMetadata.ad_network_type_2.field_name, ColumnType.text)

    click_type = ColumnMetadata(GoogleSegmentFieldsMetadata.click_type.field_name, ColumnType.text)

    conversion_adjustment_lag_bucket = ColumnMetadata(
        GoogleSegmentFieldsMetadata.conversion_adjustment_lag_bucket.field_name,
        ColumnType.text)

    conversion_lag_bucket = ColumnMetadata(GoogleSegmentFieldsMetadata.conversion_lag_bucket.field_name,
                                           ColumnType.text)

    conversion_tracker_id = ColumnMetadata(GoogleSegmentFieldsMetadata.conversion_tracker_id.field_name,
                                           ColumnType.text)

    conversion_type_name = ColumnMetadata(GoogleSegmentFieldsMetadata.conversion_type_name.field_name, ColumnType.text)

    criterion_id = ColumnMetadata(GoogleSegmentFieldsMetadata.criterion_id.field_name, ColumnType.text)

    criterion_type = ColumnMetadata(GoogleSegmentFieldsMetadata.criterion_type.field_name, ColumnType.text)

    date = ColumnMetadata(GoogleSegmentFieldsMetadata.date.field_name, ColumnType.text)

    day_of_week = ColumnMetadata(GoogleSegmentFieldsMetadata.day_of_week.field_name, ColumnType.text)

    device = ColumnMetadata(GoogleSegmentFieldsMetadata.device.field_name, ColumnType.text)

    external_conversion_source = ColumnMetadata(GoogleSegmentFieldsMetadata.external_conversion_source.field_name,
                                                ColumnType.text)

    month = ColumnMetadata(GoogleSegmentFieldsMetadata.month.field_name, ColumnType.text)

    month_of_year = ColumnMetadata(GoogleSegmentFieldsMetadata.month_of_year.field_name, ColumnType.text)

    quarter = ColumnMetadata(GoogleSegmentFieldsMetadata.quarter.field_name, ColumnType.text)

    slot = ColumnMetadata(GoogleSegmentFieldsMetadata.slot.field_name, ColumnType.text)

    week = ColumnMetadata(GoogleSegmentFieldsMetadata.week.field_name, ColumnType.text)

    year = ColumnMetadata(GoogleSegmentFieldsMetadata.year.field_name, ColumnType.text)

    hour_of_day = ColumnMetadata(GoogleSegmentFieldsMetadata.hour_of_day.field_name, ColumnType.text)

    conversion_attribution_event_type = ColumnMetadata(
        GoogleSegmentFieldsMetadata.conversion_attribution_event_type.field_name, ColumnType.text)

    ad_format = ColumnMetadata(GoogleSegmentFieldsMetadata.ad_format.field_name, ColumnType.text)

    location_type = ColumnMetadata(GoogleSegmentFieldsMetadata.location_type.field_name, ColumnType.text)

    conversion_category_name = ColumnMetadata(GoogleSegmentFieldsMetadata.conversion_category_name.field_name,
                                              ColumnType.text)

    ad_group_id_segment = ColumnMetadata(GoogleSegmentFieldsMetadata.ad_group_id_segment.field_name, ColumnType.text)

    ad_group_name_segment = ColumnMetadata(GoogleSegmentFieldsMetadata.ad_group_name_segment.field_name,
                                           ColumnType.text)

    ad_group_status_segment = ColumnMetadata(GoogleSegmentFieldsMetadata.ad_group_status_segment.field_name,
                                             ColumnType.text)
