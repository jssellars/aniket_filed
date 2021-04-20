from enum import Enum


class GoogleFieldType(Enum):
    ATTRIBUTE = "attribute"
    SEGMENT = "segments"
    METRIC = "metrics"


class GoogleResourceType(Enum):
    CUSTOMER = "customer"
    CUSTOMER_CLIENT = "customer_client"
    CAMPAIGN = "CAMPAIGN"
    ADGROUP = "ADGROUP"
    AD_GROUP_CRITERION = "ad_group_criterion"
    KEYWORD_VIEW = "keyword_view"
