import typing
from dataclasses import dataclass, field

from Potter.FacebookApps.Infrastructure.Domain.AppStateEnum import AppStateEnum
from Potter.FacebookApps.Infrastructure.Domain.Event import Event


@dataclass
class App:
    id: typing.AnyStr = None
    name: typing.AnyStr = None
    date_created: typing.AnyStr = None
    last_updated: typing.AnyStr = None
    details_as_json: typing.Dict = field(default_factory=dict)
    state: int = AppStateEnum.INACTIVE.value
    events: typing.List[Event] = field(default_factory=list)
