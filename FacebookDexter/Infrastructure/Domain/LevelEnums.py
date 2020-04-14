from enum import Enum


class LevelEnum(Enum):
    ACCOUNT = "account"
    CAMPAIGN = "campaign"
    ADSET = "adset"
    AD = "ad"


class LevelIdKeyEnum(Enum):
    ACCOUNT = "account_id"
    CAMPAIGN = "campaign_id"
    ADSET = "adset_id"
    AD = "ad_id"


class LevelNameKeyEnum(Enum):
    ACCOUNT = "account_name"
    CAMPAIGN = "campaign_name"
    ADSET = "adset_name"
    AD = "ad_name"
