from Core.Web.GoogleAdWordsAPI.AdWordsAPI.AdWordsBaseClient import AdWordsBaseClient
from Core.mongo_adapter import MongoAdapter
from Core.settings_models import Mongo
from GoogleTuring.BackgroundTasks.Synchronizers.BaseSynchronizer import BaseSynchronizer
from GoogleTuring.Infrastructure.Domain.Structures.StructureFields import (
    AD_GROUP_CRITERIA_FIELDS,
    AD_GROUP_KEYWORDS_STRUCTURE_FIELDS,
    AD_GROUP_STRUCTURE_FIELDS,
    AD_STRUCTURE_FIELDS,
    CAMPAIGN_STRUCTURE_FIELDS,
)
from GoogleTuring.Infrastructure.Domain.Structures.StructureType import LEVELS, StructureType
from GoogleTuring.Infrastructure.Mappings.StructureMappingFactory import StructureMappingFactory
from GoogleTuring.Infrastructure.PersistenceLayer.GoogleTuringStructuresMongoRepository import (
    GoogleTuringStructuresMongoRepository,
)


class StructuresSynchronizer(BaseSynchronizer):
    def __init__(
        self,
        business_owner_id: str,
        account_id: str,
        adwords_client: AdWordsBaseClient,
        mongo_config: Mongo,
        mongo_adapter: MongoAdapter,
    ):
        super().__init__(business_owner_id, account_id, adwords_client, mongo_config)
        self.__mongo_repository = GoogleTuringStructuresMongoRepository(
            client=mongo_adapter.client, database_name=self._mongo_config.google_structures_database_name
        )

    def synchronize(self):
        level_to_dependencies = {
            StructureType.CAMPAIGN: (self._adwords_client.get_campaign_service(), CAMPAIGN_STRUCTURE_FIELDS),
            StructureType.AD_GROUP: (
                (self._adwords_client.get_ad_group_service(), self._adwords_client.get_ad_group_criterion_service()),
                (AD_GROUP_STRUCTURE_FIELDS, AD_GROUP_CRITERIA_FIELDS),
            ),
            StructureType.AD: (self._adwords_client.get_ad_group_ad_service(), AD_STRUCTURE_FIELDS),
            StructureType.AD_GROUP_KEYWORDS: (
                self._adwords_client.get_ad_group_criterion_service(),
                AD_GROUP_KEYWORDS_STRUCTURE_FIELDS,
            ),
        }
        structures_mapping_factory = StructureMappingFactory(level_to_dependencies=level_to_dependencies)

        self._adwords_client.set_client_customer_id(self._account_id)
        additional_info = None
        for level in LEVELS:
            self.__mongo_repository.collection = level.value
            structure_mapping = structures_mapping_factory.get_structure_mapping(
                level=level,
                business_owner_id=self._business_owner_id,
                account_id=str(self._account_id),
                additional_info=additional_info,
            )
            self.__mongo_repository.add_structures(structure_mapping)
            if level == StructureType.AD_GROUP:
                additional_info = structure_mapping.get_ad_group_details()
                structure_mapping.clear_ad_group_details()
