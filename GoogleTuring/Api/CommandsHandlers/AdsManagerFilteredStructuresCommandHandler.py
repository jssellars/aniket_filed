import typing

from GoogleTuring.Api.Commands.AdsManagerFilteredStructuresCommand import AdsManagerFilteredStructuresCommand
from GoogleTuring.Api.Mappings.AdsManagerStructureMinimalMapping import AdsManagerStructureMinimalMapping
from GoogleTuring.Api.Startup import startup
from GoogleTuring.Infrastructure.Mappings.LevelMapping import Level
from GoogleTuring.Infrastructure.PersistenceLayer.GoogleTuringStructuresMongoRepository import \
    GoogleTuringStructuresMongoRepository


class AdsManagerFilteredStructuresCommandHandler:

    @classmethod
    def handle(cls, level: typing.AnyStr = None, command: AdsManagerFilteredStructuresCommand = None):
        collection_name = level
        ad_account_id = str(command.ad_account_id)

        try:
            repository = GoogleTuringStructuresMongoRepository(config=startup.mongo_config,
                                                               database_name=startup.mongo_config.google_structures_database_name,
                                                               collection_name=collection_name)
            response = repository.get_structure_ids_and_names(level=Level(level),
                                                              account_id=ad_account_id,
                                                              campaign_ids=command.campaign_ids,
                                                              adgroup_ids=command.adset_ids,
                                                              statuses=command.statuses)
            if not response:
                return
            mapping = AdsManagerStructureMinimalMapping(level=collection_name)
            response = mapping.load(response, many=True)
            return response
        except Exception as e:
            raise e
