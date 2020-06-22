import typing
from dataclasses import dataclass, field


@dataclass
class BusinessOwnerStatus:
    id: int = None
    name: typing.AnyStr = None
    display_name: typing.AnyStr = None
    property_name: typing.AnyStr = None


@dataclass
class AdAccountDetails:
    id: typing.AnyStr = None
    name: typing.AnyStr = None
    business_name: typing.AnyStr = None
    business_facebook_id: typing.AnyStr = None


@dataclass
class BusinessDetails:
    id: typing.AnyStr = None
    name: typing.AnyStr = None


@dataclass
class BusinessOwnerPreferencesChangedEvent:
    user_filed_id: int = None
    id: typing.AnyStr = None
    status: BusinessOwnerStatus = field(default_factory=dict)
    ad_accounts: typing.List[AdAccountDetails] = field(default_factory=list)
    businesses: typing.List[BusinessDetails] = field(default_factory=list)
