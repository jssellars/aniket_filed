from datetime import datetime
from typing import Dict

from bson import BSON

from Core.Web.FacebookGraphAPI.GraphAPI.GraphAPISdkBase import GraphAPISdkBase
from FacebookTuring.Api.startup import config, fixtures
from Core.Web.FacebookGraphAPI.AccountAlteringRestrictions import allow_structure_changes
from Core.Web.FacebookGraphAPI.GraphAPIDomain.FacebookMiscFields import FacebookMiscFields
from FacebookTuring.Infrastructure.Domain.StructureStatusEnum import StructureStatusEnum
from Core.Web.FacebookGraphAPI.GraphAPIMappings.LevelMapping import (
    LevelToGraphAPIStructure,
    Level,
    LevelToFacebookIdKeyMapping,
)
from FacebookTuring.Infrastructure.PersistenceLayer.TuringMongoRepository import TuringMongoRepository


class AdsManagerDeleteStructureCommandHandler:
    @classmethod
    def handle(cls, level, facebook_id, business_owner_facebook_id):
        repository = TuringMongoRepository(
            config=config.mongo,
            database_name=config.mongo.structures_database_name,
            collection_name=level,
        )

        deleted_structure = repository.get_structure_details(level=Level(level), key_value=facebook_id)
        if not deleted_structure:
            return False

        if not allow_structure_changes(deleted_structure["account_id"], config):
            return None

        deleted_structure[FacebookMiscFields.level] = level
        deleted_structure[FacebookMiscFields.structure_id] = deleted_structure.get(
            LevelToFacebookIdKeyMapping.get_enum_by_name(Level(level).name).value,
            None,
        )
        to_be_deleted_structures = repository.get_structures_by_parent_id(
            level=Level(level), parent_id=deleted_structure[FacebookMiscFields.structure_id]
        )

        to_be_deleted_structures.append(deleted_structure)

        # get business owner permanent Facebook token
        business_owner_permanent_token = fixtures.business_owner_repository.get_permanent_token(
            business_owner_facebook_id
        )

        # create an instance of the Graph API SDK. This is required to authenticate user requests to FB.
        _ = GraphAPISdkBase(config.facebook, business_owner_permanent_token)
        try:
            structure = LevelToGraphAPIStructure.get(level, facebook_id)
            structure.api_delete()
        except Exception as e:
            raise e

        # Update structure to REMOVED in our DB
        try:
            for structure in to_be_deleted_structures:
                structure = mark_structure_as_removed(structure, business_owner_facebook_id)
                repository.add_structure(
                    level=Level(structure[FacebookMiscFields.level]),
                    key_value=structure[FacebookMiscFields.structure_id],
                    document=structure,
                )
        except Exception as e:
            raise e

        return True


def mark_structure_as_removed(structure: Dict, business_owner_facebook_id: str) -> Dict:
    structure[FacebookMiscFields.last_updated_at] = datetime.now()
    structure[FacebookMiscFields.business_owner_facebook_id] = business_owner_facebook_id
    structure_details = structure[FacebookMiscFields.details]
    structure_details[FacebookMiscFields.status] = StructureStatusEnum.REMOVED.name
    structure_details[FacebookMiscFields.effective_status] = StructureStatusEnum.REMOVED.name
    structure[FacebookMiscFields.status] = StructureStatusEnum.REMOVED.value
    structure[FacebookMiscFields.details] = BSON.encode(structure_details)

    return structure
