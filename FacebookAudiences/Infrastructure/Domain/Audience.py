from typing import Dict, MutableMapping
from dataclasses import dataclass

from FacebookAudiences.Infrastructure.Domain.AudienceStateEnum import AudienceStateEnum


@dataclass
class Audience:
    facebook_id: str = None
    name: str = None
    date_created: str = None
    last_updated: str = None
    source: str = None
    subtype: str = None
    type: str = None
    size: int = None
    details: MutableMapping = None
    pixel_id: str = None
    audience_state: str = AudienceStateEnum.INACTIVE.value
    locations: Dict = None
