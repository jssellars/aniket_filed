import typing
from dataclasses import dataclass


@dataclass
class AdPreview:
    business_owner_id: typing.AnyStr = None
    account_id: typing.AnyStr = None
    page_facebook_id: typing.AnyStr = None
    instagram_facebook_id: typing.AnyStr = None
    ad_format: int = None
    ad_template: typing.Dict = None
