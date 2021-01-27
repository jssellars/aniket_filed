from dataclasses import dataclass
from enum import Enum
from typing import ClassVar, Optional

from Core.mongo_adapter import MongoRepositoryBase, filter_null_values_from_documents
from FacebookDexter.Infrastructure.DexterRules.RecommendationApplyActions import ApplyActionType


class RecommendationPriority(Enum):
    HIGH = 3
    MEDIUM = 2
    LOW = 1


@dataclass
class DexterOutput:
    analysis: str
    priority: RecommendationPriority
    title: str
    subtext: str
    quote: str
    apply_action_type: Optional[ApplyActionType] = None

    RECOMMENDATION_ENTRY_MODEL: ClassVar[str] = "recommendation_entry_model"

    def process_output(self, output_repository: MongoRepositoryBase, **kwargs):
        raise NotImplementedError


@dataclass
class DexterRecommendationOutput(DexterOutput):
    trigger_variance: Optional[float] = None
    no_of_days: Optional[int] = None

    def process_output(self, output_repository: MongoRepositoryBase, **kwargs):
        result = filter_null_values_from_documents([kwargs[self.RECOMMENDATION_ENTRY_MODEL]])
        output_repository.add_one(result[0])
