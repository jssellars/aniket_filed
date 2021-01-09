from typing import Dict, List, Optional

from Core.Dexter.Infrastructure.Domain.Breakdowns import ActionBreakdownBaseEnum, BreakdownBaseEnum
from Core.Dexter.Infrastructure.Domain.LevelEnums import LevelEnum, LevelIdKeyEnum
from Core.Web.FacebookGraphAPI.GraphAPIDomain.FacebookMiscFields import FacebookMiscFields
from Core.mongo_adapter import MongoOperator, MongoProjectionState, MongoRepositoryBase, MongoRepositoryStatus
from Core.Web.FacebookGraphAPI.Models.FieldsMetadata import FieldsMetadata
from FacebookDexter.BackgroundTasks.startup import config
from pymongo.errors import AutoReconnect
from retry import retry


class StrategyDataMongoRepository(MongoRepositoryBase):
    __RETRY_LIMIT = 3

    @retry(AutoReconnect, tries=__RETRY_LIMIT, delay=1)
    def read_metrics_data(
            self, key_value: str, metrics: List[str], level: LevelEnum, breakdown: FieldsMetadata
    ) -> List[Dict]:
        on_metrics = metrics + [
            FieldsMetadata.result_type.name,
            FieldsMetadata.date_start.name,
            FieldsMetadata.date_stop.name,
            LevelIdKeyEnum[level.value.upper()].value,
        ]
        if breakdown != FieldsMetadata.breakdown_none:
            on_metrics.append(breakdown.name)

        off_metrics = ["_id"]

        result = self.get(
            query={
                MongoOperator.AND.value: [
                    {LevelIdKeyEnum.get_enum_by_name(level.name).value: {MongoOperator.EQUALS.value: key_value}}
                ]
            },
            projection={
                **{m: MongoProjectionState.OFF.value for m in off_metrics},
                **{m: MongoProjectionState.ON.value for m in on_metrics},
            },
        )

        for entry in result:
            if breakdown.name not in entry:
                entry.update({"breakdown": breakdown.name})

        return result

    def get_structures_by_key(self, key: str, key_value: str, level: LevelEnum, structure_key: str) -> List[Dict]:
        on_metrics = [
            structure_key,
            f"{level.value}_name",
            FieldsMetadata.campaign_id.name,
            FieldsMetadata.campaign_name.name,
            FacebookMiscFields.details,
        ]
        off_metrics = ["_id"]

        return self.get(
            query={
                MongoOperator.AND.value: [
                    {key: {MongoOperator.EQUALS.value: key_value}},
                    {FieldsMetadata.status.name: {MongoOperator.EQUALS.value: MongoRepositoryStatus.ACTIVE.value}},
                ]
            },
            projection={
                **{m: MongoProjectionState.OFF.value for m in off_metrics},
                **{m: MongoProjectionState.ON.value for m in on_metrics},
            },
        )

    def set_insights_collection(
            self, level: LevelEnum, breakdown: FieldsMetadata, action_breakdown: FieldsMetadata
    ) -> None:
        self.database = config.mongo.insights_database
        self.collection = "_".join([level.value, breakdown.name, action_breakdown.name])

    def set_structures_collection(self, level: LevelEnum) -> None:
        self.database = config.mongo.structures_database
        self.collection = level.value
