import typing
from copy import deepcopy
from datetime import datetime

from bson import BSON

from Core.Tools.Logger.Helpers import log_operation_mongo
from Core.Tools.Logger.LoggerMessageBase import LoggerMessageTypeEnum
from Core.Tools.Logger.LoggingLevelEnum import LoggingLevelEnum
from Core.Tools.Misc.Constants import DEFAULT_DATETIME_ISO
from Core.Tools.MongoRepository.MongoOperator import MongoOperator
from Core.Tools.MongoRepository.MongoRepositoryBase import MongoRepositoryBase, MongoProjectionState
from FacebookTuring.Infrastructure.Domain.MiscFieldsEnum import MiscFieldsEnum
from FacebookTuring.Infrastructure.Domain.StructureStatusEnum import StructureStatusEnum
from FacebookTuring.Infrastructure.Mappings.LevelMapping import Level, LevelToFacebookIdKeyMapping, \
    LevelToFacebookNameKeyMapping


class TuringMongoRepository(MongoRepositoryBase):

    def __init__(self, *args, **kwargs):
        super(TuringMongoRepository, self).__init__(*args, **kwargs)

    def get_campaigns_by_ad_account(self, account_id: typing.AnyStr = None) -> typing.List[typing.Dict]:
        self.set_collection(Level.CAMPAIGN.value)
        query = {
            MongoOperator.AND.value: [
                {
                    MiscFieldsEnum.account_id: {
                        MongoOperator.EQUALS.value: account_id
                    }
                },
                {
                    MiscFieldsEnum.status: {
                        MongoOperator.IN.value: [StructureStatusEnum.ACTIVE.value,
                                                 StructureStatusEnum.PAUSED.value]
                    }
                }
            ]
        }
        projection = {
            MongoOperator.GROUP_KEY.value: MongoProjectionState.OFF.value
        }
        try:
            campaigns = self.get(query, projection)
        except Exception as e:
            raise e

        return self.__decode_structure_details_from_bson(campaigns)

    def get_adsets_by_campaign_id(self, campaign_ids: typing.List[typing.AnyStr] = None) -> typing.List[typing.Dict]:
        self.set_collection(Level.ADSET.value)
        query = {
            MongoOperator.AND.value: [
                {
                    LevelToFacebookIdKeyMapping.CAMPAIGN.value: {
                        MongoOperator.IN.value: campaign_ids
                    }
                },
                {
                    MiscFieldsEnum.status: {
                        MongoOperator.IN.value: [StructureStatusEnum.ACTIVE.value,
                                                 StructureStatusEnum.PAUSED.value]
                    }
                }
            ]
        }
        projection = {
            MongoOperator.GROUP_KEY.value: MongoProjectionState.OFF.value
        }

        try:
            adsets = self.get(query, projection)
        except Exception as e:
            raise e

        return self.__decode_structure_details_from_bson(adsets)

    def get_active_structure_ids(self, key_name: typing.AnyStr = None, key_value: typing.AnyStr = None) -> typing.List[
        typing.Dict]:
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

        operation_start_time = datetime.now()
        try:
            results = self.collection.find(query, projection)
            results = list(results)
        except Exception as e:
            operation_end_time = datetime.now()
            duration = (operation_end_time - operation_start_time).total_seconds()
            log_operation_mongo(logger=self._logger,
                                log_level=LoggerMessageTypeEnum.ERROR,
                                description="Failed to get active structures ids. Reason %s" % str(e),
                                timestamp=operation_end_time,
                                duration=duration,
                                query=query,
                                projection=projection)
            raise e

        if self._logger.level == LoggingLevelEnum.DEBUG.value:
            operation_end_time = datetime.now()
            duration = (operation_end_time - operation_start_time).total_seconds()
            log_operation_mongo(logger=self._logger,
                                log_level=LoggerMessageTypeEnum.EXEC_DETAILS,
                                data=results,
                                description="Get active structures ids",
                                timestamp=operation_end_time,
                                duration=duration,
                                query=query,
                                projection=projection)

        return results

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

    def get_structure_ids_and_names(self,
                                    level: Level = None,
                                    account_id: typing.AnyStr = None,
                                    campaign_ids: typing.List[typing.AnyStr] = None,
                                    adset_ids: typing.List[typing.AnyStr] = None,
                                    statuses: typing.List[int] = None) -> typing.List[typing.Dict]:
        self.set_collection(collection_name=level.value)

        query = {
            MongoOperator.AND.value: [
                {
                    LevelToFacebookIdKeyMapping.get_enum_by_name(Level.ACCOUNT.name).value: {
                        MongoOperator.EQUALS.value: account_id
                    }
                }
            ]
        }
        if campaign_ids:
            query_by_campaign_ids = {
                LevelToFacebookIdKeyMapping.get_enum_by_name(Level.CAMPAIGN.name).value: {
                    MongoOperator.IN.value: campaign_ids
                }
            }
            query[MongoOperator.AND.value].append(deepcopy(query_by_campaign_ids))

        if adset_ids:
            query_by_adset_ids = {
                LevelToFacebookIdKeyMapping.get_enum_by_name(Level.ADSET.name).value: {
                    MongoOperator.IN.value: adset_ids
                }
            }
            query[MongoOperator.AND.value].append(deepcopy(query_by_adset_ids))

        if statuses is None:
            statuses = [StructureStatusEnum.ACTIVE.value, StructureStatusEnum.PAUSED.value]

        query_by_status = {
            MiscFieldsEnum.status: {
                MongoOperator.IN.value: statuses
            }
        }
        query[MongoOperator.AND.value].append(deepcopy(query_by_status))

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

        operation_start_time = datetime.now()
        try:
            results = self.collection.find(query, projection)
            results = list(results)
        except Exception as e:
            operation_end_time = datetime.now()
            duration = (operation_end_time - operation_start_time).total_seconds()
            log_operation_mongo(logger=self._logger,
                                log_level=LoggerMessageTypeEnum.ERROR,
                                description="Failed to get structures by id and name. Reason %s" % str(e),
                                timestamp=operation_end_time,
                                duration=duration,
                                query=query,
                                projection=projection)
            raise e

        if self._logger.level == LoggingLevelEnum.DEBUG.value:
            operation_end_time = datetime.now()
            duration = (operation_end_time - operation_start_time).total_seconds()
            log_operation_mongo(logger=self._logger,
                                log_level=LoggerMessageTypeEnum.EXEC_DETAILS,
                                data=results,
                                description="Get structures by id and name",
                                timestamp=operation_end_time,
                                duration=duration,
                                query=query,
                                projection=projection)

        return results

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
                        MongoOperator.IN.value: [StructureStatusEnum.ACTIVE.value,
                                                 StructureStatusEnum.PAUSED.value,
                                                 StructureStatusEnum.COMPLETED.value]
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
        return self.__decode_structure_details_from_bson(structures)

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
        structures = self.__decode_structure_details_from_bson(structures)
        return [structure[MiscFieldsEnum.details] for structure in structures]

    @staticmethod
    def __decode_structure_details_from_bson(structures: typing.List[typing.Any] = None) -> typing.List[typing.Any]:
        for index in range(len(structures)):
            encoded_structure = structures[index].get(MiscFieldsEnum.details, {})
            if encoded_structure:
                structures[index][MiscFieldsEnum.details] = BSON.decode(encoded_structure)
            else:
                structures[index][MiscFieldsEnum.details] = {}
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

    def __get_structure_id(self, structure: typing.Any = None, level: Level = None) -> typing.AnyStr:
        if isinstance(structure, dict):
            return structure.get(LevelToFacebookIdKeyMapping.get_enum_by_name(level.name).value)
        else:
            return getattr(structure, LevelToFacebookIdKeyMapping.get_enum_by_name(level.name).value)

    def add_structures_many_with_deprecation(self,
                                             level: Level = None,
                                             structures: typing.List[typing.Any] = None) -> typing.NoReturn:
        self.set_collection(collection_name=level.value)
        for structure in structures:
            structure_id = self.__get_structure_id(structure, level)
            if isinstance(structure, dict):
                current_structure_details = structure.get(MiscFieldsEnum.details)
            else:
                current_structure_details = BSON.decode(structure.details)
            existing_structure_details = self.get_structure_details(level=level, key_value=structure_id)
            if existing_structure_details and \
                    current_structure_details != existing_structure_details.get(MiscFieldsEnum.details):
                self.deprecate_structure(level=level, key_value=structure_id)
                if isinstance(structure, dict):
                    structure[MiscFieldsEnum.date_added] = datetime.now().strftime(DEFAULT_DATETIME_ISO)
                else:
                    structure.date_added = datetime.now().strftime(DEFAULT_DATETIME_ISO)
                self.add_one(structure)
            elif not existing_structure_details:
                if isinstance(structure, dict):
                    structure[MiscFieldsEnum.date_added] = datetime.now().strftime(DEFAULT_DATETIME_ISO)
                else:
                    structure.date_added = datetime.now().strftime(DEFAULT_DATETIME_ISO)
                self.add_one(structure)

    def deprecate_structure(self, level: Level = None, key_value: typing.AnyStr = None) -> typing.NoReturn:
        self.set_collection(collection_name=level.value)
        query_filter = {
            LevelToFacebookIdKeyMapping.get_enum_by_name(level.name).value: {
                MongoOperator.EQUALS.value: key_value
            }
        }
        query = {
            MongoOperator.SET.value: {
                MiscFieldsEnum.status: StructureStatusEnum.DEPRECATED.value
            }
        }
        self.update_many(query_filter=query_filter, query=query)

    def deprecate_structures_by_account_id(self,
                                           account_id: typing.AnyStr = None,
                                           level: Level = None) -> typing.NoReturn:
        self.set_collection(collection_name=level.value)
        query_filter = {
            MiscFieldsEnum.account_id: {
                MongoOperator.EQUALS.value: account_id
            }
        }
        query = {
            MongoOperator.SET.value: {
                MiscFieldsEnum.status: StructureStatusEnum.DEPRECATED.value
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
        structure_ids = [self.__get_structure_id(structure, level) for structure in structures]
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
                          if self.__get_structure_id(structure, level) in new_structures_ids]

        if new_structures:
            self.add_many(new_structures)

        # update common structures
        common_structures_ids = list(existing_structures_ids.intersection(structure_ids))
        common_structures = [structure for structure in structures
                             if self.__get_structure_id(structure, level) in common_structures_ids]

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

    def get_latest_by_account_id(self,
                                 collection: typing.AnyStr = None,
                                 start_date: typing.Union[datetime, typing.AnyStr] = None,
                                 account_id: typing.AnyStr = None) -> typing.List[typing.Dict]:
        self.set_database(self.config.structures_database_name)
        self.set_collection(collection)
        query = {
            MongoOperator.AND.value: [
                {
                    MiscFieldsEnum.account_id: {
                        MongoOperator.EQUALS.value: account_id
                    }
                },
                {
                    MiscFieldsEnum.date_added: {
                        MongoOperator.GREATERTHANEQUAL.value: start_date
                    }
                }
            ]
        }
        projection = {
            MongoOperator.GROUP_KEY.value: MongoProjectionState.ON.value
        }
        results = self.get(query=query, projection=projection)
        return results

    def new_insights_repository(self):
        repository = TuringMongoRepository(config=self.config, database_name=self.config.insights_database_name,
                                           logger=self._logger)
        return repository

    def new_structures_repository(self):
        repository = TuringMongoRepository(config=self.config, database_name=self.config.structures_database_name,
                                           logger=self._logger)
        return repository
