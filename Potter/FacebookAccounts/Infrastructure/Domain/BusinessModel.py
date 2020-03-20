import typing
from dataclasses import dataclass, field


@dataclass
class BusinessModel:
    id: str = None
    name: str = None
    ad_accounts: typing.List[typing.Any] = field(default_factory=list) # List[AdAccountModel]