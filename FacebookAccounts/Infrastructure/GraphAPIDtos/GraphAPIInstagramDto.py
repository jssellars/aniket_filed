import typing
from dataclasses import dataclass, field


@dataclass
class GraphAPIInstagramDto:
    ig_accounts: typing.List[typing.Dict] = field(default_factory=list)
