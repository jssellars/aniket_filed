from Core.Web.FacebookGraphAPI.GraphAPIDomain.AdModel import AdModel
from Core.Web.FacebookGraphAPI.GraphAPIDomain.AdModelFields import AdModelFields
from Core.Web.FacebookGraphAPI.GraphAPIDomain.AdSetModel import AdSetModel
from Core.Web.FacebookGraphAPI.GraphAPIDomain.AdSetModelFields import AdSetModelFields
from Core.Web.FacebookGraphAPI.GraphAPIDomain.CampaignModel import CampaignModel
from Core.Web.FacebookGraphAPI.GraphAPIDomain.CampaignModelFields import CampaignModelFields
from Core.Web.FacebookGraphAPI.GraphAPIMappings.AdMapping import AdMapping
from Core.Web.FacebookGraphAPI.GraphAPIMappings.AdSetMapping import AdSetMapping
from Core.Web.FacebookGraphAPI.GraphAPIMappings.CampaignMapping import CampaignMapping
from Core.Web.FacebookGraphAPI.GraphAPIMappings.LevelMapping import Level


class StructureMapping:
    """Convert a FB Structure to Domain structure model"""

    @classmethod
    def get(cls, level):
        if level == Level.ACCOUNT.value:
            return None
        if level == Level.CAMPAIGN.value:
            return CampaignMapping(target=CampaignModel)
        elif level == Level.ADSET.value:
            return AdSetMapping(target=AdSetModel)
        elif level == Level.AD.value:
            return AdMapping(target=AdModel)
        else:
            raise ValueError(f"Invalid level: {level} provided.")


class StructureFields:
    """Get a list of fields to get for each structure"""

    @classmethod
    def get(cls, level):
        if level == Level.ACCOUNT.value:
            return None
        elif level == Level.CAMPAIGN.value:
            return CampaignModelFields
        elif level == Level.ADSET.value:
            return AdSetModelFields
        elif level == Level.AD.value:
            return AdModelFields
        else:
            raise ValueError(f"Invalid level: {level} provided.")
