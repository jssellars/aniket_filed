from GoogleTuring.Infrastructure.Domain.Structures.StructureType import StructureType
from GoogleTuring.Infrastructure.Mappings.AdGroupAdStructureMapping import AdGroupAdStructureMapping
from GoogleTuring.Infrastructure.Mappings.AdGroupKeywordsMapping import AdGroupKeywordsMapping
from GoogleTuring.Infrastructure.Mappings.AdGroupStructureMapping import AdGroupStructureMapping
from GoogleTuring.Infrastructure.Mappings.CampaignStructureMapping import CampaignStructureMapping


class StructureMappingFactory:
    def __init__(self, level_to_dependencies=None):
        self.__level_to_dependencies = level_to_dependencies

    def get_structure_mapping(self, level, business_owner_id, account_id, additional_info=None, entries=None):
        if self.__level_to_dependencies:
            service, structure_fields = self.__level_to_dependencies[level]
        else:
            service = None
            structure_fields = None

        if level == StructureType.CAMPAIGN:
            return CampaignStructureMapping(business_owner_id=business_owner_id, account_id=account_id,
                                            service=service, structure_fields=structure_fields,
                                            entries=entries)
        elif level == StructureType.AD_GROUP:
            ad_group_service, criterion_service = service
            ad_group_structure_fields, criterion_fields = structure_fields
            return AdGroupStructureMapping(business_owner_id=business_owner_id, account_id=account_id,
                                           service=ad_group_service,
                                           structure_fields=ad_group_structure_fields,
                                           criterion_service=criterion_service, criterion_fields=criterion_fields,
                                           entries=entries)
        elif level == StructureType.AD:
            return AdGroupAdStructureMapping(business_owner_id=business_owner_id, account_id=account_id,
                                             ad_group_details=additional_info,
                                             service=service, structure_fields=structure_fields, entries=entries)
        elif level == StructureType.AD_GROUP_KEYWORDS:
            return AdGroupKeywordsMapping(business_owner_id=business_owner_id, account_id=account_id, service=service,
                                          structure_fields=structure_fields,
                                          ad_group_details=additional_info, entries=entries)
