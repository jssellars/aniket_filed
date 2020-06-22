import typing
from datetime import datetime

from Core.Tools.Logger.MongoLoggers.MongoLogger import MongoLogger
from FacebookDexter.Infrastructure.Domain.Breakdowns import BreakdownEnum, ActionBreakdownEnum
from FacebookDexter.Infrastructure.Domain.DaysEnum import DaysEnum
from FacebookDexter.Infrastructure.Domain.LevelEnums import LevelEnum


class RecommendationTemplateBuilderBase:

    def __init__(self):
        self._repository = None
        self._structure_id = None
        self._level = None
        self._breakdown = None
        self._action_breakdown = None
        self._keywords = None
        self._default_interests_number = 5
        self._external_services = None
        self._ad_account_id = None
        self._business_owner_repo_session = None
        self._facebook_config = None
        self._business_owner_id = None
        self.__logger = None
        self._date_stop = None
        self._time_interval = None
        self._debug = None

    @property
    def logger(self):
        if self._repository is not None and self.__logger is None:
            self.__logger = MongoLogger(repository=self._repository,
                                        database_name=self._repository.config.logs_database)
        return self.__logger

    def set_repository(self, repository: typing.Any = None):
        self._repository = repository
        return self

    def set_structure_id(self, structure_id: typing.AnyStr = None):
        self._structure_id = structure_id
        return self

    def set_level(self, level: LevelEnum = None):
        self._level = level
        return self

    def set_breakdown(self, breakdown: BreakdownEnum = None):
        self._breakdown = breakdown
        return self

    def set_action_breakdown(self, action_breakdown: ActionBreakdownEnum = None):
        self._action_breakdown = action_breakdown
        return self

    def set_external_services(self, external_services: typing.Any = None):
        self._external_services = external_services
        return self

    def set_ad_account_id(self, ad_account_id: typing.AnyStr = None):
        self._ad_account_id = ad_account_id
        return self

    def set_business_onwer_repo_session(self, business_owner_repo_session: typing.Any = None):
        self._business_owner_repo_session = business_owner_repo_session
        return self

    def set_facebook_config(self, facebook_config: typing.Any = None):
        self._facebook_config = facebook_config
        return self

    def set_business_owner_id(self, business_owner_id: typing.AnyStr = None):
        self._business_owner_id = business_owner_id
        return self

    def set_date_stop(self, date_stop: typing.Union[datetime, typing.AnyStr] = None):
        self._date_stop = date_stop
        return self

    def set_time_interval(self, time_interval: DaysEnum = None):
        self._time_interval = time_interval
        return self

    def set_debug_mode(self, debug: bool = None):
        self._debug = debug
        return self
