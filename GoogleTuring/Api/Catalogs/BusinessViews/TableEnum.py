from enum import Enum


class TableEnum(Enum):
    AD_PERFORMANCES = 'AdPerformances'

    CAMPAIGN_PERFORMANCES = 'CampaignPerformances'
    CAMPAIGN_GENDER_PERFORMANCES = 'CampaignGenderPerformances'
    CAMPAIGN_GEO_PERFORMANCES = 'CampaignGeoPerformances'
    CAMPAIGN_AGE_RANGE_PERFORMANCES = 'CampaignAgeRangePerformances'
    CAMPAIGN_KEYWORDS_PERFORMANCES = 'CampaignKeywordsPerformances'

    AD_GROUP_PERFORMANCES = 'AdGroupPerformances'
    AD_GROUP_GENDER_PERFORMANCES = 'AdGroupGenderPerformances'
    AD_GROUP_GEO_PERFORMANCES = 'AdGroupGeoPerformances'
    AD_GROUP_AGE_RANGE_PERFORMANCES = 'AdGroupAgeRangePerformances'
    AD_GROUP_KEYWORDS_PERFORMANCES = 'AdGroupKeywordsPerformances'
