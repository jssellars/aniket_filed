import typing
from dataclasses import dataclass


@dataclass
class GetProductsForCatalogRequest:
    page_size: int = 50
    business_owner_facebook_id: typing.AnyStr = None
    business_facebook_id: typing.AnyStr = None
    product_catalog_facebook_id: typing.AnyStr = None
    filed_user_id: int = None
