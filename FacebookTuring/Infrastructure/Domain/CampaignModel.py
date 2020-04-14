from dataclasses import dataclass


@dataclass
class CampaignModel:
    """Domain campaign model"""
    business_owner_facebook_id: str = None
    account_id: str = None
    campaign_name: str = None
    campaign_id: str = None
    last_updated_at: str = None
    details: dict = None
    actions: dict = None
    status: str = None