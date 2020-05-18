import typing
from dataclasses import dataclass, field

from Potter.FacebookApps.Infrastructure.Domain.App import App


@dataclass
class GetAllAppsMessageResponse:
    message_type = "GetAllAppsMessageResponse"
    business_owner_facebook_id: typing.AnyStr = None
    ad_account_id: typing.AnyStr = None
    apps: typing.List[App] = field(default_factory=list)
    errors: typing.List[typing.Dict] = field(default_factory=list)
