import typing

from FacebookDexter.Infrastructure.Domain.Breakdowns import BreakdownMetadata
from FacebookDexter.Infrastructure.Domain.LevelEnums import LevelEnum
from FacebookDexter.Infrastructure.Domain.Metrics.Metric import Metric
from FacebookDexter.Infrastructure.PersistanceLayer.DexterMongoRepository import DexterMongoRepository


class MetricCalculatorBuilder:
    def __init__(self,
                 facebook_id: typing.AnyStr = None,
                 metric: Metric = None,
                 level: LevelEnum = None,
                 breakdown_metadata: BreakdownMetadata = None,
                 mongo_repository: DexterMongoRepository = None,
                 fuzzyfier_factory: typing.Any = None):
        self.__facebook_id = facebook_id
        self.__metric = metric
        self.__level = level
        self.__breakdown_metadata = breakdown_metadata
        self.__repository = mongo_repository
        self.__fuzzyfier_factory = fuzzyfier_factory
        self.__metrics = None

    def set_fuzzyfier_factory(self, fuzzyfier_factory: typing.Any) -> typing.Any:
        self.__fuzzyfier_factory = fuzzyfier_factory
        return self

    def set_metric(self, metric: Metric = None) -> typing.Any:
        self.__metric = metric
        return self

    def set_breakdown_metadata(self, breakdown_metadata: BreakdownMetadata = None) -> typing.Any:
        self.__breakdown_metadata = breakdown_metadata
        return self

    def set_repository(self, repository: DexterMongoRepository = None) -> typing.Any:
        self.__repository = repository
        return self

    def set_facebook_id(self, facebook_id: typing.AnyStr = None) -> typing.Any:
        self.__facebook_id = facebook_id
        return self

    def set_level(self, level: LevelEnum = None) -> typing.Any:
        self.__level = level
        return self
