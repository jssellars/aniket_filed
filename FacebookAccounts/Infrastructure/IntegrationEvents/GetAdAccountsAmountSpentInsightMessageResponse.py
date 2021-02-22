from dataclasses import dataclass
from datetime import datetime
from typing import List


@dataclass
class SpendingPerDay:
    date: datetime
    amount: float


@dataclass
class FacebookAdAccountsSpending:
    ad_account_id: str
    business_id: str
    business_name: str
    currency: str
    spendings_per_day: List[SpendingPerDay]


@dataclass
class GetAdAccountsAmountSpentInsightMessageResponse:
    message_type = "GetAdAccountsAmountSpentInsightMessageResponse"
    filed_user_id: int
    business_owner_facebook_id: int
    spendings: List[FacebookAdAccountsSpending]
