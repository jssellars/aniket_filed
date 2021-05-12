from enum import Enum


class AdsServiceType(Enum):
    LOCATION_CRITERION_SERVICE = "LocationCriterionService"
    CUSTOMER_SERVICE = "CustomerService"
    CAMPAIGN_SERVICE = "CampaignService"
    AD_GROUP_SERVICE = "AdGroupService"
    AD_GROUP_AD_SERVICE = "AdGroupAdService"
    AD_SERVICE = "GoogleAdsService"
    AD_GROUP_CRITERION_SERVICE = "AdGroupCriterionService"
    CAMPAIGN_CRITERION_SERVICE = "CampaignCriterionService"
    CAMPAIGN_BUDGET_SERVICE = "CampaignBudgetService"
    BUDGET_SERVICE = "BudgetService"
    SEARCH_GOOGLE_ADS_REQUEST = "SearchGoogleAdsRequest"
    CAMPAIGN_OPERATION = "CampaignOperation"
    CAMPAIGN_BUDGET_OPERATION = "CampaignBudgetOperation"
    AD_GROUP_OPERATION = "AdGroupOperation"
    AD_GROUP_CRITERION_OPERATION = "AdGroupCriterionOperation"
    CAMPAIGN_STATUS_ENUM = "CampaignStatusEnum"
    KEYWORD_MATCH_TYPE_ENUM = "KeywordMatchTypeEnum"
