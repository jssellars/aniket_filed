from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


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
    campaigns: Optional[List[Dict]] = field(default_factory=list)
    adsets: Optional[List[Dict]] = field(default_factory=list)
    ads: Optional[List[Dict]] = field(default_factory=list)


@dataclass
class AddAdsetAdPublishRequest:
    user_filed_id: int
    business_owner_facebook_id: str
    ad_account_id: str
    parent_level: str
    child_level: str
    parent_ids: List[str]
    child_ids: List[str]
    adsets: Optional[List[Dict]] = field(default_factory=list)
    ads: Optional[List[Dict]] = field(default_factory=list)
