from dataclasses import asdict
from math import ceil
from typing import Dict, Union

import humps
from bson import ObjectId

from Core.Dexter.Infrastructure.Domain.LevelEnums import LevelEnum, LevelIdKeyEnum
from Core.Dexter.Infrastructure.Domain.Recommendations.RecommendationEnums import RecommendationStatusEnum
from Core.Dexter.Infrastructure.Domain.Recommendations.RecommendationFields import (
    RecommendationField,
    StructureTreeField,
)
from Core.mongo_adapter import MongoOperator, MongoProjectionState, MongoRepositoryBase
from Core.Web.FacebookGraphAPI.AccountAlteringRestrictions import allow_structure_changes
from Core.Web.FacebookGraphAPI.GraphAPI.GraphAPISdkBase import GraphAPISdkBase
from FacebookDexter.Api.Commands.RecommendationPageCommand import NumberOfPagesCommand, RecommendationPageCommand
from FacebookDexter.Api.startup import config, fixtures
from FacebookDexter.Infrastructure.DexterApplyActions.ApplyTypes import get_apply_action
from FacebookDexter.Infrastructure.DexterApplyActions.RecommendationApplyActions import ApplyButtonType
from FacebookDexter.Infrastructure.DexterRules.BreakdownAndAudiencesTemplates import HIDDEN_INTERESTS_MESSAGE
from FacebookDexter.Infrastructure.DexterRules.DexterOuputFormat import get_formatted_message, get_output_enum
from FacebookDexter.Infrastructure.DexterRules.OverTimeTrendTemplates import RecommendationPriority

RECOMMENDATION_FIELDS = [
    RecommendationField.TEMPLATE,
    RecommendationField.BUSINESS_OWNER_ID,
    RecommendationField.BREAKDOWN,
    RecommendationField.ACCOUNT_ID,
    RecommendationField.STRUCTURE_ID,
    RecommendationField.STRUCTURE_NAME,
    RecommendationField.CAMPAIGN_ID,
    RecommendationField.CAMPAIGN_NAME,
    RecommendationField.METRICS,
    RecommendationField.LEVEL,
    RecommendationField.PRIORITY,
    RecommendationField.TRIGGER_VARIANCE,
    RecommendationField.TIME_INTERVAL,
    RecommendationField.OBJECT_ID,
    RecommendationField.CHANNEL,
    RecommendationField.UNDERPERFORMING_BREAKDOWNS,
    RecommendationField.HIDDEN_INTERESTS,
    RecommendationField.APPLY_PARAMETERS,
    RecommendationField.IS_LABS,
    RecommendationField.PIXEL_ID,
    RecommendationField.ALGORITHM_TYPE,
]

UNUSED_FE_FIELDS = [
    RecommendationField.TEMPLATE,
    RecommendationField.TRIGGER_VARIANCE,
    RecommendationField.ACCOUNT_ID,
    RecommendationField.OBJECT_ID,
    RecommendationField.HIDDEN_INTERESTS,
    RecommendationField.APPLY_PARAMETERS,
]


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


def apply_recommendation(recommendation_id: str, business_owner_id: str):
    recommendation_repository = MongoRepositoryBase(
        config=config.mongo,
        database_name=config.mongo.recommendations_database_name,
        collection_name=config.mongo.recommendations_collection_name,
    )

    query_filter = {
        MongoOperator.AND.value: [
            {RecommendationField.OBJECT_ID.value: {MongoOperator.EQUALS.value: ObjectId(recommendation_id)}},
            {RecommendationField.STATUS.value: RecommendationStatusEnum.ACTIVE.value},
            {RecommendationField.BUSINESS_OWNER_ID.value: business_owner_id},
        ]
    }

    db_result = recommendation_repository.get(
        query_filter,
        projection={m.value: MongoProjectionState.ON.value for m in RECOMMENDATION_FIELDS},
    )

    if not db_result:
        raise Exception("Recommendation was not found")

    recommendation = db_result[0]

    template_key = recommendation.get(RecommendationField.TEMPLATE.value)

    # if not allow_structure_changes(recommendation[RecommendationField.ACCOUNT_ID.value].replace("act_", ""), config):
    #     raise {"message": "CannotAlterStructureForCurrentEnvironmentAndAdAccount"}

    output_enum = get_output_enum(template_key)

    if not output_enum:
        raise Exception("Recommendation template key not valid")

    dexter_output = output_enum[template_key].value

    return (
        recommendation,
        recommendation_repository,
        query_filter,
        dexter_output,
    )


def perform_recommendation_action(
    recommendation, recommendation_repository, query_filter, business_owner_id, headers, dexter_output, command
):
    apply_button_type = ApplyButtonType(command.apply_button_type)
    permanent_token = fixtures.business_owner_repository.get_permanent_token(business_owner_id)

    _ = GraphAPISdkBase(config.facebook, permanent_token)

    # Get the specific action instance and let it deal with the action
    apply_action = get_apply_action(dexter_output.apply_action_type, config, fixtures)
    success_feedback = apply_action.process_action(recommendation, headers, apply_button_type, command=asdict(command))

    # In the end, mark the recommendation as applied
    query = {
        MongoOperator.SET.value: {
            RecommendationField.STATUS.value: RecommendationStatusEnum.APPLIED.value,
        }
    }
    recommendation_repository.update_one(query_filter, query)

    return success_feedback


def get_number_of_pages(command: NumberOfPagesCommand, business_owner_id: str):
    recommendation_repository = MongoRepositoryBase(
        config=config.mongo,
        database_name=config.mongo.recommendations_database_name,
        collection_name=config.mongo.recommendations_collection_name,
    )
    on_metrics = ["_id"]

    query = _get_recommendations_query(command, business_owner_id)

    result = recommendation_repository.get(
        query=query,
        projection={m: MongoProjectionState.ON.value for m in on_metrics},
    )

    return humps.camelize(dict(number_of_pages=ceil(len(result) / command.page_size)))


def read_recommendations_page(command: RecommendationPageCommand, business_owner_id: str):
    skipped_entries = (command.page_number - 1) * command.page_size

    recommendation_repository = MongoRepositoryBase(
        config=config.mongo,
        database_name=config.mongo.recommendations_database_name,
        collection_name=config.mongo.recommendations_collection_name,
    )

    query = _get_recommendations_query(command, business_owner_id)

    result = recommendation_repository.get_data_slice(
        query=query,
        projection={m.value: MongoProjectionState.ON.value for m in RECOMMENDATION_FIELDS},
        limit=command.page_size,
        skip=skipped_entries,
        sort_query=[(RecommendationField.PRIORITY.value, -1)],
    )

    recommendations = [_convert_db_entry_to_recommendation(entry) for entry in result]

    if command.structure_filter:
        command.structure_filter = None

        query = _get_recommendations_query(command, business_owner_id)
        result = recommendation_repository.get_data_slice(
            query=query,
            projection={m.value: MongoProjectionState.ON.value for m in RECOMMENDATION_FIELDS},
            limit=command.page_size,
            skip=skipped_entries,
            sort_query=[(RecommendationField.PRIORITY.value, -1)],
        )

    recommendations_structure_tree = _get_recommendations_structure_tree(result)

    return dict(
        recommendations=humps.camelize(recommendations),
        recommendations_structure_tree=humps.camelize(recommendations_structure_tree),
    )


def _convert_db_entry_to_recommendation(entry: Dict) -> Dict:
    output_enum = get_output_enum(entry[RecommendationField.TEMPLATE.value])
    if not output_enum:
        return {}

    output_value = output_enum[entry[RecommendationField.TEMPLATE.value]].value

    entry[RecommendationField.ANALYSIS.value] = get_formatted_message(
        entry[RecommendationField.TEMPLATE.value],
        trigger_variance=entry.get(RecommendationField.TRIGGER_VARIANCE.value),
        no_of_days=entry.get(RecommendationField.TIME_INTERVAL.value),
        underperforming_breakdowns=entry.get(RecommendationField.UNDERPERFORMING_BREAKDOWNS.value),
        pixel_id=entry.get(RecommendationField.PIXEL_ID.value),
        structure_name=entry.get(RecommendationField.STRUCTURE_NAME.value),
    )

    entry[RecommendationField.PRIORITY.value] = RecommendationPriority(
        entry[RecommendationField.PRIORITY.value]
    ).name.title()

    entry[RecommendationField.TITLE.value] = output_value.title
    entry[RecommendationField.SUBTEXT.value] = output_value.subtext
    entry[RecommendationField.QUOTE.value] = output_value.quote.format(
        pixel_id=entry.get(RecommendationField.PIXEL_ID.value)
    )
    entry[RecommendationField.AD_ACCOUNT_ID.value] = entry[RecommendationField.ACCOUNT_ID.value]
    entry[RecommendationField.RECOMMENDATION_ID.value] = str(entry[RecommendationField.OBJECT_ID.value])
    entry[RecommendationField.IS_APPLICABLE.value] = RecommendationField.APPLY_PARAMETERS.value in entry

    if output_value.apply_action_type:
        entry[RecommendationField.APPLY_TOOLTIP.value] = output_value.apply_action_type.value.APPLY_TOOLTIP.format(
            level=entry[RecommendationField.LEVEL.value]
        )

    hidden_interests = entry.get(RecommendationField.HIDDEN_INTERESTS.value)
    if hidden_interests:
        entry[RecommendationField.QUOTE.value] = entry[
            RecommendationField.QUOTE.value
        ] + HIDDEN_INTERESTS_MESSAGE.format(hidden_interests=hidden_interests)

    _pop_ununsed_fields(entry)

    return entry


def _pop_ununsed_fields(entry: Dict) -> None:
    for field in UNUSED_FE_FIELDS:
        entry.pop(field.value, None)


def _get_recommendations_structure_tree(recommendations: list):
    structure_tree = []
    for recommendation in recommendations:
        parent_index = next(
            (
                i
                for i, structure in enumerate(structure_tree)
                if structure[StructureTreeField.CAMPAIGN_ID.value]
                == recommendation[RecommendationField.CAMPAIGN_ID.value]
            ),
            None,
        )

        if recommendation[RecommendationField.LEVEL.value] == LevelEnum.CAMPAIGN.value:
            if not parent_index:
                structure_tree.append(_create_campaign_node(recommendation))

        elif recommendation[RecommendationField.LEVEL.value] == LevelEnum.ADSET.value:
            if parent_index:
                adset_child_list = structure_tree[parent_index][StructureTreeField.ADSETS.value]
                adset_index = next(
                    (
                        i
                        for i, adset in enumerate(adset_child_list)
                        if adset[StructureTreeField.ADSET_ID.value]
                        == recommendation[RecommendationField.STRUCTURE_ID.value]
                    ),
                    None,
                )
                if not adset_index:
                    adset_child_list.append(_create_adset_node(recommendation))
            else:
                structure_tree.append(_create_campaign_node(recommendation, _create_adset_node(recommendation)))

    return structure_tree


def _create_campaign_node(recommendation, adsets=None):
    if adsets is None:
        adsets = []
    else:
        adsets = [adsets]
    return {
        StructureTreeField.CAMPAIGN_ID.value: recommendation[RecommendationField.CAMPAIGN_ID.value],
        StructureTreeField.CAMPAIGN_NAME.value: recommendation[RecommendationField.CAMPAIGN_NAME.value],
        StructureTreeField.ADSETS.value: adsets,
    }


def _create_adset_node(recommendation):
    return {
        StructureTreeField.ADSET_ID.value: recommendation[RecommendationField.STRUCTURE_ID.value],
        StructureTreeField.ADSET_NAME.value: recommendation[RecommendationField.STRUCTURE_NAME.value],
    }


def _get_recommendations_query(
    command: Union[NumberOfPagesCommand, RecommendationPageCommand], business_owner_id: str
) -> Dict:
    if command.priorities:
        priorities = [RecommendationPriority[priority.upper()].value for priority in command.priorities]
    else:
        priorities = [x.value for x in RecommendationPriority]

    query = {
        MongoOperator.AND.value: [
            {LevelIdKeyEnum.ACCOUNT.value: {MongoOperator.EQUALS.value: command.ad_account_id}},
            {RecommendationField.PRIORITY.value: {MongoOperator.IN.value: priorities}},
            {RecommendationField.STATUS.value: RecommendationStatusEnum.ACTIVE.value},
            {RecommendationField.BUSINESS_OWNER_ID.value: business_owner_id},
            {RecommendationField.IS_LABS.value: command.is_labs},
        ]
    }

    if command.level:
        query[MongoOperator.AND.value].append({RecommendationField.LEVEL.value: command.level})

    if command.structure_ids:
        query[MongoOperator.AND.value].append(
            {RecommendationField.STRUCTURE_ID.value: {MongoOperator.IN.value: command.structure_ids}}
        )

    if command.labs_filter:
        query[MongoOperator.AND.value].append(
            {RecommendationField.ALGORITHM_TYPE.value: {MongoOperator.IN.value: command.labs_filter}}
        )

    if command.structure_filter:
        if command.structure_filter["structure_level"] == LevelEnum.CAMPAIGN.value:
            query[MongoOperator.AND.value].append(
                {RecommendationField.CAMPAIGN_ID.value: command.structure_filter["structure_id"]}
            )
        elif command.structure_filter["structure_level"] == LevelEnum.ADSET.value:
            query[MongoOperator.AND.value].append(
                {RecommendationField.STRUCTURE_ID.value: command.structure_filter["structure_id"]}
            )

    return query
