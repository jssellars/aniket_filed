from enum import Enum


class AdWordsServiceType(Enum):
    LOCATION_CRITERION_SERVICE = 'LocationCriterionService'
    CAMPAIGN_SERVICE = 'CampaignService'
    AD_GROUP_SERVICE = 'AdGroupService'
    AD_GROUP_AD_SERVICE = 'AdGroupAdService'
    AD_SERVICE = 'AdService'
    AD_GROUP_CRITERION_SERVICE = 'AdGroupCriterionService'
    CAMPAIGN_CRITERION_SERVICE = 'CampaignCriterionService'
    BUDGET_SERVICE = 'BudgetService'
