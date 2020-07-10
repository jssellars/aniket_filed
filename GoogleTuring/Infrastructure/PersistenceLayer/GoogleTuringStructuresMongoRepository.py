# todo: update GoogleTuring repo to latest MongoRepositoryBase
import typing

from bson import BSON

from Core.Tools.MongoRepository.MongoOperator import MongoOperator
from Core.Tools.MongoRepository.MongoRepositoryBase import MongoProjectionState
from GoogleTuring.Infrastructure.Domain.MiscFieldsEnum import MiscFieldsEnum
from GoogleTuring.Infrastructure.Domain.StructureStatusEnum import StructureStatusEnum
from GoogleTuring.Infrastructure.Domain.Structures.StructureStatus import StructureStatus
from GoogleTuring.Infrastructure.Domain.Structures.StructureType import LEVEL_TO_ID
from GoogleTuring.Infrastructure.PersistenceLayer.StatusChangerMongoRepository import StatusChangerMongoRepository
from GoogleTuring.Infrastructure.Mappings.LevelMapping import Level, LevelToGoogleIdKeyMapping, \
    LevelToGoogleNameKeyMapping


class GoogleTuringStructuresMongoRepository(StatusChangerMongoRepository):
    def update_removed_structures(self, deleted_customer_ids):
        if deleted_customer_ids:
            collection_names = self.database.list_collection_names()
            for collection_name in collection_names:
                self.collection = collection_name
                self.change_status_many(ids=deleted_customer_ids, new_status=StructureStatus.REMOVED.value,
                                        id_key="account_id")

    def add_structures(self, structure_mapping):
        processed_entries = structure_mapping.process()
        id_key = structure_mapping.get_structure_id()
        structure_ids = list(map(lambda x: x[id_key], processed_entries))

        query = {
            MongoOperator.AND.value: [{
                id_key: {
                    MongoOperator.IN.value: structure_ids
                },
                "status": {MongoOperator.IN.value: [StructureStatus.ENABLED.value, StructureStatus.PAUSED.value]}
            }]
        }

        existing_structures = self.get(query)
        existing_ids = list(map(lambda x: x[id_key], existing_structures))

        removed_structures_ids = list(set(existing_ids) - set(structure_ids))
        if removed_structures_ids:
            self.change_status_many(ids=removed_structures_ids, new_status=StructureStatus.REMOVED.value,
                                    id_key=id_key)

        new_structures_ids = list(set(structure_ids) - set(existing_ids))
        if new_structures_ids:
            new_structures = list(filter(lambda x: x[id_key] in new_structures_ids, processed_entries))
            self.add_many(new_structures)

        common_structures_ids = list(set(structure_ids) & set(existing_ids))
        common_structures = list(filter(lambda x: x[id_key] in common_structures_ids, processed_entries))

        if common_structures_ids:
            self.change_status_many(ids=common_structures_ids, new_status=StructureStatus.DEPRECATED.value,
                                    id_key=id_key)
            self.add_many(common_structures)

    def update_structure(self, structure_mapping):
        processed_entry = structure_mapping.process()[0]
        id_key = structure_mapping.get_structure_id()
        structure_id = processed_entry[id_key]

        self.change_status_many(ids=[structure_id], new_status=StructureStatus.DEPRECATED.value, id_key=id_key)
        self.add_one(processed_entry)

    def get_additional_info(self, level, structure_id):
        id_key = LEVEL_TO_ID[level]
        query = {
            MongoOperator.AND.value: [{
                id_key: {
                    MongoOperator.EQUALS.value: structure_id
                },
                "status": {MongoOperator.IN.value: [StructureStatus.ENABLED.value, StructureStatus.PAUSED.value]}
            }]
        }

        additional_info = self.get(query)[-1]
        return additional_info

    def get_structure_ids_and_names(self, level: Level = None, account_id: typing.AnyStr = None) -> typing.List[
        typing.Dict]:
        self.set_collection(collection_name=level.value)
        query = {
            MongoOperator.AND.value: [
                {
                    LevelToGoogleIdKeyMapping.get_enum_by_name(Level.ACCOUNT.name).value: {
                        MongoOperator.EQUALS.value: account_id
                    }
                },
                {
                    MiscFieldsEnum.status: {
                        MongoOperator.IN.value: [
                            StructureStatusEnum.ACTIVE.value,
                            StructureStatusEnum.REMOVED.value
                        ]
                    }
                }
            ]
        }
        projection = {
            MongoOperator.GROUP_KEY.value: MongoProjectionState.OFF.value,
            LevelToGoogleIdKeyMapping.get_enum_by_name(level.name).value: MongoProjectionState.ON.value,
            LevelToGoogleNameKeyMapping.get_enum_by_name(level.name).value: MongoProjectionState.ON.value
        }
        structures = self.get(query, projection)
        return structures

    def get_structure_details(self, level: Level = None, key_value: typing.AnyStr = None) -> typing.Dict:
        self.set_collection(collection_name=level.value)
        query, projection = self.__get_structure_details_query(level, key_value)
        structure = self.first_or_default(query, projection)
        if MiscFieldsEnum.details in structure.keys():
            structure[MiscFieldsEnum.details] = BSON.decode(structure[MiscFieldsEnum.details])
        return structure

    @staticmethod
    def __get_structure_details_query(level: Level = None,
                                      key_value: typing.AnyStr = None) -> typing.Tuple[typing.Dict, typing.Dict]:
        query = {
            MongoOperator.AND.value: [
                {
                    LevelToGoogleIdKeyMapping.get_enum_by_name(level.name).value: {
                        MongoOperator.EQUALS.value: key_value
                    }
                },
                {
                    MiscFieldsEnum.status: {
                        MongoOperator.EQUALS.value: StructureStatusEnum.ACTIVE.value
                    }
                }
            ]
        }
        projection = {
            MongoOperator.GROUP_KEY.value: MongoProjectionState.OFF.value
        }
        return query, projection