import typing
from dataclasses import dataclass


@dataclass
class PixelStatsRow:
    aggregation: typing.AnyStr = None
    value: typing.AnyStr = None
    count: int = None
    start_time: typing.AnyStr = None

    def __getitem__(self, item):
        return getattr(self, item)


@dataclass
class FlatPixelStatsModel:
    stats: typing.List[PixelStatsRow] = None
