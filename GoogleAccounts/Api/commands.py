from dataclasses import dataclass
from typing import Optional


@dataclass
class GetAccountsCommand:
    authorization_code: str = None


@dataclass
class AdAccountInsightsCommand:
    from_date: str = None
    to_date: str = None


@dataclass
class GoogleHeaders:
    client_id: str
    client_secret: str
    token: str
    refresh_token: str
    scopes: str
