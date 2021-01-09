from Core.Dexter.Infrastructure.Domain.DexterJournalEnums import DexterEngineRunJournalEnum
from Core.Dexter.Infrastructure.Domain.LevelEnums import LevelIdKeyEnum

from Core.mongo_adapter import MongoOperator, MongoRepositoryBase, MongoProjectionState
from FacebookDexter.Api.Commands.DexterApiGetCountsByCategoryCommand import DexterApiGetCountsByCategoryCommand
from FacebookDexter.Api.startup import config
from FacebookDexter.Infrastructure.Domain.Recommendations.RecommendationCategory import RecommendationCategory
from FacebookDexter.Infrastructure.Domain.Recommendations.RecommendationType import RecommendationType


# TODO: This will be deleted for V1 once the FE team finishes the new interface
def get_categories_count(command: DexterApiGetCountsByCategoryCommand):
    recommendation_repository = MongoRepositoryBase(
        config=config.mongo,
        database_name=config.mongo.recommendations_database_name,
        collection_name=config.mongo.recommendations_collection_name,
    )

    result = dict()
    for recommendation_type in RecommendationType:
        result[recommendation_type.value] = 0

    for recommendation_category in RecommendationCategory:
        result[recommendation_category.value] = 0

    on_metrics = [
        LevelIdKeyEnum.CAMPAIGN.value,
    ]
    off_metrics = ["_id"]

    repo_result = recommendation_repository.get(
        query={
            MongoOperator.AND.value: [
                {
                    LevelIdKeyEnum.CAMPAIGN.value: {
                        MongoOperator.IN.value: command.campaign_ids
                    }
                },
                {
                    DexterEngineRunJournalEnum.CHANNEL.value: {
                        MongoOperator.EQUALS.value: command.channel
                    }
                },
            ]
        },
        projection={
            **{m: MongoProjectionState.OFF.value for m in off_metrics},
            **{m: MongoProjectionState.ON.value for m in on_metrics},
        },
    )

    result[RecommendationCategory.OPTIMIZE_BUDGET.value] = len(repo_result)
    result[RecommendationType.PERFORMANCE.value] = len(repo_result)

    return result
