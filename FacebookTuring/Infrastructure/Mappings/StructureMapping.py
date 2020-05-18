from FacebookTuring.Infrastructure.Domain.AdModel import AdModel
from FacebookTuring.Infrastructure.Domain.AdModelFields import AdModelFields
from FacebookTuring.Infrastructure.Domain.AdSetModel import AdSetModel
from FacebookTuring.Infrastructure.Domain.AdSetModelFields import AdSetModelFields
from FacebookTuring.Infrastructure.Domain.CampaignModel import CampaignModel
from FacebookTuring.Infrastructure.Domain.CampaignModelFields import CampaignModelFields
from FacebookTuring.Infrastructure.Mappings.AdMapping import AdMapping
from FacebookTuring.Infrastructure.Mappings.AdSetMapping import AdSetMapping
from FacebookTuring.Infrastructure.Mappings.CampaignMapping import CampaignMapping
from FacebookTuring.Infrastructure.Mappings.LevelMapping import Level


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
