import logging
import sys
import typing
from copy import deepcopy
from datetime import datetime
from typing import List, Dict, AnyStr

from bson import BSON
from pymongo.errors import AutoReconnect
from retry import retry

from Core.Web.FacebookGraphAPI.Models.FieldsMetricStructureMetadata import FieldsMetricStructureMetadata
from Core.constants import DEFAULT_DATETIME_ISO
from Core.mongo_adapter import MongoRepositoryBase, MongoProjectionState, MongoOperator
from Core.Web.FacebookGraphAPI.GraphAPIDomain.GraphAPIInsightsFields import GraphAPIInsightsFields
from Core.Web.FacebookGraphAPI.GraphAPIDomain.FacebookMiscFields import FacebookMiscFields
from FacebookTuring.Infrastructure.Domain.StructureStatusEnum import StructureStatusEnum
from Core.Web.FacebookGraphAPI.GraphAPIMappings.LevelMapping import LevelToFacebookIdKeyMapping, \
    LevelToFacebookNameKeyMapping, Level

logger = logging.getLogger(__name__)


class TuringMongoRepository(MongoRepositoryBase):
    __RETRY_LIMIT = 3

    def __init__(self, *args, **kwargs):
        super(TuringMongoRepository, self).__init__(*args, **kwargs)

    def get_campaigns_by_ad_account(self, account_id: typing.AnyStr = None) -> typing.List[typing.Dict]:
        self.collection = Level.CAMPAIGN.value
        query = {
            MongoOperator.AND.value: [
                {
                    FacebookMiscFields.account_id: {
                        MongoOperator.EQUALS.value: account_id
                    }
                },
                {
                    FacebookMiscFields.status: {
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

    def get_campaigns_by_objectives(self, objectives: typing.List, account_id: typing.AnyStr = None) -> typing.List[typing.Dict]:
        self.collection = Level.CAMPAIGN.value
        query = {
            MongoOperator.AND.value: [
                {
                    FacebookMiscFields.account_id: {
                        MongoOperator.EQUALS.value: account_id
                    }
                },
                {
                    FieldsMetricStructureMetadata.objective.name: {
                        MongoOperator.IN.value: objectives
                    }
                },
                {
                    FacebookMiscFields.status: {
                        MongoOperator.IN.value: [StructureStatusEnum.ACTIVE.value,
                                                 StructureStatusEnum.PAUSED.value]
                    }
                }
            ]
        }
        projection = {
            MongoOperator.GROUP_KEY.value: MongoProjectionState.OFF.value,
            FieldsMetricStructureMetadata.campaign_id.name: MongoProjectionState.ON.value
        }
        try:
            campaigns = self.get(query, projection)
        except Exception as e:
            raise e

        return self.__decode_structure_details_from_bson(campaigns)

    def get_adsets_by_campaign_id(self, campaign_ids: typing.List[typing.AnyStr] = None) -> typing.List[typing.Dict]:
        self.collection = Level.ADSET.value
        query = {
            MongoOperator.AND.value: [
                {
                    LevelToFacebookIdKeyMapping.CAMPAIGN.value: {
                        MongoOperator.IN.value: campaign_ids
                    }
                },
                {
                    FacebookMiscFields.status: {
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

    @retry(AutoReconnect, tries=__RETRY_LIMIT, delay=1)
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
                    FacebookMiscFields.status: {
                        MongoOperator.EQUALS.value: StructureStatusEnum.ACTIVE.value
                    }
                }
            ]
        }

        projection = {
            MongoOperator.GROUP_KEY.value: MongoProjectionState.OFF.value
        }

        start = datetime.now()
        try:
            results = self.collection.find(query, projection)
            results = list(results)
        except Exception as e:
            logger.error(
                f"Failed to get active structures ids || {repr(e)}",
                extra=dict(duration=(datetime.now() - start).total_seconds(), query=query, projection=projection),
            )
            raise e

        logger.debug(
            "Get active structures ids",
            extra=dict(
                data_size=sys.getsizeof(results),
                duration=(datetime.now() - start).total_seconds(),
                query=query,
                projection=projection),
        )

        return results

    @retry(AutoReconnect, tries=__RETRY_LIMIT, delay=1)
    def get_bo_structures_by_ids(self, business_owner_id: AnyStr, structure_id_key: AnyStr,
                                 structure_ids: List[AnyStr]) -> List[Dict]:
        query = {
            MongoOperator.AND.value: [
                {
                    structure_id_key: {
                        MongoOperator.IN.value: structure_ids
                    }
                },
                {
                    FacebookMiscFields.status: {
                        MongoOperator.IN.value: [StructureStatusEnum.ACTIVE.value,
                                                 StructureStatusEnum.PAUSED.value]
                    }
                },
                {
                    "business_owner_facebook_id": business_owner_id
                }
            ]
        }

        projection = {
            MongoOperator.GROUP_KEY.value: MongoProjectionState.OFF.value
        }

        try:
            structures = list(self.collection.find(query, projection))
            for structure in structures:
                if FacebookMiscFields.details in structure:
                    structure[FacebookMiscFields.details] = BSON.decode(structure[FacebookMiscFields.details])
        except Exception as e:
            logger.error(f"Failed to get active structures ids || {repr(e)}")
            raise e

        return structures

    @retry(AutoReconnect, tries=__RETRY_LIMIT, delay=1)
    def get_bo_structures_by_id(self, business_owner_id: AnyStr, structure_id_key: AnyStr,
                                structure_id: AnyStr) -> List[Dict]:
        query = {
            MongoOperator.AND.value: [
                {
                    structure_id_key: structure_id
                },
                {
                    FacebookMiscFields.status: {
                        MongoOperator.IN.value: [StructureStatusEnum.ACTIVE.value,
                                                 StructureStatusEnum.PAUSED.value]
                    }
                },
                {
                    "business_owner_facebook_id": business_owner_id
                }
            ]
        }

        projection = {
            MongoOperator.GROUP_KEY.value: MongoProjectionState.OFF.value
        }

        try:
            structures = list(self.collection.find(query, projection))
            for structure in structures:
                if FacebookMiscFields.details in structure:
                    structure[FacebookMiscFields.details] = BSON.decode(structure[FacebookMiscFields.details])
        except Exception as e:
            logger.error(f"Failed to get active structures ids || {repr(e)}")
            raise e

        return structures

    def get_bo_unique_campaign_ids(self, business_owner_id: AnyStr, structure_id_key: AnyStr,
                                   structure_ids: List[AnyStr]):
        query = {
            MongoOperator.AND.value: [
                {
                    structure_id_key: {
                        MongoOperator.IN.value: structure_ids
                    }
                },
                {
                    FacebookMiscFields.status: {
                        MongoOperator.IN.value: [StructureStatusEnum.ACTIVE.value,
                                                 StructureStatusEnum.PAUSED.value]
                    }
                },
                {
                    "business_owner_facebook_id": business_owner_id
                }
            ]
        }

        try:
            campaign_ids = list(self.collection.distinct("campaign_id", query))
        except Exception as e:
            logger.error(f"Failed to get active structures ids || {repr(e)}")
            raise e

        return campaign_ids

    def get_structure_ids(self, level: Level = None, account_id: typing.AnyStr = None) -> typing.List[typing.AnyStr]:
        self.collection = level.value
        query = {
            MongoOperator.AND.value: [
                {
                    LevelToFacebookIdKeyMapping.get_enum_by_name(Level.ACCOUNT.name).value: {
                        MongoOperator.EQUALS.value: account_id
                    }
                },
                {
                    FacebookMiscFields.status: {
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

    def get_structure_info(self,
                           level: Level = None,
                           account_id: typing.AnyStr = None,
                           campaign_ids: typing.List[typing.AnyStr] = None,
                           adset_ids: typing.List[typing.AnyStr] = None,
                           statuses: typing.List[int] = None) -> typing.List[typing.Dict]:
        self.collection = level.value

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
            FacebookMiscFields.status: {
                MongoOperator.IN.value: statuses
            }
        }
        query[MongoOperator.AND.value].append(deepcopy(query_by_status))

        projection = {
            MongoOperator.GROUP_KEY.value: MongoProjectionState.OFF.value,
            LevelToFacebookIdKeyMapping.CAMPAIGN.value: MongoProjectionState.ON.value,
            LevelToFacebookIdKeyMapping.ADSET.value: MongoProjectionState.ON.value,
            LevelToFacebookIdKeyMapping.AD.value: MongoProjectionState.ON.value,
            LevelToFacebookNameKeyMapping.CAMPAIGN.value: MongoProjectionState.ON.value,
            LevelToFacebookNameKeyMapping.ADSET.value: MongoProjectionState.ON.value,
            LevelToFacebookNameKeyMapping.AD.value: MongoProjectionState.ON.value,
            FacebookMiscFields.status: MongoProjectionState.ON.value
        }
        structures = self.get(query, projection)
        return structures

    def get_structure_ids_and_names(self,
                                    level: Level = None,
                                    account_id: typing.AnyStr = None,
                                    campaign_ids: typing.List[typing.AnyStr] = None,
                                    adset_ids: typing.List[typing.AnyStr] = None,
                                    statuses: typing.List[int] = None) -> typing.List[typing.Dict]:
        self.collection = level.value

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
            FacebookMiscFields.status: {
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

    @retry(AutoReconnect, tries=__RETRY_LIMIT, delay=1)
    def get_id_and_name_by_key(self,
                               level: Level = None,
                               key_value: typing.Any = None,
                               id_key_name: typing.AnyStr = None,
                               name_key_name: typing.AnyStr = None) -> typing.List[typing.Dict]:
        self.collection = level.value
        # only get active data
        query = {
            MongoOperator.AND.value: [
                {
                    LevelToFacebookIdKeyMapping.get_enum_by_name(level.name).value: {
                        MongoOperator.EQUALS.value: key_value
                    }
                },
                {
                    FacebookMiscFields.status: {
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

        start = datetime.now()
        try:
            results = self.collection.find(query, projection)
            results = list(results)
        except Exception as e:
            logger.error(
                f"Failed to get structures by id and name || {repr(e)}",
                extra=dict(duration=(datetime.now() - start).total_seconds(), query=query, projection=projection),
            )
            raise e

        logger.debug(
            "Get structures by id and name",
            extra=dict(
                data_size=sys.getsizeof(results),
                duration=(datetime.now() - start).total_seconds(),
                query=query,
                projection=projection,
            ),
        )

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
                    FacebookMiscFields.status: {
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
        self.collection = level.value
        query, projection = self.__get_structure_details_query(level, key_value)
        structure = self.first_or_default(query, projection)
        if FacebookMiscFields.details in structure.keys():
            structure[FacebookMiscFields.details] = BSON.decode(structure[FacebookMiscFields.details])
        return structure

    def get_structure_details_many(self,
                                   level: Level = None,
                                   key_value: typing.AnyStr = None) -> typing.List[typing.Dict]:
        self.collection = level.value
        query, projection = self.__get_structure_details_query(level, key_value)
        structures = self.get(query, projection)
        return self.__decode_structure_details_from_bson(structures)

    def get_all_structures_by_ad_account_id(self, level: Level = None, account_id: typing.AnyStr = None) -> \
            typing.List[typing.Dict]:
        self.collection = level.value
        query = {
            MongoOperator.AND.value: [
                {
                    LevelToFacebookIdKeyMapping.ACCOUNT.value: {
                        MongoOperator.EQUALS.value: account_id
                    }
                },
                {
                    FacebookMiscFields.status: {
                        MongoOperator.NOTIN.value: [StructureStatusEnum.ARCHIVED.value,
                                                    StructureStatusEnum.REMOVED.value,
                                                    StructureStatusEnum.DEPRECATED.value]
                    }
                }
            ]
        }

        projection = {
            FacebookMiscFields.details: MongoProjectionState.ON.value,
            MongoOperator.GROUP_KEY.value: MongoProjectionState.OFF.value
        }

        structures = self.get(query, projection)
        structures = self.__decode_structure_details_from_bson(structures)
        return [structure[FacebookMiscFields.details] for structure in structures]

    def get_ad_account_slice(self,
                             level: Level = None,
                             account_id: typing.AnyStr = None,
                             structure_key: typing.AnyStr = None,
                             structure_ids: typing.List[typing.AnyStr] = None,
                             start_row: int = 0,
                             end_row: int = 0
                             ) -> typing.List[typing.Dict]:
        self.collection = level.value
        query = {
            MongoOperator.AND.value: [
                {
                    LevelToFacebookIdKeyMapping.ACCOUNT.value: {
                        MongoOperator.EQUALS.value: account_id
                    }
                },
                {
                    FacebookMiscFields.status: {
                        MongoOperator.NOTIN.value: [StructureStatusEnum.ARCHIVED.value,
                                                    StructureStatusEnum.REMOVED.value,
                                                    StructureStatusEnum.DEPRECATED.value]
                    }
                }
            ]
        }
        if structure_ids:
            query_filter = {
                structure_key: {
                    MongoOperator.IN.value: structure_ids
                }
            }
            query[MongoOperator.AND.value].append(query_filter)

        projection = {
            FacebookMiscFields.details: MongoProjectionState.ON.value,
            MongoOperator.GROUP_KEY.value: MongoProjectionState.OFF.value
        }

        sort_query = [("created_time", -1)]

        structures = self.get_data_slice(query=query, projection=projection, limit=end_row, skip=start_row, sort_query=sort_query)
        structures = self.__decode_structure_details_from_bson(structures)
        return [structure[FacebookMiscFields.details] for structure in structures]

    def get_results_fields_from_adsets(self,
                                       structure_ids: typing.List[typing.AnyStr] = None,
                                       structure_key: typing.AnyStr = None) -> \
            typing.List[typing.Dict]:
        self.collection = Level.ADSET.value
        query = {
            MongoOperator.AND.value: [
                {
                    structure_key: {
                        MongoOperator.IN.value: structure_ids
                    }
                },
                {
                    FacebookMiscFields.status: {
                        MongoOperator.NOTIN.value: [StructureStatusEnum.ARCHIVED.value,
                                                    StructureStatusEnum.REMOVED.value,
                                                    StructureStatusEnum.DEPRECATED.value]
                    }
                }
            ]
        }

        projection = {
            GraphAPIInsightsFields.custom_event_type: MongoProjectionState.ON.value,
            GraphAPIInsightsFields.optimization_goal: MongoProjectionState.ON.value,
            structure_key: MongoProjectionState.ON.value,
            MongoOperator.GROUP_KEY.value: MongoProjectionState.OFF.value
        }

        structures = self.get(query, projection)
        return structures

    def get_all_structures_by_id_list(self,
                                      level: Level = None,
                                      structure_ids: typing.List[typing.AnyStr] = None,
                                      structure_key: typing.AnyStr = None) -> \
            typing.List[typing.Dict]:
        self.collection = level.value
        query = {
            MongoOperator.AND.value: [
                {
                    structure_key: {
                        MongoOperator.IN.value: structure_ids
                    }
                },
                {
                    FacebookMiscFields.status: {
                        MongoOperator.NOTIN.value: [StructureStatusEnum.ARCHIVED.value,
                                                    StructureStatusEnum.DEPRECATED.value]
                    }
                }
            ]
        }

        projection = {
            FacebookMiscFields.details: MongoProjectionState.ON.value,
            MongoOperator.GROUP_KEY.value: MongoProjectionState.OFF.value
        }

        structures = self.get(query, projection)
        structures = self.__decode_structure_details_from_bson(structures)
        return [structure[FacebookMiscFields.details] for structure in structures if FacebookMiscFields.details in structure]

    def get_structures_by_parent_id(self, level: Level, parent_id) -> List[Dict]:

        child_results = []
        if level == Level.CAMPAIGN:
            child_results = self.get_children_from_parent_key(
                LevelToFacebookIdKeyMapping.CAMPAIGN.value, parent_id, Level.ADSET
            )
            child_results += self.get_children_from_parent_key(
                LevelToFacebookIdKeyMapping.CAMPAIGN.value, parent_id, Level.AD
            )
        elif level == Level.ADSET:
            child_results = self.get_children_from_parent_key(
                LevelToFacebookIdKeyMapping.ADSET.value, parent_id, Level.AD
            )

        return child_results

    def get_children_from_parent_key(self, parent_key: str, parent_id: str, level: Level) -> List[Dict]:
        self.collection = level.value
        query = {
            MongoOperator.AND.value: [
                {parent_key: {MongoOperator.EQUALS.value: parent_id}},
                {
                    FacebookMiscFields.status: {
                        MongoOperator.NOTIN.value: [
                            StructureStatusEnum.ARCHIVED.value,
                            StructureStatusEnum.DEPRECATED.value,
                            StructureStatusEnum.REMOVED.value,
                        ]
                    }
                },
            ]
        }

        projection = {
            "_id": MongoProjectionState.OFF.value,
        }

        result = self.get(query, projection)
        for entry in result:
            entry.update(
                {
                    FacebookMiscFields.level: level.value,
                    FacebookMiscFields.structure_id: entry[LevelToFacebookIdKeyMapping[level.name].value],
                    FacebookMiscFields.details: BSON.decode(entry[FacebookMiscFields.details])
                }
            )

        return result

    @staticmethod
    def __decode_structure_details_from_bson(structures: typing.List[typing.Any] = None) -> typing.List[typing.Any]:
        for index in range(len(structures)):
            encoded_structure = structures[index].get(FacebookMiscFields.details, {})
            if encoded_structure:
                structures[index][FacebookMiscFields.details] = BSON.decode(encoded_structure)
            else:
                structures[index][FacebookMiscFields.details] = {}
        return structures

    # TODO: This function can be removed once the delete functionality is properly working
    def change_status(self,
                      level: Level = None,
                      key_value: typing.Any = None,
                      current_status: int = None,
                      new_status: int = None) -> typing.NoReturn:
        self.collection = level.value
        if current_status is None:
            current_status = [StructureStatusEnum.ACTIVE.value,
                              StructureStatusEnum.REMOVED.value,
                              StructureStatusEnum.PAUSED.value]
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
                    FacebookMiscFields.status: {
                        MongoOperator.IN.value: current_status
                    }
                }
            ]
        }
        query = {
            MongoOperator.SET.value: {
                FacebookMiscFields.status: new_status,
                FacebookMiscFields.last_updated_at: datetime.now()
            }
        }
        self.update_one(query_filter, query)

    def change_status_many(self,
                           level: Level = None,
                           key_value: typing.Any = None,
                           current_status: int = None,
                           new_status: int = None) -> typing.NoReturn:
        self.collection = level.value
        query_filter = {
            MongoOperator.AND.value: [
                {
                    LevelToFacebookIdKeyMapping.get_enum_by_name(level.name).value: {
                        MongoOperator.IN.value: key_value
                    }
                },
                {
                    FacebookMiscFields.status: {
                        MongoOperator.EQUALS.value: current_status
                    }
                }
            ]
        }
        query = {
            MongoOperator.SET.value: {
                FacebookMiscFields.status: new_status,
                FacebookMiscFields.last_updated_at: datetime.now()
            }
        }
        self.update_many(query_filter, query)

    def __get_structure_id(self, structure: typing.Any = None, level: Level = None) -> typing.AnyStr:
        if isinstance(structure, dict):
            return structure.get(LevelToFacebookIdKeyMapping.get_enum_by_name(level.name).value)
        else:
            return getattr(structure, LevelToFacebookIdKeyMapping.get_enum_by_name(level.name).value)

    def add_updated_structures(self, level, account_id: str, structures: List[Dict]) -> None:
        self.collection = level.value
        self.delete_many({FacebookMiscFields.account_id: account_id})
        self.add_many(structures)

    def add_structure(self, level: Level = None, key_value: typing.Any = None,
                      document: typing.Dict = None) -> typing.NoReturn:
        self.collection = level.value
        query_filter = {
            MongoOperator.AND.value: [
                {
                    LevelToFacebookIdKeyMapping.get_enum_by_name(level.name).value: {
                        MongoOperator.EQUALS.value: key_value
                    }
                },
                {
                    FacebookMiscFields.status: {
                        MongoOperator.IN.value: [
                            StructureStatusEnum.ACTIVE.value,
                            StructureStatusEnum.PAUSED.value,
                            StructureStatusEnum.REMOVED.value,
                        ]
                    }
                }
            ]

        }
        self.delete_many(query_filter)
        try:
            self.add_one(self._convert_to_dict(document))
        except Exception as e:
            raise e

    def get_latest_by_account_id(self,
                                 collection: typing.AnyStr = None,
                                 start_date: typing.Union[datetime, typing.AnyStr] = None,
                                 account_id: typing.AnyStr = None) -> typing.List[typing.Dict]:
        self.database = self.config.structures_database_name
        self.collection = collection
        query = {
            MongoOperator.AND.value: [
                {
                    FacebookMiscFields.account_id: {
                        MongoOperator.EQUALS.value: account_id
                    }
                },
                {
                    FacebookMiscFields.date_added: {
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
        return TuringMongoRepository(config=self.config, database_name=self.config.insights_database_name)

    def new_structures_repository(self):
        return TuringMongoRepository(config=self.config, database_name=self.config.structures_database_name)
