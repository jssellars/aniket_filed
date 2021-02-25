import logging
from dataclasses import dataclass
from typing import ClassVar, Dict, List, Optional, Tuple

from Core.Dexter.Infrastructure.Domain.LevelEnums import LevelEnum, LevelIdKeyEnum
from Core.Web.FacebookGraphAPI.Models.FieldsMetadata import FieldsMetadata
from FacebookDexter.Infrastructure.DexterRules.OverTimeTrendBuckets.StrategyTimeBucket import (
    StrategyTimeBucket,
    TrendEnum,
)
from FacebookDexter.Infrastructure.PersistanceLayer.StrategyJournalMongoRepository import (
    ReportRecommendationDataModel,
    StructureRecommendationModel,
)


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
