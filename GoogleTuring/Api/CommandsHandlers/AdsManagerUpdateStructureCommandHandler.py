import logging

from google.ads.googleads.errors import GoogleAdsException

from GoogleTuring.Api.CommandsHandlers.GoogleTokenGetter import GoogleTokenGetter
from GoogleTuring.Infrastructure.AdsAPIHandlers.AdsAPIStructuresHandler import AdsAPIStructuresHandler
from GoogleTuring.Infrastructure.AdWordsAPIHandlers.AdWordsAPIStructuresHandler import AdWordsAPIStructuresHandler
from GoogleTuring.Infrastructure.Domain.Structures.StructureFields import AD_GROUP_CRITERIA_FIELDS
from GoogleTuring.Infrastructure.Domain.Structures.StructureType import StructureType
from GoogleTuring.Infrastructure.Mappings.StructureMappingFactory import StructureMappingFactory
from GoogleTuring.Infrastructure.PersistenceLayer.GoogleTuringStructuresMongoRepository import (
    GoogleTuringStructuresMongoRepository,
)

logger = logging.getLogger(__name__)


class AdsManagerUpdateStructureCommandHandler(GoogleTokenGetter):
    @classmethod
    def handle(cls, config, command, account_id, level, structure_id, business_owner_google_id):
        business_owner_permanent_token = cls._get_permanent_token(business_owner_google_id)
        additional_info = None
        if business_owner_permanent_token:
            try:
                level = StructureType.get_enum_by_value(level)
                mongo_repository = GoogleTuringStructuresMongoRepository(
                    config=config.mongo,
                    database_name=config.mongo.google_structures_database_name,
                    collection_name=level.value,
                )
                if level in [StructureType.AD, StructureType.AD_GROUP_KEYWORDS]:
                    additional_info = mongo_repository.get_additional_info(level, structure_id)

                updated_structure, helper_service = AdWordsAPIStructuresHandler.update_structure(
                    config=config,
                    permanent_token=business_owner_permanent_token,
                    client_customer_id=account_id,
                    level=level,
                    structure_id=structure_id,
                    details=command.details,
                    data_source_name=command.dataSourceName,
                    additional_info=additional_info,
                )
            except Exception as e:
                logger.exception(repr(e))
                raise e

        else:
            raise Exception("Google account not found")

        try:

            if helper_service:
                structure_mapping_factory = StructureMappingFactory(
                    {level: ((None, helper_service), (None, AD_GROUP_CRITERIA_FIELDS))}
                )
            else:
                structure_mapping_factory = StructureMappingFactory()

            structure_mapping = structure_mapping_factory.get_structure_mapping(
                level,
                business_owner_google_id,
                account_id,
                entries=[updated_structure],
                additional_info=additional_info,
            )
            mongo_repository.update_structure(structure_mapping)
        except Exception as e:
            raise e


class AdsManagerUpdateStructureCommandHandlerAdsAPI:
    @classmethod
    def handle(cls, refresh_token, google_config, command, level):
        try:
            return AdsAPIStructuresHandler.update_structure(
                config=google_config, refresh_token=refresh_token, command=command, level=level
            )

        except GoogleAdsException as ex:
            logger.exception(f"Request with ID '{ex.request_id}' failed with status {ex.error.code().name}")
