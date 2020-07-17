from enum import Enum

from Core.Web.FacebookGraphAPI.Models.FieldsMetadata import FieldsMetadata


class InsightsSyncronizerBreakdownEnum(Enum):
    NONE = FieldsMetadata.breakdown_none
    AGE = FieldsMetadata.age_breakdown
    GENDER = FieldsMetadata.gender_breakdown
    PLACEMENT = FieldsMetadata.placement
    DEVICE = FieldsMetadata.impression_device
    PLATFORM = FieldsMetadata.publisher_platform
    HOUR = FieldsMetadata.hourly_stats_aggregated_by_advertiser_time_zone


class InsightsSyncronizerActionBreakdownEnum(Enum):
    NONE = FieldsMetadata.action_none
