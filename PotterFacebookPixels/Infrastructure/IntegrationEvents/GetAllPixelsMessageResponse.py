import typing
from dataclasses import dataclass

from PotterFacebookPixels.Infrastructure.Domain.Pixel import Pixel


@dataclass
class GetAllPixelsMessageResponse:
    message_type: str = "GetAllPixelsMessageResponse"
    business_owner_facebook_id: typing.AnyStr = None
    ad_account_id: typing.AnyStr = None
    pixels: typing.List[Pixel] = None
    errors: typing.List[typing.Any] = None
