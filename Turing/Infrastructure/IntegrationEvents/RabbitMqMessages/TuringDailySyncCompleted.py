from dataclasses import dataclass
from datetime import datetime
from typing import List


@dataclass
class UpdatedBusinessOwnersDetails:
    business_owner_facebook_id: str = None
    account_ids: List[str] = None


@dataclass
class TuringDailySyncCompleted:

    updated_facebook_business_owners: List[UpdatedBusinessOwnersDetails]
    message_type: str = "TuringDailySyncCompleted"
    timestamp: datetime = datetime.now()
