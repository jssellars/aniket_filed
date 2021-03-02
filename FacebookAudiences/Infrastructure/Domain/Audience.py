from typing import Dict, List, MutableMapping
from dataclasses import dataclass, field

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
    locations: List[Dict] = field(default_factory=list)
    languages: List[Dict] = field(default_factory=list)
    interests: List[Dict] = field(default_factory=list)
    narrow_interests: List[Dict] = field(default_factory=list)
    excluded_interests: List[Dict] = field(default_factory=list)
