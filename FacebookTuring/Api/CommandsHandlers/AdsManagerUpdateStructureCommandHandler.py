from datetime import datetime

from Core.settings import Prod
from Core.Web.FacebookGraphAPI.AccountAlteringRestrictions import AccountEnvNotAllowedException, allow_structure_changes
from Core.Web.FacebookGraphAPI.GraphAPI.GraphAPIClientBase import GraphAPIClientBase
from Core.Web.FacebookGraphAPI.GraphAPI.GraphAPIClientConfig import GraphAPIClientBaseConfig
from Core.Web.FacebookGraphAPI.GraphAPI.GraphAPISdkBase import GraphAPISdkBase
from Core.Web.FacebookGraphAPI.GraphAPIMappings.LevelMapping import (
    Level,
    LevelToFacebookIdKeyMapping,
    LevelToGraphAPIStructure,
)
from Core.Web.FacebookGraphAPI.GraphAPIMappings.StructureMapping import StructureFields, StructureMapping
from Core.Web.FacebookGraphAPI.Models.FieldsMetadata import FieldsMetadata
from FacebookTuring.Api.startup import config, fixtures
from FacebookTuring.Infrastructure.GraphAPIRequests.GraphAPIRequestSingleStructure import GraphAPIRequestSingleStructure
from FacebookTuring.Infrastructure.PersistenceLayer.TuringMongoRepository import TuringMongoRepository


class AdsManagerUpdateStructureCommandHandler:
    @classmethod
    def handle(cls, command=None, level=None, facebook_id=None, business_owner_facebook_id=None):
        business_owner_permanent_token = fixtures.business_owner_repository.get_permanent_token(
            business_owner_facebook_id
        )

        # create an instance of the Graph API SDK. This is required to authenticate user requests to FB.
        _ = GraphAPISdkBase(config.facebook, business_owner_permanent_token)

        graph_api_client = GraphAPIClientBase(business_owner_permanent_token)
        structure_fields = StructureFields.get(level)
        graph_api_client.config = cls.build_facebook_api_client_get_details_config(
            facebook_id=facebook_id,
            business_owner_permanent_token=business_owner_permanent_token,
            fields=structure_fields.get_structure_fields(),
        )
        updated_structure, _ = graph_api_client.call_facebook()
        if isinstance(updated_structure, Exception):
            raise updated_structure

        if not allow_structure_changes(updated_structure["account_id"], config):
            raise AccountEnvNotAllowedException

        if level == Level.CAMPAIGN.value and config.environment != Prod.environment:
            raise AccountEnvNotAllowedException

        structure = LevelToGraphAPIStructure.get(level, facebook_id)
        structure.api_update(params=command.details)

        graph_api_client = GraphAPIClientBase(business_owner_permanent_token)
        structure_fields = StructureFields.get(level)
        graph_api_client.config = cls.build_facebook_api_client_get_details_config(
            facebook_id=facebook_id,
            business_owner_permanent_token=business_owner_permanent_token,
            fields=structure_fields.get_structure_fields(),
        )
        updated_structure, _ = graph_api_client.call_facebook()
        if isinstance(updated_structure, Exception):
            raise updated_structure

        new_effective_status = updated_structure[FieldsMetadata.effective_status.name]

        # Map Facebook structure to domain model
        mapping = StructureMapping.get(level)
        updated_structure = mapping.load(updated_structure)
        updated_structure.last_updated_at = datetime.now()
        updated_structure.business_owner_facebook_id = business_owner_facebook_id

        repository = TuringMongoRepository(
            config=config.mongo, database_name=config.mongo.structures_database_name, collection_name=level
        )
        structure_id = getattr(updated_structure, LevelToFacebookIdKeyMapping.get_enum_by_name(Level(level).name).value)
        repository.add_structure(level=Level(level), key_value=structure_id, document=updated_structure)

        return {FieldsMetadata.effective_status.name: new_effective_status.replace("_", " ").capitalize()}

    @classmethod
    def build_facebook_api_client_get_details_config(
        cls, business_owner_permanent_token=None, facebook_id=None, fields=None
    ):
        config = GraphAPIClientBaseConfig()
        config.tryPartialRequests = True
        config.request = GraphAPIRequestSingleStructure(
            facebook_id=facebook_id, business_owner_permanent_token=business_owner_permanent_token, fields=fields
        )
        return config
