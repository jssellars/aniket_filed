import typing
from dataclasses import dataclass
from datetime import datetime
from typing import List


@dataclass
class AdAccountDetails:
    facebook_id: str = None
    from_date: str = None
    to_date: str = None


@dataclass
class GetAdAccountsAmountSpentInsightMessageRequest:
    filed_user_id: int
    business_owner_facebook_id: str
    ad_account_ids: List[str]
    dates: List[datetime]


"""
Sample request
{
    "filed_user_id": 1,
    "user_id": "1623950661230875",
    "from_date": "",
    "to_date": "",
    "ad_accounts_details": [
        {
            "facebook_id": "act_2066904460189854",
            "from_date": "2020-01-01",
            "to_date": "2020-02-01"
        }
    ]
}
"""
