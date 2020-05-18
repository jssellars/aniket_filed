import functools
import operator
import typing
from time import sleep

from facebook_business.exceptions import FacebookRequestError

from Core.Web.BusinessOwnerRepository.BusinessOwnerRepository import BusinessOwnerRepository
from Core.Web.FacebookGraphAPI.GraphAPIDomain.GraphAPIInsightsFields import GraphAPIInsightsFields
from Core.Web.FacebookGraphAPI.Models.Field import Field
from Core.Web.FacebookGraphAPI.Models.FieldsMetadata import FieldsMetadata
from FacebookTuring.BackgroundTasks.Orchestrators.InsightsSyncronizerBreakdowns import InsightsSyncronizerBreakdownEnum
from FacebookTuring.BackgroundTasks.Orchestrators.InsightsSyncronizerFields import INSIGHTS_SYNCRONIZER_FIELDS
from FacebookTuring.BackgroundTasks.Startup import startup
from FacebookTuring.Infrastructure.GraphAPIHandlers.GraphAPIInsightsHandler import GraphAPIInsightsHandler
from FacebookTuring.Infrastructure.Mappings.LevelMapping import Level
from FacebookTuring.Infrastructure.PersistenceLayer.TuringMongoRepository import TuringMongoRepository


class InsightsSyncronizer:
    RATE_LIMIT_EXCEPTION_STATUS = 80000
    SLEEP_ON_RATE_LIMIT_EXCEPTION = 3600

    def __init__(self,
                 business_owner_id: typing.AnyStr = None,
                 account_id: typing.AnyStr = None,
                 level: Level = None,
                 breakdown: Field = None,
                 action_breakdown: Field = None,
                 date_start: typing.AnyStr = None,
                 date_stop: typing.AnyStr = None):
        self.business_owner_id = business_owner_id
        self.account_id = account_id
        self.level = level
        self.breakdown = breakdown
        self.action_breakdown = action_breakdown
        self.date_start = date_start
        self.date_stop = date_stop
        self.__requested_fields = INSIGHTS_SYNCRONIZER_FIELDS
        self.__ad_account_id = "act_" + self.account_id
        self.__permanent_token = None
        self.__mongo_repository = None

    def run(self) -> typing.NoReturn:
        try:
            if self.breakdown is not None and self.breakdown != InsightsSyncronizerBreakdownEnum.NONE.value:
                self.__requested_fields.append(self.breakdown)
            response = GraphAPIInsightsHandler.get_reports_insights(permanent_token=self.permanent_token,
                                                                    ad_account_id=self.__ad_account_id,
                                                                    fields=self.__get_fields(),
                                                                    parameters=self.__get_parameters(),
                                                                    requested_fields=self.__requested_fields)
            self.__mongo_repository.set_collection(self.__get_mongo_repository_collection())
            self.__mongo_repository.add_many(response)
        except FacebookRequestError as fb_ex:
            if fb_ex.http_status() == self.RATE_LIMIT_EXCEPTION_STATUS:
                sleep(self.SLEEP_ON_RATE_LIMIT_EXCEPTION)
        except Exception as e:
            raise e

    def set_mongo_repository(self, mongo_repository: TuringMongoRepository = None) -> typing.Any:
        self.__mongo_repository = mongo_repository
        return self

    def close_database_connection(self):
        self.__mongo_repository.close()

    @property
    def permanent_token(self) -> typing.AnyStr:
        if self.__permanent_token is None:
            self.__permanent_token = BusinessOwnerRepository(startup.session).get_permanent_token(
                self.business_owner_id)
        return self.__permanent_token

    def __get_fields(self) -> typing.List[typing.AnyStr]:
        fields = [field.facebook_fields for field in self.__requested_fields]
        fields = functools.reduce(operator.iconcat, fields, [])
        return fields

    def __get_breakdowns(self) -> typing.List[typing.AnyStr]:
        return self.breakdown.facebook_fields if self.breakdown.name != FieldsMetadata.breakdown_none.name else []

    def __get_action_breakdowns(self) -> typing.List[typing.AnyStr]:
        action_breakdowns = [field.action_breakdowns for field in self.__requested_fields]
        action_breakdowns = functools.reduce(operator.iconcat, action_breakdowns, [])
        if self.action_breakdown and self.action_breakdown != FieldsMetadata.action_none.name:
            action_breakdowns.extend(self.action_breakdown.facebook_fields)
        return action_breakdowns

    def __get_time_range(self) -> typing.Dict:
        time_range = {
            GraphAPIInsightsFields.since: self.date_start,
            GraphAPIInsightsFields.until: self.date_stop
        }
        return time_range

    def __get_parameters(self) -> typing.Dict:
        parameters = {
            "level": self.level.value,
            "breakdowns": self.__get_breakdowns(),
            "action_breakdowns": list(set(self.__get_action_breakdowns())),
            "time_increment": FieldsMetadata.day.facebook_value,
            "time_range": self.__get_time_range()
        }
        return parameters

    def __get_mongo_repository_collection(self) -> typing.AnyStr:
        collection_name = self.level.value + "_" + self.breakdown.name + "_" + self.action_breakdown.name
        return collection_name

    def check_data(self, date_start: typing.AnyStr = None, date_stop: typing.AnyStr = None) -> bool:
        check_data_parameters = {
            "level": self.level.value,
            "time_range": {
                GraphAPIInsightsFields.since: date_start,
                GraphAPIInsightsFields.until: date_stop
            }
        }
        try:
            response = GraphAPIInsightsHandler.get_reports_insights(permanent_token=self.permanent_token,
                                                                    ad_account_id=self.__ad_account_id,
                                                                    fields=[FieldsMetadata.impressions.name],
                                                                    parameters=check_data_parameters,
                                                                    requested_fields=[FieldsMetadata.impressions])
            return True if response else False
        except Exception as e:
            raise e