from dataclasses import dataclass, field
from typing import Dict, List, Optional

from Core.facebook.sdk_adapter.smart_create.constants import FB_MAX_AGE, FB_MIN_AGE
from Core.Web.FacebookGraphAPI.GraphAPIDomain.FacebookMiscFields import FacebookGender


@dataclass
class Location:
    key: str
    name: str
    type: str
    country_code: str
    country_name: str
    supports_region: bool
    supports_city: bool
    city_or_country_name: str
    selected_location_string: str
    region: Optional[str] = None
    region_id: Optional[str] = None


@dataclass
class GeoLocations:
    countries: List[str]


@dataclass
class AgeGroup:
    age_min: int
    age_max: int


@dataclass
class GenderGroup:
    genders: List[FacebookGender]


@dataclass
class Interest:
    id: str
    name: str


@dataclass
class CustomAudience:
    id: str


@dataclass
class FlexibleTargeting:
    interests: Optional[List[Interest]] = field(default_factory=list)
    # TODO: The fields below may be used for complex targeting
    # friends_of_connections
    # connections
    # behaviors
    # college_years
    # education_majors
    # education_schools
    # education_statuses
    # family_statuses
    # home_value
    # interested_in
    # income
    # industries
    # life_events
    # user_adclusters
    # work_positions
    # work_employers


@dataclass
class Targeting:
    flexible_spec: List[FlexibleTargeting]
    age_min: Optional[int] = FB_MIN_AGE
    age_max: Optional[int] = FB_MAX_AGE
    custom_audiences: Optional[List[CustomAudience]] = field(default=list)
    excluded_custom_audiences: Optional[List[CustomAudience]] = field(default=list)
    genders: Optional[List[int]] = field(default_factory=list)
    exclusions: Optional[FlexibleTargeting] = None
    locales: Optional[List[str]] = field(default_factory=list)
    geo_locations: Optional[Dict] = field(default_factory=dict)
    device_platforms: Optional[List[str]] = field(default_factory=list)
    targeting_optimization: Optional[str] = None
    facebook_positions: Optional[List[str]] = field(default_factory=list)
    instagram_positions: Optional[List[str]] = field(default_factory=list)
    user_device: Optional[List[str]] = field(default_factory=list)
    user_os: Optional[List[str]] = field(default_factory=list)
    audience_network_positions: Optional[List[str]] = field(default_factory=list)
    publisher_platforms: Optional[List[str]] = field(default_factory=list)
