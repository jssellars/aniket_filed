from dataclasses import dataclass
from typing import Optional


@dataclass
class GooglePerformanceInsightsResponse:
    campaign_id: str
    campaign_name: str
    impressions: int
    clicks: int
    ctr: float
    average_cpc: Optional[float] = None
    adgroup_id: Optional[str] = None
    adgroup_name: Optional[str] = None
    keyword_id: Optional[str] = None
    keyword_text: Optional[str] = None
    keyword_match_type: Optional[str] = None
    date: Optional[str] = None
    device: Optional[str] = None
