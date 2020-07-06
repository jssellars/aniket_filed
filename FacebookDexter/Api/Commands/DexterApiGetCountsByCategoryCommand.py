from dataclasses import dataclass

from typing import List


@dataclass
class DexterApiGetCountsByCategoryCommand:
    channel: str
    campaign_ids: List[str]
