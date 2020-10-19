import typing
from dataclasses import dataclass


@dataclass
class PixelsInsightsCommand:
    business_owner_facebook_id: typing.AnyStr = None
    level: typing.AnyStr = None
    facebook_id: typing.AnyStr = None
    facebook_name: typing.AnyStr = None
    breakdown: typing.AnyStr = None  # aggregation value from Facebook
    start_time: typing.AnyStr = None  # "YYYY-MM-DD"
    end_time: typing.AnyStr = None  # "YYYY-MM-DD"
