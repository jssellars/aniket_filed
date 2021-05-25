from enum import Enum


class GoogleFieldType(Enum):
    ATTRIBUTE = "attribute"
    SEGMENT = "segments"
    METRIC = "metrics"


class GoogleResourceType(Enum):
    CUSTOMER = "customer"
    CUSTOMER_CLIENT = "customer_client"
    CAMPAIGN = "campaign"
    ADGROUP = "ad_group"
    Ad = "ad_group_ad"
    KEYWORD_VIEW = "keyword_view"
    AD_GROUP_CRITERION = "ad_group_criterion"
    BIDDING_STRATEGY = "bidding_strategy"
    USER_INTEREST = "user_interest"
    CUSTOM_INTEREST = "custom_interest"
    CAMPAIGN_BUDGET = "campaign_budget"
