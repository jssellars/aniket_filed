import typing
from dataclasses import dataclass

from Potter.FacebookProductCatalogs.Infrastructure.Domain.ProductSet import ProductSet


@dataclass
class GetProductSetsForCatalogResponse:
    message_type = 'GetProductSetsForCatalogResponse'
    business_owner_facebook_id: typing.AnyStr = None
    business_facebook_id: typing.AnyStr = None
    product_catalog_facebook_id: typing.AnyStr = None
    filed_user_id: int = None
    product_sets: typing.List[ProductSet] = None
    errors: typing.List[typing.Dict] = None
