import typing
from dataclasses import dataclass

from Potter.FacebookAccounts.Infrastructure.Domain.BusinessModel import BusinessModel


@dataclass
class BusinessOwner:
    facebook_id: str = None


@dataclass
class GetBusinessOwnersTreesMessageResponse:
    message_type: str = "GetBusinessOwnersTreesMessageResponse" # todo: might need to remove this from here
    facebook_id: str = None
    businesses: typing.List[BusinessModel] = None
    errors: typing.List[typing.Dict] = None
