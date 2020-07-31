import typing
from dataclasses import dataclass


@dataclass
class GetProductCatalogsForBusinessRequest:
    business_owner_facebook_id: typing.AnyStr = None
    business_facebook_id: typing.AnyStr = None
    filed_user_id: int = None
