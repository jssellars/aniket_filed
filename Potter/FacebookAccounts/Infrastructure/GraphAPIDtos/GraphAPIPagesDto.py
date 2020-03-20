import typing
from dataclasses import dataclass


@dataclass
class GraphAPIPagesDto:
    pages: typing.List[typing.Dict] = None