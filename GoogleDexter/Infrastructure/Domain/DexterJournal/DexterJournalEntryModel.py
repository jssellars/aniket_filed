from dataclasses import dataclass
from datetime import datetime


@dataclass
class DexterJournalEntryModel:
    business_owner_id: str = None
    ad_account_id: str = None
    algorithm_type: str = None
    run_status: int = None
    level: str = None
    start_timestamp: datetime = None
    end_timestamp: datetime or None = None
