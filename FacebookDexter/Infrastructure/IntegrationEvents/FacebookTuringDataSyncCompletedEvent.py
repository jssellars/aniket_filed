import math
import typing
from dataclasses import dataclass, field

BATCH_SIZE = 0.01


@dataclass
class FacebookTuringDataSyncCompletedEvent:
    business_owner_facebook_id: str = None
    ad_account_ids: typing.List[str] = field(default_factory=list())

    def __len__(self):
        return len(self.ad_account_ids)

    def get_batch_size(self):
        return math.ceil((BATCH_SIZE * len(self)))
