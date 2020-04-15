from enum import Enum

from GoogleTuring.Infrastructure.Domain.GoogleBaseFields import BASE_FIELDS
from GoogleTuring.Infrastructure.Domain.GoogleFieldMetadata import GoogleFieldMetadata
from GoogleTuring.Infrastructure.Domain.SpecificFields import AD_GROUP_FIELDS


class Level(Enum):
    CAMPAIGN = 'campaign'
    AD_GROUP = 'ad_group'
    AD = 'ad'


LEVEL_TO_FIELDS = {
    Level.CAMPAIGN: BASE_FIELDS,
    Level.AD_GROUP: BASE_FIELDS + AD_GROUP_FIELDS,
}

LEVEL_TO_IDENTIFIER = {
    Level.CAMPAIGN: GoogleFieldMetadata.campaign_id,
    Level.AD_GROUP: GoogleFieldMetadata.ad_group_id,
    Level.AD: GoogleFieldMetadata.ad_id
}
