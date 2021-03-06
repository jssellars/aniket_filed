import typing

from bson import BSON

from Core.Dexter.Infrastructure.Domain.Breakdowns import BreakdownMetadataBase
from Core.Dexter.Infrastructure.Domain.LevelEnums import LevelEnum
from Core.mongo_adapter import MongoRepositoryBase, MongoProjectionState, \
    MongoRepositoryStatus, MongoOperator
from GoogleDexter.Infrastructure.Domain.Breakdowns import GoogleActionBreakdownEnum, GoogleBreakdownEnum
from GoogleDexter.Infrastructure.Domain.LevelEnums import GoogleLevelIdKeyEnum, GoogleLevelNameKeyEnum


class GoogleDexterMongoRepository(MongoRepositoryBase):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def is_available(self, level: LevelEnum = None, key_value: typing.AnyStr = None) -> bool:
        self._database = self._client[self._config.insights_database]
        collection_name = level.value + "_" + GoogleBreakdownEnum.NONE.value.name + "_" + GoogleActionBreakdownEnum.NONE.value.name
        self.collection = collection_name

        query = {
            GoogleLevelIdKeyEnum.get_enum_by_name(level.name).value: {
                MongoOperator.EQUALS.value: key_value
            }
        }
        results = self.get(query)
        return len(results) > 0

    def get_breakdown_values(self,
                             key_value: typing.AnyStr = None,
                             level: LevelEnum = None,
                             date_start: typing.AnyStr = None,
                             date_stop: typing.AnyStr = None,
                             breakdown: GoogleBreakdownEnum = GoogleBreakdownEnum.NONE,
                             action_breakdown: GoogleActionBreakdownEnum = GoogleActionBreakdownEnum.NONE) -> \
    typing.List[
        typing.Tuple[typing.AnyStr, typing.AnyStr]]:
        self._database = self._client[self._config.insights_database]
        collection_name = level.value + "_" + breakdown.value.name + "_" + action_breakdown.value.name
        self.collection = collection_name

        query = {
            MongoOperator.AND.value: [
                {
                    GoogleLevelIdKeyEnum.get_enum_by_name(level.name).value: {MongoOperator.EQUALS.value: key_value}
                },
                {
                    "date_start": {MongoOperator.GREATERTHANEQUAL.value: date_start}
                },
                {
                    "date_start": {MongoOperator.LESSTHANEQUAL.value: date_stop}
                }
            ]
        }

        projection = {"_id": MongoProjectionState.OFF.value}
        if breakdown != GoogleBreakdownEnum.NONE and action_breakdown == GoogleActionBreakdownEnum.NONE:
            projection[breakdown.value.name] = MongoProjectionState.ON.value
            raw_breakdowns = self.get(query, projection)
            breakdown_values = [(entry[breakdown.value.name], GoogleActionBreakdownEnum.NONE.value.name) for entry in
                                raw_breakdowns]
            return list(set(breakdown_values))

        elif breakdown == GoogleBreakdownEnum.NONE and action_breakdown != GoogleActionBreakdownEnum.NONE:
            projection[action_breakdown.value.name] = MongoProjectionState.ON.value
            raw_breakdowns = self.get(query, projection)
            breakdown_values = [(GoogleActionBreakdownEnum.NONE.value.name, entry[action_breakdown.value.name]) for
                                entry in
                                raw_breakdowns]
            return list(set(breakdown_values))

        elif breakdown != GoogleBreakdownEnum.NONE and action_breakdown != GoogleActionBreakdownEnum.NONE:
            projection[breakdown.value.name] = MongoProjectionState.ON.value
            projection[action_breakdown.value.name] = MongoProjectionState.ON.value
            raw_breakdowns = self.get(query, projection)
            breakdown_values = [(entry[breakdown.value.name], entry[action_breakdown.value.name]) for entry in
                                raw_breakdowns]
            return list(set(breakdown_values))

        else:
            return list()

    def get_metrics_values(self,
                           key_value: typing.AnyStr = None,
                           date_start: typing.AnyStr = None,
                           date_stop: typing.AnyStr = None,
                           metrics: typing.List[typing.AnyStr] = None,
                           level: LevelEnum = None,
                           breakdown_metadata: BreakdownMetadataBase = None) -> typing.List[typing.Dict]:
        self._database = self._client[self._config.insights_database]
        collection_name = (level.value + "_" +
                           breakdown_metadata.breakdown.value.name + "_" +
                           breakdown_metadata.action_breakdown.value.name)
        self.collection = collection_name

        # build mongo query
        query = [
            {
                MongoOperator.GROUP.value: {
                    MongoOperator.GROUP_KEY.value: {
                        GoogleLevelIdKeyEnum.get_enum_by_name(
                            level.name).value: f"{MongoOperator.DOLLAR_SIGN.value}{GoogleLevelIdKeyEnum.get_enum_by_name(level.name).value}",
                        "date_start": f"{MongoOperator.DOLLAR_SIGN.value}date_start"
                    },
                }
            },
            {
                MongoOperator.MATCH.value: {
                    MongoOperator.AND.value:
                        [
                            {
                                f"{MongoOperator.GROUP_KEY.value}.date_start": {
                                    MongoOperator.GREATERTHANEQUAL.value: date_start}
                            },
                            {
                                f"{MongoOperator.GROUP_KEY.value}.date_start": {
                                    MongoOperator.LESSTHANEQUAL.value: date_stop}
                            },
                            {
                                f"{MongoOperator.GROUP_KEY.value}.{GoogleLevelIdKeyEnum.get_enum_by_name(level.name).value}": {
                                    MongoOperator.EQUALS.value: key_value}
                            }
                        ]
                }
            },
            {
                MongoOperator.SORT.value: {
                    "_id": -1
                }
            }
        ]

        # add breakdown to group by
        if breakdown_metadata.breakdown != GoogleBreakdownEnum.NONE:
            query[0][MongoOperator.GROUP.value][MongoOperator.GROUP_KEY.value][
                breakdown_metadata.breakdown.value.name] = \
                f"{MongoOperator.DOLLAR_SIGN.value}{breakdown_metadata.breakdown.value.name}"

            breakdown_value_filter = {
                f"{MongoOperator.GROUP_KEY.value}.{breakdown_metadata.breakdown.value.name}": {
                    MongoOperator.EQUALS.value: breakdown_metadata.breakdown_value}
            }
            query[1][MongoOperator.MATCH.value][MongoOperator.AND.value].append(breakdown_value_filter)

        # add action breakdown to group by
        if breakdown_metadata.action_breakdown != GoogleActionBreakdownEnum.NONE:
            query[0][MongoOperator.GROUP.value][MongoOperator.GROUP_KEY.value][
                breakdown_metadata.action_breakdown.value.name] = \
                f"{MongoOperator.DOLLAR_SIGN.value}{breakdown_metadata.action_breakdown.value.name}"

            breakdown_value_filter = {
                f"{MongoOperator.GROUP_KEY.value}.{breakdown_metadata.action_breakdown.value.name}": {
                    MongoOperator.EQUALS.value: breakdown_metadata.action_breakdown_value}
            }
            query[1][MongoOperator.MATCH.value][MongoOperator.AND.value].append(breakdown_value_filter)

        # add desired metrics to query
        metrics_dict = {metric: {MongoOperator.SUM.value: f"{MongoOperator.DOLLAR_SIGN.value}{metric}"}
                        for metric in metrics}
        query[0][MongoOperator.GROUP.value].update(metrics_dict)

        try:
            results = list(self.collection.aggregate(query))
        except Exception as e:
            raise Exception(str(e))

        return results

    def get_min_value(self,
                      key_value: typing.AnyStr = None,
                      metrics: typing.List[typing.AnyStr] = None,
                      level: LevelEnum = None,
                      breakdown_metadata: BreakdownMetadataBase = None) -> typing.List[typing.Dict]:
        self._database = self._client[self._config.insights_database]
        collection_name = (level.value + "_" +
                           breakdown_metadata.breakdown.value.name + "_" +
                           breakdown_metadata.action_breakdown.value.name)
        self.collection = collection_name

        # build mongo query
        query = [
            {
                MongoOperator.GROUP.value: {
                    MongoOperator.GROUP_KEY.value: {
                        GoogleLevelIdKeyEnum.get_enum_by_name(
                            level.name).value: f"{MongoOperator.DOLLAR_SIGN.value}{GoogleLevelIdKeyEnum.get_enum_by_name(level.name).value}"
                    },
                }
            },
            {
                MongoOperator.MATCH.value: {
                    MongoOperator.AND.value:
                        [
                            {
                                f"{MongoOperator.GROUP_KEY.value}.{GoogleLevelIdKeyEnum.get_enum_by_name(level.name).value}": {
                                    MongoOperator.EQUALS.value: key_value}
                            }
                        ]
                }
            },
            {
                MongoOperator.SORT.value: {
                    "_id": -1
                }
            }
        ]

        # add breakdown to group by
        if breakdown_metadata.breakdown != GoogleBreakdownEnum.NONE:
            query[0][MongoOperator.GROUP.value][MongoOperator.GROUP_KEY.value][
                breakdown_metadata.breakdown.value.name] = \
                f"{MongoOperator.DOLLAR_SIGN.value}{breakdown_metadata.breakdown.value.name}"

            breakdown_value_filter = {
                breakdown_metadata.breakdown.value.name: {
                    MongoOperator.EQUALS.value: breakdown_metadata.breakdown_value}
            }
            query[1][MongoOperator.MATCH.value][MongoOperator.AND.value].append(breakdown_value_filter)

        # add action breakdown to group by
        if breakdown_metadata.action_breakdown != GoogleActionBreakdownEnum.NONE:
            query[0][MongoOperator.GROUP.value][MongoOperator.GROUP_KEY.value][
                breakdown_metadata.action_breakdown.value.name] = \
                f"{MongoOperator.DOLLAR_SIGN.value}{breakdown_metadata.action_breakdown.value.name}"

            breakdown_value_filter = {
                breakdown_metadata.action_breakdown.value.name: {
                    MongoOperator.EQUALS.value: breakdown_metadata.action_breakdown_value}
            }
            query[1][MongoOperator.MATCH.value][MongoOperator.AND.value].append(breakdown_value_filter)

        # add desired metrics to query
        metrics_dict = {metric: {MongoOperator.MIN.value: f"{MongoOperator.DOLLAR_SIGN.value}{metric}"} for
                        metric in metrics}
        query[0][MongoOperator.GROUP.value].update(metrics_dict)

        try:
            results = list(self.collection.aggregate(query))
        except Exception as e:
            raise Exception(str(e))

        return results

    def get_max_value(self,
                      key_value: typing.AnyStr = None,
                      metrics: typing.List[typing.AnyStr] = None,
                      level: LevelEnum = None,
                      breakdown_metadata: BreakdownMetadataBase = None) -> typing.List[typing.Dict]:
        self._database = self._client[self._config.insights_database]
        collection_name = (level.value + "_" +
                           breakdown_metadata.breakdown.value.name + "_" +
                           breakdown_metadata.action_breakdown.value.name)
        self.collection = collection_name

        # build mongo query
        query = [
            {
                MongoOperator.GROUP.value: {
                    MongoOperator.GROUP_KEY.value: {
                        GoogleLevelIdKeyEnum.get_enum_by_name(
                            level.name).value: f"{MongoOperator.DOLLAR_SIGN.value}{GoogleLevelIdKeyEnum.get_enum_by_name(level.name).value}",
                        "date_start": f"{MongoOperator.DOLLAR_SIGN.value}date_start"
                    },
                }
            },
            {
                MongoOperator.MATCH.value: {
                    MongoOperator.AND.value:
                        [
                            {
                                f"{MongoOperator.GROUP_KEY.value}.{GoogleLevelIdKeyEnum.get_enum_by_name(level.name).value}": {
                                    MongoOperator.EQUALS.value: key_value}
                            }
                        ]
                }
            },
            {
                MongoOperator.SORT.value: {
                    "_id": -1
                }
            }
        ]

        # add breakdown to group by
        if breakdown_metadata.breakdown != GoogleBreakdownEnum.NONE:
            query[0][MongoOperator.GROUP.value][MongoOperator.GROUP_KEY.value][
                breakdown_metadata.breakdown.value.name] = \
                f"{MongoOperator.DOLLAR_SIGN.value}{breakdown_metadata.breakdown.value.name}"

            breakdown_value_filter = {
                breakdown_metadata.breakdown.value.name: {
                    MongoOperator.EQUALS.value: breakdown_metadata.breakdown_value}
            }
            query[1][MongoOperator.MATCH.value][MongoOperator.AND.value].append(breakdown_value_filter)

        # add action breakdown to group by
        if breakdown_metadata.action_breakdown != GoogleActionBreakdownEnum.NONE:
            query[0][MongoOperator.GROUP.value][MongoOperator.GROUP_KEY.value][
                breakdown_metadata.action_breakdown.value.name] = \
                f"{MongoOperator.DOLLAR_SIGN.value}{breakdown_metadata.action_breakdown.value.name}"

            breakdown_value_filter = {
                breakdown_metadata.action_breakdown.value.name: {
                    MongoOperator.EQUALS.value: breakdown_metadata.action_breakdown_value}
            }
            query[1][MongoOperator.MATCH.value][MongoOperator.AND.value].append(breakdown_value_filter)

        # add desired metrics to query
        metrics_dict = {metric: {MongoOperator.MAX.value: f"{MongoOperator.DOLLAR_SIGN.value}{metric}"}
                        for metric in metrics}
        query[0][MongoOperator.GROUP.value].update(metrics_dict)

        try:
            results = list(self.collection.aggregate(query))
        except Exception as e:
            raise Exception(str(e))

        return results

    def get_recommendation_meta_information(self,
                                            key_value: typing.AnyStr = None,
                                            level: LevelEnum = None) -> typing.Union[typing.Dict, typing.NoReturn]:
        self._database = self._client[self._config.structures_database]
        self.collection = level.value

        # build mongo query
        query = {
            MongoOperator.AND.value: [
                {
                    GoogleLevelIdKeyEnum.get_enum_by_name(level.name).value: {
                        MongoOperator.EQUALS.value: key_value
                    }
                },
                {
                    "status": {
                        MongoRepositoryStatus.ACTIVE.value
                    }
                }
            ]
        }

        # build mongo projection
        projection = {
            "_id": MongoProjectionState.OFF.value,
            GoogleLevelIdKeyEnum.CAMPAIGN.value: MongoProjectionState.ON.value,
            GoogleLevelNameKeyEnum.CAMPAIGN.value: MongoProjectionState.ON.value,
            GoogleLevelIdKeyEnum.ADGROUP.value: MongoProjectionState.ON.value,
            GoogleLevelNameKeyEnum.ADGROUP.value: MongoProjectionState.ON.value,
            GoogleLevelIdKeyEnum.AD.value: MongoProjectionState.ON.value,
            GoogleLevelNameKeyEnum.AD.value: MongoProjectionState.ON.value,
            GoogleLevelIdKeyEnum.ACCOUNT.value: MongoProjectionState.ON.value
        }

        return self.get(query=query, projection=projection)

    def get_ad_account_id(self, key_value: typing.AnyStr = None, level: LevelEnum = None) -> typing.AnyStr:
        self._database = self._client[self._config.structures_database]
        self.collection = level.value

        # build mongo query
        query = {
            MongoOperator.AND.value: [
                {
                    GoogleLevelIdKeyEnum.get_enum_by_name(level.name).value: {
                        MongoOperator.EQUALS.value: key_value
                    }
                },
                {
                    "status": MongoRepositoryStatus.ACTIVE.value
                }
            ]
        }

        # build mongo projection
        projection = {
            "_id": MongoProjectionState.OFF.value,
            GoogleLevelIdKeyEnum.ACCOUNT.value: MongoProjectionState.ON.value
        }

        ad_account_id = self.first_or_default(query=query, projection=projection)
        if GoogleLevelIdKeyEnum.ACCOUNT.value in ad_account_id.keys():
            ad_account_id = ad_account_id[GoogleLevelIdKeyEnum.ACCOUNT.value]
        else:
            ad_account_id = None

        return ad_account_id

    def get_structure_details(self,
                              key_value: typing.AnyStr = None,
                              level: LevelEnum = None) -> typing.Union[typing.Dict, typing.NoReturn]:
        self._database = self._client[self._config.structures_database]
        self.collection = level.value

        # build mongo query
        query = {
            MongoOperator.AND.value: [
                {
                    GoogleLevelIdKeyEnum.get_enum_by_name(level.name).value: {
                        MongoOperator.EQUALS.value: key_value
                    }
                },
                {
                    "status": {
                        MongoOperator.EQUALS.value: MongoRepositoryStatus.ACTIVE.value
                    }
                }
            ]
        }

        # build mongo projection
        projection = {
            "_id": MongoProjectionState.OFF.value,
            "details": MongoProjectionState.ON.value
        }

        structure_details = self.first_or_default(query=query, projection=projection)
        if structure_details:
            structure_details = BSON.decode(structure_details.get("details", {}))
        return structure_details

    def get_ads_by_adgroup_id(self, key_value: typing.AnyStr = None) -> typing.List[typing.AnyStr]:
        self._database = self._client[self._config.insights_database]
        collection_name = (LevelEnum.AD.value + "_" +
                           GoogleBreakdownEnum.NONE.value.name + "_" +
                           GoogleActionBreakdownEnum.NONE.value.name)
        self.collection = collection_name

        query = {
            GoogleLevelIdKeyEnum.ADGROUP.value: {MongoOperator.EQUALS.value: key_value},
        }

        projection = {
            "_id": MongoProjectionState.OFF.value,
            GoogleLevelIdKeyEnum.AD.value: MongoProjectionState.ON.value
        }

        return list(set([entry[GoogleLevelIdKeyEnum.AD.value] for entry in self.get(query, projection)]))

    def get_adgroups_by_campaign_id(self, key_value: typing.AnyStr = None) -> typing.List[typing.AnyStr]:
        self._database = self._client[self._config.insights_database]
        collection_name = (LevelEnum.ADGROUP.value + "_" +
                           GoogleBreakdownEnum.NONE.value.name + "_" +
                           GoogleActionBreakdownEnum.NONE.value.name)
        self.collection = collection_name

        query = {
            GoogleLevelIdKeyEnum.CAMPAIGN.value: {MongoOperator.EQUALS.value: key_value},
        }
        projection = {
            "_id": MongoProjectionState.OFF.value,
            GoogleLevelIdKeyEnum.ADGROUP.value: MongoProjectionState.ON.value
        }

        return list(set([entry[GoogleLevelIdKeyEnum.ADGROUP.value] for entry in self.get(query, projection)]))

    def get_campaigns_by_account_id(self, key_value: typing.AnyStr = None) -> typing.List[typing.AnyStr]:
        self._database = self._client[self._config.insights_database]
        collection_name = (LevelEnum.CAMPAIGN.value + "_" +
                           GoogleBreakdownEnum.NONE.value.name + "_" +
                           GoogleActionBreakdownEnum.NONE.value.name)
        self.collection = collection_name

        query = {
            GoogleLevelIdKeyEnum.ACCOUNT.value: {MongoOperator.EQUALS.value: key_value}
        }
        projection = {
            "_id": MongoProjectionState.OFF.value,
            GoogleLevelIdKeyEnum.CAMPAIGN.value: MongoProjectionState.ON.value
        }

        return list(set([entry[GoogleLevelIdKeyEnum.CAMPAIGN.value] for entry in self.get(query, projection)]))

    def get_adgroup_id_by_campaign_id(self, key_value: typing.AnyStr = None) -> typing.AnyStr:
        self._database = self._client[self._config.structures_database]
        self.collection = LevelEnum.ADGROUP.value

        query = {
            MongoOperator.AND.value: [
                {
                    GoogleLevelIdKeyEnum.CAMPAIGN.value: {MongoOperator.EQUALS.value: key_value},
                },
                {
                    "status": {MongoOperator.EQUALS.value: MongoRepositoryStatus.ACTIVE.value}
                }
            ]
        }
        projection = {
            "_id": MongoProjectionState.OFF.value,
            GoogleLevelIdKeyEnum.ADGROUP.value: MongoProjectionState.ON.value
        }

        result = self.first_or_default(query, projection)
        return result.get(GoogleLevelIdKeyEnum.ADGROUP.value)

    def get_adgroup_id_by_ad_id(self, key_value: typing.AnyStr = None) -> typing.AnyStr:
        self._database = self._client[self._config.structures_database]
        self.collection = LevelEnum.AD.value

        query = {
            MongoOperator.AND.value: [
                {
                    GoogleLevelIdKeyEnum.ADGROUP.value: {MongoOperator.EQUALS.value: key_value},
                },
                {
                    "status": {MongoOperator.EQUALS.value: MongoRepositoryStatus.ACTIVE.value}
                }
            ]
        }
        projection = {
            "_id": MongoProjectionState.OFF.value,
            GoogleLevelIdKeyEnum.ADGROUP.value: MongoProjectionState.ON.value
        }

        result = self.first_or_default(query, projection)
        return result.get(GoogleLevelIdKeyEnum.ADGROUP.value)
