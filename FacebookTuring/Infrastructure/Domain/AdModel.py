from dataclasses import dataclass


@dataclass
class AdModel:
    """Domain ad model"""
    business_owner_facebook_id: str = None
    account_id: str = None
    campaign_name: str = None
    campaign_id: str = None
    adset_name: str = None
    adset_id: str = None
    ad_name: str = None
    ad_id: str = None
    last_updated_at: str = None
    details: dict = None
    actions: dict = None
    status: str = None