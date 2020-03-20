from datetime import datetime

from facebook_business.adobjects.ad import Ad
from facebook_business.adobjects.adset import AdSet
from facebook_business.adobjects.campaign import Campaign

from Core.Web.BusinessOwnerRepository.BusinessOwnerRepository import BusinessOwnerRepository
from Core.Web.FacebookGraphAPI.GraphAPI.GraphAPIClientBase import GraphAPIClientBase
from Core.Web.FacebookGraphAPI.GraphAPI.GraphAPIClientConfig import GraphAPIClientBaseConfig
from Core.Web.FacebookGraphAPI.GraphAPI.GraphAPISdkBase import GraphAPISdkBase
from Turing.Infrastructure.GraphAPIRequests.GraphAPIRequestStructures import GraphAPIRequestStructures
from Core.Web.FacebookGraphAPI.Tools import Tools
from Turing.Api.Startup import startup
from Turing.Infrastructure.Mappings.LevelMapping import Level, LevelToGraphAPIStructure
from Turing.Infrastructure.Mappings.StructureMapping import StructureMapping, StructureFields
from Turing.Infrastructure.PersistenceLayer.TuringMongoRepository import TuringMongoRepository


class AdsManagerDuplicateStructureCommandHandler:

    graph_api_client = None

    def handle(self, command, level, facebook_id, business_owner_facebook_id):
        # get business owner permanent Facebook token
        business_owner_permanent_token = BusinessOwnerRepository(startup.Session).get_permanent_token(business_owner_facebook_id)

        # Create a Facebook API client
        facebook_api_sdk_client = GraphAPISdkBase(startup.facebook_config, business_owner_permanent_token)
        self.graph_api_client = GraphAPIClientBase(business_owner_permanent_token)

        if command.parent_ids:
            for parent_id in command.parent_ids:
                self.duplicate_structure(command,
                                         business_owner_facebook_id,
                                         business_owner_permanent_token,
                                         level,
                                         facebook_id,
                                         parent_id)
        else:
            self.duplicate_structure(command,
                                     business_owner_facebook_id,
                                     business_owner_permanent_token,
                                     level,
                                     facebook_id)

        return 204

    def duplicate_structure(self,
                            command,
                            business_owner_facebook_id,
                            business_owner_permanent_token,
                            level,
                            facebook_id,
                            parent_id=None):
        for index in range(command.number_of_copies):
            new_structure_facebook_id = self.duplicate_structure_on_facebook(level, facebook_id, parent_id)

            # get full STRUCTURE for newly created entity
            new_structure_details = self.get_new_structure_details(business_owner_permanent_token, new_structure_facebook_id, level)

            # Add new STRUCTURE
            self.save_structure_details(business_owner_facebook_id, new_structure_details, level)

    def duplicate_structure_on_facebook(self, level, facebook_id, parent_id=None):
        structure = LevelToGraphAPIStructure.get(level, facebook_id)
        params = self.create_duplicate_parameters(level, parent_id)
        new_structure_id = structure.create_copies(params=params)
        new_structure_id = Tools.convert_to_json(new_structure_id)[0]["ad_object_ids"]

        return new_structure_id

    def get_new_structure_details(self, business_owner_permanent_token, facebook_id, level):
        structure_fields = StructureFields.get(level)
        self.graph_api_client.config = self.build_facebook_api_client_get_details_config(facebook_id,
                                                                                           business_owner_permanent_token,
                                                                                           structure_fields.level,
                                                                                           structure_fields.to_fields_list())
        new_structure_details = self.graph_api_client.call_facebook()

        mapping = StructureMapping.get(level)
        new_structure_details = mapping.load(new_structure_details)
        return new_structure_details

    def save_structure_details(self, structure, business_owner_facebook_id, level):
        structure.business_owner_facebook_id = business_owner_facebook_id
        structure.last_updated_at = datetime.now()

        mongo_repository = TuringMongoRepository(config=startup.mongo_config,
                                                 databaseName=startup.mongo_config['structures_database_name'],
                                                 collection_name=level)
        mongo_repository.AddOne(structure)

    @staticmethod
    def build_facebook_api_client_get_details_config(business_owner_permanent_token, facebook_id, level, fields):
        config = GraphAPIClientBaseConfig()
        config.try_partial_requests = True
        config.request = GraphAPIRequestStructures(facebook_id=facebook_id,
                                                   business_owner_permanent_token=business_owner_permanent_token,
                                                   level=level,
                                                   fields=fields)
        config.fields = fields

        return config

    def create_duplicate_parameters(self, level, parent_id=None):
        if level == Level.CAMPAIGN:
            return self.duplicate_campaign_parameters()
        elif level == Level.ADSET:
            return self.duplicate_adset_parameters(parent_id)
        elif level == Level.AD:
            return self.duplicate_ad_parameters(parent_id)
        else:
            raise ValueError(f"Unknown level supplied: {level}. Please try again using campaign, adset, or ad")

    @staticmethod
    def duplicate_campaign_parameters():
        parameters = {
            "deep_copy": True,
            "status_option": Campaign.StatusOption.paused
        }
        return parameters

    @staticmethod
    def duplicate_adset_parameters(parent_id):
        parameters = {
            "campaign_id": parent_id,
            "deep_copy": True,
            "status_option": AdSet.StatusOption.paused
        }
        return parameters

    @staticmethod
    def duplicate_ad_parameters(parent_id):
        parameters = {
            "adset_id": parent_id,
            "status_option": Ad.StatusOption.paused
        }
        return parameters