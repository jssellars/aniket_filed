from dataclasses import dataclass
from typing import Callable, Optional

from Core.Web.GoogleAdsAPI.Models.GoogleFieldType import GoogleFieldType, GoogleResourceType


@dataclass
class GoogleField:
    name: str
    field_name: str
    field_type: GoogleFieldType
    resource_type: Optional[GoogleResourceType] = None
    conversion_function: Optional[Callable] = None
