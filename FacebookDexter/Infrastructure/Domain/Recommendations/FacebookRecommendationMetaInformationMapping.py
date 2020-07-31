from Core.Dexter.Infrastructure.Domain.LevelEnums import LevelEnum
from Core.Dexter.Infrastructure.Domain.Recommendations.RecommendationMetaInformationMappingBase import \
    RecommendationMetaInformationMappingBase


class FacebookRecommendationMetaInformationMapping(RecommendationMetaInformationMappingBase):
    _mapping = {
        LevelEnum.CAMPAIGN: {"structure_id": "campaign_id",
                             "parent_id": "campaign_id",
                             "campaign_id": "campaign_id",
                             "structure_name": "campaign_name",
                             "parent_name": "campaign_name",
                             "campaign_name": "campaign_name",
                             "ad_account_id": "account_id"},
        LevelEnum.ADSET: {"structure_id": "adset_id",
                          "parent_id": "campaign_id",
                          "campaign_id": "campaign_id",
                          "structure_name": "adset_name",
                          "parent_name": "campaign_name",
                          "campaign_name": "campaign_name",
                          "ad_account_id": "account_id"},
        LevelEnum.AD: {"structure_id": "ad_id",
                       "parent_id": "adset_id",
                       "campaign_id": "campaign_id",
                       "structure_name": "ad_name",
                       "parent_name": "adset_name",
                       "campaign_name": "campaign_name",
                       "ad_account_id": "account_id"}
    }

    def __init__(self, level):
        super().__init__(level)

