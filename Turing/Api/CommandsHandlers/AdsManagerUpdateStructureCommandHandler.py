from datetime import datetime

from Core.Web.BusinessOwnerRepository.BusinessOwnerRepository import BusinessOwnerRepository
from Core.Web.FacebookGraphAPI.GraphAPI.GraphAPIClientBase import GraphAPIClientBase
from Core.Web.FacebookGraphAPI.GraphAPI.GraphAPIClientConfig import GraphAPIClientBaseConfig
from Core.Web.FacebookGraphAPI.GraphAPI.GraphAPISdkBase import GraphAPISdkBase
from Turing.Api.Startup import startup
from Turing.Infrastructure.GraphAPIRequests.GraphAPIRequestSingleStructure import GraphAPIRequestSingleStructure
from Turing.Infrastructure.Mappings.LevelMapping import LevelToGraphAPIStructure, LevelToFacebookNameKeyMapping, LevelToFacebookIdKeyMapping
from Turing.Infrastructure.Mappings.StructureMapping import StructureFields, StructureMapping
from Turing.Infrastructure.PersistenceLayer.TuringMongoRepository import TuringMongoRepository


class AdsManagerUpdateStructureCommandHandler:

    @classmethod
    def handle(cls, command=None, level=None, facebook_id=None, business_owner_facebook_id=None):
        business_owner_permanent_token = BusinessOwnerRepository(startup.Session).get_permanent_token(business_owner_facebook_id)

        # create an instance of the Graph API SDK. This is required to authenticate user requests to FB.
        facebook_api_sdk_client = GraphAPISdkBase(startup.facebook_config, business_owner_permanent_token)
        try:
            structure = LevelToGraphAPIStructure.get(level, facebook_id)
            structure.api_update(params=command.details)
        except Exception as e:
            raise e

        try:
            graph_api_client = GraphAPIClientBase(business_owner_permanent_token)
            structure_fields = StructureFields.get(level)
            graph_api_client.config = cls.build_facebook_api_client_get_details_config(facebook_id=facebook_id,
                                                                                       business_owner_permanent_token=business_owner_permanent_token,
                                                                                       level=level,
                                                                                       fields=structure_fields.get_structure_fields())
            updated_structure, _ = graph_api_client.call_facebook()

            # Map Facebook structure to domain model
            mapping = StructureMapping.get(level)
            updated_structure = mapping.load(updated_structure)
            updated_structure.last_updated_at = datetime.now()
            updated_structure.business_owner_facebook_id = business_owner_facebook_id
        except Exception as e:
            raise e

        try:
            mongo_repository = TuringMongoRepository(config=startup.mongo_config,
                                                     database_name=startup.mongo_config['structures_database_name'],
                                                     collection_name=level)
            mongo_repository.add_updated_structure(updated_structure,
                                                   id_key=LevelToFacebookIdKeyMapping.get_by_name(level))
        except Exception as e:
            raise e

    @classmethod
    def build_facebook_api_client_get_details_config(cls, business_owner_permanent_token=None, facebook_id=None, level=None, fields=None):
        # todo: remove after finalising the *ModelFields classes.
        fields = list(set(fields)) # keep unique fields only
        try:
            fields.remove(LevelToFacebookIdKeyMapping.get_by_name(level))
            fields.remove(LevelToFacebookNameKeyMapping.get_by_name(level))
        except ValueError:
            pass
        except Exception as e:
            raise e

        config = GraphAPIClientBaseConfig()
        config.tryPartialRequests = True
        config.request = GraphAPIRequestSingleStructure(facebook_id=facebook_id,
                                                        business_owner_permanent_token=business_owner_permanent_token,
                                                        fields=fields)
        return config
