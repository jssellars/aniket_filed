import typing
from ast import parse
from datetime import datetime, timedelta
from threading import Thread

from bson import BSON
from Core.Dexter.Infrastructure.Domain.LevelEnums import LevelIdKeyEnum
from Core.mongo_adapter import MongoOperator
from Core.Web.FacebookGraphAPI.GraphAPIDomain.GraphAPIInsightsFields import GraphAPIInsightsFields
from Core.Web.FacebookGraphAPI.GraphAPIMappings.ObjectiveToResultsMapper import (
    AdSetOptimizationToResult,
    PixelCustomEventTypeToResult,
)
from Core.Web.FacebookGraphAPI.Models.FieldsMetadata import FieldsMetadata
from FacebookTuring.BackgroundTasks.Orchestrators.InsightsSynchronizer import InsightsSynchronizer
from FacebookTuring.BackgroundTasks.Orchestrators.InsightsSyncronizerBreakdowns import (
    InsightsSynchronizerActionBreakdownEnum,
    InsightsSynchronizerBreakdownEnum,
)
from FacebookTuring.BackgroundTasks.Orchestrators.InsightsSyncronizerFields import (
    FREEMIUM_USER_INSIGHTS_SYNCHRONIZER_FIELDS,
    INSIGHTS_SYNCHRONIZER_FIELDS,
)
from FacebookTuring.BackgroundTasks.Orchestrators.StructuresSyncronizer import StructuresSyncronizer
from FacebookTuring.BackgroundTasks.startup import config, fixtures
from FacebookTuring.BackgroundTasks.SynchronizerConfig import SynchronizerConfigRuntime, SynchronizerConfigStatic
from FacebookTuring.Infrastructure.Domain.AdAccountSyncStatusEnum import AdAccountSyncStatusEnum
from FacebookTuring.Infrastructure.Domain.MiscFieldsEnum import MiscFieldsEnum
from FacebookTuring.Infrastructure.Domain.StructureStatusEnum import StructureStatusEnum
from FacebookTuring.Infrastructure.IntegrationEvents.MessageTypeEnum import UserTypeEnum
from FacebookTuring.Infrastructure.Mappings.LevelMapping import Level, LevelToFacebookIdKeyMapping
from FacebookTuring.Infrastructure.Mappings.StructureMapping import StructureFields
from FacebookTuring.Infrastructure.PersistenceLayer.TuringAdAccountJournalRepository import (
    TuringAdAccountJournalRepository,
)
from FacebookTuring.Infrastructure.PersistenceLayer.TuringMongoRepository import TuringMongoRepository

import logging

logger = logging.getLogger(__name__)


SYNC_DAYS_INTERVAL = 2
DAYS_UNTIL_OBSOLETE = 31
USER_CONFIGS_BY_TYPE = {
    UserTypeEnum.FREEMIUM: SynchronizerConfigStatic(
        levels=[Level.AD],
        breakdowns=list(InsightsSynchronizerBreakdownEnum),
        action_breakdowns=list(InsightsSynchronizerActionBreakdownEnum),
        requested_fields=FREEMIUM_USER_INSIGHTS_SYNCHRONIZER_FIELDS,
    ),
    UserTypeEnum.PAYED: SynchronizerConfigStatic(
        levels=[Level.CAMPAIGN, Level.ADSET, Level.AD],
        breakdowns=list(InsightsSynchronizerBreakdownEnum),
        action_breakdowns=list(InsightsSynchronizerActionBreakdownEnum),
        requested_fields=INSIGHTS_SYNCHRONIZER_FIELDS,
    ),
}


def sync(
    structures_repository: TuringMongoRepository = None,
    insights_repository: TuringMongoRepository = None,
    account_journal_repository: TuringAdAccountJournalRepository = None,
    business_owner_details: typing.List[typing.Dict] = None,
    user_type: UserTypeEnum = None,
) -> None:
    user_config_static = USER_CONFIGS_BY_TYPE.get(user_type, USER_CONFIGS_BY_TYPE[UserTypeEnum.PAYED])

    for entry in business_owner_details:
        last_synced_on = entry[MiscFieldsEnum.last_synced_on]
        if isinstance(last_synced_on, str):
            try:
                last_synced_on = parse(last_synced_on)
            except Exception as e:
                raise e

        now = datetime.now().date()
        if last_synced_on.date() < now:
            try:
                user_config_runtime = SynchronizerConfigRuntime(
                    insights_repository=insights_repository,
                    structure_repository=structures_repository,
                    account_journal_repository=account_journal_repository,
                    business_owner_id=entry[MiscFieldsEnum.business_owner_id],
                    account_id=entry[MiscFieldsEnum.account_id],
                    date_start=last_synced_on,
                )

                # Structures needs to be synced first in order to get the result type for insights (AdSet level needed)
                # Careful if doing multithreading about this, there are some problems with the SQL connections if
                # initiated multiple times at the same time
                user_config_runtime.account_journal_repository.change_account_structures_sync_status(
                    user_config_runtime.account_id, AdAccountSyncStatusEnum.PENDING, start_date=datetime.now()
                )
                user_config_runtime.account_journal_repository.change_account_insights_sync_status(
                    user_config_runtime.account_id, AdAccountSyncStatusEnum.PENDING, start_date=datetime.now()
                )

                sync_structures(user_config_static=user_config_static, user_config_runtime=user_config_runtime)
                sync_insights(user_config_static=user_config_static, user_config_runtime=user_config_runtime)


            except Exception as e:
                logger.exception(
                    f"Failed sync data for business owner: {entry[MiscFieldsEnum.business_owner_id]}"
                    f" and ad account: {entry[MiscFieldsEnum.account_id]} || {repr(e)}"
                )

        levels = [Level.CAMPAIGN, Level.ADSET, Level.AD]

        delete_old_insights(insights_repository=insights_repository)

        delete_old_structures(
            structure_repository=structures_repository,
            levels=levels,
            business_owner_id=entry[MiscFieldsEnum.business_owner_id],
        )


def sync_insights(user_config_static: SynchronizerConfigStatic, user_config_runtime: SynchronizerConfigRuntime) -> None:
    user_config_runtime.account_journal_repository.change_account_insights_sync_status(
        user_config_runtime.account_id, AdAccountSyncStatusEnum.IN_PROGRESS, start_date=datetime.now()
    )
    has_errors = False
    # sync data up to midnight the current day to avoid syncing
    # partial insights
    date_stop = datetime.now() - timedelta(days=1)

    for level in user_config_static.levels:
        if level in [Level.CAMPAIGN, Level.ADSET]:
            for breakdown in user_config_static.breakdowns:
                for action_breakdown in user_config_static.action_breakdowns:
                    synchronizer = InsightsSynchronizer(
                        business_owner_id=user_config_runtime.business_owner_id,
                        account_id=user_config_runtime.account_id,
                        level=level,
                        breakdown=breakdown.value,
                        action_breakdown=action_breakdown.value,
                        requested_fields=user_config_static.requested_fields,
                    )
                    synchronizer.set_mongo_repository(user_config_runtime.insights_repository)

                    if sync_insights_base(synchronizer, user_config_runtime.date_start, date_stop):
                        has_errors = True
        else:
            synchronizer = InsightsSynchronizer(
                business_owner_id=user_config_runtime.business_owner_id,
                account_id=user_config_runtime.account_id,
                level=level,
                breakdown=InsightsSynchronizerBreakdownEnum.NONE.value,
                action_breakdown=InsightsSynchronizerActionBreakdownEnum.NONE.value,
                requested_fields=user_config_static.requested_fields,
            )
            synchronizer.set_mongo_repository(user_config_runtime.insights_repository)
            has_errors = sync_insights_base(synchronizer, user_config_runtime.date_start, date_stop)

    sync_status = AdAccountSyncStatusEnum.COMPLETED_WITH_ERRORS if has_errors else AdAccountSyncStatusEnum.COMPLETED

    user_config_runtime.account_journal_repository.change_account_insights_sync_status(
        user_config_runtime.account_id, sync_status, end_date=datetime.now()
    )


def sync_insights_base(
    synchronizer: InsightsSynchronizer = None, date_start: datetime = None, date_stop: datetime = None
) -> bool:
    has_errors = False
    try:
        available_data = synchronizer.check_data(date_start.date().isoformat(), date_stop.date().isoformat())
    except Exception as e:
        logger.exception(f"There was no data for dates {date_start} and {date_stop} || {repr(e)}")
        available_data = []
        has_errors = True

    if not available_data:
        return has_errors

    while date_stop >= date_start:
        # The data is taken from Facebook in groups of max 3 days in order to avoid failed requests
        if date_start + timedelta(SYNC_DAYS_INTERVAL) <= date_stop:
            current_date_stop = date_start + timedelta(SYNC_DAYS_INTERVAL)
        else:
            current_date_stop = date_stop

        synchronizer.date_start = date_start.date().isoformat()
        synchronizer.date_stop = current_date_stop.date().isoformat()
        try:
            synchronizer.run()
        except Exception as e:
            logger.exception(
                f"Failed to sync data for dates {synchronizer.date_start}"
                f" and {synchronizer.date_stop} || {repr(e)}"
            )
            has_errors = True
        date_start = current_date_stop + timedelta(days=1)

    return has_errors


def sync_structures(
    user_config_static: SynchronizerConfigStatic, user_config_runtime: SynchronizerConfigRuntime
) -> typing.NoReturn:
    user_config_runtime.account_journal_repository.change_account_structures_sync_status(
        user_config_runtime.account_id, AdAccountSyncStatusEnum.IN_PROGRESS, start_date=datetime.now()
    )
    has_errors = False

    for level in user_config_static.levels:
        synchronizer = StructuresSyncronizer(
            business_owner_id=user_config_runtime.business_owner_id,
            account_id=user_config_runtime.account_id,
            level=level,
        )
        try:
            (
                synchronizer.set_mongo_repository(user_config_runtime.structure_repository)
                .set_facebook_config(config.facebook)
                .run()
            )
        except Exception as e:
            logger.exception(
                f"Failed sync structures for business owner: {user_config_runtime.business_owner_id}"
                f" and ad account: {user_config_runtime.account_id} || {repr(e)}")
            has_errors = True

    # mark campaigns and adsets as completed based on the end time value
    try:
        mark_structures_as_completed(
            account_id=user_config_runtime.account_id, structures_repository=user_config_runtime.structure_repository
        )
    except Exception as e:
        logger.exception(
            f"Failed updating completed structure ids for business owner: {user_config_runtime.business_owner_id}"
            f" and ad account: {user_config_runtime.account_id} || {repr(e)}"
        )
        has_errors = True

    sync_status = AdAccountSyncStatusEnum.COMPLETED_WITH_ERRORS if has_errors else AdAccountSyncStatusEnum.COMPLETED

    user_config_runtime.account_journal_repository.change_account_structures_sync_status(
        user_config_runtime.account_id, sync_status, end_date=datetime.now()
    )


def mark_structures_as_completed(
    account_id: typing.AnyStr = None, structures_repository: TuringMongoRepository = None
) -> typing.NoReturn:
    campaigns = structures_repository.get_campaigns_by_ad_account(account_id)
    campaign_ids = [campaign[LevelToFacebookIdKeyMapping.CAMPAIGN.value] for campaign in campaigns]
    adsets = structures_repository.get_adsets_by_campaign_id(campaign_ids)
    completed_campaigns, completed_adsets = mark_completed_campaigns_and_adsets(campaigns, adsets)

    update_status_for_completed_structures(
        structures_repository=structures_repository,
        completed_structures=completed_campaigns,
        structure_key=LevelToFacebookIdKeyMapping.CAMPAIGN.value,
        level=Level.CAMPAIGN.value,
    )

    update_status_for_completed_structures(
        structures_repository=structures_repository,
        completed_structures=completed_adsets,
        structure_key=LevelToFacebookIdKeyMapping.ADSET.value,
        level=Level.ADSET.value,
    )


def update_status_for_completed_structures(
    structures_repository: TuringMongoRepository = None,
    completed_structures: typing.List = None,
    structure_key: typing.AnyStr = None,
    level: typing.AnyStr = None,
):
    completed_structure_ids = [
        structure[structure_key]
        for structure in completed_structures
        if structure[MiscFieldsEnum.status] == StructureStatusEnum.COMPLETED.value
    ]

    structures_repository.collection = level
    structures_repository.update_structure_status(
        structure_key=structure_key,
        structure_ids=completed_structure_ids,
        status_key=MiscFieldsEnum.status,
        status_value=StructureStatusEnum.COMPLETED.value,
    )


def mark_completed_campaigns_and_adsets(
    campaigns: typing.List[typing.Dict] = None, adsets: typing.List[typing.Dict] = None
) -> typing.Tuple[typing.List[typing.Dict], typing.List[typing.Dict]]:
    for index in range(len(campaigns)):
        campaign_id = campaigns[index][LevelToFacebookIdKeyMapping.CAMPAIGN.value]
        campaign_adsets = [
            adset for adset in adsets if adset[LevelToFacebookIdKeyMapping.CAMPAIGN.value] == campaign_id
        ]

        completed_adsets = mark_completed_adset(campaign_adsets)
        if completed_adsets == len(campaign_adsets):
            campaigns[index][MiscFieldsEnum.status] = StructureStatusEnum.COMPLETED.value

        campaigns[index][MiscFieldsEnum.details] = BSON.encode(campaigns[index][MiscFieldsEnum.details])

    for index in range(len(adsets)):
        adsets[index][MiscFieldsEnum.details] = BSON.encode(adsets[index][MiscFieldsEnum.details])

    return campaigns, adsets


def mark_completed_adset(adsets: typing.List[typing.Dict] = None) -> int:
    completed_adsets = 0
    for adset in adsets:
        end_time = adset.get(MiscFieldsEnum.end_time)
        if end_time:
            end_time = datetime.strptime(end_time, "%Y-%m-%dT%H:%M:%S%z")
            now = datetime.now(end_time.tzinfo)
            if end_time < now:
                adset[MiscFieldsEnum.status] = StructureStatusEnum.COMPLETED.value
                completed_adsets += 1
    return completed_adsets


def delete_old_insights(insights_repository: TuringMongoRepository) -> typing.NoReturn:
    insights_collections = insights_repository.get_collections()
    for insights_collection in insights_collections:
        insights_repository.collection = insights_collection
        date = (datetime.now() - timedelta(days=DAYS_UNTIL_OBSOLETE)).date().isoformat()
        insights_repository.delete_many_older_than_date(date)


def delete_old_structures(
    structure_repository: TuringMongoRepository = None,
    levels: typing.List[Level] = None,
    business_owner_id: typing.AnyStr = None,
) -> typing.NoReturn:
    for level in levels:
        structure_repository.collection = level.value

        query = {
            MongoOperator.AND.value: [
                {
                    "date_added": {
                        MongoOperator.LESSTHANEQUAL.value: (datetime.now() - timedelta(days=DAYS_UNTIL_OBSOLETE))
                        .date()
                        .isoformat()
                    }
                },
                {"status": {MongoOperator.NOTEQUAL.value: StructureStatusEnum.ACTIVE.value}},
            ]
        }

        old_structures = structure_repository.get(query)
        if old_structures:
            structure_ids_to_delete, structures_to_insert = get_structures_to_modify(
                old_structures=old_structures, level=level, business_owner_id=business_owner_id
            )

            query_filter = {
                LevelToFacebookIdKeyMapping.get_enum_by_name(level.name).value: {
                    MongoOperator.IN.value: structure_ids_to_delete
                }
            }

            structure_repository.delete_many(query_filter)
            structure_repository.add_many(structures_to_insert)


def get_structures_to_modify(
    old_structures: typing.List[typing.Dict], level: Level = None, business_owner_id: typing.AnyStr = None
) -> (typing.List[any], typing.List[any]):
    fields = StructureFields.get(level.value)
    required_fields = fields.get_required_structure_fields()
    structure_ids_to_delete = []
    structures_to_insert = []

    for old_structure in old_structures:
        minimum_structure = {}
        details = {}
        try:
            for required_field in required_fields:
                if required_field in old_structure:
                    minimum_structure[required_field] = old_structure[required_field]
                elif MiscFieldsEnum.details in old_structure:
                    current_structure_details = BSON.decode(old_structure[MiscFieldsEnum.details])
                    if required_field in current_structure_details:
                        details[required_field] = current_structure_details[required_field]
                    elif "targetingsentencelines" not in details:
                        check_targeting_sentence(
                            current_structure_details=current_structure_details,
                            details=details,
                            required_field=required_field,
                        )
        except Exception as e:
            logger.exception(f"Failed to get modified structure || {repr(e)}")

        minimum_structure[MiscFieldsEnum.business_owner_id] = business_owner_id
        minimum_structure[MiscFieldsEnum.details] = BSON.encode(details)
        structure_ids_to_delete.append(old_structure[LevelToFacebookIdKeyMapping.get_enum_by_name(level.name).value])
        structures_to_insert.append(minimum_structure)

    return structure_ids_to_delete, structures_to_insert


def check_targeting_sentence(
    current_structure_details: typing.AnyStr, details: typing.Dict, required_field: typing.AnyStr
):
    targeting_lines_structure = "targetingsentencelines"
    targeting_sentence_lines_entry = current_structure_details[targeting_lines_structure]
    if targeting_lines_structure in targeting_sentence_lines_entry:
        targeting_sentence_lines_values = targeting_sentence_lines_entry[targeting_lines_structure]
        for target_group in targeting_sentence_lines_values:
            if target_group["content"].lower().replace(":", "") == required_field:
                details[targeting_lines_structure] = targeting_sentence_lines_entry
                break


def update_results_for_insights(
    structures_repository: TuringMongoRepository = None,
    insights_repository: TuringMongoRepository = None,
    levels: typing.List = None,
):
    for level in levels:
        if level in [Level.CAMPAIGN, Level.ADSET]:
            for breakdown in InsightsSynchronizerBreakdownEnum:
                for action_breakdown in InsightsSynchronizerActionBreakdownEnum:
                    insights_repository.collection = level.value + "_" + breakdown.value.name + "_" + action_breakdown.value.name
                    structure_key = LevelIdKeyEnum.get_enum_by_name(level.value.upper()).value
                    update_insight_records_with_result(
                        level=level.value,
                        structures_repository=structures_repository,
                        insights_repository=insights_repository,
                        structure_key=structure_key,
                    )

        else:
            insights_repository.collection = "_".join(
                [
                    level.value,
                    InsightsSynchronizerBreakdownEnum.NONE.value.name,
                    InsightsSynchronizerActionBreakdownEnum.NONE.value.name
                ]
            )

            structure_key = LevelIdKeyEnum.get_enum_by_name(level.ADSET.name.upper()).value
            update_insight_records_with_result(
                level=level.value,
                structures_repository=structures_repository,
                insights_repository=insights_repository,
                structure_key=structure_key,
            )


def update_insight_records_with_result(
    level: typing.AnyStr = None,
    structure_key: typing.AnyStr = None,
    insights_repository: TuringMongoRepository = None,
    structures_repository: TuringMongoRepository = None,
):
    insights = insights_repository.get_all()
    structure_ids = [x[structure_key] for x in insights if structure_key in x]

    structures = structures_repository.get_results_fields_from_adsets(
        structure_ids=structure_ids, structure_key=structure_key
    )

    for insight in insights:
        for structure in structures:
            if insight[structure_key] == structure[structure_key]:
                results_field_value = None
                if GraphAPIInsightsFields.custom_event_type in structure \
                        and structure[GraphAPIInsightsFields.custom_event_type]:
                    custom_event_type = PixelCustomEventTypeToResult.get_enum_by_name(
                        structure[GraphAPIInsightsFields.custom_event_type]
                    )
                    if custom_event_type:
                        results_field_value = custom_event_type.value.name
                elif GraphAPIInsightsFields.optimization_goal in structure\
                        and structure[GraphAPIInsightsFields.optimization_goal]:
                    optimization_goal = AdSetOptimizationToResult.get_enum_by_name(
                        structure[GraphAPIInsightsFields.optimization_goal]
                    )
                    if optimization_goal:
                        results_field_value = optimization_goal.value.name
                if results_field_value and results_field_value in insight:
                    query = {MongoOperator.SET.value: {FieldsMetadata.results.name: insight[results_field_value]}}
                    collection_key = LevelIdKeyEnum.get_enum_by_name(level.upper()).value
                    query_filter = {
                        collection_key: {MongoOperator.EQUALS.value: insight[collection_key]},
                        FieldsMetadata.date_start.name: {
                            MongoOperator.EQUALS.value: insight[FieldsMetadata.date_start.name]
                        },
                    }
                    insights_repository.update_one(query_filter=query_filter, query=query)
                    break
