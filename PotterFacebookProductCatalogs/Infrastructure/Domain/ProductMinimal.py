import typing
from dataclasses import dataclass


@dataclass
class ProductMinimal:
    set_id: typing.AnyStr = None
    product_ids: typing.List[typing.AnyStr] = None
