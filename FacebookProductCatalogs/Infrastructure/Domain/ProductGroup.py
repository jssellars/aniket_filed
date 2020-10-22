import typing
from dataclasses import dataclass

from FacebookProductCatalogs.Infrastructure.Domain.Product import Product


@dataclass
class ProductGroup:
    id: typing.AnyStr = None
    retailer_id: typing.AnyStr = None
    products: typing.List[Product] = None
