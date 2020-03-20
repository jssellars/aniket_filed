from dataclasses import dataclass


@dataclass
class AdAccountModel:
    facebook_id: str = None
    name: str = None
    owner_business_facebook_id: str = None
    owner_business_name: str = None
    currency: str = None
    status: int = None