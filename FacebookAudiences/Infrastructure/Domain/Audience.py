import typing
from dataclasses import dataclass

from FacebookAudiences.Infrastructure.Domain.AudienceStateEnum import AudienceStateEnum


@dataclass
class Audience:
    facebook_id: typing.AnyStr = None
    name: typing.AnyStr = None
    date_created: typing.AnyStr = None
    last_updated: typing.AnyStr = None
    source: typing.AnyStr = None
    subtype: typing.AnyStr = None
    type: typing.AnyStr = None
    size: int = None
    details: typing.MutableMapping = None
    pixel_id: typing.AnyStr = None
    audience_state: typing.AnyStr = AudienceStateEnum.INACTIVE.value
