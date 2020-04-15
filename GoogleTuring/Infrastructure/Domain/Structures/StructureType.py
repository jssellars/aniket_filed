from enum import Enum


class StructureType(Enum):
    AD = 'ad'
    AD_GROUP = 'ad_group'
    CAMPAIGN = 'campaign'
    AD_GROUP_KEYWORDS = 'ad_group_keywords'


LEVELS = [
    StructureType.CAMPAIGN,
    StructureType.AD_GROUP,
    StructureType.AD,
    StructureType.AD_GROUP_KEYWORDS
]
