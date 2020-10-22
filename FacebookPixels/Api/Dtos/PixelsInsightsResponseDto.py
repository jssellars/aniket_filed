import typing
from dataclasses import dataclass


@dataclass
class PixelsInsightsResponseDto:
    breakdown: typing.AnyStr = None
    value: typing.AnyStr = None
    count: int = None
    timestamp: typing.AnyStr = None
