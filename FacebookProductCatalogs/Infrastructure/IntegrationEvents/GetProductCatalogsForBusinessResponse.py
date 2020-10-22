import typing
from dataclasses import dataclass

from FacebookProductCatalogs.Infrastructure.Domain.ProductCatalog import ProductCatalog


@dataclass
class GetProductCatalogsForBusinessResponse:
    message_type: str = "GetProductCatalogsForBusinessResponse"
    business_owner_facebook_id: typing.AnyStr = None
    business_facebook_id: typing.AnyStr = None
    filed_user_id: int = None
    product_catalogs: typing.List[ProductCatalog] = None
    errors: typing.List[typing.Dict] = None
