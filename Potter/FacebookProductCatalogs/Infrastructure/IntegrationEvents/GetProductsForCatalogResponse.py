import typing
from dataclasses import dataclass, field

from Potter.FacebookProductCatalogs.Infrastructure.Domain.ProductGroup import ProductGroup


@dataclass
class GetProductsForCatalogResponse:
    message_type: typing.AnyStr = 'GetProductsForCatalogResponse'
    business_owner_facebook_id: typing.AnyStr = None
    product_catalog_facebook_id: typing.AnyStr = None
    business_facebook_id: typing.AnyStr = None
    filed_user_id: int = None
    product_groups: typing.List[ProductGroup] = field(default_factory=list)
    errors: typing.List[typing.Dict] = field(default_factory=list)
