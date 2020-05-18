import typing
from dataclasses import dataclass


@dataclass
class BusinessDto:
    id: typing.AnyStr = None
    name: typing.AnyStr = None
