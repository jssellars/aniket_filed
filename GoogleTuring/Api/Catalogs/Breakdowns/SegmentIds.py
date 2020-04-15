from Core.Tools.Misc.Autoincrement import Autoincrement
from GoogleTuring.Api.Catalogs.Views.ViewColumnsMaster.ViewColumnsMaster import ViewColumnsMaster


class SegmentIds:
    __id = Autoincrement(0)
    ad_network_type_1 = ViewColumnsMaster.ad_network_type_1.id

    ad_network_type_2 = ViewColumnsMaster.ad_network_type_2.id

    click_type = ViewColumnsMaster.click_type.id

    conversion_adjustment_lag_bucket = ViewColumnsMaster.conversion_adjustment_lag_bucket.id

    conversion_lag_bucket = ViewColumnsMaster.conversion_lag_bucket.id

    conversion_tracker_id = ViewColumnsMaster.conversion_tracker_id.id

    conversion_type_name = ViewColumnsMaster.conversion_type_name.id

    criterion_id = ViewColumnsMaster.criterion_id.id

    criterion_type = ViewColumnsMaster.criterion_type.id

    date = ViewColumnsMaster.date.id

    day_of_week = ViewColumnsMaster.day_of_week.id

    device = ViewColumnsMaster.device.id

    external_conversion_source = ViewColumnsMaster.external_conversion_source.id

    month = ViewColumnsMaster.month.id

    month_of_year = ViewColumnsMaster.month_of_year.id

    quarter = ViewColumnsMaster.quarter.id

    slot = ViewColumnsMaster.slot.id

    week = ViewColumnsMaster.week.id

    year = ViewColumnsMaster.year.id

    hour_of_day = ViewColumnsMaster.hour_of_day.id

    conversion_attribution_event_type = ViewColumnsMaster.conversion_attribution_event_type.id

    ad_format = ViewColumnsMaster.ad_format.id

    location_type = ViewColumnsMaster.location_type.id

    conversion_category_name = ViewColumnsMaster.conversion_category_name.id

    ad_group_id_segment = ViewColumnsMaster.ad_group_id_segment.id

    ad_group_name_segment = ViewColumnsMaster.ad_group_name_segment.id

    ad_group_status_segment = ViewColumnsMaster.ad_group_status_segment.id
