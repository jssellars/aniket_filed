import math
import typing
from dataclasses import dataclass

BATCH_SIZE = 0.25


@dataclass
class FacebookTuringDataSyncCompletedEvent:
    business_owner_facebook_id: str = None
    ad_account_ids: typing.List[str] = None

    def __len__(self):
        return len(self.ad_account_ids)

    def get_batch_size(self):
        return math.ceil((BATCH_SIZE * len(self)))
