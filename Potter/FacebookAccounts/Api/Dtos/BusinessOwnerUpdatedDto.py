import typing
from dataclasses import dataclass


@dataclass
class BusinessOwnerUpdatedDto:
    facebook_id: str = None
    requested_permissions: str = None
    businesses: typing.List[typing.Any] = None  # List[BusinessModel]
