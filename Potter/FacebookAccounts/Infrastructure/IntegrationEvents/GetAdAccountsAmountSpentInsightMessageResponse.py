import typing
from dataclasses import dataclass


@dataclass
class GetAdAccountsAmountSpentInsightMessageResponse:
    message_type = "GetAdAccountsAmountSpentInsightMessageResponse"
    filed_user_id: int = None
    user_id: str = None
    from_date: str = None
    to_date: str = None
    ad_accounts_amount_spent: typing.List[typing.Any] = None # typing.List[AdAccountAmountSpentModel]
    errors: typing.List[typing.Dict] = None
