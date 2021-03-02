from dataclasses import dataclass
from typing import List, MutableMapping

from FacebookAudiences.Infrastructure.Domain.Audience import Audience


@dataclass
class GetAllAudiencesMessageResponse:
    message_type = "GetAllAudiencesMessageResponse"
    business_owner_facebook_id: str = None
    ad_account_id: str = None
    business_id: str = None
    audiences: List[Audience] = None
    errors: List[MutableMapping] = None
