import logging
from dataclasses import dataclass
from typing import List, Optional

logger = logging.getLogger(__name__)


@dataclass
class BreakdownData:
    breakdown_key: str
    data_points: List[float]
    total: Optional[float] = None


@dataclass
class BreakdownGroupedData:
    no_of_days: int
    metric_name: str
    breakdown_data: List[BreakdownData]

    def get_breakdown_datapoints(self, breakdown: str) -> Optional[List[float]]:
        for breakdown_point in self.breakdown_data:
            if breakdown_point.breakdown_key == breakdown:
                return breakdown_point.data_points

        return None

    def get_breakdown_total(self, breakdown: str) -> Optional[float]:
        for breakdown_point in self.breakdown_data:
            if breakdown_point.breakdown_key == breakdown:
                return breakdown_point.total

        return None

    def get_breakdowns(self) -> List[str]:
        result = set()
        for breakdown_point in self.breakdown_data:
            result.add(breakdown_point.breakdown_key)

        return list(result)


def get_group_data_from_list(
    grouped_data: List[BreakdownGroupedData], metric_name: str, no_of_days: int
) -> Optional[BreakdownGroupedData]:
    for data_group in grouped_data:
        if data_group.no_of_days == no_of_days and data_group.metric_name == metric_name:
            return data_group

    return None


def get_number_of_days(grouped_data: List[BreakdownGroupedData], metric_name: str):
    result = []

    for data_group in grouped_data:
        if data_group.metric_name == metric_name:
            result.append(data_group.no_of_days)

    return result
