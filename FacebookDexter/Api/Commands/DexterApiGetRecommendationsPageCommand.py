from dataclasses import dataclass

from typing import List


@dataclass
class DexterApiGetRecommendationsPageCommand:
    page_number: int
    page_size: int
    recommendation_filter: dict
    recommendation_sort: dict
    excluded_ids: List[str]


