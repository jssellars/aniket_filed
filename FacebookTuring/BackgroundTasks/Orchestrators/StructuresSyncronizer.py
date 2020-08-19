import functools
import operator
import typing
from time import sleep

from facebook_business.exceptions import FacebookRequestError

from Core.Web.BusinessOwnerRepository.BusinessOwnerRepository import BusinessOwnerRepository
from Core.Web.FacebookGraphAPI.GraphAPI.GraphAPIClientBase import GraphAPIClientBase
from Core.Web.FacebookGraphAPI.GraphAPI.GraphAPIClientConfig import GraphAPIClientBaseConfig
from Core.Web.FacebookGraphAPI.GraphAPI.GraphAPISdkBase import GraphAPISdkBase
from Core.Web.FacebookGraphAPI.GraphAPIDomain.GraphAPIInsightsFields import GraphAPIInsightsFields
from Core.Web.FacebookGraphAPI.Models.Field import Field
from FacebookTuring.BackgroundTasks.Startup import startup
from FacebookTuring.Infrastructure.GraphAPIRequests.GraphAPIRequestStructures import GraphAPIRequestStructures
from FacebookTuring.Infrastructure.Mappings.LevelMapping import Level
from FacebookTuring.Infrastructure.Mappings.StructureMapping import StructureFields, StructureMapping
from FacebookTuring.Infrastructure.PersistenceLayer.TuringMongoRepository import TuringMongoRepository


class StructuresSyncronizer:
    RATE_LIMIT_EXCEPTION_STATUS = 80004
    SLEEP_ON_RATE_LIMIT_EXCEPTION = 3600

    def __init__(self,
                 business_owner_id: typing.AnyStr = None,
                 account_id: typing.AnyStr = None,
                 level: Level = None):
        self.business_owner_id = business_owner_id
        self.account_id = account_id
        self.level = level

        self.__ad_account_id = "act_" + self.account_id
        self.__permanent_token = None
        self.__mongo_repository = None
        self.__facebook_config = None

    def run(self) -> typing.NoReturn:
        try:
            # get structures for ad account
            fields = StructureFields.get(self.level.value)

            # stop run if there are no available fields to sync for the desired level
            if not fields:
                return

            structures_response = self.__sync(permanent_token=self.permanent_token,
                                              level=self.level,
                                              account_id=self.__ad_account_id,
                                              fields=fields.get_structure_fields())

            # set business owner id
            structures = self.__set_business_owner_id(structures_response, self.business_owner_id)

            # remove incomplete structures
            structures = [structure for structure in structures if self.__is_complete_structure(structure, self.level)]

            # insert structures
            self.__mongo_repository.add_structures_many_with_deprecation(level=self.level, structures=structures)
        except FacebookRequestError as fb_ex:
            if fb_ex.http_status() == self.RATE_LIMIT_EXCEPTION_STATUS:
                sleep(self.SLEEP_ON_RATE_LIMIT_EXCEPTION)
        except Exception as e:
            raise e

    def __is_complete_structure(self, structure=None, level=None) -> bool:
        if level == Level.CAMPAIGN:
            if getattr(structure, GraphAPIInsightsFields.campaign_name) is None or \
                    getattr(structure, GraphAPIInsightsFields.campaign_id) is None:
                return False

        if level == Level.ADSET:
            if getattr(structure, GraphAPIInsightsFields.campaign_name) is None or \
                    getattr(structure, GraphAPIInsightsFields.campaign_id) is None or \
                    getattr(structure, GraphAPIInsightsFields.adset_name) is None or \
                    getattr(structure, GraphAPIInsightsFields.adset_id) is None:
                return False

        if level == Level.AD:
            if getattr(structure, GraphAPIInsightsFields.campaign_name) is None or \
                    getattr(structure, GraphAPIInsightsFields.campaign_id) is None or \
                    getattr(structure, GraphAPIInsightsFields.adset_name) is None or \
                    getattr(structure, GraphAPIInsightsFields.adset_id) is None or \
                    getattr(structure, GraphAPIInsightsFields.ad_name) is None or \
                    getattr(structure, GraphAPIInsightsFields.ad_id) is None:
                return False

        return True

    def __sync(self,
               level: Level = None,
               account_id: typing.AnyStr = None,
               permanent_token: typing.AnyStr = None,
               fields: typing.List[typing.AnyStr] = None) -> typing.NoReturn:

        # create an instance of the Graph API SDK. This is required to authenticate user requests to FB.
        _ = GraphAPISdkBase(self.__facebook_config, permanent_token)

        try:
            graph_api_client = GraphAPIClientBase(permanent_token)
            graph_api_client.config = self.build_get_structure_config(permanent_token=permanent_token,
                                                                      level=level.value,
                                                                      ad_account_id=account_id,
                                                                      fields=fields)
            structures, _ = graph_api_client.call_facebook()
            if isinstance(structures, Exception):
                raise structures

            # Map Facebook structure to domain model
            mapping = StructureMapping.get(level.value)
            structures = mapping.load(structures, many=True)
        except Exception as e:
            raise e

        return structures

    def build_get_structure_config(self,
                                   permanent_token: typing.AnyStr = None,
                                   level: typing.AnyStr = None,
                                   ad_account_id: typing.AnyStr = None,
                                   fields: typing.List[typing.AnyStr] = None,
                                   filter_params: typing.List[typing.Dict] = None) -> GraphAPIClientBaseConfig:
        get_structure_config = GraphAPIClientBaseConfig()
        get_structure_config.try_partial_requests = True
        get_structure_config.fields = fields
        get_structure_config.required_field = 'id'
        level = level + "s"  # todo: find a better way to get the endpoint level for multiple actors by ad account
        get_structure_config.request = GraphAPIRequestStructures(facebook_id=ad_account_id,
                                                                 business_owner_permanent_token=permanent_token,
                                                                 level=level,
                                                                 fields=fields,
                                                                 filter_params=filter_params)

        return get_structure_config

    def set_mongo_repository(self, mongo_repository: TuringMongoRepository = None) -> typing.Any:
        self.__mongo_repository = mongo_repository
        return self

    def set_facebook_config(self, facebook_config=None):
        self.__facebook_config = facebook_config
        return self

    @property
    def permanent_token(self) -> typing.AnyStr:
        if self.__permanent_token is None:
            self.__permanent_token = BusinessOwnerRepository(startup.session).get_permanent_token(
                self.business_owner_id)
        return self.__permanent_token

    @staticmethod
    def __get_fields(fields: typing.List[Field] = None) -> typing.List[typing.AnyStr]:
        fields = [field.facebook_fields for field in fields]
        fields = functools.reduce(operator.iconcat, fields, [])
        return fields

    @staticmethod
    def __set_business_owner_id(structures: typing.List[typing.Any] = None, business_owner_id: typing.AnyStr = None) -> \
            typing.List[typing.Any]:
        for index in range(len(structures)):
            structures[index].business_owner_facebook_id = business_owner_id
        return structures
