from enum import Enum
from GoogleTuring.Infrastructure.Domain.GoogleFieldMetadata import GoogleFieldMetadata


class Breakdown(Enum):
    # age_range
    AGE_RANGE = 'age_range'

    # gender
    GENDER = 'gender'

    # keywords
    KEYWORDS = 'keywords'

    # geo
    REGION = 'region'
    COUNTRY = 'country'
    CITY = 'city'


class BreakdownType(Enum):
    AGE_BREAKDOWN = 'age_breakdown'
    GENDER_BREAKDOWN = 'gender_breakdown'
    KEYWORDS_BREAKDOWN = 'keywords_breakdown'
    GEO_BREAKDOWN = 'geo_breakdown'


DEFAULT_GEO_BREAKDOWN = Breakdown.COUNTRY
DEFAULT_TIME_BREAKDOWN_FIELD = GoogleFieldMetadata.date

BREAKDOWN_TO_FIELD = {
    Breakdown.AGE_RANGE: GoogleFieldMetadata.age_range,
    Breakdown.GENDER: GoogleFieldMetadata.gender,
    Breakdown.KEYWORDS: GoogleFieldMetadata.keywords,
    Breakdown.REGION: GoogleFieldMetadata.region_name,
    Breakdown.COUNTRY: GoogleFieldMetadata.country_name,
    Breakdown.CITY: GoogleFieldMetadata.city_name
}
