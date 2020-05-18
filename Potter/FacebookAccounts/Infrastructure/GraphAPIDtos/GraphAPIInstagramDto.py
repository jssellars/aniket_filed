import typing
from dataclasses import dataclass


@dataclass
class GraphAPIInstagramDto:
    ig_accounts: typing.List[typing.Dict] = None
