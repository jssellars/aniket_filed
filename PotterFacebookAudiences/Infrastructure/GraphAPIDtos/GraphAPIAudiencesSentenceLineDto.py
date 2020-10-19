import typing
from dataclasses import dataclass


@dataclass
class GraphAPIAudiencesSentenceLineDto:
    content: typing.AnyStr = None
    children: typing.List[typing.AnyStr] = None
