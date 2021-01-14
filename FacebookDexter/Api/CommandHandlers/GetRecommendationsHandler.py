from math import ceil
from typing import Dict, Union

import humps
from bson import ObjectId

from Core.Dexter.Infrastructure.Domain.LevelEnums import LevelIdKeyEnum
from Core.Dexter.Infrastructure.Domain.Recommendations.RecommendationEnums import RecommendationStatusEnum
from Core.Dexter.Infrastructure.Domain.Recommendations.RecommendationFields import RecommendationField
from Core.mongo_adapter import MongoRepositoryBase, MongoProjectionState, MongoOperator
from FacebookDexter.Api.Commands.RecommendationPageCommand import RecommendationPageCommand, NumberOfPagesCommand
from FacebookDexter.Api.startup import config
from FacebookDexter.Infrastructure.DexterRules.BreakdownAndAudiencesTemplates import HIDDEN_INTERESTS_MESSAGE
from FacebookDexter.Infrastructure.DexterRules.DexterOutput import get_formatted_message, get_output_enum
from FacebookDexter.Infrastructure.DexterRules.OverTimeTrendTemplates import RecommendationPriority

ON_METRICS = [
    RecommendationField.TEMPLATE,
    RecommendationField.BREAKDOWN,
    RecommendationField.ACCOUNT_ID,
    RecommendationField.STRUCTURE_ID,
    RecommendationField.STRUCTURE_NAME,
    RecommendationField.METRICS,
    RecommendationField.LEVEL,
    RecommendationField.PRIORITY,
    RecommendationField.TRIGGER_VARIANCE,
    RecommendationField.TIME_INTERVAL,
    RecommendationField.OBJECT_ID,
    RecommendationField.CHANNEL,
    RecommendationField.BREAKDOWN_GROUP,
    RecommendationField.HIDDEN_INTERESTS,
]


def get_number_of_pages(command: NumberOfPagesCommand):
    recommendation_repository = MongoRepositoryBase(
        config=config.mongo,
        database_name=config.mongo.recommendations_database_name,
        collection_name=config.mongo.recommendations_collection_name,
    )
    on_metrics = ["_id"]

    query = get_query(command)

    result = recommendation_repository.get(
        query=query,
        projection={
            **{m: MongoProjectionState.ON.value for m in on_metrics},
        },
    )

    return humps.camelize(dict(number_of_pages=ceil(len(result) / command.page_size)))


def read_recommendations_page(command: RecommendationPageCommand):
    skipped_entries = (command.page_number - 1) * command.page_size

    recommendation_repository = MongoRepositoryBase(
        config=config.mongo,
        database_name=config.mongo.recommendations_database_name,
        collection_name=config.mongo.recommendations_collection_name,
    )

    query = get_query(command)

    result = recommendation_repository.get_data_slice(
        query=query,
        projection={
            **{m.value: MongoProjectionState.ON.value for m in ON_METRICS},
        },
        limit=command.page_size,
        skip=skipped_entries,
        sort_query=[(RecommendationField.PRIORITY.value, -1)],
    )

    result = [convert_db_entry_to_recommendation(entry) for entry in result]

    return dict(recommendations=humps.camelize(result))


def convert_db_entry_to_recommendation(entry: Dict) -> Dict:
    output_enum = get_output_enum(entry[RecommendationField.TEMPLATE.value])
    if not output_enum:
        return {}

    output_value = output_enum[entry[RecommendationField.TEMPLATE.value]].value

    entry[RecommendationField.ANALYSIS.value] = get_formatted_message(
        entry[RecommendationField.TEMPLATE.value],
        trigger_variance=entry.get(RecommendationField.TRIGGER_VARIANCE.value),
        no_of_days=entry.get(RecommendationField.TIME_INTERVAL.value),
        breakdown_group=entry.get(RecommendationField.BREAKDOWN_GROUP.value),
    )

    entry[RecommendationField.PRIORITY.value] = RecommendationPriority(
        entry[RecommendationField.PRIORITY.value]
    ).name.title()

    entry[RecommendationField.TITLE.value] = output_value[2]
    entry[RecommendationField.SUBTEXT.value] = output_value[3]
    entry[RecommendationField.QUOTE.value] = output_value[4]
    entry[RecommendationField.AD_ACCOUNT_ID.value] = entry[RecommendationField.ACCOUNT_ID.value]
    entry[RecommendationField.RECOMMENDATION_ID.value] = str(entry[RecommendationField.OBJECT_ID.value])

    hidden_interests = entry.get(RecommendationField.HIDDEN_INTERESTS.value)
    if hidden_interests:
        entry[RecommendationField.QUOTE.value] = (
                entry[RecommendationField.QUOTE.value]
                + HIDDEN_INTERESTS_MESSAGE.format(hidden_interests=hidden_interests)
        )

    pop_ununsed_fields(entry)

    return entry


def pop_ununsed_fields(entry: Dict) -> None:
    entry.pop(RecommendationField.TEMPLATE.value)
    entry.pop(RecommendationField.TRIGGER_VARIANCE.value)
    entry.pop(RecommendationField.ACCOUNT_ID.value)
    entry.pop(RecommendationField.OBJECT_ID.value)
    entry.pop(RecommendationField.BREAKDOWN_GROUP.value)
    entry.pop(RecommendationField.HIDDEN_INTERESTS.value)


def get_query(command: Union[NumberOfPagesCommand, RecommendationPageCommand]) -> Dict:
    if command.priorities:
        priorities = [RecommendationPriority[priority.upper()].value for priority in command.priorities]
    else:
        priorities = [x.value for x in RecommendationPriority]

    query = {
        MongoOperator.AND.value: [
            {LevelIdKeyEnum.ACCOUNT.value: {MongoOperator.EQUALS.value: command.ad_account_id}},
            {RecommendationField.PRIORITY.value: {MongoOperator.IN.value: priorities}},
            {RecommendationField.STATUS.value: RecommendationStatusEnum.ACTIVE.value},
        ]
    }

    if command.level:
        query[MongoOperator.AND.value].append(
            {RecommendationField.LEVEL.value: {MongoOperator.EQUALS.value: command.level}}
        )

    return query


def dismiss_recommendation(recommendation_id: str):
    recommendation_repository = MongoRepositoryBase(
        config=config.mongo,
        database_name=config.mongo.recommendations_database_name,
        collection_name=config.mongo.recommendations_collection_name,
    )

    query_filter = {RecommendationField.OBJECT_ID.value: {MongoOperator.EQUALS.value: ObjectId(recommendation_id)}}
    query = {
        MongoOperator.SET.value: {
            RecommendationField.STATUS.value: RecommendationStatusEnum.DISMISSED.value,
        }
    }
    recommendation_repository.update_one(query_filter, query)

    return
