from dataclasses import dataclass
from datetime import datetime
from typing import List

DEFAULT_DATE_TIME = '%Y-%m-%d'


@dataclass
class UpdatedBusinessOwnersDetails:
    business_owner_facebook_id: str = None
    ad_account_ids: List[str] = None


@dataclass
class FacebookTuringDataSyncCompletedEvent:
    business_owners: List[UpdatedBusinessOwnersDetails]
    message_type: str = "FacebookTuringDataSyncCompletedEvent"
    timestamp: datetime = datetime.now().strftime(DEFAULT_DATE_TIME)
