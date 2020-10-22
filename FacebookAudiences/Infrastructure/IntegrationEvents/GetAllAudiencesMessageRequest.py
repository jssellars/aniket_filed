import typing
from dataclasses import dataclass


@dataclass
class GetAllAudiencesMessageRequest:
    business_owner_facebook_id: typing.AnyStr = None
    business_id: typing.AnyStr = None
    ad_account_id: typing.AnyStr = None
