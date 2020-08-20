from Core.Web.BusinessOwnerRepository.BusinessOwnerRepository import BusinessOwnerRepository
from Core.Web.FacebookGraphAPI.GraphAPI.GraphAPISdkBase import GraphAPISdkBase
from FacebookTuring.Api.Startup import startup, logger
from FacebookTuring.Infrastructure.Domain.StructureStatusEnum import StructureStatusEnum
from FacebookTuring.Infrastructure.Mappings.LevelMapping import LevelToGraphAPIStructure, Level
from FacebookTuring.Infrastructure.PersistenceLayer.TuringMongoRepository import TuringMongoRepository


class AdsManagerDeleteStructureCommandHandler:

    @classmethod
    def handle(cls, level, facebook_id, business_owner_facebook_id):
        repository = TuringMongoRepository(config=startup.mongo_config,
                                           database_name=startup.mongo_config['structures_database_name'],
                                           collection_name=level,
                                           logger=logger)

        existing_structure_id = repository.get_structure_details(level=Level(level), key_value=facebook_id)
        if not existing_structure_id:
            return False

        # get business owner permanent Facebook token
        business_owner_permanent_token = BusinessOwnerRepository(startup.session).get_permanent_token(
            business_owner_facebook_id)

        # create an instance of the Graph API SDK. This is required to authenticate user requests to FB.
        _ = GraphAPISdkBase(startup.facebook_config, business_owner_permanent_token)
        try:
            structure = LevelToGraphAPIStructure.get(level, facebook_id)
            structure.api_delete()
        except Exception as e:
            raise e

        # Update structure to REMOVED in our DB
        try:
            repository.change_status(level=Level(level),
                                     new_status=StructureStatusEnum.REMOVED.value,
                                     key_value=facebook_id)
        except Exception as e:
            raise e

        return True
