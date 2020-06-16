from enum import Enum

from GoogleTuring.Infrastructure.Domain.GoogleFieldsMetadata import GoogleFieldsMetadata


class Breakdown(Enum):
    # age_range
    AGE_RANGE = 'age'

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
DEFAULT_TIME_BREAKDOWN_FIELD = GoogleFieldsMetadata.date

BREAKDOWN_TO_FIELD = {
    Breakdown.AGE_RANGE: GoogleFieldsMetadata.age_range,
    Breakdown.GENDER: GoogleFieldsMetadata.gender,
    Breakdown.KEYWORDS: GoogleFieldsMetadata.keywords,
    Breakdown.REGION: GoogleFieldsMetadata.region_name,
    Breakdown.COUNTRY: GoogleFieldsMetadata.country_name,
    Breakdown.CITY: GoogleFieldsMetadata.city_name
}
