from enum import Enum

from Core.Web.FacebookGraphAPI.Models.FieldsMetadata import FieldsMetadata


class InsightsSyncronizerBreakdownEnum(Enum):
    NONE = FieldsMetadata.breakdown_none
    AGE = FieldsMetadata.age_breakdown
    GENDER = FieldsMetadata.gender_breakdown
    PLACEMENT = FieldsMetadata.placement
    DEVICE = FieldsMetadata.impression_device
    PLATFORM = FieldsMetadata.publisher_platform


class InsightsSyncronizerActionBreakdownEnum(Enum):
    NONE = FieldsMetadata.action_none
