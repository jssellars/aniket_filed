import typing
from datetime import datetime

from Core.Tools.Logger.MongoLoggers.MongoLogger import MongoLogger
from FacebookDexter.Engine.Algorithms.FuzzyRuleBasedOptimization.Fuzzifiers.RuleBasedOptimizationFuzzyfierFactory import \
    RuleBasedOptimizationFuzzyfierFactory
from FacebookDexter.Engine.Algorithms.FuzzyRuleBasedOptimization.Rules import Rules
from FacebookDexter.Infrastructure.Constants import DEFAULT_DATETIME
from FacebookDexter.Infrastructure.Domain.DaysEnum import DaysEnum
from FacebookDexter.Infrastructure.Domain.LevelEnums import LevelEnum
from FacebookDexter.Infrastructure.Domain.Rules.RuleEvaluator import RuleEvaluator
from FacebookDexter.Infrastructure.PersistanceLayer.DexterMongoRepository import DexterMongoRepository


class RuleBasedOptimizationBuilder:

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

    def set_repository(self, repository: DexterMongoRepository = None):
        self._mongo_repository = repository
        return self

    def set_rules(self, rules: Rules = None):
        self._rules = rules
        return self

    def set_fuzzyfier_factory(self, fuzzyfier_factory: RuleBasedOptimizationFuzzyfierFactory = None):
        self._fuzzyfier_factory = fuzzyfier_factory
        return self

    def set_rule_evaluator(self, rule_evaluator: RuleEvaluator = None):
        self._rule_evaluator = rule_evaluator
        return self

    def set_level(self, level: LevelEnum = None):
        self._level = level
        return self

    def set_dexter_config(self, dexter_config: typing.Any = None):
        self._dexter_config = dexter_config
        return self

    def set_date_stop(self, date_stop: typing.AnyStr = None):
        self._date_stop = datetime.strptime(date_stop, DEFAULT_DATETIME)
        return self

    def set_time_interval(self, time_interval: DaysEnum = None):
        self._time_interval = time_interval
        return self