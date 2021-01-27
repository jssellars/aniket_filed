from typing import Dict

import humps
from bson import ObjectId

from Core.Dexter.Infrastructure.Domain.LevelEnums import LevelIdKeyEnum
from Core.Dexter.Infrastructure.Domain.Recommendations.RecommendationFields import RecommendationField
from Core.mongo_adapter import MongoRepositoryBase, MongoOperator, MongoProjectionState
from FacebookDexter.Api.Commands.DexterApiGetRecommendationsPageCommand import DexterApiGetRecommendationsPageCommand
from FacebookDexter.Api.startup import config
from FacebookDexter.Infrastructure.DexterRules.DexterOuputFormat import get_formatted_message
from FacebookDexter.Infrastructure.Domain.Recommendations.RecommendationType import RecommendationType


def get_recommendations_page(command: DexterApiGetRecommendationsPageCommand):
    recommendation_repository = MongoRepositoryBase(
        config=config.mongo,
        database_name=config.mongo.recommendations_database_name,
        collection_name=config.mongo.recommendations_collection_name,
    )

    on_metrics = [
        RecommendationField.TEMPLATE.value,
        RecommendationField.CAMPAIGN_ID.value,
        RecommendationField.CAMPAIGN_NAME.value,
        RecommendationField.CREATED_AT.value,
        RecommendationField.STRUCTURE_ID.value,
        RecommendationField.STRUCTURE_NAME.value,
        RecommendationField.METRICS.value,
        RecommendationField.LEVEL.value,
        RecommendationField.OBJECT_ID.value,
        RecommendationField.TRIGGER_VARIANCE.value,
        RecommendationField.TIME_INTERVAL.value,
    ]

    # TODO: This is only a workaround until we properly fix the related recommendations endpoint
    if LevelIdKeyEnum.CAMPAIGN.value not in command.recommendation_filter:
        repo_result = []
    else:
        repo_result = recommendation_repository.get(
            query={
                LevelIdKeyEnum.CAMPAIGN.value: {
                    MongoOperator.IN.value: command.recommendation_filter[LevelIdKeyEnum.CAMPAIGN.value]
                }
            },
            projection={
                **{m: MongoProjectionState.ON.value for m in on_metrics},
            },
        )

    count_by_type = {}
    for recommendation_type in RecommendationType:
        count_by_type[recommendation_type.value] = 0

    count_by_type[RecommendationType.PERFORMANCE.value] = len(repo_result)

    recommendations = [convert_db_entry_to_recommendation(entry) for entry in repo_result]

    return dict(count=len(repo_result), recommendations=humps.camelize(recommendations), countsByType=count_by_type)


def get_recommendations_by_id(recommendation_id: str, recommendation_repository: MongoRepositoryBase):
    on_metrics = [
        RecommendationField.TEMPLATE.value,
        RecommendationField.CAMPAIGN_ID.value,
        RecommendationField.CAMPAIGN_NAME.value,
        RecommendationField.CREATED_AT.value,
        RecommendationField.STRUCTURE_ID.value,
        RecommendationField.STRUCTURE_NAME.value,
        RecommendationField.METRICS.value,
        RecommendationField.LEVEL.value,
        RecommendationField.OBJECT_ID.value,
        RecommendationField.TRIGGER_VARIANCE.value,
        RecommendationField.TIME_INTERVAL.value,
    ]

    repo_result = recommendation_repository.get(
        query={RecommendationField.OBJECT_ID.value: ObjectId(recommendation_id)},
        projection={
            **{m: MongoProjectionState.ON.value for m in on_metrics},
        },
    )

    return humps.camelize([convert_db_entry_to_recommendation(entry) for entry in repo_result][0])


def convert_db_entry_to_recommendation(entry: Dict) -> Dict:
    return {
        RecommendationField.TEMPLATE.value: get_formatted_message(
            entry[RecommendationField.TEMPLATE.value],
            trigger_variance=entry.get("trigger_variance", None),
            no_of_days=entry.get("time_interval", None),
            breakdown_group=entry.get("breakdown_group", None),
        ),
        RecommendationField.LEVEL.value: entry[RecommendationField.LEVEL.value],
        RecommendationField.CAMPAIGN_ID.value: entry[RecommendationField.CAMPAIGN_ID.value],
        RecommendationField.CAMPAIGN_NAME.value: entry[RecommendationField.CAMPAIGN_NAME.value],
        RecommendationField.PARENT_NAME.value: entry[RecommendationField.CAMPAIGN_NAME.value],
        RecommendationField.PARENT_ID.value: entry[RecommendationField.CAMPAIGN_ID.value],
        RecommendationField.STRUCTURE_ID.value: entry[RecommendationField.STRUCTURE_ID.value],
        RecommendationField.STRUCTURE_NAME.value: entry[RecommendationField.STRUCTURE_NAME.value],
        RecommendationField.RECOMMENDATION_TYPE.value: RecommendationType.PERFORMANCE.value,
        RecommendationField.CREATED_AT.value: entry[RecommendationField.CREATED_AT.value].isoformat(),
        RecommendationField.SOURCE.value: "Dexter",
        RecommendationField.METRICS.value: entry[RecommendationField.METRICS.value],
        RecommendationField.OBJECT_ID.value.replace("_", ""): str(entry[RecommendationField.OBJECT_ID.value]),
    }
