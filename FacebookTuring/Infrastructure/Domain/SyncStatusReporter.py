import typing
from datetime import datetime

from Core.Tools.Logger.LoggerMessageBase import LoggerMessageBase, LoggerMessageTypeEnum
from FacebookTuring.Infrastructure.Domain.MiscFieldsEnum import MiscFieldsEnum
from FacebookTuring.Infrastructure.Domain.SyncStatusReport import SyncStatusReport
from FacebookTuring.Infrastructure.Mappings.LevelMapping import Level
from FacebookTuring.Infrastructure.PersistenceLayer.TuringAdAccountJournalRepository import \
    TuringAdAccountJournalRepository
from FacebookTuring.Infrastructure.PersistenceLayer.TuringMongoRepository import TuringMongoRepository


class SyncStatusReporter:

    def __init__(self,
                 account_journal_repository: TuringAdAccountJournalRepository = None,
                 structures_repository: TuringMongoRepository = None,
                 logger: typing.Any = None):
        self.__account_journal_repository = account_journal_repository
        self.__structures_repository = structures_repository
        self.__logger = logger

    def compile_report(self):
        # get latest accounts journal state
        accounts_latest_state = self.__account_journal_repository.get_all()

        # compile report
        reports = []
        for state in accounts_latest_state:
            try:
                sync_start_date = state[MiscFieldsEnum.structures_sync_start_date]
                sync_end_date = state[MiscFieldsEnum.insights_sync_end_date]

                last_updated_campaigns = self.__structures_repository.get_latest_by_account_id(
                    account_id=state[MiscFieldsEnum.account_id],
                    start_date=state[MiscFieldsEnum.structures_sync_start_date],
                    collection=Level.CAMPAIGN.value)
                last_updated_adsets = self.__structures_repository.get_latest_by_account_id(
                    account_id=state[MiscFieldsEnum.account_id],
                    start_date=state[MiscFieldsEnum.structures_sync_start_date],
                    collection=Level.ADSET.value)
                last_updated_ads = self.__structures_repository.get_latest_by_account_id(
                    account_id=state[MiscFieldsEnum.account_id],
                    start_date=state[MiscFieldsEnum.structures_sync_start_date],
                    collection=Level.AD.value)

                report = SyncStatusReport(ad_account_id=state[MiscFieldsEnum.account_id],
                                          number_of_campaigns=len(last_updated_campaigns),
                                          number_of_adsets=len(last_updated_adsets),
                                          number_of_ads=len(last_updated_ads),
                                          last_synced_on=state[MiscFieldsEnum.last_synced_on],
                                          sync_start_date=sync_start_date,
                                          sync_end_date=sync_end_date,
                                          details=state)
                reports.append(report)
            except Exception as e:
                log = LoggerMessageBase(mtype=LoggerMessageTypeEnum.ERROR,
                                        name="Facebook Turing Daily Sync Error",
                                        description="Failed to generate sync report for "
                                                    "business owner {}, ad account {}. "
                                                    "Reason: {}".format(state[MiscFieldsEnum.business_owner_id],
                                                                        state[MiscFieldsEnum.account_id],
                                                                        str(e)))
                self.__logger.logger.exception(log.to_dict())

        return reports

    def commit_report(self, report: typing.List[SyncStatusReport] = None) -> typing.NoReturn:
        created_at = datetime.now()
        self.__account_journal_repository.save_sync_report(report=report, created_at=created_at)

    def send_report(self, report: typing.List[SyncStatusReport] = None) -> typing.NoReturn:
        # todo: implement this method after Notifications.API (C#) can send attachements
        raise NotImplementedError
