import typing
from datetime import datetime, timedelta
from threading import Thread

from dateutil.parser import parse

from Core.Tools.Logger.LoggerMessageBase import LoggerMessageBase, LoggerMessageTypeEnum
from FacebookTuring.BackgroundTasks.Orchestrators.InsightsSyncronizer import InsightsSyncronizer
from FacebookTuring.BackgroundTasks.Orchestrators.InsightsSyncronizerBreakdowns import \
    InsightsSyncronizerBreakdownEnum, InsightsSyncronizerActionBreakdownEnum
from FacebookTuring.BackgroundTasks.Orchestrators.StructuresSyncronizer import StructuresSyncronizer
from FacebookTuring.BackgroundTasks.Startup import startup, logger
from FacebookTuring.Infrastructure.Domain.AdAccountSyncStatusEnum import AdAccountSyncStatusEnum
from FacebookTuring.Infrastructure.Domain.MiscFieldsEnum import MiscFieldsEnum
from FacebookTuring.Infrastructure.Domain.StructureStatusEnum import StructureStatusEnum
from FacebookTuring.Infrastructure.Mappings.LevelMapping import Level, LevelToFacebookIdKeyMapping
from FacebookTuring.Infrastructure.PersistenceLayer.TuringAdAccountJournalRepository import \
    TuringAdAccountJournalRepository
from FacebookTuring.Infrastructure.PersistenceLayer.TuringMongoRepository import TuringMongoRepository

NEXT_DAY = timedelta(days=1)
SYNC_DAYS_INTERVAL = 3
DEFAULT_DATETIME_FORMAT = '%Y-%m-%d'
DEFAULT_DATETIME_ISO_FORMAT = '%Y-%m-%d %H:%M:%S'


def sync(structures_repository: TuringMongoRepository = None,
         insights_repository: TuringMongoRepository = None,
         account_journal_repository: TuringAdAccountJournalRepository = None,
         business_owner_details: typing.List[typing.Dict] = None) -> typing.NoReturn:
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
                structure_thread = Thread(target=sync_structures,
                                          args=(structures_repository,
                                                account_journal_repository,
                                                entry[MiscFieldsEnum.business_owner_id],
                                                entry[MiscFieldsEnum.account_id]))

                # start a new thread for synchronizing all insights
                insights_thread = Thread(target=sync_insights,
                                         args=(insights_repository,
                                               account_journal_repository,
                                               entry[MiscFieldsEnum.business_owner_id],
                                               entry[MiscFieldsEnum.account_id],
                                               last_synced_on))

                # run synchronizer threads
                structure_thread.start()
                insights_thread.start()

                # wait for current account sync to finish
                structure_thread.join()
                insights_thread.join()
            except Exception as e:
                log = LoggerMessageBase(mtype=LoggerMessageTypeEnum.ERROR,
                                        name="Facebook Turing Daily Sync Error",
                                        description="Failed sync data for business owner: %s and ad account: %s. "
                                                    "Reason: %s" % (entry[MiscFieldsEnum.business_owner_id],
                                                                    entry[MiscFieldsEnum.account_id],
                                                                    str(e)))
                logger.logger.exception(log.to_dict())


def sync_structures(structures_repository: TuringMongoRepository = None,
                    account_journal_repository: TuringAdAccountJournalRepository = None,
                    business_owner_id: typing.AnyStr = None,
                    account_id: typing.AnyStr = None) -> typing.NoReturn:
    account_journal_repository.change_account_structures_sync_status(account_id,
                                                                     AdAccountSyncStatusEnum.IN_PROGRESS,
                                                                     start_date=datetime.now())
    has_errors = False

    levels = [Level.CAMPAIGN, Level.ADSET, Level.AD]
    for level in levels:
        syncronizer = StructuresSyncronizer(business_owner_id=business_owner_id,
                                            account_id=account_id,
                                            level=level)
        try:
            (syncronizer.
             set_mongo_repository(structures_repository).
             set_facebook_config(startup.facebook_config).
             run())
        except Exception as e:
            log = LoggerMessageBase(mtype=LoggerMessageTypeEnum.ERROR,
                                    name="Facebook Turing Daily Sync Error",
                                    description="Failed sync structures for business owner: %s and ad account: %s. "
                                                "Reason: %s" % (business_owner_id, account_id, str(e)))
            logger.logger.exception(log.to_dict())
            has_errors = True

    # mark campaigns and adsets as completed based on the end time value
    try:
        mark_structures_as_completed(account_id=account_id, structures_repository=structures_repository)
    except Exception as e:
        log = LoggerMessageBase(mtype=LoggerMessageTypeEnum.ERROR,
                                name="Facebook Turing Daily Sync Error",
                                description="Failed updating completed structure ids for business owner: %s and ad "
                                            "account: %s. Reason: %s" % (business_owner_id, account_id, str(e)))
        logger.logger.exception(log.to_dict())
        has_errors = True
    if has_errors:
        sync_status = AdAccountSyncStatusEnum.COMPLETED_WITH_ERRORS
    else:
        sync_status = AdAccountSyncStatusEnum.COMPLETED

    account_journal_repository.change_account_structures_sync_status(account_id,
                                                                     sync_status,
                                                                     end_date=datetime.now())

    # mark campaigns and adsets as completed based on the end time value
    try:
        mark_structures_as_completed(account_id=account_id, structures_repository=structures_repository)
    except Exception as e:
        log = LoggerMessageBase(mtype=LoggerMessageTypeEnum.ERROR,
                                name="Facebook Turing Daily Sync Error",
                                description="Failed updating completed structure ids for business owner: %s and ad "
                                            "account: %s. Reason: %s" % (business_owner_id, account_id, str(e)))
        logger.logger.exception(log.to_dict())
        has_errors = True
    if has_errors:
        sync_status = AdAccountSyncStatusEnum.COMPLETED_WITH_ERRORS
    else:
        sync_status = AdAccountSyncStatusEnum.COMPLETED

    account_journal_repository.change_account_structures_sync_status(account_id,
                                                                     sync_status,
                                                                     end_date=datetime.now())


def sync_insights(insights_repository: TuringMongoRepository = None,
                  account_journal_repository: TuringAdAccountJournalRepository = None,
                  business_owner_id: typing.AnyStr = None,
                  account_id: typing.AnyStr = None,
                  date_start: datetime = None) -> typing.NoReturn:
    account_journal_repository.change_account_insights_sync_status(account_id,
                                                                   AdAccountSyncStatusEnum.IN_PROGRESS,
                                                                   start_date=datetime.now())
    has_errors = False
    # sync data up to midnight the current day to avoid syncing
    # partial insights
    date_stop = datetime.now() - timedelta(days=1)

    levels = [Level.CAMPAIGN, Level.ADSET, Level.AD]
    for level in levels:
        if level in [Level.CAMPAIGN, Level.ADSET]:
            for breakdown in InsightsSyncronizerBreakdownEnum:
                for action_breakdown in InsightsSyncronizerActionBreakdownEnum:
                    syncronizer = InsightsSyncronizer(business_owner_id=business_owner_id,
                                                      account_id=account_id,
                                                      level=level,
                                                      breakdown=breakdown.value,
                                                      action_breakdown=action_breakdown.value)
                    syncronizer.set_mongo_repository(insights_repository)
                    has_errors = sync_insights_base(syncronizer, date_start, date_stop)
        else:
            syncronizer = InsightsSyncronizer(business_owner_id=business_owner_id,
                                              account_id=account_id,
                                              level=level,
                                              breakdown=InsightsSyncronizerBreakdownEnum.NONE.value,
                                              action_breakdown=InsightsSyncronizerActionBreakdownEnum.NONE.value)
            syncronizer.set_mongo_repository(insights_repository)
            has_errors = sync_insights_base(syncronizer, date_start, date_stop)

    if has_errors:
        sync_status = AdAccountSyncStatusEnum.COMPLETED_WITH_ERRORS
    else:
        sync_status = AdAccountSyncStatusEnum.COMPLETED

    account_journal_repository.change_account_insights_sync_status(account_id,
                                                                   sync_status,
                                                                   end_date=datetime.now())


def sync_insights_base(syncronizer: InsightsSyncronizer = None,
                       date_start: datetime = None,
                       date_stop: datetime = None) -> bool:
    has_errors = False
    try:
        data_available = syncronizer.check_data(date_start.strftime(DEFAULT_DATETIME_FORMAT),
                                                date_stop.strftime(DEFAULT_DATETIME_FORMAT))
    except:
        log = LoggerMessageBase(mtype=LoggerMessageTypeEnum.ERROR,
                                name="Facebook Turing Daily Sync Error",
                                description="There was no data for dates {} and {}".format(date_start, date_stop))
        logger.logger.exception(log.to_dict())
        data_available = []
        has_errors = True

    if data_available:
        while date_stop >= date_start:
            current_date_stop = date_start + timedelta(SYNC_DAYS_INTERVAL)
            date_start_sync = date_start.strftime(DEFAULT_DATETIME_FORMAT)
            date_stop_sync = current_date_stop.strftime(DEFAULT_DATETIME_FORMAT)

            syncronizer.date_start = date_start_sync
            syncronizer.date_stop = date_stop_sync
            try:
                syncronizer.run()
            except Exception as e:
                log = LoggerMessageBase(mtype=LoggerMessageTypeEnum.ERROR,
                                        name="Facebook Turing Daily Sync Error",
                                        description="Failed to sync data for dates {} and {}. Reason: {}".format(
                                            date_start_sync, date_stop_sync, str(e)))
                logger.logger.exception(log.to_dict())
                has_errors = True
            date_start = current_date_stop + NEXT_DAY

    return has_errors


def mark_structures_as_completed(account_id: typing.AnyStr=None,
                                 structures_repository: TuringMongoRepository = None) -> typing.NoReturn:
    campaigns = structures_repository.get_campaigns_by_ad_account(account_id)
    campaign_ids = [campaign[LevelToFacebookIdKeyMapping.CAMPAIGN.value] for campaign in campaigns]
    adsets = structures_repository.get_adsets_by_campaign_id(campaign_ids)
    campaigns, adsets = mark_completed_campaigns_and_adsets(campaigns, adsets)

    structures_repository.add_structure_many(account_id, Level.CAMPAIGN, campaigns)
    structures_repository.add_structure_many(account_id, Level.ADSET, adsets)


def mark_completed_campaigns_and_adsets(campaigns: typing.List[typing.Dict] = None,
                                        adsets: typing.List[typing.Dict] = None) -> typing.Tuple[typing.List[typing.Dict],
                                                                                                 typing.List[typing.Dict]]:
    for index in range(len(campaigns)):
        campaign_id = campaigns[index][LevelToFacebookIdKeyMapping.CAMPAIGN.value]
        campaign_adsets = [adset for adset in adsets
                           if adset[LevelToFacebookIdKeyMapping.CAMPAIGN.value] == campaign_id]

        completed_adsets = mark_completed_adset(campaign_adsets)
        if completed_adsets == len(campaign_adsets):
            campaigns[index][MiscFieldsEnum.status] = StructureStatusEnum.COMPLETED.value

    return campaigns, adsets


def mark_completed_adset(adsets: typing.List[typing.Dict] = None) -> int:
    completed_adsets = 0
    for adset in adsets:
        end_time = adset.get(MiscFieldsEnum.end_time)
        if end_time:
            end_time = datetime.strptime(end_time, '%Y-%m-%dT%H:%M:%S%z')
            now = datetime.now(end_time.tzinfo)
            if end_time < now:
                adset[MiscFieldsEnum.status] = StructureStatusEnum.COMPLETED.value
                completed_adsets += 1
    return completed_adsets
