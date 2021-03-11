import logging
import sys
import typing
from copy import deepcopy
from datetime import datetime
from typing import Dict, List, Tuple

from bson import BSON
from pymongo.errors import AutoReconnect
from retry import retry

from Core.mongo_adapter import MongoOperator, MongoProjectionState, MongoRepositoryBase
from Core.Web.FacebookGraphAPI.GraphAPIDomain.FacebookMiscFields import FacebookMiscFields
from Core.Web.FacebookGraphAPI.GraphAPIDomain.StructureStatusEnum import StructureStatusEnum
from Core.Web.FacebookGraphAPI.GraphAPIMappings.LevelMapping import (
    Level,
    LevelToFacebookIdKeyMapping,
    LevelToFacebookNameKeyMapping,
)
from Core.Web.FacebookGraphAPI.Models.FieldsMetricStructureMetadata import FieldsMetricStructureMetadata

logger = logging.getLogger(__name__)


class TuringMongoRepository(MongoRepositoryBase):
    __RETRY_LIMIT = 3

    def __init__(self, *args, **kwargs):
        super(TuringMongoRepository, self).__init__(*args, **kwargs)

    def get_campaigns_by_ad_account(self, account_id: str = None) -> typing.List[typing.Dict]:
        self.collection = Level.CAMPAIGN.value
        query = {
            MongoOperator.AND.value: [
                {FacebookMiscFields.account_id: {MongoOperator.EQUALS.value: account_id}},
                {
                    FacebookMiscFields.status: {
                        MongoOperator.IN.value: [StructureStatusEnum.ACTIVE.value, StructureStatusEnum.PAUSED.value]
                    }
                },
            ]
        }
        projection = {MongoOperator.GROUP_KEY.value: MongoProjectionState.OFF.value}
        try:
            campaigns = self.get(query, projection)
        except Exception as e:
            raise e

        return self.__decode_structure_details_from_bson(campaigns)

    def get_campaigns_by_objectives(self, objectives: typing.List, account_id: str = None) -> typing.List[typing.Dict]:
        self.collection = Level.CAMPAIGN.value
        query = {
            MongoOperator.AND.value: [
                {FacebookMiscFields.account_id: {MongoOperator.EQUALS.value: account_id}},
                {FieldsMetricStructureMetadata.objective.name: {MongoOperator.IN.value: objectives}},
                {
                    FacebookMiscFields.status: {
                        MongoOperator.IN.value: [StructureStatusEnum.ACTIVE.value, StructureStatusEnum.PAUSED.value]
                    }
                },
            ]
        }
        projection = {
            MongoOperator.GROUP_KEY.value: MongoProjectionState.OFF.value,
            FieldsMetricStructureMetadata.campaign_id.name: MongoProjectionState.ON.value,
        }
        try:
            campaigns = self.get(query, projection)
        except Exception as e:
            raise e

        return self.__decode_structure_details_from_bson(campaigns)

    def get_adsets_by_campaign_id(self, campaign_ids: typing.List[str] = None) -> typing.List[typing.Dict]:
        self.collection = Level.ADSET.value
        query = {
            MongoOperator.AND.value: [
                {LevelToFacebookIdKeyMapping.CAMPAIGN.value: {MongoOperator.IN.value: campaign_ids}},
                {
                    FacebookMiscFields.status: {
                        MongoOperator.IN.value: [StructureStatusEnum.ACTIVE.value, StructureStatusEnum.PAUSED.value]
                    }
                },
            ]
        }
        projection = {MongoOperator.GROUP_KEY.value: MongoProjectionState.OFF.value}

        try:
            adsets = self.get(query, projection)
        except Exception as e:
            raise e

        return self.__decode_structure_details_from_bson(adsets)

    @retry(AutoReconnect, tries=__RETRY_LIMIT, delay=1)
    def get_active_structure_ids(self, key_name: str = None, key_value: str = None) -> typing.List[typing.Dict]:
        query = {
            MongoOperator.AND.value: [
                {key_name: {MongoOperator.EQUALS.value: key_value}},
                {FacebookMiscFields.status: {MongoOperator.EQUALS.value: StructureStatusEnum.ACTIVE.value}},
            ]
        }

        projection = {MongoOperator.GROUP_KEY.value: MongoProjectionState.OFF.value}

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
                projection=projection,
            ),
        )

        return results

    def get_structure_info(
        self,
        level: Level = None,
        account_id: str = None,
        campaign_ids: typing.List[str] = None,
        adset_ids: typing.List[str] = None,
        statuses: typing.List[int] = None,
    ) -> typing.List[typing.Dict]:
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

        query_by_status = {FacebookMiscFields.status: {MongoOperator.IN.value: statuses}}
        query[MongoOperator.AND.value].append(deepcopy(query_by_status))

        projection = {
            MongoOperator.GROUP_KEY.value: MongoProjectionState.OFF.value,
            LevelToFacebookIdKeyMapping.CAMPAIGN.value: MongoProjectionState.ON.value,
            LevelToFacebookIdKeyMapping.ADSET.value: MongoProjectionState.ON.value,
            LevelToFacebookIdKeyMapping.AD.value: MongoProjectionState.ON.value,
            LevelToFacebookNameKeyMapping.CAMPAIGN.value: MongoProjectionState.ON.value,
            LevelToFacebookNameKeyMapping.ADSET.value: MongoProjectionState.ON.value,
            LevelToFacebookNameKeyMapping.AD.value: MongoProjectionState.ON.value,
            FacebookMiscFields.status: MongoProjectionState.ON.value,
        }
        structures = self.get(query, projection)
        return structures

    def get_structure_ids_and_names(
        self,
        level: Level = None,
        account_id: str = None,
        campaign_ids: typing.List[str] = None,
        adset_ids: typing.List[str] = None,
        statuses: typing.List[int] = None,
    ) -> typing.List[typing.Dict]:
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

        query_by_status = {FacebookMiscFields.status: {MongoOperator.IN.value: statuses}}
        query[MongoOperator.AND.value].append(deepcopy(query_by_status))

        projection = {
            MongoOperator.GROUP_KEY.value: MongoProjectionState.OFF.value,
            LevelToFacebookIdKeyMapping.get_enum_by_name(level.name).value: MongoProjectionState.ON.value,
            LevelToFacebookNameKeyMapping.get_enum_by_name(level.name).value: MongoProjectionState.ON.value,
        }
        structures = self.get(query, projection)
        return structures

    @staticmethod
    def __get_structure_details_query(level: Level = None, key_value: str = None) -> Tuple[Dict, Dict]:
        query = {
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
                            StructureStatusEnum.COMPLETED.value,
                        ]
                    }
                },
            ]
        }
        projection = {MongoOperator.GROUP_KEY.value: MongoProjectionState.OFF.value}
        return query, projection

    def get_structure_details(self, level: Level = None, key_value: str = None) -> typing.Dict:
        self.collection = level.value
        query, projection = self.__get_structure_details_query(level, key_value)
        structure = self.first_or_default(query, projection)
        if FacebookMiscFields.details in structure.keys():
            structure[FacebookMiscFields.details] = BSON.decode(structure[FacebookMiscFields.details])
        return structure

    def get_all_structures_by_ad_account_id(
        self, level: Level = None, account_id: str = None
    ) -> typing.List[typing.Dict]:
        self.collection = level.value
        query = {
            MongoOperator.AND.value: [
                {LevelToFacebookIdKeyMapping.ACCOUNT.value: {MongoOperator.EQUALS.value: account_id}},
                {
                    FacebookMiscFields.status: {
                        MongoOperator.NOTIN.value: [
                            StructureStatusEnum.ARCHIVED.value,
                            StructureStatusEnum.REMOVED.value,
                            StructureStatusEnum.DEPRECATED.value,
                        ]
                    }
                },
            ]
        }

        projection = {
            FacebookMiscFields.details: MongoProjectionState.ON.value,
            MongoOperator.GROUP_KEY.value: MongoProjectionState.OFF.value,
        }

        structures = self.get(query, projection)
        structures = self.__decode_structure_details_from_bson(structures)
        return [structure[FacebookMiscFields.details] for structure in structures]

    def get_ad_account_slice(
        self,
        level: Level = None,
        account_id: str = None,
        structure_key: str = None,
        structure_ids: typing.List[str] = None,
        start_row: int = 0,
        end_row: int = 0,
    ) -> typing.List[typing.Dict]:
        self.collection = level.value
        query = {
            MongoOperator.AND.value: [
                {LevelToFacebookIdKeyMapping.ACCOUNT.value: {MongoOperator.EQUALS.value: account_id}},
                {
                    FacebookMiscFields.status: {
                        MongoOperator.NOTIN.value: [
                            StructureStatusEnum.ARCHIVED.value,
                            StructureStatusEnum.REMOVED.value,
                            StructureStatusEnum.DEPRECATED.value,
                        ]
                    }
                },
            ]
        }
        if structure_ids:
            query_filter = {structure_key: {MongoOperator.IN.value: structure_ids}}
            query[MongoOperator.AND.value].append(query_filter)

        projection = {
            FacebookMiscFields.details: MongoProjectionState.ON.value,
            MongoOperator.GROUP_KEY.value: MongoProjectionState.OFF.value,
        }

        sort_query = [("created_time", -1)]

        structures = self.get_data_slice(
            query=query, projection=projection, limit=end_row, skip=start_row, sort_query=sort_query
        )
        structures = self.__decode_structure_details_from_bson(structures)
        return [structure[FacebookMiscFields.details] for structure in structures]

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
                    FacebookMiscFields.details: BSON.decode(entry[FacebookMiscFields.details]),
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

    def add_updated_structures(self, level, structures: List[Dict]) -> None:
        self.collection = level.value
        self.add_many(structures)

    def add_structure(
        self, level: Level = None, key_value: typing.Any = None, document: typing.Dict = None
    ) -> typing.NoReturn:
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
                },
            ]
        }
        self.delete_many(query_filter)
        try:
            self.add_one(self._convert_to_dict(document))
        except Exception as e:
            raise e

    def get_latest_by_account_id(
        self,
        collection: str = None,
        start_date: typing.Union[datetime, str] = None,
        account_id: str = None,
    ) -> typing.List[typing.Dict]:
        self.database = self.config.structures_database_name
        self.collection = collection
        query = {
            MongoOperator.AND.value: [
                {FacebookMiscFields.account_id: {MongoOperator.EQUALS.value: account_id}},
                {FacebookMiscFields.date_added: {MongoOperator.GREATERTHANEQUAL.value: start_date}},
            ]
        }
        projection = {MongoOperator.GROUP_KEY.value: MongoProjectionState.ON.value}
        results = self.get(query=query, projection=projection)
        return results
