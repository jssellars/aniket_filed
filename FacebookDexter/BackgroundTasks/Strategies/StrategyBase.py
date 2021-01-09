import logging
from dataclasses import dataclass
from typing import ClassVar, List, Optional

from Core.Dexter.Infrastructure.Domain.LevelEnums import LevelEnum
from Core.Web.FacebookGraphAPI.Models.FieldsMetadata import FieldsMetadata
from FacebookDexter.BackgroundTasks.Strategies.StrategyTimeBucket import StrategyTimeBucket, TrendEnum

logger = logging.getLogger(__name__)


@dataclass
class BreakdownData:
    breakdown_group: str
    data_points: List[float]
    total: Optional[float] = None


@dataclass
class DexterGroupedData:
    no_of_days: int
    metric_name: str
    breakdown_data: List[BreakdownData]

    def get_breakdown_datapoints(self, breakdown: str) -> Optional[List[float]]:
        for breakdown_point in self.breakdown_data:
            if breakdown_point.breakdown_group == breakdown:
                return breakdown_point.data_points

        return None

    def get_breakdown_total(self, breakdown: str) -> Optional[float]:
        for breakdown_point in self.breakdown_data:
            if breakdown_point.breakdown_group == breakdown:
                return breakdown_point.total

        return None

    def get_breakdowns(self) -> List[str]:
        result = set()
        for breakdown_point in self.breakdown_data:
            result.add(breakdown_point.breakdown_group)

        return list(result)


def get_group_data_from_list(
    grouped_data: List[DexterGroupedData], metric_name: str, no_of_days: int
) -> Optional[DexterGroupedData]:
    for data_group in grouped_data:
        if data_group.no_of_days == no_of_days and data_group.metric_name == metric_name:
            return data_group

    return None


def get_number_of_days(grouped_data: List[DexterGroupedData], metric_name: str):
    result = []

    for data_group in grouped_data:
        if data_group.metric_name == metric_name:
            result.append(data_group.no_of_days)

    return result


@dataclass
class DexterStrategyBase:
    ALGORITHM: ClassVar[str] = "Base_Algorithm"
    levels: List[LevelEnum]
    breakdowns: List[FieldsMetadata]
    action_breakdowns: List[FieldsMetadata]
    time_buckets: List[StrategyTimeBucket]

    def trend(self, reference_data: List[float], current_data: List[float]) -> Optional[TrendEnum]:
        raise NotImplementedError

    def variance(
        self, reference_data: List[float], current_data: List[float], trend: Optional[TrendEnum] = None
    ) -> Optional[float]:
        raise NotImplementedError

    def generate_recommendation(self, *args):
        raise NotImplementedError
