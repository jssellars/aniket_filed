from googleads import adwords

from Core.Web.GoogleAdWordsAPI.AdWordsBaseClient import AdWordsBaseClient
from GoogleTuring.Infrastructure.Domain.Enums.FiledGoogleInsightsTableEnum import FiledGoogleInsightsTableEnum
from GoogleTuring.Infrastructure.Domain.GoogleFieldsMetadata import GoogleFieldsMetadata
from GoogleTuring.Infrastructure.Domain.Structures.StructureType import StructureType
from GoogleTuring.Infrastructure.Mappings.UpdateStructureOperandMapper import UpdateStructureOperandMapper


class AdWordsStructuresClient(AdWordsBaseClient):
    def __get_delete_service_from_level(self, level):
        if level == StructureType.CAMPAIGN:
            return self.get_campaign_service()
        elif level == StructureType.AD_GROUP:
            return self.get_ad_group_service()
        elif level == StructureType.AD:
            return self.get_ad_group_ad_service()

    def __get_update_services_from_level(self, level, data_source_name):
        if data_source_name in [FiledGoogleInsightsTableEnum.AGE_RANGE.value,
                                FiledGoogleInsightsTableEnum.GENDER.value,
                                FiledGoogleInsightsTableEnum.KEYWORDS.value]:
            if level == StructureType.CAMPAIGN:
                return self.get_campaign_criterion_service(), None
            elif level == StructureType.AD_GROUP or level == StructureType.AD_GROUP_KEYWORDS:
                return self.get_ad_group_criterion_service(), None
            return None

        elif level == StructureType.CAMPAIGN:
            return self.get_campaign_service(), self.get_budget_service()
        elif level == StructureType.AD_GROUP:
            return self.get_ad_group_service(), self.get_ad_group_criterion_service()
        elif level == StructureType.AD:
            return self.get_ad_group_ad_service(), None

    @staticmethod
    def __get_remove_operations(level, structure_id):
        if level == StructureType.AD:
            operations = [{
                'operator': 'REMOVE',
                'operand': {
                    'id': structure_id
                }
            }]

        else:
            operations = [{
                'operator': 'SET',
                'operand': {
                    'id': structure_id,
                    'status': 'REMOVED'
                }
            }]
        return operations

    def delete_structure(self, structure_id, level):
        service = self.__get_delete_service_from_level(level)
        operations = self.__get_remove_operations(level, structure_id)
        service.mutate(operations)

    @staticmethod
    def __get_budget_id_for_campaign(campaign_service, campaign_id):
        fields = ['Id', 'BudgetId', 'BudgetName', 'Amount']
        query = (adwords.ServiceQueryBuilder()
                 .Select(*fields)
                 .Where('Id').EqualTo(campaign_id)
                 .Limit(0, 100)
                 .Build())

        entries = []
        try:
            for page in query.Pager(campaign_service):
                if 'entries' in page:
                    entries.extend(page['entries'])
        except Exception as e:
            # TODO: log error
            print("Exception " + e.__str__() + " has occurred")

        budget_id = entries[0]['budget']['budgetId']
        return budget_id

    def update_structure(self, structure_id, level, details, data_source_name, additional_info):
        service, helper_service = self.__get_update_services_from_level(level, data_source_name)
        if level == StructureType.CAMPAIGN and GoogleFieldsMetadata.amount.field_name in details:
            budget_id = self.__get_budget_id_for_campaign(service, structure_id)
            additional_info = {'budget_id': budget_id}

        operand, extra_operand = UpdateStructureOperandMapper.map(details=details, structure_id=structure_id,
                                                                  additional_info=additional_info, level=level)

        operations = [{
            'operator': 'SET',
            'operand': operand
        }]

        if extra_operand:
            extra_operations = [{
                'operator': 'SET',
                'operand': extra_operand
            }]
            helper_service.mutate(extra_operations)
            helper_service = None

        result = service.mutate(operations)['value'][0]
        return result, helper_service
