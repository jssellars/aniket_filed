from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum
from typing import ClassVar, Optional

from Core.constants import DEFAULT_DATETIME_ISO
from Core.Dexter.Infrastructure.Domain.Recommendations.RecommendationFields import RecommendationField
from Core.mongo_adapter import MongoOperator, MongoRepositoryBase, filter_null_values_from_documents
from FacebookDexter.Infrastructure.DexterApplyActions.ApplyTypes import ApplyActionType

TIMEDELTA_FOR_NEW_RECOMMENDATIONS = 15


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
        recommendation_entry = kwargs[self.RECOMMENDATION_ENTRY_MODEL]
        structure_id = recommendation_entry.get(RecommendationField.STRUCTURE_ID.value)
        recommendation_template = recommendation_entry.get(RecommendationField.TEMPLATE.value)

        query = {
            MongoOperator.AND.value: [
                {RecommendationField.STRUCTURE_ID.value: structure_id},
                {RecommendationField.TEMPLATE.value: recommendation_template},
                {
                    RecommendationField.CREATED_AT.value: {
                        MongoOperator.GREATERTHAN.value: (
                            datetime.now() - timedelta(days=TIMEDELTA_FOR_NEW_RECOMMENDATIONS)
                        ).isoformat()
                    }
                },
            ]
        }

        historical_recommendations = output_repository.get(query)
        if historical_recommendations:
            return

        result = filter_null_values_from_documents([recommendation_entry])
        output_repository.add_one(result[0])
