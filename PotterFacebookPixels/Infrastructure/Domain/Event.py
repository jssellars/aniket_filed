import typing
from dataclasses import dataclass


@dataclass
class Event:
    id: typing.AnyStr = None
    name: typing.AnyStr = None
    custom_event_type: typing.AnyStr = None
    date_created: typing.AnyStr = None
    last_updated: typing.AnyStr = None
    event_activity: typing.AnyStr = None
    event_count: int = None
    event_type: int = None
    details_as_json: typing.Dict = None
    rule_as_json: typing.Dict = None
    state: int = None
