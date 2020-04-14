from dataclasses import dataclass
from typing import List


@dataclass
class AdsManagerDuplicateStructureCommand:
    number_of_duplicates: str = None
    parent_ids: List[str] = None
