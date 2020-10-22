import typing
from dataclasses import dataclass

from FacebookPixels.Infrastructure.GraphAPIDtos.GraphAPIBusinessDto import BusinessDto


@dataclass
class DataSourcesDto:
    id: typing.AnyStr = None
    source_type: typing.AnyStr = None


@dataclass
class GraphAPICustomConversionDto:
    account_id: typing.AnyStr = None
    aggregation_rule: typing.AnyStr = None
    business: BusinessDto = None
    creation_time: typing.AnyStr = None
    custom_event_type: typing.AnyStr = None  # returns a CustomEventType string
    data_sources: typing.List[DataSourcesDto] = None
    default_conversion_value: int = None
    description: typing.AnyStr = None
    event_source_type: typing.AnyStr = None
    first_fired_time: typing.AnyStr = None
    id: typing.AnyStr = None
    is_archived: bool = None
    is_unavailable: bool = None
    last_fired_time: typing.AnyStr = None
    name: typing.AnyStr = None
    retention_days: int = None
    rule: typing.AnyStr = None
    pixel_id: typing.AnyStr = None
