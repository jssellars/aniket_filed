import logging
from dataclasses import dataclass
from datetime import datetime
from typing import List

from marshmallow import EXCLUDE, fields

from Core.fixtures import Fixtures
from Core.mapper import MapperBase, MapperNestedField
from Core.Web.FacebookGraphAPI.GraphAPI.GraphAPIClientBase import GraphAPIClientBase
from Core.Web.FacebookGraphAPI.GraphAPI.GraphAPIClientConfig import GraphAPIClientBaseConfig
from Core.Web.FacebookGraphAPI.GraphAPIMappings.LevelMapping import Level, LevelToFacebookIdKeyMapping
from Core.Web.FacebookGraphAPI.GraphAPIMappings.StructureMapping import StructureFields, StructureMapping
from FacebookTuring.Infrastructure.GraphAPIRequests.GraphAPIRequestSingleStructure import GraphAPIRequestSingleStructure
from FacebookTuring.Infrastructure.PersistenceLayer.TuringMongoRepository import TuringMongoRepository

logger = logging.getLogger(__name__)


@dataclass
class NewCreatedStructureKeys:
    level: str
    account_id: str
    facebook_id: str


class DexterCreatedEventMapping(MapperBase):
    business_owner_id = fields.String()
    new_created_structures = MapperNestedField(target=NewCreatedStructureKeys, many=True)

    class Meta:
        unknown = EXCLUDE


@dataclass
class DexterNewCreatedStructureEvent:
    business_owner_id: str
    new_created_structures: List[NewCreatedStructureKeys]


class DexterNewCreatedStructuresHandler:
    RATE_LIMIT_EXCEPTION_STATUS = 80004
    SLEEP_ON_RATE_LIMIT_EXCEPTION = 3600
    __repository = None
    _config = None

    @classmethod
    def set_repository(cls, repository: TuringMongoRepository = None):
        cls.__repository = repository
        return cls

    @classmethod
    def set_config(cls, config=None):
        cls._config = config
        return cls

    @classmethod
    def handle(cls, message: DexterNewCreatedStructureEvent, fixtures: Fixtures):

        permanent_token = fixtures.business_owner_repository.get_permanent_token(message.business_owner_id)
        for structure in message.new_created_structures:
            cls.__sync(permanent_token, message.business_owner_id, structure)

    @classmethod
    def __sync(cls, permanent_token: str, business_owner_id: str, structure: NewCreatedStructureKeys) -> None:

        # create an instance of the Graph API SDK. This is required to authenticate user requests to FB.
        try:
            graph_api_client = GraphAPIClientBase(permanent_token)
            structure_fields = StructureFields.get(structure.level)
            graph_api_client.config = cls.build_facebook_api_client_get_details_config(
                facebook_id=structure.facebook_id,
                business_owner_permanent_token=permanent_token,
                fields=structure_fields.get_structure_fields(),
            )
            updated_structure, _ = graph_api_client.call_facebook()
            if isinstance(updated_structure, Exception):
                raise updated_structure

            # Map Facebook structure to domain model
            mapping = StructureMapping.get(structure.level)
            updated_structure = mapping.load(updated_structure)
            updated_structure.last_updated_at = datetime.now()
            updated_structure.business_owner_facebook_id = business_owner_id
            updated_structure.account_id = structure.account_id
        except Exception as e:
            raise e

        try:
            structure_id = getattr(
                updated_structure, LevelToFacebookIdKeyMapping.get_enum_by_name(Level(structure.level).name).value
            )
            cls.__repository.add_structure(
                level=Level[structure.level.upper()], key_value=structure_id, document=updated_structure
            )
        except Exception as e:
            raise e

    @classmethod
    def build_facebook_api_client_get_details_config(
        cls, business_owner_permanent_token=None, facebook_id=None, fields=None
    ) -> GraphAPIClientBaseConfig:
        api_config = GraphAPIClientBaseConfig()
        api_config.try_partial_requests = False
        api_config.request = GraphAPIRequestSingleStructure(
            facebook_id=facebook_id, business_owner_permanent_token=business_owner_permanent_token, fields=fields
        )
        api_config.fields = fields
        return api_config
