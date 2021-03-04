import typing
from enum import Enum

from Core.Web.FacebookGraphAPI.GraphAPIDomain.StructureStatusEnum import StructureStatusEnum


class EffectiveStatusEnum(Enum):

    ACTIVE = "ACTIVE"
    PAUSED = "PAUSED"
    DELETED = "DELETED"
    PENDING_REVIEW = "PENDING_REVIEW"
    DISAPPROVED = "DISAPPROVED"
    PREAPPROVED = "PREAPPROVED"
    PENDING_BILLING_INFO = "PENDING_BILLING_INFO"
    CAMPAIGN_PAUSED = "CAMPAIGN_PAUSED"
    ARCHIVED = "ARCHIVED"
    ADSET_PAUSED = "ADSET_PAUSED"
    IN_PROCESS = "IN_PROCESS"
    WITH_ISSUES = "WITH_ISSUES"


def map_facebook_status(facebook_status: typing.AnyStr = None) -> int:
    if not facebook_status:
        return StructureStatusEnum.DEPRECATED.value

    # facebook_status_enum = Campaign.Status
    status_map = {
        EffectiveStatusEnum.ACTIVE.value: StructureStatusEnum.ACTIVE.value,
        EffectiveStatusEnum.ARCHIVED.value: StructureStatusEnum.REMOVED.value,
        EffectiveStatusEnum.PAUSED.value: StructureStatusEnum.PAUSED.value,
        EffectiveStatusEnum.DELETED.value: StructureStatusEnum.REMOVED.value,
        EffectiveStatusEnum.PENDING_REVIEW.value: StructureStatusEnum.PAUSED.value,
        EffectiveStatusEnum.DISAPPROVED.value: StructureStatusEnum.REMOVED.value,
        EffectiveStatusEnum.PREAPPROVED.value: StructureStatusEnum.PAUSED.value,
        EffectiveStatusEnum.PENDING_BILLING_INFO.value: StructureStatusEnum.PAUSED.value,
        EffectiveStatusEnum.CAMPAIGN_PAUSED.value: StructureStatusEnum.PAUSED.value,
        EffectiveStatusEnum.WITH_ISSUES.value: StructureStatusEnum.PAUSED.value,
        EffectiveStatusEnum.ADSET_PAUSED.value: StructureStatusEnum.PAUSED.value,
        EffectiveStatusEnum.IN_PROCESS.value: StructureStatusEnum.PAUSED.value,
    }

    return status_map[facebook_status]
