import typing
from dataclasses import dataclass


@dataclass
class GraphAPIPixelStatsDataDto:
    value: str = None
    count: int = None


@dataclass
class GraphAPIPixelStatsDto:
    data: typing.List[GraphAPIPixelStatsDataDto] = None
    start_time: typing.AnyStr = None
    aggregation: typing.AnyStr = None
