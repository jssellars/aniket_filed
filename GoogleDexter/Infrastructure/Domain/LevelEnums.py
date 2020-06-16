from Core.Tools.Misc.EnumerationBase import EnumerationBase


class LevelEnum(EnumerationBase):
    ACCOUNT = "account"
    CAMPAIGN = "campaign"
    ADGROUP = "adgroup"
    AD = "ad"


class LevelIdKeyEnum(EnumerationBase):
    ACCOUNT = "account_id"
    CAMPAIGN = "campaign_id"
    ADGROUP = "adgroup_id"
    AD = "ad_id"


class LevelNameKeyEnum(EnumerationBase):
    ACCOUNT = "account_name"
    CAMPAIGN = "campaign_name"
    ADGROUP = "adgroup_name"
    AD = "ad_name"
