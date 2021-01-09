from enum import Enum

from Core.Web.FacebookGraphAPI.Models.FieldsMetadata import FieldsMetadata


class InsightsSynchronizerBreakdownEnum(Enum):
    NONE = FieldsMetadata.breakdown_none
    AGE_GENDER = FieldsMetadata.age_gender
    PLACEMENT = FieldsMetadata.placement
    # AGE = FieldsMetadata.age_breakdown
    # GENDER = FieldsMetadata.gender_breakdown
    # DEVICE = FieldsMetadata.impression_device
    # PLATFORM = FieldsMetadata.publisher_platform
    # HOUR = FieldsMetadata.hourly_stats_aggregated_by_advertiser_time_zone
    # FREQUENCY_VALUE = FieldsMetadata.frequency_value
    # DAY = FieldsMetadata.day
    # COUNTRY = FieldsMetadata.country
    # REGION = FieldsMetadata.region


class InsightsSynchronizerActionBreakdownEnum(Enum):
    NONE = FieldsMetadata.action_none
    # Commented as these action breakdowns are not relevant at this stage of the project. Haven't deleted it as they
    # might become relevant in the future.
    # CONVERSION_DEVICE = FieldsMetadata.device
    # VIDEO_VIEW_TYPE = FieldsMetadata.video_type
    # VIDEO_SOUND = FieldsMetadata.video_sound
    # CAROUSEL_CARD_NAME = FieldsMetadata.carousel_card_name
