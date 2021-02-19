import functools
import logging
import operator
import typing
from time import sleep
from typing import List

from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.exceptions import FacebookRequestError

from Core.Web.FacebookGraphAPI.GraphAPI.GraphAPIClientConfig import GraphAPIClientBaseConfig
from Core.Web.FacebookGraphAPI.GraphAPI.GraphAPISdkBase import GraphAPISdkBase
from Core.Web.FacebookGraphAPI.GraphAPIDomain.GraphAPIInsightsFields import GraphAPIInsightsFields
from Core.Web.FacebookGraphAPI.GraphAPIMappings.LevelMapping import Level
from Core.Web.FacebookGraphAPI.Models.Field import Field
from FacebookTuring.BackgroundTasks.startup import fixtures
from FacebookTuring.Infrastructure.GraphAPIRequests.GraphAPIRequestStructures import GraphAPIRequestStructures
from FacebookTuring.Infrastructure.Mappings.StructureMapping import StructureFields, StructureMapping
from FacebookTuring.Infrastructure.PersistenceLayer.TuringMongoRepository import TuringMongoRepository

logger = logging.getLogger(__name__)


class StructuresSyncronizer:
    RATE_LIMIT_EXCEPTION_STATUS = 80004
    SLEEP_ON_RATE_LIMIT_EXCEPTION = 3600

    def __init__(self, business_owner_id: typing.AnyStr = None, account_id: typing.AnyStr = None, level: Level = None):
        self.business_owner_id = business_owner_id
        self.account_id = account_id
        self.level = level

        self.__ad_account_id = "act_" + self.account_id
        self.__permanent_token = None
        self.__mongo_repository = None

    def run(self) -> typing.NoReturn:
        try:
            # get structures for ad account
            fields = StructureFields.get(self.level.value)

            # stop run if there are no available fields to sync for the desired level
            if not fields:
                return

            structures_response = self.__sync(
                level=self.level,
                account_id=self.__ad_account_id,
                fields=fields.get_structure_fields(),
            )

            # set business owner id
            structures = self.__set_business_owner_id(structures_response, self.business_owner_id)

            # remove incomplete structures
            structures = [structure for structure in structures if self.__is_complete_structure(structure, self.level)]

            # insert structures
            self.__mongo_repository.add_updated_structures(self.level, self.__ad_account_id, structures)
        except FacebookRequestError as fb_ex:
            if fb_ex.http_status() == self.RATE_LIMIT_EXCEPTION_STATUS:
                sleep(self.SLEEP_ON_RATE_LIMIT_EXCEPTION)
            else:
                raise
        except Exception:
            raise

    def __is_complete_structure(self, structure=None, level=None) -> bool:
        if level == Level.CAMPAIGN:
            if (
                    getattr(structure, GraphAPIInsightsFields.campaign_name) is None
                    or getattr(structure, GraphAPIInsightsFields.campaign_id) is None
            ):
                return False

        if level == Level.ADSET:
            if (
                    getattr(structure, GraphAPIInsightsFields.campaign_name) is None
                    or getattr(structure, GraphAPIInsightsFields.campaign_id) is None
                    or getattr(structure, GraphAPIInsightsFields.adset_name) is None
                    or getattr(structure, GraphAPIInsightsFields.adset_id) is None
            ):
                return False

        if level == Level.AD:
            if (
                    getattr(structure, GraphAPIInsightsFields.campaign_name) is None
                    or getattr(structure, GraphAPIInsightsFields.campaign_id) is None
                    or getattr(structure, GraphAPIInsightsFields.adset_name) is None
                    or getattr(structure, GraphAPIInsightsFields.adset_id) is None
                    or getattr(structure, GraphAPIInsightsFields.ad_name) is None
                    or getattr(structure, GraphAPIInsightsFields.ad_id) is None
            ):
                return False

        return True

    def __sync(
            self,
            level: Level = None,
            account_id: typing.AnyStr = None,
            fields: typing.List[typing.AnyStr] = None,
    ) -> List:

        try:
            # create an instance of the Graph API SDK. This is required to authenticate user requests to FB.
            ad_account = AdAccount(account_id)

            if level == Level.CAMPAIGN:
                structures = ad_account.get_campaigns(fields=fields)
            elif level == Level.ADSET:
                structures = ad_account.get_ad_sets(fields=fields)
            elif level == Level.AD:
                structures = ad_account.get_ads(fields=fields)
            else:
                structures = None

            if not structures:
                return []

            # Map Facebook structure to domain model
            mapping = StructureMapping.get(level.value)
            structures = mapping.load([structure.export_all_data() for structure in structures], many=True)
        except Exception as e:
            raise e

        return structures

    def build_get_structure_config(
            self,
            permanent_token: typing.AnyStr = None,
            level: typing.AnyStr = None,
            ad_account_id: typing.AnyStr = None,
            fields: typing.List[typing.AnyStr] = None,
            filter_params: typing.List[typing.Dict] = None,
    ) -> GraphAPIClientBaseConfig:
        api_config = GraphAPIClientBaseConfig()
        api_config.try_partial_requests = True
        api_config.fields = fields
        api_config.required_field = "id"
        level = level + "s"  # todo: find a better way to get the endpoint level for multiple actors by ad account
        api_config.request = GraphAPIRequestStructures(
            facebook_id=ad_account_id,
            business_owner_permanent_token=permanent_token,
            level=level,
            fields=fields,
            filter_params=filter_params,
        )

        return api_config

    def set_mongo_repository(self, mongo_repository: TuringMongoRepository = None) -> typing.Any:
        self.__mongo_repository = mongo_repository
        return self

    @staticmethod
    def __get_fields(fields: typing.List[Field] = None) -> typing.List[typing.AnyStr]:
        fields = [field.facebook_fields for field in fields]
        fields = functools.reduce(operator.iconcat, fields, [])
        return fields

    @staticmethod
    def __set_business_owner_id(
            structures: typing.List[typing.Any] = None, business_owner_id: typing.AnyStr = None
    ) -> typing.List[typing.Any]:
        for index in range(len(structures)):
            structures[index].business_owner_facebook_id = business_owner_id
        return structures
