from datetime import datetime
from typing import Dict

from bson import BSON

from Core.Web.BusinessOwnerRepository.BusinessOwnerRepository import BusinessOwnerRepository
from Core.Web.FacebookGraphAPI.GraphAPI.GraphAPISdkBase import GraphAPISdkBase
from FacebookTuring.Api.Startup import startup, logger
from FacebookTuring.Infrastructure.Domain.MiscFieldsEnum import MiscFieldsEnum
from FacebookTuring.Infrastructure.Domain.StructureStatusEnum import StructureStatusEnum
from FacebookTuring.Infrastructure.Mappings.LevelMapping import (
    LevelToGraphAPIStructure,
    Level,
    LevelToFacebookIdKeyMapping,
)
from FacebookTuring.Infrastructure.PersistenceLayer.TuringMongoRepository import TuringMongoRepository


class AdsManagerDeleteStructureCommandHandler:
    @classmethod
    def handle(cls, level, facebook_id, business_owner_facebook_id):
        repository = TuringMongoRepository(
            config=startup.mongo_config,
            database_name=startup.mongo_config["structures_database_name"],
            collection_name=level,
            logger=logger,
        )

        deleted_structure = repository.get_structure_details(level=Level(level), key_value=facebook_id)
        if not deleted_structure:
            return False

        deleted_structure[MiscFieldsEnum.level] = level
        deleted_structure[MiscFieldsEnum.structure_id] = deleted_structure.get(
            LevelToFacebookIdKeyMapping.get_enum_by_name(Level(level).name).value,
            None,
        )
        to_be_deleted_structures = repository.get_structures_by_parent_id(
            level=Level(level), parent_id=deleted_structure[MiscFieldsEnum.structure_id]
        )

        to_be_deleted_structures.append(deleted_structure)

        # get business owner permanent Facebook token
        business_owner_permanent_token = BusinessOwnerRepository(startup.session).get_permanent_token(
            business_owner_facebook_id
        )

        # create an instance of the Graph API SDK. This is required to authenticate user requests to FB.
        _ = GraphAPISdkBase(startup.facebook_config, business_owner_permanent_token)
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
                    level=Level(structure[MiscFieldsEnum.level]),
                    key_value=structure[MiscFieldsEnum.structure_id],
                    document=structure,
                )
        except Exception as e:
            raise e

        return True


def mark_structure_as_removed(structure: Dict, business_owner_facebook_id: str) -> Dict:
    structure[MiscFieldsEnum.last_updated_at] = datetime.now()
    structure[MiscFieldsEnum.business_owner_facebook_id] = business_owner_facebook_id
    structure_details = structure[MiscFieldsEnum.details]
    structure_details[MiscFieldsEnum.status] = StructureStatusEnum.REMOVED.name
    structure_details[MiscFieldsEnum.effective_status] = StructureStatusEnum.REMOVED.name
    structure[MiscFieldsEnum.status] = StructureStatusEnum.REMOVED.value
    structure[MiscFieldsEnum.details] = BSON.encode(structure_details)

    return structure
