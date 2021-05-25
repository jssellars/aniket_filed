import typing

from Core.Web.GoogleAdsAPI.AdsAPIMappings.LevelMapping import Level
from GoogleTuring.Api.Commands.AdsManagerFilteredStructuresCommand import AdsManagerFilteredStructuresCommand
from GoogleTuring.Api.Mappings.ReportsStructureMinimalMapping import ReportsStructureMinimalMapping
from GoogleTuring.Api.startup import config
from GoogleTuring.Infrastructure.PersistenceLayer.GoogleTuringStructuresMongoRepository import (
    GoogleTuringStructuresMongoRepository,
)


class AdsManagerFilteredStructuresCommandHandler:
    @classmethod
    def handle(cls, level: typing.AnyStr = None, command: AdsManagerFilteredStructuresCommand = None):
        collection_name = level
        ad_account_id = str(command.ad_account_id)

        try:
            repository = GoogleTuringStructuresMongoRepository(
                config=config.mongo,
                database_name=config.mongo.google_structures_database_name,
                collection_name=collection_name,
            )
            response = repository.get_structure_info(
                level=Level(level),
                account_id=ad_account_id,
                campaign_ids=command.campaign_ids,
                adgroup_ids=command.adset_ids,
                statuses=command.statuses,
            )

            mapping = ReportsStructureMinimalMapping(level=collection_name)
            response = mapping.load(response, many=True)
            return response
        except Exception as e:
            raise e
