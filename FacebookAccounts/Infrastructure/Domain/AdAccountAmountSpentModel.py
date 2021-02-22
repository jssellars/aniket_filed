from dataclasses import dataclass

from typing import Optional


@dataclass
class AdAccountAmountSpentModel:
    ad_account_id: str
    business_id: str
    business_name: str
    currency: str
    date: Optional[str] = None
    amount_spent: Optional[float] = 0
