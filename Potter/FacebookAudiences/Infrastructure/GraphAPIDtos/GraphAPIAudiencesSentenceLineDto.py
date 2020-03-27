from dataclasses import dataclass

import typing


@dataclass
class GraphAPIAudiencesSentenceLineDto:
    content: typing.AnyStr = None
    children: typing.List[typing.AnyStr] = None