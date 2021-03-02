from typing import Dict, List
from dataclasses import dataclass, field

from FacebookAudiences.Infrastructure.GraphAPIDtos.GraphAPIAudiencesPermissionsForActionsDto import \
    GraphAPIAudiencesPermissionsForActionsDto
from FacebookAudiences.Infrastructure.GraphAPIDtos.GraphAPIAudiencesSentenceLineDto import \
    GraphAPIAudiencesSentenceLineDto


@dataclass
class AdAccount:
    account_id: str = None
    id: str = None


@dataclass
class GraphAPISavedAudienceDto:
    account: AdAccount = None
    approximate_count: int = None
    description: str = None
    extra_info: str = None
    id: str = None
    name: str = None
    permission_for_actions: GraphAPIAudiencesPermissionsForActionsDto = None
    run_status: str = None
    targeting: Dict = None
    sentence_lines: List[GraphAPIAudiencesSentenceLineDto] = None
    time_created: str = None
    time_updated: str = None
    locations: List[Dict] = field(default_factory=list)
    languages: List[Dict] = field(default_factory=list)
    interests: List[Dict] = field(default_factory=list)
    narrow_interests: List[Dict] = field(default_factory=list)
    excluded_interests: List[Dict] = field(default_factory=list)
