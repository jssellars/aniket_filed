from Core.Tools.Misc.Utils import converter_dot_placeholder, convert_placeholder_to_key_dot
from Core.Tools.MongoRepository.MongoRepositoryBase import MongoRepositoryBase
from FacebookTuring.Api.Mappings.AdsManagerStructureMapping import AdsManagerStructureMapping
from FacebookTuring.Api.Mappings.AdsManagerStructureMinimalMapping import AdsManagerStructureMinimalMapping
from FacebookTuring.Api.Startup import startup
from FacebookTuring.Infrastructure.Mappings.LevelMapping import LevelToFacebookIdKeyMapping, LevelToFacebookNameKeyMapping


class AdsManagerGetStructuresQuery:

    @classmethod
    def get_structures(cls, level, ad_account_id):
        collection_name = level
        ad_account_id = ad_account_id.split("_")[1]
        id_key = LevelToFacebookIdKeyMapping.get_by_name(level)
        name_key = LevelToFacebookNameKeyMapping.get_by_name(level)

        try:
            mongo_repository = MongoRepositoryBase(config=startup.mongo_config,
                                                   database_name=startup.mongo_config.structures_database_name,
                                                   collection_name=collection_name)
            response = mongo_repository.get_id_and_name_by_key(key=LevelToFacebookIdKeyMapping.ACCOUNT.value,
                                                               values=[ad_account_id],
                                                               id_key=id_key,
                                                               name_key=name_key)
            mongo_repository.connection_handler.close()

            if response:
                response = converter_dot_placeholder(response, convert_placeholder_to_key_dot)
            mapping = AdsManagerStructureMinimalMapping(level=collection_name)
            response = mapping.load(response, many=True)  # [{"facebookId": entry['id'], "name": entry["name"]} for entry in response]
            return response
        except Exception as e:
            raise e

    @classmethod
    def get_structure_details(cls, level, facebook_id):
        collection_name = level

        try:
            mongo_repository = MongoRepositoryBase(config=startup.mongo_config,
                                                   database_name=startup.mongo_config.structures_database_name,
                                                   collection_name=collection_name)

            id_field_key = LevelToFacebookIdKeyMapping.get_by_name(level)
            structure_details = mongo_repository.get_first_by_key(id_field_key, [facebook_id])
            if structure_details:
                structure_details = converter_dot_placeholder(structure_details, convert_placeholder_to_key_dot)
            elif not structure_details:
                return

            mapping = AdsManagerStructureMapping(level=level)
            response = mapping.load(structure_details)
            return response
        except Exception as e:
            raise e