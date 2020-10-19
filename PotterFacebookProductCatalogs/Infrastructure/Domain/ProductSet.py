import typing
from dataclasses import dataclass


@dataclass
class ProductSet:
    id: typing.AnyStr = None
    name: typing.AnyStr = None
    details: typing.Dict = None
