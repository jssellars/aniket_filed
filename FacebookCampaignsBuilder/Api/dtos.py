import typing
from dataclasses import dataclass, field


@dataclass
class PublishCampaignResponse:
    business_owner_facebook_id: typing.AnyStr = None
    ad_account_id: typing.AnyStr = None
    campaigns: typing.List[typing.AnyStr] = field(default_factory=list)
