from Core.Metadata.Columns.ColumnMetadata import ColumnMetadata
from Core.Metadata.Columns.ColumnType import ColumnType

from GoogleTuring.Infrastructure.Domain.GoogleSegmentFieldsMetadata import GoogleSegmentFieldsMetadata


class GoogleSegmentMetadataColumnsPool:
    # Structure fields and parameters
    # Object names, IDs, statuses, and dates
    ad_network_type_1 = ColumnMetadata(GoogleSegmentFieldsMetadata.ad_network_type_1.name, ColumnType.text)

    ad_network_type_2 = ColumnMetadata(GoogleSegmentFieldsMetadata.ad_network_type_2.name, ColumnType.text)

    click_type = ColumnMetadata(GoogleSegmentFieldsMetadata.click_type.name, ColumnType.text)

    conversion_adjustment_lag_bucket = ColumnMetadata(
        GoogleSegmentFieldsMetadata.conversion_adjustment_lag_bucket.name,
        ColumnType.text)

    conversion_lag_bucket = ColumnMetadata(GoogleSegmentFieldsMetadata.conversion_lag_bucket.name,
                                           ColumnType.text)

    conversion_tracker_id = ColumnMetadata(GoogleSegmentFieldsMetadata.conversion_tracker_id.name,
                                           ColumnType.text)

    conversion_type_name = ColumnMetadata(GoogleSegmentFieldsMetadata.conversion_type_name.name, ColumnType.text)

    criterion_id = ColumnMetadata(GoogleSegmentFieldsMetadata.criterion_id.name, ColumnType.text)

    criterion_type = ColumnMetadata(GoogleSegmentFieldsMetadata.criterion_type.name, ColumnType.text)

    date = ColumnMetadata(GoogleSegmentFieldsMetadata.date.name, ColumnType.text)

    day_of_week = ColumnMetadata(GoogleSegmentFieldsMetadata.day_of_week.name, ColumnType.text)

    device = ColumnMetadata(GoogleSegmentFieldsMetadata.device.name, ColumnType.text)

    external_conversion_source = ColumnMetadata(GoogleSegmentFieldsMetadata.external_conversion_source.name,
                                                ColumnType.text)

    month = ColumnMetadata(GoogleSegmentFieldsMetadata.month.name, ColumnType.text)

    month_of_year = ColumnMetadata(GoogleSegmentFieldsMetadata.month_of_year.name, ColumnType.text)

    quarter = ColumnMetadata(GoogleSegmentFieldsMetadata.quarter.name, ColumnType.text)

    slot = ColumnMetadata(GoogleSegmentFieldsMetadata.slot.name, ColumnType.text)

    week = ColumnMetadata(GoogleSegmentFieldsMetadata.week.name, ColumnType.text)

    year = ColumnMetadata(GoogleSegmentFieldsMetadata.year.name, ColumnType.text)

    hour_of_day = ColumnMetadata(GoogleSegmentFieldsMetadata.hour_of_day.name, ColumnType.text)

    conversion_attribution_event_type = ColumnMetadata(
        GoogleSegmentFieldsMetadata.conversion_attribution_event_type.name, ColumnType.text)

    ad_format = ColumnMetadata(GoogleSegmentFieldsMetadata.ad_format.name, ColumnType.text)

    location_type = ColumnMetadata(GoogleSegmentFieldsMetadata.location_type.name, ColumnType.text)

    conversion_category_name = ColumnMetadata(GoogleSegmentFieldsMetadata.conversion_category_name.name,
                                              ColumnType.text)

    ad_group_id_segment = ColumnMetadata(GoogleSegmentFieldsMetadata.ad_group_id_segment.name, ColumnType.text)

    ad_group_name_segment = ColumnMetadata(GoogleSegmentFieldsMetadata.ad_group_name_segment.name,
                                           ColumnType.text)

    ad_group_status_segment = ColumnMetadata(GoogleSegmentFieldsMetadata.ad_group_status_segment.name,
                                             ColumnType.text)
