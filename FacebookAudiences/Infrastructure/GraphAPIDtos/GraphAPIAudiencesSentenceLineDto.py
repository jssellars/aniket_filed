from dataclasses import dataclass
from typing import List


@dataclass
class GraphAPIAudiencesSentenceLineDto:
    content: str = None
    children: List[str] = None
