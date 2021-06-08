from dataclasses import dataclass
from typing import ClassVar, Dict, List, Tuple

from Core.Dexter.Infrastructure.Domain.LevelEnums import LevelEnum, LevelIdKeyEnum
from Core.Web.FacebookGraphAPI.Models.FieldsMetadata import FieldsMetadata
from FacebookDexter.Infrastructure.PersistanceLayer.StrategyJournalMongoRepository import (
    ReportRecommendationDataModel,
    StructureRecommendationModel,
)


@dataclass
class DexterLabsStrategyBase:
    ALGORITHM: ClassVar[str] = "Base_Algorithm"
    levels: List[LevelEnum]

    def generate_recommendation(self, *args):
        raise NotImplementedError

    def get_pixel_audiences(self, account_id):
        pass

    def get_audience_by_rule(self, pixel_audiences):
        pass

    @staticmethod
    def get_structure_and_reports_data(
        business_owner: str, account_id: str, structure: Dict, level: LevelEnum, pixel_id: str
    ) -> StructureRecommendationModel:
        structure_key = LevelIdKeyEnum[level.value.upper()].value

        structure_data = StructureRecommendationModel(
            business_owner,
            f"act_{account_id}",
            structure[structure_key],
            structure[f"{level.value}_name"],
            structure[FieldsMetadata.campaign_id.name],
            structure[FieldsMetadata.campaign_name.name],
            level.value,
            pixel_id,
        )

        reports_data = ReportRecommendationDataModel(
            [{"display_name": None, "name": None}],
            {},
        )

        return structure_data, reports_data
