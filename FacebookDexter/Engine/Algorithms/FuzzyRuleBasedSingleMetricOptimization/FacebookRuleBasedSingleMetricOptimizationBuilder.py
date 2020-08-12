import typing
from datetime import datetime

from Core.Dexter.Infrastructure.Domain.DaysEnum import DaysEnum
from Core.Dexter.Infrastructure.Domain.LevelEnums import LevelEnum
from Core.Tools.Logger.MongoLoggers.MongoLogger import MongoLogger
from FacebookDexter.Engine.Algorithms.FuzzyRuleBasedSingleMetricOptimization.FacebookRuleBasedSingleMetricFuzzyfierFactory import \
    FacebookRuleBasedSingleMetricFuzzyfierFactory
from FacebookDexter.Engine.Algorithms.FuzzyRuleBasedSingleMetricOptimization.Rules import Rules
from FacebookDexter.Infrastructure.Domain.Rules.FacebookRuleEvaluator import FacebookRuleEvaluator
from FacebookDexter.Infrastructure.PersistanceLayer.FacebookDexterMongoRepository import \
    FacebookDexterMongoRepository


class FacebookRuleBasedSingleMetricOptimizationBuilder:

    def __init__(self):
        self._mongo_repository = None
        self._rules = None
        self._business_owner_repo_session = None
        self._facebook_config = None
        self._business_owner_id = None
        self._external_services = None
        self._rule_evaluator = None
        self._fuzzyfier_factory = None
        self._level = None
        self._dexter_config = None
        self.__logger = None
        self._date_stop = None
        self._time_interval = None
        self._debug = None
        self._mongo_config = None
        self._auth_token = None
        self._minimum_number_of_data_points_dict = None

    def get_logger(self):
        if self._mongo_repository is not None:
            self.__logger = MongoLogger(repository=self._mongo_repository,
                                        database_name=self._mongo_repository.config.logs_database)
        return self.__logger

    def set_business_owner_id(self, business_owner_id: typing.Any = None):
        self._business_owner_id = business_owner_id
        return self

    def set_business_owner_repo_session(self, business_owner_repo_session: typing.Any = None):
        self._business_owner_repo_session = business_owner_repo_session
        return self

    def set_facebook_config(self, facebook_config: typing.Any = None):
        self._facebook_config = facebook_config
        return self

    def set_external_services(self, external_services: typing.Any = None):
        self._external_services = external_services
        return self

    def set_repository(self, repository: FacebookDexterMongoRepository = None):
        self._mongo_repository = repository
        return self

    def set_rules(self, rules: Rules = None):
        self._rules = rules
        return self

    def set_fuzzyfier_factory(self, fuzzyfier_factory: FacebookRuleBasedSingleMetricFuzzyfierFactory = None):
        self._fuzzyfier_factory = fuzzyfier_factory
        return self

    def set_rule_evaluator(self, rule_evaluator: FacebookRuleEvaluator = None):
        self._rule_evaluator = rule_evaluator
        return self

    def set_level(self, level: LevelEnum = None):
        self._level = level
        return self

    def set_dexter_config(self, dexter_config: typing.Any = None):
        self._dexter_config = dexter_config
        return self

    def set_date_stop(self, date_stop: datetime = None):
        self._date_stop = date_stop
        return self

    def set_time_interval(self, time_interval: DaysEnum = None):
        self._time_interval = time_interval
        return self

    def set_debug_mode(self, debug):
        self._debug = debug
        return self

    def set_mongo_config(self, mongo_config: typing.Any = None):
        self._mongo_config = mongo_config
        return self

    def create_mongo_repository(self):
        self._mongo_repository = FacebookDexterMongoRepository(config=self._mongo_config)
        return self

    def close_mongo_repository(self):
        self._mongo_repository.close()
        return self

    def set_auth_token(self, auth_token: typing.AnyStr = None):
        self._auth_token = auth_token
        return self

    def set_minimum_number_of_data_points_dict(self, minimum_number_of_data_points_dict: dict = None):
        self._minimum_number_of_data_points_dict = minimum_number_of_data_points_dict
        return self
