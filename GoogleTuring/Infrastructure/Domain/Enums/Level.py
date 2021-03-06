from enum import Enum

from GoogleTuring.Infrastructure.Domain.GoogleBaseFields import BASE_FIELDS
from GoogleTuring.Infrastructure.Domain.GoogleFieldsMetadata import GoogleFieldsMetadata
from GoogleTuring.Infrastructure.Domain.SpecificFields import AD_GROUP_FIELDS


class Level(Enum):
    CAMPAIGN = "campaign"
    AD_GROUP = "ad_group"
    AD = "ad"
    KEYWORDS = "keywords"


LEVEL_TO_FIELDS = {
    Level.CAMPAIGN: BASE_FIELDS + [GoogleFieldsMetadata.impression_reach],
    Level.AD_GROUP: BASE_FIELDS + AD_GROUP_FIELDS,
}

LEVEL_TO_IDENTIFIER = {
    Level.CAMPAIGN: GoogleFieldsMetadata.campaign_id,
    Level.AD_GROUP: GoogleFieldsMetadata.ad_group_id,
    Level.AD: GoogleFieldsMetadata.ad_id,
    Level.KEYWORDS: GoogleFieldsMetadata.keywords_id,
}
