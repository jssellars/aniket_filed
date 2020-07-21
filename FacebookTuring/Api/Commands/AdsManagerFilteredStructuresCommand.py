import typing
from dataclasses import dataclass


@dataclass
class AdsManagerFilteredStructuresCommand:
    ad_account_id: typing.AnyStr = None
    campaign_ids: typing.List[typing.AnyStr] = None
    adset_ids: typing.List[typing.AnyStr] = None
