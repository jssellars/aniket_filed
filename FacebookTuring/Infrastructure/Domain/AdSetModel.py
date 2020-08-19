from dataclasses import dataclass


@dataclass
class AdSetModel:
    """Domain adset model"""
    business_owner_facebook_id: str = None
    account_id: str = None
    campaign_name: str = None
    campaign_id: str = None
    adset_name: str = None
    adset_id: str = None
    last_updated_at: str = None
    details: dict = None
    actions: dict = None
    status: str = None
    budget_remaining: str = None
    daily_budget: str = None
    lifetime_budget: str = None
    learning_stage_info: str = None
    created_time: str = None
    start_time: str = None
    end_time: str = None
    date_added: str = None
