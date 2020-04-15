from GoogleTuring.BackgroundTasks.Mappings.AdGroupAdStructureMapping import AdGroupAdStructureMapping
from GoogleTuring.BackgroundTasks.Mappings.AdGroupKeywordsMapping import AdGroupKeywordsMapping
from GoogleTuring.BackgroundTasks.Mappings.AdGroupStructureMapping import AdGroupStructureMapping
from GoogleTuring.BackgroundTasks.Mappings.CampaignStructureMapping import CampaignStructureMapping
from GoogleTuring.Infrastructure.Domain.Structures.StructureType import StructureType


class StructureMappingFactory:
    def __init__(self, level_to_dependencies):
        self.__level_to_dependencies = level_to_dependencies

    def get_structure_processor(self, level, business_owner_id, account_id, additional_info):
        service, structure_fields = self.__level_to_dependencies[level]

        if level == StructureType.CAMPAIGN:
            return CampaignStructureMapping(business_owner_id=business_owner_id, account_id=account_id, service=service, structure_fields=structure_fields)
        elif level == StructureType.AD_GROUP:
            ad_group_service, criterion_service = service
            ad_group_structure_fields, criterion_fields = structure_fields
            return AdGroupStructureMapping(business_owner_id=business_owner_id, account_id=account_id, service=ad_group_service, structure_fields=ad_group_structure_fields,
                                           criterion_service=criterion_service, criterion_fields=criterion_fields)
        elif level == StructureType.AD:
            return AdGroupAdStructureMapping(business_owner_id=business_owner_id, account_id=account_id, ad_group_details=additional_info,
                                             service=service, structure_fields=structure_fields)
        elif level == StructureType.AD_GROUP_KEYWORDS:
            return AdGroupKeywordsMapping(business_owner_id=business_owner_id, account_id=account_id, service=service, structure_fields=structure_fields,
                                          ad_group_details=additional_info)
