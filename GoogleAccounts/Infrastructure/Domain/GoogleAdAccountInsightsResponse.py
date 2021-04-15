from dataclasses import dataclass
from typing import Optional


@dataclass
class AdAccountInsightsResponse:
    account_id: str
    name: str
    business_id: str
    business_manager: str
    currency: str
    amount_spent: float
    cpc_all: float
    cpm: float
    ctr_all: float
    impressions: int
    unique_clicks_all: int
    conversions: float
    average_cost: float
    account_status: Optional[str] = None
    purchase_cost: Optional[float] = None
    unique_ctr_all: Optional[float] = None
