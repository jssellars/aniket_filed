import typing
from dataclasses import dataclass, field


@dataclass
class BusinessOwnerCreateCommand:
    facebook_id: str = None
    name: str = None
    email: str = None
    temporary_token: str = None
    requested_permissions: typing.List[typing.AnyStr] = field(default_factory=list)
    filed_user_id: int = None


@dataclass
class BusinessOwnerUpdateCommand:
    facebook_id: str = None


@dataclass
class AdAccountInsightsCommand:
    business_owner_facebook_id: str = None
    from_date: str = None
    to_date: str = None
