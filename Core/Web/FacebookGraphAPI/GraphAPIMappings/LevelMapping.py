from enum import Enum

from Core.Tools.Misc.EnumerationBase import EnumerationBase
from Core.Web.FacebookGraphAPI.GraphAPIDomain.FacebookMiscFields import FacebookMiscFields
from Core.Web.FacebookGraphAPI.Models.FieldsMetadata import FieldsMetadata
from facebook_business.adobjects.ad import Ad
from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.adobjects.adset import AdSet
from facebook_business.adobjects.campaign import Campaign


class Level(EnumerationBase):
    ACCOUNT = "account"
    CAMPAIGN = "campaign"
    ADSET = "adset"
    AD = "ad"


class FacebookLevelPlural(EnumerationBase):
    ACCOUNT = "accounts"
    CAMPAIGN = "campaigns"
    ADSET = "adsets"
    AD = "ads"


class LevelToMongoCollectionEnum(EnumerationBase):
    ACCOUNT = "account"
    CAMPAIGN = "campaign"
    ADSET = "adset"
    AD = "ad"


class LevelToFacebookIdKeyMapping(EnumerationBase):
    ACCOUNT = "account_id"
    CAMPAIGN = "campaign_id"
    ADSET = "adset_id"
    AD = "ad_id"


class LevelToFacebookRequiredIdsKeyMapping(EnumerationBase):
    ACCOUNT = ["account_id"]
    CAMPAIGN = ["campaign_id"]
    ADSET = ["campaign_id", "adset_id"]
    AD = ["campaign_id", "adset_id", "ad_id"]


class LevelToFacebookNameKeyMapping(EnumerationBase):
    ACCOUNT = "account_name"
    CAMPAIGN = "campaign_name"
    ADSET = "adset_name"
    AD = "ad_name"


class LevelToFacebookDeleteNamesKeyMapping(EnumerationBase):
    CAMPAIGN = []
    ADSET = ["campaign_name"]
    AD = ["campaign_name", "adset_name"]


class LevelToIdentificationFields(Enum):
    ACCOUNT = [FieldsMetadata.id.name, FieldsMetadata.name.name, FieldsMetadata.status.name]
    CAMPAIGN = [FieldsMetadata.id.name, FieldsMetadata.name.name, FieldsMetadata.status.name]
    ADSET = [FieldsMetadata.id.name, FieldsMetadata.name.name, FieldsMetadata.campaign_id.name, FieldsMetadata.status.name]
    AD = [
        FieldsMetadata.id.name,
        FieldsMetadata.name.name,
        FieldsMetadata.campaign_id.name,
        FieldsMetadata.adset_id.name,
        FieldsMetadata.status.name
    ]


class LevelToGraphAPIStructure:
    @classmethod
    def get(cls, level, facebook_id):
        if level == Level.ACCOUNT.value:
            return AdAccount(fbid=facebook_id)
        elif level == Level.CAMPAIGN.value:
            return Campaign(fbid=facebook_id)
        elif level == Level.ADSET.value:
            return AdSet(fbid=facebook_id)
        elif level == Level.AD.value:
            return Ad(fbid=facebook_id)
        else:
            raise ValueError(f"Unknown level {level}.")
