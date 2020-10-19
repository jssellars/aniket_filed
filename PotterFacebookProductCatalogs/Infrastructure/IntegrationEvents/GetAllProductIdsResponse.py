import typing
from dataclasses import dataclass, field


@dataclass
class GetAllProductIdsResponse:
    message_type: typing.AnyStr = 'GetAllProductIdsResponse'
    product_catalog_facebook_id: typing.AnyStr = None
    business_facebook_id: typing.AnyStr = None
    business_owner_facebook_id: typing.AnyStr = None
    filed_user_id: int = None
    product_group_ids: typing.List[typing.AnyStr] = field(default_factory=list)
    product_ids: typing.List[typing.AnyStr] = field(default_factory=list)
