import typing
from dataclasses import dataclass


@dataclass
class ProductCatalog:
    id: typing.AnyStr = None
    vertical: typing.AnyStr = None
    name: typing.AnyStr = None
    type: typing.AnyStr = None
    details: typing.Dict = None
