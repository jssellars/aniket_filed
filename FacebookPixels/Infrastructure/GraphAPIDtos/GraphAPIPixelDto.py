import typing
from dataclasses import dataclass

from FacebookPixels.Infrastructure.GraphAPIDtos.GraphAPIBusinessDto import BusinessDto


@dataclass
class CreatorDto:
    id: typing.AnyStr = None
    name: typing.AnyStr = None


@dataclass
class AdAccountDto:
    id: typing.AnyStr = None
    account_id: typing.AnyStr = None


@dataclass
class GraphAPIPixelDto:
    automatic_matching_fields: typing.List[typing.AnyStr] = None
    can_proxy: bool = None
    code: typing.AnyStr = None
    creation_time: typing.AnyStr = None
    creator: CreatorDto = None
    data_use_setting: typing.AnyStr = None
    enable_automatic_matching: bool = None
    first_party_cookie_status: typing.AnyStr = None
    id: typing.AnyStr = None
    is_created_by_business: bool = None
    is_unavailable: bool = None
    last_fired_time: typing.AnyStr = None
    name: typing.AnyStr = None
    owner_ad_account: AdAccountDto = None
    owner_business: BusinessDto = None
    domain: typing.AnyStr = None
