from dataclasses import dataclass, field
from typing import Dict, Optional, List

from FacebookCampaignsBuilder.Infrastructure.GraphAPIHandlers.smart_create.targeting import Location


@dataclass
class CampaignSplit:
    campaign_template: Dict
    all_locations: Optional[List[Location]] = field(default_factory=list)
    device: Optional[str] = None
    location: Optional[Location] = None
