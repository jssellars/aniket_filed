import typing
from dataclasses import dataclass, field

from FacebookApps.Infrastructure.GraphAPIDtos.GraphAPIAppEventTypeDto import GraphAPIAppEventTypeDto


@dataclass
class GraphAPIAppDto:
    app_event_types: typing.List[GraphAPIAppEventTypeDto] = field(default_factory=list)
    app_name: typing.AnyStr = None
    app_type: typing.AnyStr = None
    category: typing.AnyStr = None
    created_time: typing.AnyStr = None
    description: typing.AnyStr = None
    id: typing.AnyStr = None
    name: typing.AnyStr = None
