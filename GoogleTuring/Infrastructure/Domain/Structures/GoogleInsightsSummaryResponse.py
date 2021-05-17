from dataclasses import dataclass
from typing import Optional


@dataclass
class GoogleInsightsSummaryResponse:
    impressions: int
    clicks: int
    ctr: float
    average_cpc: Optional[float] = None
