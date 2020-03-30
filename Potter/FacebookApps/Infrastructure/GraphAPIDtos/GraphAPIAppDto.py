import typing
from dataclasses import dataclass, field

from Potter.FacebookApps.Infrastructure.GraphAPIDtos.GraphAPIAppEventTypeDto import GraphAPIAppEventTypeDto


@dataclass
class GraphAPIAppDto:
    id: typing.AnyStr = None,
    name: typing.AnyStr = None,
    app_event_types: typing.List[GraphAPIAppEventTypeDto] = field(default_factory=list)
    description: typing.AnyStr = None
