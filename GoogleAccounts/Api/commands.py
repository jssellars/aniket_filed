import typing
from dataclasses import dataclass


@dataclass
class GetAccountsCommand:
    authorization_code: str = None


@dataclass
class GoogleHeaders:
    client_id: str
    client_secret: str
    token: str
    refresh_token: str
    scopes: str
