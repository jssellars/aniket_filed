from GoogleTuring.Api.CommandsHandlers.AdsManagerBaseCommandHandler import AdsManagerBaseCommandHandler
from GoogleTuring.Api.Startup import startup
from GoogleTuring.Infrastructure.AdWordsAPIHandlers.AdWordsAPIStructuresHandler import AdWordsAPIStructuresHandler
from GoogleTuring.Infrastructure.Domain.Structures.StructureStatus import StructureStatus
from GoogleTuring.Infrastructure.Domain.Structures.StructureType import LEVEL_TO_ID
from GoogleTuring.Infrastructure.PersistenceLayer.GoogleTuringStructuresMongoRepository import \
    GoogleTuringStructuresMongoRepository


class AdsManagerDeleteStructureCommandHandler(AdsManagerBaseCommandHandler):

    @classmethod
    def handle(cls, account_id, level, structure_id, business_owner_google_id):
        business_owner_permanent_token = cls._get_permanent_token(business_owner_google_id)
        if business_owner_permanent_token:
            try:
                AdWordsAPIStructuresHandler.delete_structure(permanent_token=business_owner_permanent_token,
                                                             client_customer_id=account_id,
                                                             level=level,
                                                             structure_id=structure_id)
            except Exception as e:
                raise e

        else:
            raise Exception("Google account not found")

        # Update structure to REMOVED in our DB
        try:
            mongo_repository = GoogleTuringStructuresMongoRepository(config=startup.mongo_config,
                                                                     database_name=startup.mongo_config[
                                                                         'google_structures_database_name'],
                                                                     collection_name=level)
            id_key = LEVEL_TO_ID[level]
            mongo_repository.change_status_many(ids=[structure_id], new_status=StructureStatus.REMOVED.value,
                                                id_key=id_key)
        except Exception as e:
            raise e
