import functools
import logging
import operator
from time import sleep
from typing import List, Dict, Any

from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.exceptions import FacebookRequestError

from Core.Web.FacebookGraphAPI.GraphAPI.GraphAPIClientConfig import GraphAPIClientBaseConfig
from Core.Web.FacebookGraphAPI.GraphAPI.SdkGetStructures import get_sdk_structures
from Core.Web.FacebookGraphAPI.GraphAPIDomain.FacebookMiscFields import FacebookMiscFields
from Core.Web.FacebookGraphAPI.GraphAPIDomain.GraphAPIInsightsFields import GraphAPIInsightsFields
from Core.Web.FacebookGraphAPI.GraphAPIMappings.LevelMapping import Level
from Core.Web.FacebookGraphAPI.Models.Field import Field
from FacebookTuring.Infrastructure.GraphAPIRequests.GraphAPIRequestStructures import GraphAPIRequestStructures
from FacebookTuring.Infrastructure.Mappings.StructureMapping import StructureFields, StructureMapping
from FacebookTuring.Infrastructure.PersistenceLayer.TuringMongoRepository import TuringMongoRepository

logger = logging.getLogger(__name__)


class StructuresSyncronizer:
    RATE_LIMIT_EXCEPTION_STATUS = 80004
    SLEEP_ON_RATE_LIMIT_EXCEPTION = 3600
    PAGE_SIZE = 100

    def __init__(self, business_owner_id: str = None, account_id: str = None, level: Level = None):
        self.business_owner_id = business_owner_id
        self.account_id = account_id
        self.level = level

        self.__ad_account_id = "act_" + self.account_id
        self.__permanent_token = None
        self.__mongo_repository = None

    def run(self) -> None:
        try:
            # get structures for ad account
            fields = StructureFields.get(self.level.value)

            # stop run if there are no available fields to sync for the desired level
            if not fields:
                return

            self.__sync(
                level=self.level,
                account_id=self.__ad_account_id,
                fields=fields.get_structure_fields(),
            )

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
            account_id: str = None,
            fields: List[str] = None,
    ) -> None:

        structures = get_sdk_structures(account_id, level, fields, params={"limit": self.PAGE_SIZE})

        if not structures:
            return

        self.__mongo_repository.collection = level.value
        self.__mongo_repository.delete_many({FacebookMiscFields.account_id: account_id.replace("act_", "")})

        structures_slice = []
        for structure in structures:
            structures_slice.append(structure.export_all_data())

            if len(structures_slice) == self.PAGE_SIZE:
                self.map_and_insert_structures(level, structures_slice)
                structures_slice = []

        self.map_and_insert_structures(level, structures_slice)

        return

    def map_and_insert_structures(self, level: Level, structures: List[Dict]):

        structure_ids = list({structure["id"] for structure in structures})

        # Map Facebook structure to domain model
        mapping = StructureMapping.get(level.value)

        structures = mapping.load(structures, many=True)
        # set business owner id
        structures = self.__set_business_owner_id(structures, self.business_owner_id)

        # remove incomplete structures
        structures = [structure for structure in structures if self.__is_complete_structure(structure, self.level)]

        # insert structures
        self.__mongo_repository.add_updated_structures(self.level, structure_ids, structures)

    def build_get_structure_config(
            self,
            permanent_token: str = None,
            level: str = None,
            ad_account_id: str = None,
            fields: List[str] = None,
            filter_params: List[Dict] = None,
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

    def set_mongo_repository(self, mongo_repository: TuringMongoRepository = None) -> Any:
        self.__mongo_repository = mongo_repository
        return self

    @staticmethod
    def __get_fields(fields: List[Field] = None) -> List[str]:
        fields = [field.facebook_fields for field in fields]
        fields = functools.reduce(operator.iconcat, fields, [])
        return fields

    @staticmethod
    def __set_business_owner_id(
            structures: List[Any] = None, business_owner_id: str = None
    ) -> List[Any]:
        for index in range(len(structures)):
            structures[index].business_owner_facebook_id = business_owner_id
        return structures
