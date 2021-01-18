from typing import AnyStr, Dict
from dataclasses import dataclass


@dataclass
class AdPreview:
    business_owner_id: AnyStr = None
    account_id: AnyStr = None
    page_facebook_id: AnyStr = None
    instagram_facebook_id: AnyStr = None
    ad_format: int = None
    ad_template: Dict = None
    objective: AnyStr = None
