import logging
from dataclasses import dataclass
from typing import ClassVar, Dict, List, Optional, Tuple

from Core.Dexter.Infrastructure.Domain.LevelEnums import LevelEnum, LevelIdKeyEnum
from Core.Web.FacebookGraphAPI.Models.FieldsMetadata import FieldsMetadata
from FacebookDexter.BackgroundTasks.Strategies.StrategyTimeBucket import StrategyTimeBucket, TrendEnum
from FacebookDexter.Infrastructure.DexterRules.RecommendationApplyActions import ApplyActionType
from FacebookDexter.Infrastructure.PersistanceLayer.StrategyJournalMongoRepository import (
    ReportRecommendationDataModel,
    StructureRecommendationModel,
)

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

    @staticmethod
    def get_structure_and_reports_data(
        business_owner: str,
        account_id: str,
        structure: Dict,
        level: LevelEnum,
        metric_name: str,
        breakdown: FieldsMetadata,
    ) -> Tuple[StructureRecommendationModel, ReportRecommendationDataModel]:
        structure_key = LevelIdKeyEnum[level.value.upper()].value

        structure_data = StructureRecommendationModel(
            business_owner,
            f"act_{account_id}",
            structure[structure_key],
            structure[f"{level.value}_name"],
            structure[FieldsMetadata.campaign_id.name],
            structure[FieldsMetadata.campaign_name.name],
            level.value,
        )

        reports_data = ReportRecommendationDataModel(
            [{"display_name": metric_name.replace("_", " ").title(), "name": metric_name}],
            {"display_name": breakdown.name.replace("_", " ").title(), "name": breakdown.name},
        )

        return structure_data, reports_data
