from Core.Tools.Misc.EnumerationBase import EnumerationBase


class GoogleLevelIdKeyEnum(EnumerationBase):
    ACCOUNT = "ad_account_id"
    CAMPAIGN = "campaign_id"
    ADGROUP = "adgroup_id"
    AD = "ad_id"


class GoogleLevelNameKeyEnum(EnumerationBase):
    ACCOUNT = "ad_account_name"
    CAMPAIGN = "campaign_name"
    ADGROUP = "adgroup_name"
    AD = "ad_name"
