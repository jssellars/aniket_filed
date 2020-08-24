from GoogleTuring.Api.Mappings.AdsManagerStructureMapping import AdsManagerStructureMapping
from GoogleTuring.Api.Mappings.AdsManagerStructureMinimalMapping import AdsManagerStructureMinimalMapping
from GoogleTuring.Api.Startup import startup, logger
from GoogleTuring.Infrastructure.Mappings.LevelMapping import Level
from GoogleTuring.Infrastructure.PersistenceLayer.GoogleTuringStructuresMongoRepository import \
    GoogleTuringStructuresMongoRepository


class AdsManagerGetStructuresQuery:

    @classmethod
    def get_structures(cls, level, ad_account_id):
        collection_name = level

        try:
            repository = GoogleTuringStructuresMongoRepository(config=startup.mongo_config,
                                                               database_name=startup.mongo_config.google_structures_database_name,
                                                               collection_name=collection_name,
                                                               logger=logger)
            response = repository.get_structure_ids_and_names(level=Level(level),
                                                              account_id=ad_account_id)
            if not response:
                return []
            mapping = AdsManagerStructureMinimalMapping(level=collection_name)
            response = mapping.load(response, many=True)
            return response
        except Exception as e:
            raise e

    @classmethod
    def get_structure_details(cls, level, google_id):
        collection_name = level

        try:
            repository = GoogleTuringStructuresMongoRepository(config=startup.mongo_config,
                                                               database_name=startup.mongo_config.google_structures_database_name,
                                                               collection_name=collection_name,
                                                               logger=logger)
            structure_details = repository.get_structure_details(Level(level), google_id)
            if not structure_details:
                return {}

            mapping = AdsManagerStructureMapping(level=level)
            response = mapping.load(structure_details)
            return response
        except Exception as e:
            raise e
