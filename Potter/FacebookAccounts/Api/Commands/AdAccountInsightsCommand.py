from dataclasses import dataclass


@dataclass
class AdAccountInsightsCommand:
    business_owner_facebook_id: str = None
    from_date: str = None
    to_date: str = None
