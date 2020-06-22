from datetime import datetime

from facebook_business.adobjects.ad import Ad
from facebook_business.adobjects.adset import AdSet
from facebook_business.adobjects.campaign import Campaign

from Core.Web.BusinessOwnerRepository.BusinessOwnerRepository import BusinessOwnerRepository
from Core.Web.FacebookGraphAPI.GraphAPI.GraphAPIClientBase import GraphAPIClientBase
from Core.Web.FacebookGraphAPI.GraphAPI.GraphAPIClientConfig import GraphAPIClientBaseConfig
from Core.Web.FacebookGraphAPI.GraphAPI.GraphAPISdkBase import GraphAPISdkBase
from Core.Web.FacebookGraphAPI.Tools import Tools
from FacebookTuring.Api.Queries.AdsManagerCampaignTreeStructureQuery import AdsManagerCampaignTreeStructureQuery
from FacebookTuring.Api.Startup import startup
from FacebookTuring.Infrastructure.GraphAPIRequests.GraphAPIRequestSingleStructure import GraphAPIRequestSingleStructure
from FacebookTuring.Infrastructure.Mappings.LevelMapping import Level, LevelToGraphAPIStructure, \
    LevelToFacebookIdKeyMapping
from FacebookTuring.Infrastructure.Mappings.StructureMapping import StructureMapping, StructureFields
from FacebookTuring.Infrastructure.PersistenceLayer.TuringMongoRepository import TuringMongoRepository


class AdsManagerDuplicateStructureCommandHandlerException(Exception):
    pass


class AdsManagerDuplicateStructureCommandHandler:
    graph_api_client = None

    def handle(self, command, level, facebook_id, business_owner_facebook_id):
        # get business owner permanent Facebook token
        business_owner_permanent_token = (BusinessOwnerRepository(startup.session).
                                          get_permanent_token(business_owner_facebook_id))

        # Create a Facebook API client
        _ = GraphAPISdkBase(startup.facebook_config, business_owner_permanent_token)
        self.graph_api_client = GraphAPIClientBase(business_owner_permanent_token)

        if command.parent_ids:
            try:
                for parent_id in command.parent_ids:
                    self.__duplicate_structure(command,
                                               business_owner_facebook_id,
                                               business_owner_permanent_token,
                                               level,
                                               facebook_id,
                                               parent_id)
            except Exception as e:
                raise e
        else:
            try:
                self.__duplicate_structure(command,
                                           business_owner_facebook_id,
                                           business_owner_permanent_token,
                                           level,
                                           facebook_id)
            except Exception as e:
                raise e

    def __duplicate_structure(self,
                              command,
                              business_owner_facebook_id,
                              business_owner_permanent_token,
                              level,
                              facebook_id,
                              parent_id=None):
        try:
            tree = AdsManagerCampaignTreeStructureQuery.get(level, facebook_id)
        except Exception as e:
            raise AdsManagerDuplicateStructureCommandHandlerException(e)

        if level == Level.ADSET.value:
            tree["children"] = [entry for entry in tree['children'] if entry['id'] == facebook_id]

        for index in range(int(command.number_of_duplicates)):
            new_structure_facebook_id = self.__duplicate_structure_on_facebook(level, facebook_id, parent_id)

            # get full STRUCTURE for newly created entity
            new_structure_details = self.__get_new_structure_details(business_owner_permanent_token,
                                                                     new_structure_facebook_id, level)

            # Add new STRUCTURE
            self.__save_structure_details(business_owner_facebook_id=business_owner_facebook_id,
                                          structure=new_structure_details,
                                          level=level)

            if level == Level.CAMPAIGN.value:
                for adset in tree["children"]:
                    new_adset_facebook_id = self.__duplicate_adset(adset["id"], business_owner_facebook_id, business_owner_permanent_token,
                                                                   new_structure_facebook_id)

                    for ad in adset["children"]:
                        self.__duplicate_ad(ad["id"], business_owner_facebook_id, business_owner_permanent_token, new_adset_facebook_id)

            elif level == Level.ADSET.value:
                for ad_id in tree["children"]:
                    self.__duplicate_ad(ad_id, business_owner_facebook_id, business_owner_permanent_token, new_structure_facebook_id)

    def __duplicate_adset(self, adset_id, business_owner_facebook_id, business_owner_permanent_token, parent_id):
        new_adset_facebook_id = self.__duplicate_structure_on_facebook(Level.ADSET.value, adset_id, parent_id)

        # get full STRUCTURE for newly created entity
        new_adset_details = self.__get_new_structure_details(business_owner_permanent_token,
                                                             new_adset_facebook_id, Level.ADSET.value)
        # Add new STRUCTURE
        self.__save_structure_details(business_owner_facebook_id=business_owner_facebook_id,
                                      structure=new_adset_details,
                                      level=Level.ADSET.value)

        return new_adset_facebook_id

    def __duplicate_ad(self, ad_id, business_owner_facebook_id, business_owner_permanent_token, parent_id):
        new_ad_facebook_id = self.__duplicate_structure_on_facebook(Level.AD.value, ad_id, parent_id)

        # get full STRUCTURE for newly created entity
        new_ad_details = self.__get_new_structure_details(business_owner_permanent_token,
                                                          new_ad_facebook_id, Level.AD.value)
        # Add new STRUCTURE
        self.__save_structure_details(business_owner_facebook_id=business_owner_facebook_id,
                                      structure=new_ad_details,
                                      level=Level.AD.value)

    def __duplicate_structure_on_facebook(self, level, facebook_id, parent_id=None):
        structure = LevelToGraphAPIStructure.get(level, facebook_id)
        params = self.__create_duplicate_parameters(level, parent_id)
        new_structure_id = structure.create_copy(params=params)
        new_structure_id = Tools.convert_to_json(new_structure_id)
        if "ad_object_ids" in new_structure_id:
            return new_structure_id["ad_object_ids"][0]['copied_id']
        elif "copied_ad_id" in new_structure_id:
            return new_structure_id["copied_ad_id"]
        else:
            raise ValueError("Invalid duplicated structure id.")

    def __get_new_structure_details(self, business_owner_permanent_token, facebook_id, level):
        structure_fields = StructureFields.get(level)
        self.graph_api_client.config = self.__build_facebook_api_client_get_details_config(facebook_id=facebook_id,
                                                                                           business_owner_permanent_token=business_owner_permanent_token,
                                                                                           fields=structure_fields.get_structure_fields())
        new_structure_details, _ = self.graph_api_client.call_facebook()

        mapping = StructureMapping.get(level)
        new_structure_details = mapping.load(new_structure_details)
        return new_structure_details

    def __save_structure_details(self, structure=None, business_owner_facebook_id=None, level=None):
        structure.business_owner_facebook_id = business_owner_facebook_id
        structure.last_updated_at = datetime.now()

        repository = TuringMongoRepository(config=startup.mongo_config,
                                           database_name=startup.mongo_config.structures_database_name,
                                           collection_name=level)
        structure_id = getattr(structure, LevelToFacebookIdKeyMapping.get_enum_by_name(Level(level).name).value)
        repository.add_structure(level=Level(level), key_value=structure_id, document=structure)

    @staticmethod
    def __build_facebook_api_client_get_details_config(business_owner_permanent_token, facebook_id, fields):
        config = GraphAPIClientBaseConfig()
        config.try_partial_requests = False
        config.request = GraphAPIRequestSingleStructure(facebook_id=facebook_id,
                                                        business_owner_permanent_token=business_owner_permanent_token,
                                                        fields=fields)
        config.fields = fields

        return config

    def __create_duplicate_parameters(self, level, parent_id=None):
        if level == Level.CAMPAIGN.value:
            return self.__duplicate_campaign_parameters()
        elif level == Level.ADSET.value:
            return self.__duplicate_adset_parameters(parent_id)
        elif level == Level.AD.value:
            return self.__duplicate_ad_parameters(parent_id)
        else:
            raise ValueError(f"Unknown level supplied: {level}. Please try again using campaign, adset, or ad")

    @staticmethod
    def __duplicate_campaign_parameters():
        parameters = {
            "deep_copy": False,
            "status_option": Campaign.StatusOption.paused
        }
        return parameters

    @staticmethod
    def __duplicate_adset_parameters(parent_id):
        parameters = {
            "campaign_id": parent_id,
            "deep_copy": False,
            "status_option": AdSet.StatusOption.paused
        }
        return parameters

    @staticmethod
    def __duplicate_ad_parameters(parent_id):
        parameters = {
            "adset_id": parent_id,
            "status_option": Ad.StatusOption.paused
        }
        return parameters
