import typing

from facebook_business.adobjects.campaign import Campaign

from FacebookTuring.Infrastructure.Domain.StructureStatusEnum import StructureStatusEnum


def map_facebook_status(facebook_status: typing.AnyStr = None) -> int:
    if not facebook_status:
        return StructureStatusEnum.DEPRECATED.value

    facebook_status_enum = Campaign.Status
    status_map = {
        facebook_status_enum.active: StructureStatusEnum.ACTIVE.value,
        facebook_status_enum.archived: StructureStatusEnum.REMOVED.value,
        facebook_status_enum.paused: StructureStatusEnum.PAUSED.value,
        facebook_status_enum.deleted: StructureStatusEnum.REMOVED.value,
    }

    return status_map[facebook_status]
