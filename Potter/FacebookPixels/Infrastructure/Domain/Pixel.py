import typing
from dataclasses import dataclass

from Potter.FacebookPixels.Infrastructure.Domain.Event import Event


@dataclass
class Pixel:
    id: str = None
    name: str = None
    date_created: str = None
    last_updated: str = None
    domain: str = None
    creator: str = None
    owner_business_name: str = None
    details_as_json: dict = None
    state: int = None
    events: typing.List[Event] = None
