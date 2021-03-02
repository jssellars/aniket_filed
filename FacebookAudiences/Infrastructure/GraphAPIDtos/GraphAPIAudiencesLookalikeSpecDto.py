from dataclasses import dataclass
from typing import List, Any


@dataclass
class GraphAPIAudiencesLookalikeSpecDto:
    country: str = None
    is_financial_service = bool
    origin: List[Any] = None
    origin_event_name: str = None
    origin_event_source_name: str = None
    origin_event_source_type: str = None
    product_set_name: str = None
    ratio: float = None
    starting_ratio: float = None
    target_countries: List[str] = None
    target_country_names: List[str] = None
    type: str = None
