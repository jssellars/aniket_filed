import typing
from datetime import datetime

from bson import BSON

from Core.Tools.MongoRepository.MongoOperator import MongoOperator
from Core.Tools.MongoRepository.MongoRepositoryBase import MongoRepositoryBase, MongoProjectionState
from FacebookTuring.Infrastructure.Domain.MiscFieldsEnum import MiscFieldsEnum
from FacebookTuring.Infrastructure.Domain.StructureStatusEnum import StructureStatusEnum
from FacebookTuring.Infrastructure.Mappings.LevelMapping import Level, LevelToFacebookIdKeyMapping, \
    LevelToFacebookNameKeyMapping


class TuringMongoRepository(MongoRepositoryBase):

    def __init__(self, *args, **kwargs):
        super(TuringMongoRepository, self).__init__(*args, **kwargs)

    def get_active_structure_ids(self, key_name: typing.AnyStr = None, key_value: typing.AnyStr = None) -> typing.List[typing.Dict]:
        query = {
            MongoOperator.AND.value: [
                {
                    key_name: {
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

        try:
            results = self.collection.find(query, projection)
        except Exception as e:
            raise e
        return list(results)

    def get_structure_ids(self, level: Level = None, account_id: typing.AnyStr = None) -> typing.List[typing.AnyStr]:
        self.set_collection(collection_name=level.value)
        query = {
            MongoOperator.AND.value: [
                {
                    LevelToFacebookIdKeyMapping.get_enum_by_name(Level.ACCOUNT.name).value: {
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
            LevelToFacebookIdKeyMapping.get_enum_by_name(level.name).value: MongoProjectionState.ON.value
        }
        structure_ids = self.get(query, projection)
        return [structure_id.get(LevelToFacebookIdKeyMapping.get_enum_by_name(level.name).value) for structure_id in
                structure_ids]

    def get_structure_ids_and_names(self, level: Level = None, account_id: typing.AnyStr = None) -> typing.List[
        typing.Dict]:
        self.set_collection(collection_name=level.value)
        query = {
            MongoOperator.AND.value: [
                {
                    LevelToFacebookIdKeyMapping.get_enum_by_name(Level.ACCOUNT.name).value: {
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
            LevelToFacebookIdKeyMapping.get_enum_by_name(level.name).value: MongoProjectionState.ON.value,
            LevelToFacebookNameKeyMapping.get_enum_by_name(level.name).value: MongoProjectionState.ON.value
        }
        structures = self.get(query, projection)
        return structures

    def get_id_and_name_by_key(self,
                               level: Level = None,
                               key_value: typing.Any = None,
                               id_key_name: typing.AnyStr = None,
                               name_key_name: typing.AnyStr = None) -> typing.List[typing.Dict]:
        self.set_collection(collection_name=level.value)
        #  only get active data
        query = {
            MongoOperator.AND.value: [
                {
                    LevelToFacebookIdKeyMapping.get_enum_by_name(level.name).value: {
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
            MongoOperator.GROUP_KEY.value: MongoProjectionState.OFF.value,
            id_key_name: MongoProjectionState.ON.value,
            name_key_name: MongoProjectionState.ON.value,
        }
        try:
            results = self.collection.find(query, projection)
        except Exception as e:
            raise e
        return list(results)

    @staticmethod
    def __get_structure_details_query(level: Level = None,
                                      key_value: typing.AnyStr = None) -> typing.Tuple[typing.Dict, typing.Dict]:
        query = {
            MongoOperator.AND.value: [
                {
                    LevelToFacebookIdKeyMapping.get_enum_by_name(level.name).value: {
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

    def get_structure_details(self, level: Level = None, key_value: typing.AnyStr = None) -> typing.Dict:
        self.set_collection(collection_name=level.value)
        query, projection = self.__get_structure_details_query(level, key_value)
        structure = self.first_or_default(query, projection)
        if MiscFieldsEnum.details in structure.keys():
            structure[MiscFieldsEnum.details] = BSON.decode(structure[MiscFieldsEnum.details])
        return structure

    def get_structure_details_many(self,
                                   level: Level = None,
                                   key_value: typing.AnyStr = None) -> typing.List[typing.Dict]:
        self.set_collection(collection_name=level.value)
        query, projection = self.__get_structure_details_query(level, key_value)
        structures = self.get(query, projection)
        return self.__encode_structure_details_to_bson(structures)

    def get_all_structures_by_ad_account_id(self, level: Level = None, account_id: typing.AnyStr = None) -> \
            typing.List[typing.Dict]:
        self.set_collection(collection_name=level.value)
        query = {
            MongoOperator.AND.value: [
                {
                    LevelToFacebookIdKeyMapping.ACCOUNT.value: {
                        MongoOperator.EQUALS.value: account_id
                    }
                },
                {
                    MiscFieldsEnum.status: {
                        MongoOperator.NOTIN.value: [StructureStatusEnum.ARCHIVED.value,
                                                    StructureStatusEnum.REMOVED.value,
                                                    StructureStatusEnum.DEPRECATED.value]
                    }
                }
            ]
        }

        projection = {
            MiscFieldsEnum.details: MongoProjectionState.ON.value,
            MongoOperator.GROUP_KEY.value: MongoProjectionState.OFF.value
        }

        structures = self.get(query, projection)
        structures = self.__encode_structure_details_to_bson(structures)
        return [structure[MiscFieldsEnum.details] for structure in structures]

    @staticmethod
    def __encode_structure_details_to_bson(structures: typing.List[typing.Any] = None) -> typing.List[typing.Any]:
        for index in range(len(structures)):
            structures[index][MiscFieldsEnum.details] = BSON.decode(structures[index].get(MiscFieldsEnum.details, {}))
        return structures

    def change_status(self,
                      level: Level = None,
                      key_value: typing.Any = None,
                      current_status: int = None,
                      new_status: int = None) -> typing.NoReturn:
        self.set_collection(collection_name=level.value)
        if current_status is None:
            current_status = [StructureStatusEnum.ACTIVE.value,
                              StructureStatusEnum.REMOVED.value]
        else:
            current_status = [current_status]
        query_filter = {
            MongoOperator.AND.value: [
                {
                    LevelToFacebookIdKeyMapping.get_enum_by_name(level.name).value: {
                        MongoOperator.EQUALS.value: key_value
                    }
                },
                {
                    MiscFieldsEnum.status: {
                        MongoOperator.IN.value: current_status
                    }
                }
            ]
        }
        query = {
            MongoOperator.SET.value: {
                MiscFieldsEnum.status: new_status,
                MiscFieldsEnum.last_updated_at: datetime.now()
            }
        }
        self.update_one(query_filter, query)

    def change_status_many(self,
                           level: Level = None,
                           key_value: typing.Any = None,
                           current_status: int = None,
                           new_status: int = None) -> typing.NoReturn:
        self.set_collection(collection_name=level.value)
        query_filter = {
            MongoOperator.AND.value: [
                {
                    LevelToFacebookIdKeyMapping.get_enum_by_name(level.name).value: {
                        MongoOperator.IN.value: key_value
                    }
                },
                {
                    MiscFieldsEnum.status: {
                        MongoOperator.EQUALS.value: current_status
                    }
                }
            ]
        }
        query = {
            MongoOperator.SET.value: {
                MiscFieldsEnum.status: new_status,
                MiscFieldsEnum.last_updated_at: datetime.now()
            }
        }
        self.update_many(query_filter, query)

    def add_structure_many(self, account_id: typing.AnyStr = None, level: Level = None,
                           structures: typing.List[typing.Any] = None) -> typing.NoReturn:
        self.set_collection(collection_name=level.value)
        # get existing active or removed structures ids
        existing_structures_ids = self.get_structure_ids(level, account_id)
        existing_structures_ids = set(existing_structures_ids)

        # get structures ids
        structure_ids = [getattr(structure, LevelToFacebookIdKeyMapping.get_enum_by_name(level.name).value) for
                         structure in structures]
        structure_ids = set(structure_ids)

        # change current structures status to remove
        removed_structures_ids = list(existing_structures_ids - structure_ids)
        if removed_structures_ids:
            self.change_status_many(level=level,
                                    key_value=removed_structures_ids,
                                    current_status=StructureStatusEnum.ACTIVE.value,
                                    new_status=StructureStatusEnum.REMOVED.value)

        # add new structures
        new_structures_ids = list(structure_ids - existing_structures_ids)
        new_structures = [structure for structure in structures
                          if getattr(structure, LevelToFacebookIdKeyMapping.get_enum_by_name(level.name).value) in
                          new_structures_ids]

        if new_structures:
            self.add_many(new_structures)

        # update common structures
        common_structures_ids = list(existing_structures_ids.intersection(structure_ids))
        common_structures = [structure for structure in structures
                             if getattr(structure, LevelToFacebookIdKeyMapping.get_enum_by_name(level.name).value)
                             in common_structures_ids]

        if common_structures:
            self.change_status_many(level=level,
                                    key_value=common_structures_ids,
                                    current_status=StructureStatusEnum.ACTIVE.value,
                                    new_status=StructureStatusEnum.DEPRECATED.value)
            self.change_status_many(level=level,
                                    key_value=common_structures_ids,
                                    current_status=StructureStatusEnum.REMOVED.value,
                                    new_status=StructureStatusEnum.DEPRECATED.value)
            self.add_many(common_structures)

    def add_structure(self, level: Level = None, key_value: typing.Any = None,
                      document: typing.Dict = None) -> typing.NoReturn:
        self.set_collection(collection_name=level.value)
        query_filter = {
            MongoOperator.AND.value: [
                {
                    LevelToFacebookIdKeyMapping.get_enum_by_name(level.name).value: {
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
        query = {
            MongoOperator.SET.value: {
                MiscFieldsEnum.status: StructureStatusEnum.DEPRECATED.value,
                MiscFieldsEnum.last_updated_at: datetime.now()
            }
        }
        self.update_many(query_filter, query)
        try:
            self.add_one(self._convert_to_dict(document))
        except Exception as e:
            raise e

    def discard_structure_draft(self, level: Level = None, key_value: typing.AnyStr = None) -> typing.NoReturn:
        self.set_collection(collection_name=level.value)
        query_filter = {
            MongoOperator.AND.value: [
                {
                    LevelToFacebookIdKeyMapping.get_enum_by_name(level.name).value: {
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
        query = {
            MongoOperator.SET.value: {
                MiscFieldsEnum.actions: None,
                MiscFieldsEnum.last_updated_at: datetime.now()
            }
        }
        self.update_one(query_filter, query)

    def save_structure_draft(self,
                             level: Level = None,
                             key_value: typing.AnyStr = None,
                             details: typing.Dict = None) -> typing.NoReturn:
        self.set_collection(collection_name=level.value)
        query_filter = {
            MongoOperator.AND.value: [
                {
                    LevelToFacebookIdKeyMapping.get_enum_by_name(level.name).value: {
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
        query = {
            MongoOperator.SET.value: {
                MiscFieldsEnum.actions: details,
                MiscFieldsEnum.last_updated_at: datetime.now()
            }
        }
        self.update_one(query_filter, query)

    def new_insights_repository(self):
        repository = TuringMongoRepository(config=self.config, database_name=self.config.insights_database_name)
        return repository

    def new_structures_repository(self):
        repository = TuringMongoRepository(config=self.config, database_name=self.config.structures_database_name)
        return repository
