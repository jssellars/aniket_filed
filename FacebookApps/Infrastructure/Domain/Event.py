import typing
from dataclasses import dataclass, field

from FacebookApps.Infrastructure.Domain.AppStateEnum import AppStateEnum


@dataclass
class Event:
    id: typing.AnyStr = None
    name: typing.AnyStr = None
    display_name: typing.AnyStr = None
    date_created: typing.AnyStr = None
    last_updated: typing.AnyStr = None
    details_as_json: typing.Dict = field(default_factory=dict)
    event_type: typing.AnyStr = None
    state: int = AppStateEnum.INACTIVE.value
