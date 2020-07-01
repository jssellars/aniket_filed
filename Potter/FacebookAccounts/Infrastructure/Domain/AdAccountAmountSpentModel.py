from dataclasses import dataclass


@dataclass
class AdAccountAmountSpentModel:
    ad_account_id: str = None
    business_id: str = None
    business_name: str = None
    amount_spent: float = 0.0
    currency: str = None
