import typing
from dataclasses import dataclass


@dataclass
class LoggingCommand:
    details: typing.Any = None
    timestamp: typing.AnyStr = None
    user_id: typing.AnyStr = None
    business_owner_facebook_id: typing.AnyStr = None
    business_owner_google_id: typing.AnyStr = None
    jwt_token: typing.AnyStr = ""
    correlation_id: typing.AnyStr = None
