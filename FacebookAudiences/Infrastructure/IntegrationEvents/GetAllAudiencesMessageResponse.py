import typing
from dataclasses import dataclass

from FacebookAudiences.Infrastructure.Domain.Audience import Audience


@dataclass
class GetAllAudiencesMessageResponse:
    message_type = "GetAllAudiencesMessageResponse"
    business_owner_facebook_id: typing.AnyStr = None
    ad_account_id: typing.AnyStr = None
    business_id: typing.AnyStr = None
    audiences: typing.List[Audience] = None
    errors: typing.List[typing.MutableMapping] = None
