from GoogleTuring.Api.CommandsHandlers.AdsManagerBaseCommandHandler import AdsManagerBaseCommandHandler
from GoogleTuring.Api.Startup import startup
from GoogleTuring.BackgroundTasks.Mappings.StructureMappingFactory import StructureMappingFactory
from GoogleTuring.Infrastructure.AdWordsAPIHandlers.AdWordsAPIStructuresHandler import AdWordsAPIStructuresHandler
from GoogleTuring.Infrastructure.Domain.Structures.StructureFields import AD_GROUP_CRITERIA_FIELDS
from GoogleTuring.Infrastructure.Domain.Structures.StructureType import StructureType
from GoogleTuring.Infrastructure.PersistanceLayer.GoogleTuringStructuresMongoRepository import GoogleTuringStructuresMongoRepository


class AdsManagerUpdateStructureCommandHandler(AdsManagerBaseCommandHandler):
    @classmethod
    def handle(cls, command, account_id, level, structure_id, business_owner_google_id):
        business_owner_permanent_token = cls._get_permanent_token(business_owner_google_id)
        additional_info = None
        if business_owner_permanent_token:
            try:
                level = StructureType.get_enum_by_value(level)
                mongo_repository = GoogleTuringStructuresMongoRepository(config=startup.mongo_config,
                                                                         database_name=startup.mongo_config['google_structures_database_name'],
                                                                         collection_name=level.value)
                if level in [StructureType.AD, StructureType.AD_GROUP_KEYWORDS]:
                    additional_info = mongo_repository.get_additional_info(level, structure_id)

                updated_structure, helper_service = AdWordsAPIStructuresHandler.update_structure(permanent_token=business_owner_permanent_token,
                                                                                                 client_customer_id=account_id,
                                                                                                 level=level,
                                                                                                 structure_id=structure_id,
                                                                                                 details=command.details,
                                                                                                 data_source_name=command.dataSourceName,
                                                                                                 additional_info=additional_info)
            except Exception as e:
                import traceback
                traceback.print_exc()
                raise e

        else:
            raise Exception("Google account not found")

        try:

            if helper_service:
                structure_mapping_factory = StructureMappingFactory({level: ((None, helper_service), (None, AD_GROUP_CRITERIA_FIELDS))})
            else:
                structure_mapping_factory = StructureMappingFactory()

            structure_mapping = structure_mapping_factory.get_structure_mapping(level, business_owner_google_id, account_id, entries=[updated_structure], additional_info=additional_info)
            mongo_repository.update_structure(structure_mapping)
        except Exception as e:
            raise e
