import math
from dataclasses import dataclass
from typing import List


@dataclass
class BusinessOwner:
    business_owner_id: str = None
    ad_account_ids: List[str] = None

    def get_number_of_account_ids(self):
        return len(self.ad_account_ids)

    def get_batch_size(self):
        # TODO: get this 10 in a param in config
        return math.ceil((10 * self.get_number_of_account_ids()) / 100)
