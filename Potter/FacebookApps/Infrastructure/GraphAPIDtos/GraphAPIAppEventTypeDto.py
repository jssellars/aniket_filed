import typing
from dataclasses import dataclass


@dataclass
class GraphAPIAppEventTypeDto:
    event_name: typing.AnyStr = None
    display_name: typing.AnyStr = None
    parameters: typing.Any = None
