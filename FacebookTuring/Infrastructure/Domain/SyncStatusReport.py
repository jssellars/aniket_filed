import typing
from dataclasses import dataclass


@dataclass
class SyncStatusReport:
    ad_account_id: typing.AnyStr = None
    number_of_campaigns: int = None
    number_of_adsets: int = None
    number_of_ads: int = None
    last_synced_on: typing.AnyStr = None
    sync_start_date: typing.AnyStr = None
    sync_end_date: typing.AnyStr = None
    details: typing.Dict = None
