import functools
import operator
import typing
from time import sleep
from typing import List, Dict, Any

from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.adobjects.adreportrun import AdReportRun
from facebook_business.exceptions import FacebookRequestError

from Core import mongo_adapter
from Core.Web.FacebookGraphAPI.GraphAPIDomain.GraphAPIInsightsFields import GraphAPIInsightsFields
from Core.Web.FacebookGraphAPI.GraphAPIMappings.LevelMapping import Level
from Core.Web.FacebookGraphAPI.Models.Field import Field, FieldType
from Core.Web.FacebookGraphAPI.Models.FieldsMetadata import FieldsMetadata
from FacebookTuring.BackgroundTasks.Orchestrators.InsightsSyncronizerBreakdowns import InsightsSynchronizerBreakdownEnum
from FacebookTuring.BackgroundTasks.startup import config, fixtures
from FacebookTuring.Infrastructure.GraphAPIHandlers.GraphAPIInsightsHandler import GraphAPIInsightsHandler
from FacebookTuring.Infrastructure.PersistenceLayer.TuringMongoRepository import TuringMongoRepository

LEVEL_TO_STRUCTURE_FIELDS = {
    Level.CAMPAIGN: [
        FieldsMetadata.account_name,
        FieldsMetadata.account_id,
        FieldsMetadata.campaign_name,
        FieldsMetadata.campaign_id,
    ],
    Level.ADSET: [
        FieldsMetadata.account_name,
        FieldsMetadata.account_id,
        FieldsMetadata.campaign_id,
        FieldsMetadata.campaign_name,
        FieldsMetadata.adset_name,
        FieldsMetadata.adset_id,
    ],
    Level.AD: [
        FieldsMetadata.account_name,
        FieldsMetadata.account_id,
        FieldsMetadata.campaign_id,
        FieldsMetadata.campaign_name,
        FieldsMetadata.adset_id,
        FieldsMetadata.adset_name,
        FieldsMetadata.ad_name,
        FieldsMetadata.ad_id,
    ],
}


class InsightsSynchronizer:
    RATE_LIMIT_EXCEPTION_STATUS = 80000
    SLEEP_ON_RATE_LIMIT_EXCEPTION = 3600

    def __init__(
            self,
            business_owner_id: typing.AnyStr = None,
            account_id: typing.AnyStr = None,
            level: Level = None,
            breakdown: Field = None,
            action_breakdown: Field = None,
            date_start: typing.AnyStr = None,
            date_stop: typing.AnyStr = None,
            requested_fields: typing.List = None,
    ):
        self.business_owner_id = business_owner_id
        self.account_id = account_id
        self.level = level
        self.breakdown = breakdown
        self.action_breakdown = action_breakdown
        self.date_start = date_start
        self.date_stop = date_stop
        self.requested_fields = requested_fields
        self.__ad_account_id = "act_" + self.account_id
        self.__mongo_repository = None

    def run(self, ad_report_run: AdReportRun) -> None:
        try:

            response = GraphAPIInsightsHandler.process_async_report(
                config,
                ad_report_run,
                f'act_{self.account_id}',
                requested_fields=self.requested_fields,
                level=self.level.value,
            )

            response = mongo_adapter.filter_null_values_from_documents(response)
            self.__mongo_repository.collection = self.__get_mongo_repository_collection()
            self.__mongo_repository.add_many(response)
        except FacebookRequestError as fb_ex:
            if fb_ex.http_status() == self.RATE_LIMIT_EXCEPTION_STATUS:
                sleep(self.SLEEP_ON_RATE_LIMIT_EXCEPTION)
            else:
                raise
        except Exception:
            raise

    def set_mongo_repository(self, mongo_repository: TuringMongoRepository = None) -> typing.Any:
        self.__mongo_repository = mongo_repository
        return self

    def __get_fields(self) -> typing.List[typing.AnyStr]:
        fields = [
            field.facebook_fields
            for field in self.requested_fields
            if field.field_type == FieldType.INSIGHT or field.field_type == FieldType.ACTION_INSIGHT
        ]
        fields = functools.reduce(operator.iconcat, fields, [])
        return list(set(fields))

    def __get_breakdowns(self) -> typing.List[typing.AnyStr]:
        return self.breakdown.facebook_fields if self.breakdown.name != FieldsMetadata.breakdown_none.name else []

    def __get_action_breakdowns(self) -> typing.List[typing.AnyStr]:
        action_breakdowns = [field.action_breakdowns for field in self.requested_fields]
        action_breakdowns = functools.reduce(operator.iconcat, action_breakdowns, [])
        if self.action_breakdown and self.action_breakdown != FieldsMetadata.action_none.name:
            action_breakdowns.extend(self.action_breakdown.facebook_fields)
        return action_breakdowns

    def __get_time_range(self) -> typing.Dict:
        time_range = {GraphAPIInsightsFields.since: self.date_start, GraphAPIInsightsFields.until: self.date_stop}
        return time_range

    def __get_parameters(self) -> typing.Dict:
        parameters = {
            "level": self.level.value,
            "breakdowns": self.__get_breakdowns(),
            "action_breakdowns": list(set(self.__get_action_breakdowns())),
            "time_increment": FieldsMetadata.day.facebook_value,
            "time_range": self.__get_time_range(),
            "limit": 50,
        }
        return parameters

    def __get_mongo_repository_collection(self) -> typing.AnyStr:
        collection_name = self.level.value + "_" + self.breakdown.name + "_" + self.action_breakdown.name
        return collection_name

    def get_async_insights_report(self) -> List:

        if self.breakdown is not None and self.breakdown != InsightsSynchronizerBreakdownEnum.NONE.value:
            self.requested_fields += [self.breakdown]

        self.requested_fields += LEVEL_TO_STRUCTURE_FIELDS[self.level]

        ad_account = AdAccount(f'act_{self.account_id}')
        ad_report_run = ad_account.get_insights_async(fields=self.__get_fields(), params=self.__get_parameters())
        return ad_report_run
