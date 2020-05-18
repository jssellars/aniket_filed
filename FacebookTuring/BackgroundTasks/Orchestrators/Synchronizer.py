# todo: make this more efficient
import typing
from datetime import datetime, timedelta

from FacebookTuring.BackgroundTasks.Orchestrators.InsightsSyncronizer import InsightsSyncronizer
from FacebookTuring.BackgroundTasks.Orchestrators.InsightsSyncronizerBreakdowns import \
    InsightsSyncronizerBreakdownEnum, InsightsSyncronizerActionBreakdownEnum
from FacebookTuring.BackgroundTasks.Orchestrators.StructuresSyncronizer import StructuresSyncronizer
from FacebookTuring.Infrastructure.Domain.MiscFieldsEnum import MiscFieldsEnum
from FacebookTuring.Infrastructure.Mappings.LevelMapping import Level
from FacebookTuring.Infrastructure.PersistenceLayer.TuringAdAccountJournalRepository import \
    TuringAdAccountJournalRepository
from FacebookTuring.Infrastructure.PersistenceLayer.TuringMongoRepository import TuringMongoRepository

NEXT_DAY = timedelta(days=1)
SYNC_DAYS_INTERVAL = 3
DEFAULT_DATETIME_FORMAT = '%y-%m-%d'
DEFAULT_DATETIME_ISO_FORMAT = '%y-%m-%d %H:%M:%S'


def sync(structures_repository: TuringMongoRepository = None,
         insights_repository: TuringMongoRepository = None,
         account_journal_repository: TuringAdAccountJournalRepository = None,
         business_owner_details: typing.List[typing.Dict] = None) -> typing.NoReturn:
    for entry in business_owner_details:
        last_synced_on = entry[MiscFieldsEnum.last_synced_on]
        if isinstance(last_synced_on, str):
            try:
                last_synced_on = datetime.fromisoformat(last_synced_on)
            except Exception as e:
                raise e

        now = datetime.now()

        if last_synced_on < now:
            try:
                sync_structures(structures_repository, entry[MiscFieldsEnum.business_owner_id],
                                entry[MiscFieldsEnum.account_id])
                sync_insights(insights_repository, entry[MiscFieldsEnum.business_owner_id],
                              entry[MiscFieldsEnum.account_id], last_synced_on)
            except Exception as e:
                raise NotImplementedError(str(e))

        account_journal_repository.update_last_sync_time(entry[MiscFieldsEnum.account_id])


def sync_structures(structures_repository: TuringMongoRepository = None,
                    business_owner_id: typing.AnyStr = None,
                    account_id: typing.AnyStr = None) -> typing.NoReturn:
    levels = [Level.CAMPAIGN, Level.ADSET, Level.AD]

    for level in levels:
        syncronizer = StructuresSyncronizer(business_owner_id=business_owner_id,
                                            account_id=account_id,
                                            level=level)
        syncronizer.set_mongo_repository(structures_repository).run()
        syncronizer.close_database_connection()


def sync_insights(insights_repository: TuringMongoRepository = None,
                  business_owner_id: typing.AnyStr = None,
                  account_id: typing.AnyStr = None,
                  date_start: datetime = None) -> typing.NoReturn:
    date_stop = datetime.now()

    levels = [Level.CAMPAIGN, Level.ADSET, Level.AD]

    data_available = True

    for level in levels:
        if level == Level.ADSET:
            for breakdown in InsightsSyncronizerBreakdownEnum:
                for action_breakdown in InsightsSyncronizerActionBreakdownEnum:
                    syncronizer = InsightsSyncronizer(business_owner_id=business_owner_id,
                                                      account_id=account_id,
                                                      level=level,
                                                      breakdown=breakdown.value,
                                                      action_breakdown=action_breakdown.value)
                    syncronizer.set_mongo_repository(insights_repository)
                    data_available = syncronizer.check_data(date_start.strftime(DEFAULT_DATETIME_FORMAT),
                                                            date_stop.strftime(DEFAULT_DATETIME_FORMAT))

                    if data_available:
                        while date_stop >= date_start:
                            current_date_stop = date_start + timedelta(SYNC_DAYS_INTERVAL)
                            date_start_sync = date_start.strftime(DEFAULT_DATETIME_FORMAT)
                            date_stop_sync = current_date_stop.strftime(DEFAULT_DATETIME_FORMAT)

                            syncronizer.date_start = date_start_sync
                            syncronizer.date_stop = date_stop_sync
                            syncronizer.run()

                            date_start = current_date_stop + NEXT_DAY

                    syncronizer.close_database_connection()
        else:
            syncronizer = InsightsSyncronizer(business_owner_id=business_owner_id,
                                              account_id=account_id,
                                              level=level,
                                              breakdown=InsightsSyncronizerBreakdownEnum.NONE.value,
                                              action_breakdown=InsightsSyncronizerActionBreakdownEnum.NONE.value)
            syncronizer.set_mongo_repository(insights_repository)
            data_available = syncronizer.check_data(date_start.strftime(DEFAULT_DATETIME_FORMAT),
                                                    date_stop.strftime(DEFAULT_DATETIME_FORMAT))

            if data_available:
                while date_stop >= date_start:
                    current_date_stop = date_start + timedelta(SYNC_DAYS_INTERVAL)
                    date_start_sync = date_start.strftime(DEFAULT_DATETIME_FORMAT)
                    date_stop_sync = current_date_stop.strftime(DEFAULT_DATETIME_FORMAT)

                    syncronizer.date_start = date_start_sync
                    syncronizer.date_stop = date_stop_sync
                    syncronizer.run()

                    date_start = current_date_stop + NEXT_DAY

            syncronizer.close_database_connection()

        if not data_available:
            break

# def sync_insights_base(syncronizer: InsightsSyncronizer = None,
#                        date_start: datetime = None,
#                        date_stop: datetime = None):
#     data_available = syncronizer.check_data(date_start.strftime(DEFAULT_DATETIME_FORMAT),
#                                             date_stop.strftime(DEFAULT_DATETIME_FORMAT))
#
#     if data_available:
#         while date_stop >= date_start:
#             current_date_stop = date_start + timedelta(SYNC_DAYS_INTERVAL)
#             date_start_sync = date_start.strftime(DEFAULT_DATETIME_FORMAT)
#             date_stop_sync = current_date_stop.strftime(DEFAULT_DATETIME_FORMAT)
#
#             syncronizer.date_start = date_start_sync
#             syncronizer.date_stop = date_stop_sync
#             syncronizer.run()
#
#             date_start = current_date_stop + NEXT_DAY
#
#     syncronizer.close_database_connection()