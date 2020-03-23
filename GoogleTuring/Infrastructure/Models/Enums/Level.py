from enum import Enum

from GoogleTuring.Infrastructure.Models.GoogleBaseFields import BASE_FIELDS
from GoogleTuring.Infrastructure.Models.SpecificFields import AD_GROUP_FIELDS


class Level(Enum):
    CAMPAIGN = 'campaign'
    AD_GROUP = 'ad_group'
    AD = 'ad'


LEVEL_TO_FIELDS = {
    Level.CAMPAIGN: BASE_FIELDS,
    Level.AD_GROUP: BASE_FIELDS + AD_GROUP_FIELDS[:-1],
}
