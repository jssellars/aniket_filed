from Turing.Infrastructure.Domain.AdModel import AdModel
from Turing.Infrastructure.Domain.AdModelFields import AdModelFields
from Turing.Infrastructure.Domain.AdSetModel import AdSetModel
from Turing.Infrastructure.Domain.AdSetModelFields import AdSetModelFields
from Turing.Infrastructure.Domain.CampaignModel import CampaignModel
from Turing.Infrastructure.Domain.CampaignModelFields import CampaignModelFields
from Turing.Infrastructure.Mappings.AdMapping import AdMapping
from Turing.Infrastructure.Mappings.AdSetMapping import AdSetMapping
from Turing.Infrastructure.Mappings.CampaignMapping import CampaignMapping
from Turing.Infrastructure.Mappings.LevelMapping import Level


class StructureMapping:
    """Convert a FB Structure to Domain structure model"""
    @classmethod
    def get(cls, level):
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
        if level == Level.CAMPAIGN.value:
            return CampaignModelFields
        elif level == Level.ADSET.value:
            return AdSetModelFields
        elif level == Level.AD.value:
            return AdModelFields
        else:
            raise ValueError(f"Invalid level: {level} provided.")