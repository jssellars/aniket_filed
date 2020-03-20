import typing
from dataclasses import dataclass


@dataclass
class GraphAPIInstagramDto:
    facebook_id: typing.AnyStr = None
    name: typing.AnyStr = None


