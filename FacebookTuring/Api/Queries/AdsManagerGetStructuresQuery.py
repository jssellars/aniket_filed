from FacebookTuring.Api.Mappings.AdsManagerStructureMapping import AdsManagerStructureMapping
from FacebookTuring.Api.Mappings.AdsManagerStructureMinimalMapping import AdsManagerStructureMinimalMapping
from FacebookTuring.Api.Startup import startup
from FacebookTuring.Infrastructure.Mappings.LevelMapping import Level
from FacebookTuring.Infrastructure.PersistenceLayer.TuringMongoRepository import TuringMongoRepository


class AdsManagerGetStructuresQuery:

    @classmethod
    def get_structures(cls, level, ad_account_id):
        collection_name = level
        ad_account_id = ad_account_id.split("_")[1]

        try:
            repository = TuringMongoRepository(config=startup.mongo_config,
                                               database_name=startup.mongo_config.structures_database_name,
                                               collection_name=collection_name)
            response = repository.get_structure_ids_and_names(level=Level(level),
                                                              account_id=ad_account_id)
            if not response:
                return
            mapping = AdsManagerStructureMinimalMapping(level=collection_name)
            response = mapping.load(response,
                                    many=True)  # [{"facebookId": entry['id'], "name": entry["name"]} for entry in response]
            return response
        except Exception as e:
            raise e

    @classmethod
    def get_structure_details(cls, level, facebook_id):
        collection_name = level

        try:
            repository = TuringMongoRepository(config=startup.mongo_config,
                                               database_name=startup.mongo_config.structures_database_name,
                                               collection_name=collection_name)
            structure_details = repository.get_structure_details(Level(level), facebook_id)
            if not structure_details:
                return

            mapping = AdsManagerStructureMapping(level=level)
            response = mapping.load(structure_details)
            return response
        except Exception as e:
            raise e
