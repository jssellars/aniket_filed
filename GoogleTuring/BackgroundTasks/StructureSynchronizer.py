from Core.Tools.MongoRepository.MongoConnectionHandler import MongoConnectionHandler
from GoogleTuring.Infrastructure.Domain.Structures.StructureFields import CAMPAIGN_STRUCTURE_FIELDS, AD_STRUCTURE_FIELDS, AD_GROUP_KEYWORDS_STRUCTURE_FIELDS, AD_GROUP_STRUCTURE_FIELDS, \
    AD_GROUP_CRITERIA_FIELDS
from GoogleTuring.Infrastructure.Domain.Structures.StructureType import StructureType, LEVELS
from GoogleTuring.BackgroundTasks.Mappings.StructureMappingFactory import StructureMappingFactory
from GoogleTuring.Infrastructure.PersistanceLayer.GoogleTuringStructuresMongoRepository import GoogleTuringStructuresMongoRepository


class StructureSynchronizer:
    def __init__(self, business_owner_id, account_ids, adwords_client, mongo_config):
        self.__business_owner_id = business_owner_id
        self.__account_ids = account_ids
        self.__adwords_client = adwords_client
        self.__mongo_config = mongo_config

    def synchronize_structures(self):
        level_to_dependencies = {
            StructureType.CAMPAIGN: (self.__adwords_client.get_campaign_service(), CAMPAIGN_STRUCTURE_FIELDS),
            StructureType.AD_GROUP: ((self.__adwords_client.get_ad_group_service(), self.__adwords_client.get_ad_group_criterion_service()), (AD_GROUP_STRUCTURE_FIELDS, AD_GROUP_CRITERIA_FIELDS)),
            StructureType.AD: (self.__adwords_client.get_ad_group_ad_service(), AD_STRUCTURE_FIELDS),
            StructureType.AD_GROUP_KEYWORDS: (self.__adwords_client.get_ad_group_criterion_service(), AD_GROUP_KEYWORDS_STRUCTURE_FIELDS)
        }

        structures_mapping_factory = StructureMappingFactory(level_to_dependencies=level_to_dependencies)
        mongo_conn_handler = MongoConnectionHandler(self.__mongo_config)
        mongo_repository = GoogleTuringStructuresMongoRepository(client=mongo_conn_handler.client, database_name=self.__mongo_config['googleStructuresDatabaseName'])

        for account_id in self.__account_ids:
            self.__adwords_client.set_client_customer_id(account_id)
            additional_info = None
            for level in LEVELS:
                print('[Structure BT] Level: {} account_id: {}'.format(level, account_id))
                mongo_repository.collection = level.value
                structure_mapping = structures_mapping_factory.get_structure_processor(level=level, business_owner_id=self.__business_owner_id,
                                                                                           account_id=account_id,
                                                                                           additional_info=additional_info)
                mongo_repository.add_structures(structure_mapping)
                if level == StructureType.AD_GROUP:
                    additional_info = structure_mapping.get_ad_group_details()
                    structure_mapping.clear_ad_group_details()
