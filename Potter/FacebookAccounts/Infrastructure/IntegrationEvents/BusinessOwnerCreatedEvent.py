from dataclasses import dataclass
from typing import List

from Potter.FacebookAccounts.Infrastructure.Domain.BusinessModel import BusinessModel


@dataclass
class BusinessOwnerCreatedEvent:
    message_type: str = "BusinessOwnerCreatedEvent"
    facebook_id: str = None
    name: str = None
    email: str = None
    requested_permissions: str = None
    filed_user_id: int = None
    businesses: List[BusinessModel] = None
