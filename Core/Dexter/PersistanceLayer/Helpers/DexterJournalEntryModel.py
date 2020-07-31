from dataclasses import dataclass
from datetime import datetime

from Core.Dexter.Infrastructure.Domain.ChannelEnum import ChannelEnum


@dataclass
class DexterJournalEntryModel:
    business_owner_id: str = None
    ad_account_id: str = None
    run_status: int = None
    start_timestamp: datetime = None
    end_timestamp: datetime = None
    time_interval: int = None
    channel: ChannelEnum = None