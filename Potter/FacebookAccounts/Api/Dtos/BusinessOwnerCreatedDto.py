import typing
from dataclasses import dataclass


@dataclass
class BusinessOwnerCreatedDto:
    facebook_id: str = None
    name: str = None
    email: str = None
    requested_permissions: str = None
    filed_user_id: int = None
    businesses: typing.List[typing.Any] = None  # List[BusinessModel]
