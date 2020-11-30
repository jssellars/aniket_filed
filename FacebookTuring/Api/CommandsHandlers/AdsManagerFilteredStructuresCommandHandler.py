import typing

from FacebookTuring.Api.Commands.AdsManagerFilteredStructuresCommand import AdsManagerFilteredStructuresCommand
from FacebookTuring.Api.Mappings.ReportsStructureMinimalMapping import ReportsStructureMinimalMapping
from FacebookTuring.Api.Startup import startup
from FacebookTuring.Infrastructure.Mappings.LevelMapping import Level
from FacebookTuring.Infrastructure.PersistenceLayer.TuringMongoRepository import TuringMongoRepository


class AdsManagerFilteredStructuresCommandHandler:

    @classmethod
    def handle(cls, level: typing.AnyStr = None, command: AdsManagerFilteredStructuresCommand = None):
        collection_name = level
        ad_account_id = command.ad_account_id.split("_")[1]

        try:
            repository = TuringMongoRepository(config=startup.mongo_config,
                                               database_name=startup.mongo_config.structures_database_name,
                                               collection_name=collection_name)
            response = repository.get_structure_info(level=Level(level),
                                                     account_id=ad_account_id,
                                                     campaign_ids=command.campaign_ids,
                                                     adset_ids=command.adset_ids,
                                                     statuses=command.statuses)
            if not response:
                return

            mapping = ReportsStructureMinimalMapping(level=collection_name)
            response = mapping.load(response, many=True)
            return response
        except Exception as e:
            raise e
