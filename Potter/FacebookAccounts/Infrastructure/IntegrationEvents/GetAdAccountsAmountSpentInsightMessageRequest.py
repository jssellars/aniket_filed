from dataclasses import dataclass

import typing


@dataclass
class AdAccountDetails:
    facebook_id: str = None
    from_date: str = None
    to_date: str = None


@dataclass
class GetAdAccountsAmountSpentInsightMessageRequest:
    filed_user_id: int = None
    user_id: str = None
    from_date: str = None
    to_date: str = None
    ad_accounts_details: typing.List[typing.Any] = None # typing.List[AdAccountDetails]


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