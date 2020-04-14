import typing

from FacebookDexter.Infrastructure.Domain.Metrics.MetricCalculator import MetricCalculator
from FacebookDexter.Infrastructure.Domain.Rules.RuleBase import RuleBase
from FacebookDexter.Infrastructure.PersistanceLayer.DexterMongoRepository import DexterMongoRepository


class RuleEvaluatorBuilder:
    def __init__(self, facebook_id: typing.AnyStr = None, rule: RuleBase = None):
        self.__facebook_id = facebook_id
        self.__rule = rule
        self.__metric_calculator = MetricCalculator(facebook_id=facebook_id, level=rule.level)

        self.__breakdown_metadata = None

    def set_id_and_rule(self, facebook_id: typing.AnyStr = None, rule: RuleBase = None) -> typing.Any:
        self.__facebook_id = facebook_id
        self.__rule = rule
        return self

    def set_facebook_id(self, facebook_id: typing.AnyStr = None) -> typing.Any:
        self.__facebook_id = facebook_id
        return self

    def set_rule(self, rule: RuleBase = None) -> typing.Any:
        self.__rule = rule
        return self

    def set_fuzzyfier_factory(self, fuzzyfier_factory: typing.Any) -> typing.Any:
        self.__metric_calculator.set_fuzzyfier_factory(fuzzyfier_factory)
        return self

    def set_metric_calculator_repository(self, repository: DexterMongoRepository = None) -> typing.Any:
        self.__metric_calculator.set_repository(repository)
        return self
