from Core.Tools.Misc.EnumerationBase import EnumerationBase


class Level(EnumerationBase):
    ACCOUNT = "account"
    CAMPAIGN = "campaign"
    ADGROUP = "adgroup"
    AD = "ad"
    KEYWORDS = "keywords"


class LevelManyToMongoCollectionEnum(EnumerationBase):
    ACCOUNT = "accounts"
    CAMPAIGN = "campaigns"
    ADGROUP = "adgroups"
    AD = "ads"
    KEYWORDS = "keywords"


class LevelToMongoCollectionEnum(EnumerationBase):
    ACCOUNT = "account"
    CAMPAIGN = "campaign"
    ADGROUP = "adgroup"
    AD = "ad"
    KEYWORDS = "keywords"


class LevelToGoogleIdKeyMapping(EnumerationBase):
    ACCOUNT = "ad_account_id"
    CAMPAIGN = "campaign_id"
    ADGROUP = "adgroup_id"
    AD = "ad_id"
    KEYWORDS = "keywords_id"


class LevelToGoogleRequiredIdsKeyMapping(EnumerationBase):
    ACCOUNT = ["ad_account_id"]
    CAMPAIGN = ["campaign_id"]
    ADGROUP = ["campaign_id", "adgroup_id"]
    AD = ["campaign_id", "adgroup_id", "ad_id"]
    KEYWORDS = ["campaign_id", "adgroup_id", "keywords_id"]


class LevelToGoogleNameKeyMapping(EnumerationBase):
    ACCOUNT = "ad_account_name"
    CAMPAIGN = "campaign_name"
    ADGROUP = "adgroup_name"
    AD = "ad_name"
    KEYWORDS = "keywords"


class LevelToGoogleDeleteNamesKeyMapping:
    CAMPAIGN = []
    ADGROUP = ["campaign_name"]
    AD = ["campaign_name", "adgroup_name"]
    KEYWORDS = ["campaign_name", "adgroup_name"]
