import typing
from dataclasses import dataclass


@dataclass
class GraphAPIPixelStatsDataDto:
    value: str = None
    count: int = None
    event: str = None

@dataclass
class GraphAPIPixelStatsDto:
    data: typing.List[GraphAPIPixelStatsDataDto] = None
    start_time: typing.AnyStr = None
    aggregation: typing.AnyStr = None
