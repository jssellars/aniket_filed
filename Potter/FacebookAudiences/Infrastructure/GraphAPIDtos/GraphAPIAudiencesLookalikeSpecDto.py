import typing
from dataclasses import dataclass


@dataclass
class GraphAPIAudiencesLookalikeSpecDto:
    country: typing.AnyStr = None
    is_financial_service = bool
    origin: typing.List[typing.Any] = None
    origin_event_name: typing.AnyStr = None
    origin_event_source_name: typing.AnyStr = None
    origin_event_source_type: typing.AnyStr = None
    product_set_name: typing.AnyStr = None
    ratio: float = None
    starting_ratio: float = None
    target_countries: typing.List[typing.AnyStr] = None
    target_country_names: typing.List[typing.AnyStr] = None
    type: typing.AnyStr = None