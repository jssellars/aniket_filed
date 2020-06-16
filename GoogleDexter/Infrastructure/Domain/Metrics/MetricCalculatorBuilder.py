import typing
from datetime import datetime

from GoogleDexter.Infrastructure.Domain.Breakdowns import BreakdownMetadata
from GoogleDexter.Infrastructure.Domain.DaysEnum import DaysEnum
from GoogleDexter.Infrastructure.Domain.LevelEnums import LevelEnum
from GoogleDexter.Infrastructure.Domain.Metrics.Metric import Metric
from GoogleDexter.Infrastructure.PersistanceLayer.DexterMongoRepository import DexterMongoRepository


class MetricCalculatorBuilder:

    def __init__(self):
        self._structure_id = None
        self._metric = None
        self._level = None
        self._breakdown_metadata = None
        self._repository = None
        self._fuzzyfier_factory = None
        self._business_owner_id = None
        self._permanent_token = None
        self._metrics = None
        self._business_owner_repo_session = None
        self._date_stop = datetime.now()
        self._time_interval = None

    def set_fuzzyfier_factory(self, fuzzyfier_factory: typing.Any) -> typing.Any:
        self._fuzzyfier_factory = fuzzyfier_factory
        return self

    def set_metric(self, metric: Metric = None) -> typing.Any:
        self._metric = metric
        return self

    def set_breakdown_metadata(self, breakdown_metadata: BreakdownMetadata = None) -> typing.Any:
        self._breakdown_metadata = breakdown_metadata
        return self

    def set_repository(self, repository: DexterMongoRepository = None) -> typing.Any:
        self._repository = repository
        return self

    def set_structure_id(self, structure_id: typing.AnyStr = None) -> typing.Any:
        self._structure_id = structure_id
        return self

    def set_level(self, level: LevelEnum = None) -> typing.Any:
        self._level = level
        return self

    def set_business_owner_id(self, business_owner_id: str = None) -> typing.Any:
        self._business_owner_id = business_owner_id
        return self

    def set_business_owner_repo_session(self, business_owner_repo_session: typing.Any = None) -> typing.Any:
        self._business_owner_repo_session = business_owner_repo_session
        return self

    def set_date_stop(self, date_stop: str = None) -> typing.Any:
        self._date_stop = date_stop
        return self

    def set_time_interval(self, time_interval: DaysEnum = None) -> typing.Any:
        self._time_interval = time_interval
        return self
