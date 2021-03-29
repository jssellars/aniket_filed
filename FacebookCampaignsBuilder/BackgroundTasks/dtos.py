from dataclasses import dataclass
from typing import Any, Dict, List


@dataclass
class SmartCreatePublishRequest:
    user_filed_id: int
    business_owner_facebook_id: str
    ad_account_id: str
    template_id: int
    step_one_details: Dict[str, Any]
    step_two_details: Dict[str, Any]
    step_three_details: Dict[str, Any]
    step_four_details: Dict[str, Any]


@dataclass
class SmartEditPublishRequest:
    user_filed_id: int
    business_owner_facebook_id: str
    ad_account_id: str
    campaigns: List[Dict]
    adsets: List[Dict]
    ads: List[Dict]
