from Core.Tools.MongoRepository.MongoRepositoryStatusBase import MongoRepositoryStatusBase
from Core.Web.BusinessOwnerRepository.BusinessOwnerRepository import BusinessOwnerRepository
from Core.Web.FacebookGraphAPI.GraphAPI.GraphAPISdkBase import GraphAPISdkBase
from FacebookTuring.Api.Startup import startup
from FacebookTuring.Infrastructure.Mappings.LevelMapping import LevelToGraphAPIStructure, LevelToFacebookIdKeyMapping
from FacebookTuring.Infrastructure.PersistenceLayer.TuringMongoRepository import TuringMongoRepository


class AdsManagerDeleteStructureCommandHandler:

    @classmethod
    def handle(cls, level, facebook_id, business_owner_facebook_id):
        # get business owner permanent Facebook token
        business_owner_permanent_token = BusinessOwnerRepository(startup.Session).get_permanent_token(business_owner_facebook_id)

        # create an instance of the Graph API SDK. This is required to authenticate user requests to FB.
        facebook_api_sdk_client = GraphAPISdkBase(startup.facebook_config, business_owner_permanent_token)
        try:
            structure = LevelToGraphAPIStructure.get(level, facebook_id)
            structure.api_delete()
        except Exception as e:
            raise e

        # Update structure to REMOVED in our DB
        try:
            mongo_repository = TuringMongoRepository(config=startup.mongo_config,
                                                     database_name=startup.mongo_config['structures_database_name'],
                                                     collection_name=level)
            id_key = LevelToFacebookIdKeyMapping.get_by_name(level)
            response = mongo_repository.change_status(id=facebook_id, new_status=MongoRepositoryStatusBase.REMOVED.value, id_key=id_key)
            return response
        except Exception as e:
            raise e