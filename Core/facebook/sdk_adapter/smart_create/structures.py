from dataclasses import dataclass, field
from typing import Dict, Optional, List

from Core.facebook.sdk_adapter.smart_create.targeting import Location


@dataclass
class CampaignSplit:
    campaign_template: Dict
    all_locations: Optional[List[Location]] = field(default_factory=list)
    device: Optional[str] = None
    location: Optional[Location] = None
