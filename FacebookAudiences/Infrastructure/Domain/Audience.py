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
    state: int = AudienceStateEnum.INACTIVE.value
    locations: List[Dict] = field(default_factory=list)
    languages: List[Dict] = field(default_factory=list)
    interests: List[Dict] = field(default_factory=list)
    narrow_interests: List[Dict] = field(default_factory=list)
    excluded_interests: List[Dict] = field(default_factory=list)
    age_range: Dict = field(default_factory=dict)
    gender: int = None
    custom_audiences: List[Dict] = field(default_factory=list)
    included_custom_audiences: List[Dict] = field(default_factory=list)
    # Renamed 'excluded' to 'exclude' to be consistent with Filed Saved Audience Field
    exclude_custom_audiences: List[Dict] = field(default_factory=list)
