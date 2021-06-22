from datetime import datetime
from typing import Dict

from bson import BSON
from facebook_business.exceptions import FacebookRequestError

from Core.settings import Prod
from Core.Web.FacebookGraphAPI.AccountAlteringRestrictions import AccountEnvNotAllowedException, allow_structure_changes
from Core.Web.FacebookGraphAPI.GraphAPI.GraphAPISdkBase import GraphAPISdkBase
from Core.Web.FacebookGraphAPI.GraphAPIDomain.FacebookMiscFields import FacebookMiscFields
from Core.Web.FacebookGraphAPI.GraphAPIDomain.StructureStatusEnum import StructureStatusEnum
from Core.Web.FacebookGraphAPI.GraphAPIMappings.LevelMapping import (
    Level,
    LevelToFacebookIdKeyMapping,
    LevelToGraphAPIStructure,
)
from FacebookTuring.Api.startup import config, fixtures
from FacebookTuring.Infrastructure.PersistenceLayer.TuringMongoRepository import TuringMongoRepository


class AdsManagerDeleteStructureCommandHandler:
    @classmethod
    def handle(cls, level, facebook_id, business_owner_facebook_id):

        # get business owner permanent Facebook token
        business_owner_permanent_token = fixtures.business_owner_repository.get_permanent_token(
            business_owner_facebook_id
        )
        _ = GraphAPISdkBase(config.facebook, business_owner_permanent_token)

        fb_structure = LevelToGraphAPIStructure.get(level, facebook_id)

        repository = TuringMongoRepository(
            config=config.mongo,
            database_name=config.mongo.structures_database_name,
            collection_name=level,
        )

        deleted_structure = repository.get_structure_details(level=Level(level), key_value=facebook_id)

        # If the structure is not in db, just delete it from Facebook Graph API
        if not deleted_structure:
            fb_structure.api_delete()
            return True

        if not allow_structure_changes(deleted_structure["account_id"].replace("act_", ""), config):
            raise AccountEnvNotAllowedException

        if level == Level.CAMPAIGN.value and config.environment != Prod.environment:
            raise AccountEnvNotAllowedException

        deleted_structure[FacebookMiscFields.level] = level
        deleted_structure[FacebookMiscFields.structure_id] = deleted_structure.get(
            LevelToFacebookIdKeyMapping.get_enum_by_name(Level(level).name).value,
            None,
        )
        to_be_deleted_structures = repository.get_structures_by_parent_id(
            level=Level(level), parent_id=deleted_structure[FacebookMiscFields.structure_id]
        )

        to_be_deleted_structures.append(deleted_structure)

        fb_structure.api_delete()

        # Update structure to REMOVED in our DB
        for structure in to_be_deleted_structures:
            structure = mark_structure_as_removed(structure, business_owner_facebook_id)
            repository.add_structure(
                level=Level(structure[FacebookMiscFields.level]),
                key_value=structure[FacebookMiscFields.structure_id],
                document=structure,
            )

        return True


class AdsDeleteStructureCommandHandler:
    @staticmethod
    def handle(level, facebook_id, business_owner_facebook_id):
        # get business owner permanent Facebook token
        business_owner_permanent_token = fixtures.business_owner_repository.get_permanent_token(
            business_owner_facebook_id
        )
        _ = GraphAPISdkBase(config.facebook, business_owner_permanent_token)

        try:
            fb_structure = LevelToGraphAPIStructure.get(level, facebook_id)
            fb_structure.api_delete()
        except FacebookRequestError as e:
            raise Exception(f"FB error: {e}")
        except Exception as e:
            raise Exception(f"Py Error: {e}")


def mark_structure_as_removed(structure: Dict, business_owner_facebook_id: str) -> Dict:
    structure[FacebookMiscFields.last_updated_at] = datetime.now()
    structure[FacebookMiscFields.business_owner_facebook_id] = business_owner_facebook_id
    structure_details = structure[FacebookMiscFields.details]
    structure_details[FacebookMiscFields.status] = StructureStatusEnum.REMOVED.name
    structure_details[FacebookMiscFields.effective_status] = StructureStatusEnum.REMOVED.name
    structure[FacebookMiscFields.status] = StructureStatusEnum.REMOVED.value
    structure[FacebookMiscFields.details] = BSON.encode(structure_details)

    return structure
