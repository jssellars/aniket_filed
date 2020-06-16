from Core.Tools.Misc.EnumerationBase import EnumerationBase


class StructureType(EnumerationBase):
    AD = 'ad'
    AD_GROUP = 'adgroup'
    CAMPAIGN = 'campaign'
    AD_GROUP_KEYWORDS = 'keywords'


LEVELS = [
    StructureType.CAMPAIGN,
    StructureType.AD_GROUP,
    StructureType.AD,
    StructureType.AD_GROUP_KEYWORDS
]

LEVEL_TO_ID = {
    StructureType.AD: 'ad_id',
    StructureType.AD_GROUP: 'adgroup_id',
    StructureType.CAMPAIGN: 'campaign_id',
    StructureType.AD_GROUP_KEYWORDS: 'keywords_id'
}
