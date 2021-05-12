from dataclasses import dataclass
from typing import Dict, List, Optional


@dataclass
class AdsManagerUpdateStructureCommand:
    client_manager_id: str
    client_customer_id: str
    edit_details: List
    campaign_id: Optional[str] = None
    ad_group_id: Optional[str] = None
    keyword_id: Optional[str] = None
