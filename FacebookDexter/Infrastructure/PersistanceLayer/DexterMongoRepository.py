import typing

from bson import BSON

from Core.Tools.MongoRepository.MongoOperator import MongoOperator
from Core.Tools.MongoRepository.MongoRepositoryBase import MongoRepositoryBase, MongoProjectionState
from Core.Tools.MongoRepository.MongoRepositoryStatusBase import MongoRepositoryStatusBase
from FacebookDexter.Infrastructure.Domain.Breakdowns import BreakdownMetadata, BreakdownEnum, ActionBreakdownEnum
from FacebookDexter.Infrastructure.Domain.LevelEnums import LevelEnum, LevelIdKeyEnum, LevelNameKeyEnum


class DexterMongoRepository(MongoRepositoryBase):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def get_breakdown_values(self,
                             key_value: typing.AnyStr = None,
                             level: LevelEnum = None,
                             date_start: typing.AnyStr = None,
                             date_stop: typing.AnyStr = None,
                             breakdown: BreakdownEnum = BreakdownEnum.NONE,
                             action_breakdown: ActionBreakdownEnum = ActionBreakdownEnum.NONE) -> typing.List[
        typing.Tuple[typing.AnyStr, typing.AnyStr]]:
        self._database = self._client[self._config.insights_database]
        collection_name = level.value + "_" + breakdown.value.name + "_" + action_breakdown.value.name
        self.set_collection(collection_name)

        query = {
            MongoOperator.AND.value: [
                {
                    LevelIdKeyEnum.get_enum_by_name(level.name).value: {MongoOperator.EQUALS.value: key_value}
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
        if breakdown != BreakdownEnum.NONE and action_breakdown == ActionBreakdownEnum.NONE:
            projection[breakdown.value.name] = MongoProjectionState.ON.value
            raw_breakdowns = self.get(query, projection)
            breakdown_values = [(entry[breakdown.value.name], ActionBreakdownEnum.NONE.value.name) for entry in
                                raw_breakdowns]
            return list(set(breakdown_values))

        elif breakdown == BreakdownEnum.NONE and action_breakdown != ActionBreakdownEnum.NONE:
            projection[action_breakdown.value.name] = MongoProjectionState.ON.value
            raw_breakdowns = self.get(query, projection)
            breakdown_values = [(ActionBreakdownEnum.NONE.value.name, entry[action_breakdown.value.name]) for entry in
                                raw_breakdowns]
            return list(set(breakdown_values))

        elif breakdown != BreakdownEnum.NONE and action_breakdown != ActionBreakdownEnum.NONE:
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
                           breakdown_metadata: BreakdownMetadata = None) -> typing.List[typing.Dict]:
        self._database = self._client[self._config.insights_database]
        collection_name = level.value + "_" + breakdown_metadata.breakdown.value.name + "_" + breakdown_metadata.action_breakdown.value.name
        self.set_collection(collection_name)

        # build mongo query
        query = [
            {
                MongoOperator.GROUP.value: {
                    MongoOperator.GROUP_KEY.value: {
                        LevelIdKeyEnum.get_enum_by_name(
                            level.name).value: f"{MongoOperator.DOLLAR_SIGN.value}{LevelIdKeyEnum.get_enum_by_name(level.name).value}",
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
                                f"{MongoOperator.GROUP_KEY.value}.{LevelIdKeyEnum.get_enum_by_name(level.name).value}": {
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

        #  add breakdown to group by
        if breakdown_metadata.breakdown != BreakdownEnum.NONE:
            query[0][MongoOperator.GROUP.value][MongoOperator.GROUP_KEY.value][
                breakdown_metadata.breakdown.value.name] = \
                f"{MongoOperator.DOLLAR_SIGN.value}{breakdown_metadata.breakdown.value.name}"

            breakdown_value_filter = {
                f"{MongoOperator.GROUP_KEY.value}.{breakdown_metadata.breakdown.value.name}": {
                    MongoOperator.EQUALS.value: breakdown_metadata.breakdown_value}
            }
            query[1][MongoOperator.MATCH.value][MongoOperator.AND.value].append(breakdown_value_filter)

        # add action breakdown to group by
        if breakdown_metadata.action_breakdown != ActionBreakdownEnum.NONE:
            query[0][MongoOperator.GROUP.value][MongoOperator.GROUP_KEY.value][
                breakdown_metadata.action_breakdown.value.name] = \
                f"{MongoOperator.DOLLAR_SIGN.value}{breakdown_metadata.action_breakdown.value.name}"

            breakdown_value_filter = {
                f"{MongoOperator.GROUP_KEY.value}.{breakdown_metadata.action_breakdown.value.name}": {
                    MongoOperator.EQUALS.value: breakdown_metadata.action_breakdown_value}
            }
            query[1][MongoOperator.MATCH.value][MongoOperator.AND.value].append(breakdown_value_filter)

        # add desired metrics to query
        metrics_dict = {metric: {MongoOperator.SUM.value: f"{MongoOperator.DOLLAR_SIGN.value}{metric}"} for metric in
                        metrics}
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
                      breakdown_metadata: BreakdownMetadata = None) -> typing.List[typing.Dict]:
        self._database = self._client[self._config.insights_database]
        collection_name = level.value + "_" + breakdown_metadata.breakdown.value.name + "_" + breakdown_metadata.action_breakdown.value.name
        self.set_collection(collection_name)

        # build mongo query
        query = [
            {
                MongoOperator.GROUP.value: {
                    MongoOperator.GROUP_KEY.value: {
                        LevelIdKeyEnum.get_enum_by_name(
                            level.name).value: f"{MongoOperator.DOLLAR_SIGN.value}{LevelIdKeyEnum.get_enum_by_name(level.name).value}"
                    },
                }
            },
            {
                MongoOperator.MATCH.value: {
                    MongoOperator.AND.value:
                        [
                            {
                                f"{MongoOperator.GROUP_KEY.value}.{LevelIdKeyEnum.get_enum_by_name(level.name).value}": {
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

        #  add breakdown to group by
        if breakdown_metadata.breakdown != BreakdownEnum.NONE:
            query[0][MongoOperator.GROUP.value][MongoOperator.GROUP_KEY.value][
                breakdown_metadata.breakdown.value.name] = \
                f"{MongoOperator.DOLLAR_SIGN.value}{breakdown_metadata.breakdown.value.name}"

            breakdown_value_filter = {
                breakdown_metadata.breakdown.value.name: {
                    MongoOperator.EQUALS.value: breakdown_metadata.breakdown_value}
            }
            query[1][MongoOperator.MATCH.value][MongoOperator.AND.value].append(breakdown_value_filter)

        # add action breakdown to group by
        if breakdown_metadata.action_breakdown != ActionBreakdownEnum.NONE:
            query[0][MongoOperator.GROUP.value][MongoOperator.GROUP_KEY.value][
                breakdown_metadata.action_breakdown.value.name] = \
                f"{MongoOperator.DOLLAR_SIGN.value}{breakdown_metadata.action_breakdown.value.name}"

            breakdown_value_filter = {
                breakdown_metadata.action_breakdown.value.name: {
                    MongoOperator.EQUALS.value: breakdown_metadata.action_breakdown_value}
            }
            query[1][MongoOperator.MATCH.value][MongoOperator.AND.value].append(breakdown_value_filter)

        # add desired metrics to query
        metrics_dict = {metric: {MongoOperator.MIN.value: f"{MongoOperator.DOLLAR_SIGN.value}{metric}"} for metric in
                        metrics}
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
                      breakdown_metadata: BreakdownMetadata = None) -> typing.List[typing.Dict]:
        self._database = self._client[self._config.insights_database]
        collection_name = level.value + "_" + breakdown_metadata.breakdown.value.name + "_" + breakdown_metadata.action_breakdown.value.name
        self.set_collection(collection_name)

        # build mongo query
        query = [
            {
                MongoOperator.GROUP.value: {
                    MongoOperator.GROUP_KEY.value: {
                        LevelIdKeyEnum.get_enum_by_name(
                            level.name).value: f"{MongoOperator.DOLLAR_SIGN.value}{LevelIdKeyEnum.get_enum_by_name(level.name).value}",
                        "date_start": f"{MongoOperator.DOLLAR_SIGN.value}date_start"
                    },
                }
            },
            {
                MongoOperator.MATCH.value: {
                    MongoOperator.AND.value:
                        [
                            {
                                f"{MongoOperator.GROUP_KEY.value}.{LevelIdKeyEnum.get_enum_by_name(level.name).value}": {
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

        #  add breakdown to group by
        if breakdown_metadata.breakdown != BreakdownEnum.NONE:
            query[0][MongoOperator.GROUP.value][MongoOperator.GROUP_KEY.value][
                breakdown_metadata.breakdown.value.name] = \
                f"{MongoOperator.DOLLAR_SIGN.value}{breakdown_metadata.breakdown.value.name}"

            breakdown_value_filter = {
                breakdown_metadata.breakdown.value.name: {
                    MongoOperator.EQUALS.value: breakdown_metadata.breakdown_value}
            }
            query[1][MongoOperator.MATCH.value][MongoOperator.AND.value].append(breakdown_value_filter)

        # add action breakdown to group by
        if breakdown_metadata.action_breakdown != ActionBreakdownEnum.NONE:
            query[0][MongoOperator.GROUP.value][MongoOperator.GROUP_KEY.value][
                breakdown_metadata.action_breakdown.value.name] = \
                f"{MongoOperator.DOLLAR_SIGN.value}{breakdown_metadata.action_breakdown.value.name}"

            breakdown_value_filter = {
                breakdown_metadata.action_breakdown.value.name: {
                    MongoOperator.EQUALS.value: breakdown_metadata.action_breakdown_value}
            }
            query[1][MongoOperator.MATCH.value][MongoOperator.AND.value].append(breakdown_value_filter)

        # add desired metrics to query
        metrics_dict = {metric: {MongoOperator.MAX.value: f"{MongoOperator.DOLLAR_SIGN.value}{metric}"} for metric in
                        metrics}
        query[0][MongoOperator.GROUP.value].update(metrics_dict)

        try:
            results = list(self.collection.aggregate(query))
        except Exception as e:
            raise Exception(str(e))

        return results

    def get_recommendation_meta_information(self, key_value: typing.AnyStr = None, level: LevelEnum = None) -> \
            typing.Union[typing.Dict, typing.NoReturn]:
        self._database = self._client[self._config.structures_database]
        self.set_collection(level.value)

        # build mongo query
        query = {
            MongoOperator.AND.value: [
                {
                    LevelIdKeyEnum.get_enum_by_name(level.name).value: {
                        MongoOperator.EQUALS.value: key_value
                    }
                },
                {
                    "status": {
                        MongoRepositoryStatusBase.ACTIVE.value
                    }
                }
            ]
        }

        # build mongo projection
        projection = {
            "_id": MongoProjectionState.OFF.value,
            LevelIdKeyEnum.CAMPAIGN.value: MongoProjectionState.ON.value,
            LevelNameKeyEnum.CAMPAIGN.value: MongoProjectionState.ON.value,
            LevelIdKeyEnum.ADSET.value: MongoProjectionState.ON.value,
            LevelNameKeyEnum.ADSET.value: MongoProjectionState.ON.value,
            LevelIdKeyEnum.AD.value: MongoProjectionState.ON.value,
            LevelNameKeyEnum.AD.value: MongoProjectionState.ON.value,
            LevelIdKeyEnum.ACCOUNT.value: MongoProjectionState.ON.value
        }

        return self.get(query=query, projection=projection)

    def get_ad_account_id(self, key_value: typing.AnyStr = None, level: LevelEnum = None) -> typing.AnyStr:
        self._database = self._client[self._config.structures_database]
        self.set_collection(level.value)

        # build mongo query
        query = {
            MongoOperator.AND.value: [
                {
                    LevelIdKeyEnum.get_enum_by_name(level.name).value: {
                        MongoOperator.EQUALS.value: key_value
                    }
                },
                {
                    "status": MongoRepositoryStatusBase.ACTIVE.value
                }
            ]
        }

        # build mongo projection
        projection = {
            "_id": MongoProjectionState.OFF.value,
            LevelIdKeyEnum.ACCOUNT.value: MongoProjectionState.ON.value
        }

        ad_account_id = self.first_or_default(query=query, projection=projection)
        if LevelIdKeyEnum.ACCOUNT.value in ad_account_id.keys():
            ad_account_id = 'act_' + ad_account_id[LevelIdKeyEnum.ACCOUNT.value]
        else:
            ad_account_id = None

        return ad_account_id

    def get_structure_details(self, key_value: typing.AnyStr = None, level: LevelEnum = None) -> typing.Union[
        typing.Dict, typing.NoReturn]:
        self._database = self._client[self._config.structures_database]
        self.set_collection(level.value)

        # build mongo query
        query = {
            MongoOperator.AND.value: [
                {
                    LevelIdKeyEnum.get_enum_by_name(level.name).value: {
                        MongoOperator.EQUALS.value: key_value
                    }
                },
                {
                    "status": {
                        MongoOperator.EQUALS.value: MongoRepositoryStatusBase.ACTIVE.value
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

    def get_ads_by_adset_id(self, key_value: typing.AnyStr = None) -> typing.List[typing.Dict]:
        self._database = self._client[self._config.structures_database]
        self.set_collection(LevelEnum.AD.value)

        query = {
            MongoOperator.AND.value: [
                {
                    LevelIdKeyEnum.ADSET.value: {MongoOperator.EQUALS.value: key_value},
                },
                {
                    "status": {MongoOperator.EQUALS.value: MongoRepositoryStatusBase.ACTIVE.value}
                }
            ]
        }

        projection = {
            "_id": MongoProjectionState.OFF.value,
            LevelIdKeyEnum.AD.value: MongoProjectionState.ON.value
        }

        return [entry[LevelIdKeyEnum.AD.value] for entry in self.get(query, projection)]

    def get_adsets_by_campaign_id(self, key_value: typing.AnyStr = None) -> typing.List[typing.Dict]:
        self._database = self._client[self._config.structures_database]
        self.set_collection(LevelEnum.ADSET.value)

        query = {
            MongoOperator.AND.value: [
                {
                    LevelIdKeyEnum.CAMPAIGN.value: {MongoOperator.EQUALS.value: key_value},
                },
                {
                    "status": {MongoOperator.EQUALS.value: MongoRepositoryStatusBase.ACTIVE.value}
                }
            ]
        }
        projection = {
            "_id": MongoProjectionState.OFF.value,
            LevelIdKeyEnum.ADSET.value: MongoProjectionState.ON.value
        }

        return [entry[LevelIdKeyEnum.ADSET.value] for entry in self.get(query, projection)]

    def get_campaigns_by_account_id(self, key_value: typing.AnyStr = None) -> typing.List[typing.Dict]:
        self._database = self._client[self._config.structures_database]
        self.set_collection(LevelEnum.CAMPAIGN.value)

        query = {
            MongoOperator.AND.value: [
                {
                    LevelIdKeyEnum.ACCOUNT.value: {MongoOperator.EQUALS.value: key_value},
                },
                {
                    "status": {MongoOperator.EQUALS.value: MongoRepositoryStatusBase.ACTIVE.value}
                }
            ]
        }
        projection = {
            "_id": MongoProjectionState.OFF.value,
            LevelIdKeyEnum.CAMPAIGN.value: MongoProjectionState.ON.value
        }

        return [entry[LevelIdKeyEnum.CAMPAIGN.value] for entry in self.get(query, projection)]

    def get_adset_id_by_campaign_id(self, key_value: typing.AnyStr = None) -> typing.List[typing.Dict]:
        self._database = self._client[self._config.structures_database]
        self.set_collection(LevelEnum.ADSET.value)

        query = {
            MongoOperator.AND.value: [
                {
                    LevelIdKeyEnum.CAMPAIGN.value: {MongoOperator.EQUALS.value: key_value},
                },
                {
                    "status": {MongoOperator.EQUALS.value: MongoRepositoryStatusBase.ACTIVE.value}
                }
            ]
        }
        projection = {
            "_id": MongoProjectionState.OFF.value,
            LevelIdKeyEnum.ADSET.value: MongoProjectionState.ON.value
        }

        result = self.first_or_default(query, projection)
        return result[LevelIdKeyEnum.ADSET.value]

    def get_adset_id_by_ad_id(self, key_value: typing.AnyStr = None) -> typing.List[typing.Dict]:
        self._database = self._client[self._config.structures_database]
        self.set_collection(LevelEnum.AD.value)

        query = {
            MongoOperator.AND.value: [
                {
                    LevelIdKeyEnum.ADSET.value: {MongoOperator.EQUALS.value: key_value},
                },
                {
                    "status": {MongoOperator.EQUALS.value: MongoRepositoryStatusBase.ACTIVE.value}
                }
            ]
        }
        projection = {
            "_id": MongoProjectionState.OFF.value,
            LevelIdKeyEnum.ADSET.value: MongoProjectionState.ON.value
        }

        result = self.first_or_default(query, projection)
        return result[LevelIdKeyEnum.ADSET.value]
