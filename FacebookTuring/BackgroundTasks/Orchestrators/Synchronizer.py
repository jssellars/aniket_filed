import typing
from datetime import datetime, timedelta
from threading import Thread

from bson import BSON
from dateutil.parser import parse

from Core.Dexter.Infrastructure.Domain.LevelEnums import LevelIdKeyEnum
from Core.Tools.Logger.LoggerMessageBase import LoggerMessageBase, LoggerMessageTypeEnum
from Core.Tools.MongoRepository.MongoOperator import MongoOperator
from Core.Web.FacebookGraphAPI.GraphAPIDomain.GraphAPIInsightsFields import GraphAPIInsightsFields
from Core.Web.FacebookGraphAPI.GraphAPIMappings.ObjectiveToResultsMapper import (
    PixelCustomEventTypeToResult,
    AdSetOptimizationToResult,
)
from Core.Web.FacebookGraphAPI.Models.FieldsMetadata import FieldsMetadata
from FacebookTuring.BackgroundTasks.Orchestrators.InsightsSyncronizer import InsightsSyncronizer
from FacebookTuring.BackgroundTasks.Orchestrators.InsightsSyncronizerBreakdowns import (
    InsightsSyncronizerBreakdownEnum,
    InsightsSyncronizerActionBreakdownEnum,
)
from FacebookTuring.BackgroundTasks.Orchestrators.StructuresSyncronizer import StructuresSyncronizer
from FacebookTuring.BackgroundTasks.Startup import startup, logger
from FacebookTuring.Infrastructure.Domain.AdAccountSyncStatusEnum import AdAccountSyncStatusEnum
from FacebookTuring.Infrastructure.Domain.MiscFieldsEnum import MiscFieldsEnum
from FacebookTuring.Infrastructure.Domain.StructureStatusEnum import StructureStatusEnum
from FacebookTuring.Infrastructure.Mappings.LevelMapping import Level, LevelToFacebookIdKeyMapping
from FacebookTuring.Infrastructure.Mappings.StructureMapping import StructureFields
from FacebookTuring.Infrastructure.PersistenceLayer.TuringAdAccountJournalRepository import (
    TuringAdAccountJournalRepository,
)
from FacebookTuring.Infrastructure.PersistenceLayer.TuringMongoRepository import TuringMongoRepository

NEXT_DAY = timedelta(days=1)
SYNC_DAYS_INTERVAL = 3
DEFAULT_DATETIME_FORMAT = "%Y-%m-%d"
DEFAULT_DATETIME_ISO_FORMAT = "%Y-%m-%d %H:%M:%S"
DAYS_UNTIL_OBSOLETE = 31


def sync(
        structures_repository: TuringMongoRepository = None,
        insights_repository: TuringMongoRepository = None,
        account_journal_repository: TuringAdAccountJournalRepository = None,
        business_owner_details: typing.List[typing.Dict] = None,
) -> typing.NoReturn:
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
                # start a new thread for synchronizing structures
                structure_thread = Thread(
                    target=sync_structures,
                    args=(
                        structures_repository,
                        account_journal_repository,
                        entry[MiscFieldsEnum.business_owner_id],
                        entry[MiscFieldsEnum.account_id],
                    ),
                )

                # start a new thread for synchronizing all insights
                insights_thread = Thread(
                    target=sync_insights,
                    args=(
                        insights_repository,
                        account_journal_repository,
                        entry[MiscFieldsEnum.business_owner_id],
                        entry[MiscFieldsEnum.account_id],
                        last_synced_on,
                    ),
                )

                # run synchronizer threads
                structure_thread.start()
                insights_thread.start()

                # wait for current account sync to finish
                structure_thread.join()
                insights_thread.join()

            except Exception as e:
                log = LoggerMessageBase(
                    mtype=LoggerMessageTypeEnum.ERROR,
                    name="Facebook Turing Daily Sync Error",
                    description="Failed sync data for business owner: %s and ad account: %s. "
                                "Reason: %s" % (entry[MiscFieldsEnum.business_owner_id], entry[MiscFieldsEnum.account_id], str(e)),
                )
                logger.logger.exception(log.to_dict())

        levels = [Level.CAMPAIGN, Level.ADSET, Level.AD]
        update_results_for_insights(
            insights_repository=insights_repository,
            structures_repository=structures_repository,
            levels=levels
        )

        delete_old_insights(insights_repository=insights_repository)

        delete_old_structures(
            structure_repository=structures_repository,
            levels=levels,
            business_owner_id=entry[MiscFieldsEnum.business_owner_id],
        )


def sync_structures(
        structures_repository: TuringMongoRepository = None,
        account_journal_repository: TuringAdAccountJournalRepository = None,
        business_owner_id: typing.AnyStr = None,
        account_id: typing.AnyStr = None,
) -> typing.NoReturn:
    account_journal_repository.change_account_structures_sync_status(
        account_id, AdAccountSyncStatusEnum.IN_PROGRESS, start_date=datetime.now()
    )
    has_errors = False

    levels = [Level.CAMPAIGN, Level.ADSET, Level.AD]
    for level in levels:
        syncronizer = StructuresSyncronizer(business_owner_id=business_owner_id, account_id=account_id, level=level)
        try:
            (syncronizer.set_mongo_repository(structures_repository).set_facebook_config(startup.facebook_config).run())
        except Exception as e:
            log = LoggerMessageBase(
                mtype=LoggerMessageTypeEnum.ERROR,
                name="Facebook Turing Daily Sync Error",
                description="Failed sync structures for business owner: %s and ad account: %s. "
                            "Reason: %s" % (business_owner_id, account_id, str(e)),
            )
            logger.logger.exception(log.to_dict())
            has_errors = True

    # mark campaigns and adsets as completed based on the end time value
    try:
        mark_structures_as_completed(account_id=account_id, structures_repository=structures_repository)
    except Exception as e:
        log = LoggerMessageBase(
            mtype=LoggerMessageTypeEnum.ERROR,
            name="Facebook Turing Daily Sync Error",
            description="Failed updating completed structure ids for business owner: %s and ad "
                        "account: %s. Reason: %s" % (business_owner_id, account_id, str(e)),
        )
        logger.logger.exception(log.to_dict())
        has_errors = True

    if has_errors:
        sync_status = AdAccountSyncStatusEnum.COMPLETED_WITH_ERRORS
    else:
        sync_status = AdAccountSyncStatusEnum.COMPLETED

    account_journal_repository.change_account_structures_sync_status(account_id, sync_status, end_date=datetime.now())


def sync_insights(
        insights_repository: TuringMongoRepository = None,
        account_journal_repository: TuringAdAccountJournalRepository = None,
        business_owner_id: typing.AnyStr = None,
        account_id: typing.AnyStr = None,
        date_start: datetime = None,
) -> typing.NoReturn:
    account_journal_repository.change_account_insights_sync_status(
        account_id, AdAccountSyncStatusEnum.IN_PROGRESS, start_date=datetime.now()
    )
    has_errors = False
    # sync data up to midnight the current day to avoid syncing
    # partial insights
    date_stop = datetime.now() - timedelta(days=1)

    levels = [Level.CAMPAIGN, Level.ADSET, Level.AD]
    for level in levels:
        if level in [Level.CAMPAIGN, Level.ADSET]:
            for breakdown in InsightsSyncronizerBreakdownEnum:
                for action_breakdown in InsightsSyncronizerActionBreakdownEnum:
                    syncronizer = InsightsSyncronizer(
                        business_owner_id=business_owner_id,
                        account_id=account_id,
                        level=level,
                        breakdown=breakdown.value,
                        action_breakdown=action_breakdown.value,
                    )
                    syncronizer.set_mongo_repository(insights_repository)
                    has_errors = sync_insights_base(syncronizer, date_start, date_stop)
        else:
            syncronizer = InsightsSyncronizer(
                business_owner_id=business_owner_id,
                account_id=account_id,
                level=level,
                breakdown=InsightsSyncronizerBreakdownEnum.NONE.value,
                action_breakdown=InsightsSyncronizerActionBreakdownEnum.NONE.value,
            )
            syncronizer.set_mongo_repository(insights_repository)
            has_errors = sync_insights_base(syncronizer, date_start, date_stop)

    if has_errors:
        sync_status = AdAccountSyncStatusEnum.COMPLETED_WITH_ERRORS
    else:
        sync_status = AdAccountSyncStatusEnum.COMPLETED

    account_journal_repository.change_account_insights_sync_status(
        account_id,
        sync_status,
        end_date=datetime.now()
    )


def sync_insights_base(
        syncronizer: InsightsSyncronizer = None,
        date_start: datetime = None,
        date_stop: datetime = None
) -> bool:
    has_errors = False
    try:
        data_available = syncronizer.check_data(
            date_start.strftime(DEFAULT_DATETIME_FORMAT), date_stop.strftime(DEFAULT_DATETIME_FORMAT)
        )
    except:
        log = LoggerMessageBase(
            mtype=LoggerMessageTypeEnum.ERROR,
            name="Facebook Turing Daily Sync Error",
            description="There was no data for dates {} and {}".format(date_start, date_stop),
        )
        logger.logger.exception(log.to_dict())
        data_available = []
        has_errors = True

    if data_available:
        while date_stop >= date_start:
            # The data is taken from Facebook in groups of max 3 days in order to avoid failed requests
            if date_start + timedelta(SYNC_DAYS_INTERVAL) <= date_stop:
                current_date_stop = date_start + timedelta(SYNC_DAYS_INTERVAL)
            else:
                current_date_stop = date_start + (date_stop - date_start)

            date_start_sync = date_start.strftime(DEFAULT_DATETIME_FORMAT)
            date_stop_sync = current_date_stop.strftime(DEFAULT_DATETIME_FORMAT)

            syncronizer.date_start = date_start_sync
            syncronizer.date_stop = date_stop_sync
            try:
                syncronizer.run()
            except Exception as e:
                log = LoggerMessageBase(
                    mtype=LoggerMessageTypeEnum.ERROR,
                    name="Facebook Turing Daily Sync Error",
                    description="Failed to sync data for dates {} and {}. Reason: {}".format(
                        date_start_sync, date_stop_sync, str(e)
                    ),
                )
                logger.logger.exception(log.to_dict())
                has_errors = True
            date_start = current_date_stop + NEXT_DAY

    return has_errors


def mark_structures_as_completed(
        account_id: typing.AnyStr = None,
        structures_repository: TuringMongoRepository = None
) -> typing.NoReturn:
    campaigns = structures_repository.get_campaigns_by_ad_account(account_id)
    campaign_ids = [campaign[LevelToFacebookIdKeyMapping.CAMPAIGN.value] for campaign in campaigns]
    adsets = structures_repository.get_adsets_by_campaign_id(campaign_ids)
    campaigns, adsets = mark_completed_campaigns_and_adsets(campaigns, adsets)

    structures_repository.add_structures_many_with_deprecation(level=Level.CAMPAIGN, structures=campaigns)
    structures_repository.add_structures_many_with_deprecation(level=Level.ADSET, structures=adsets)


def mark_completed_campaigns_and_adsets(
        campaigns: typing.List[typing.Dict] = None,
        adsets: typing.List[typing.Dict] = None
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
        insights_repository.set_collection(insights_collection)
        date = (datetime.now() - timedelta(days=DAYS_UNTIL_OBSOLETE)).strftime("%Y-%m-%d")
        insights_repository.delete_many_older_than_date(date)


def delete_old_structures(
        structure_repository: TuringMongoRepository = None,
        levels: typing.List[Level] = None,
        business_owner_id: typing.AnyStr = None,
) -> typing.NoReturn:
    for level in levels:
        structure_repository.set_collection(level.value)

        query = {
            MongoOperator.AND.value: [
                {
                    "date_added": {
                        MongoOperator.LESSTHANEQUAL.value: (
                                datetime.now() - timedelta(days=DAYS_UNTIL_OBSOLETE)
                        ).strftime("%Y-%m-%d")
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
        old_structures: typing.List[typing.Dict],
        level: Level = None,
        business_owner_id: typing.AnyStr = None
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
            log = LoggerMessageBase(
                mtype=LoggerMessageTypeEnum.ERROR,
                name="Facebook Turing Daily Sync Error",
                description="Failed to get modified structure. Reason: {}".format(str(e)),
            )
            logger.logger.exception(log.to_dict())

        minimum_structure[MiscFieldsEnum.business_owner_id] = business_owner_id
        minimum_structure[MiscFieldsEnum.details] = BSON.encode(details)
        structure_ids_to_delete.append(old_structure[LevelToFacebookIdKeyMapping.get_enum_by_name(level.name).value])
        structures_to_insert.append(minimum_structure)

    return structure_ids_to_delete, structures_to_insert


def check_targeting_sentence(
        current_structure_details: typing.AnyStr,
        details: typing.Dict,
        required_field: typing.AnyStr
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
            for breakdown in InsightsSyncronizerBreakdownEnum:
                for action_breakdown in InsightsSyncronizerActionBreakdownEnum:
                    insights_repository.set_collection(
                        level.value + "_" + breakdown.value.name + "_" + action_breakdown.value.name
                    )
                    structure_key = LevelIdKeyEnum.get_enum_by_name(level.value.upper()).value
                    update_insight_records_with_result(
                        level=level.value,
                        structures_repository=structures_repository,
                        insights_repository=insights_repository,
                        structure_key=structure_key
                    )

        else:
            insights_repository.set_collection(
                level.value
            )

            structure_key = LevelIdKeyEnum.get_enum_by_name(level.ADSET.name.upper()).value
            update_insight_records_with_result(
                level=level.value,
                structures_repository=structures_repository,
                insights_repository=insights_repository,
                structure_key=structure_key
            )


def update_insight_records_with_result(
        level: typing.AnyStr = None,
        structure_key: typing.AnyStr = None,
        insights_repository: TuringMongoRepository = None,
        structures_repository: TuringMongoRepository = None
):
    insights = insights_repository.get_all()
    structure_ids = [x[structure_key] for x in insights if structure_key in x]

    structures = structures_repository.get_results_fields_from_adsets(
        structure_ids=structure_ids,
        structure_key=structure_key
    )

    for insight in insights:
        for structure in structures:
            if insight[structure_key] == structure[structure_key]:
                results_field_value = None
                if GraphAPIInsightsFields.custom_event_type in structure.keys():
                    custom_event_type = PixelCustomEventTypeToResult.get_enum_by_name(
                        structure[GraphAPIInsightsFields.custom_event_type]
                    )
                    if custom_event_type:
                        results_field_value = custom_event_type.value.name
                elif GraphAPIInsightsFields.optimization_goal in structure.keys():
                    optimization_goal = AdSetOptimizationToResult.get_enum_by_name(
                        structure[GraphAPIInsightsFields.optimization_goal]
                    )
                    if optimization_goal:
                        results_field_value = optimization_goal.value.name
                if results_field_value and results_field_value in insight.keys():
                    query = {
                        MongoOperator.SET.value: {
                            FieldsMetadata.results.name: insight[results_field_value]
                        }
                    }
                    collection_key = LevelIdKeyEnum.get_enum_by_name(level.upper()).value
                    query_filter = {
                        collection_key: {
                            MongoOperator.EQUALS.value: insight[collection_key]
                        },
                        FieldsMetadata.date_start.name: {
                            MongoOperator.EQUALS.value: insight[FieldsMetadata.date_start.name]
                        },
                    }
                    insights_repository.update_one(
                        query_filter=query_filter,
                        query=query
                    )
                    break
