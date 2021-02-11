import typing
from dataclasses import dataclass, field


@dataclass
class AdSetTree:
    facebook_id: typing.AnyStr = None
    ads: typing.List[typing.AnyStr] = field(default_factory=list)


@dataclass
class CampaignTree:
    facebook_id: typing.AnyStr = None
    name: typing.AnyStr = None
    ad_sets: typing.List[AdSetTree] = field(default_factory=list)


@dataclass
class CampaignCreatedEvent:
    message_type = "CampaignCreatedEvent"
    business_owner_id: typing.AnyStr = None
    account_id: typing.AnyStr = None
    campaign_tree: typing.List[CampaignTree] = field(default_factory=list)
