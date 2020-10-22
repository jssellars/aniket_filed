import typing
from dataclasses import dataclass, field


@dataclass
class PublishCampaignResponse:
    business_owner_facebook_id: typing.AnyStr = None
    campaign_goal: typing.AnyStr = None
    ad_account_id: typing.AnyStr = None
    use_dexter_optimization: bool = None
    campaign_template_filed_id: typing.AnyStr = None
    user_filed_id: int = None
    average_conversion_value: float = None
    campaigns: typing.List[typing.AnyStr] = field(default_factory=list)
