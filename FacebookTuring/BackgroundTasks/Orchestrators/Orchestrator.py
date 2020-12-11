import copy
import math
import typing
from collections import defaultdict
from datetime import datetime
from threading import Thread

from FacebookTuring.BackgroundTasks.Orchestrators.Synchronizer import sync
from FacebookTuring.BackgroundTasks.startup import config, fixtures
from FacebookTuring.Infrastructure.Domain.AdAccountSyncStatusEnum import AdAccountSyncStatusEnum
from FacebookTuring.Infrastructure.Domain.MiscFieldsEnum import MiscFieldsEnum
from FacebookTuring.Infrastructure.Domain.SyncStatusReporter import SyncStatusReporter
from FacebookTuring.Infrastructure.IntegrationEvents.FacebookTuringDataSyncCompletedEvent import (
    UpdatedBusinessOwnersDetails,
    FacebookTuringDataSyncCompletedEvent,
)
from FacebookTuring.Infrastructure.IntegrationEvents.MessageTypeEnum import UserTypeEnum
from FacebookTuring.Infrastructure.PersistenceLayer.TuringAdAccountJournalRepository import (
    TuringAdAccountJournalRepository,
)
from FacebookTuring.Infrastructure.PersistenceLayer.TuringMongoRepository import TuringMongoRepository


import logging

logger = logging.getLogger(__name__)


class Orchestrator:
    ACCOUNTS_PER_THREAD = 0.20

    def __init__(
            self,
            insights_repository: TuringMongoRepository = None,
            structures_repository: TuringMongoRepository = None,
            account_journal_repository: TuringAdAccountJournalRepository = None,
    ):

        self.__insights_repository = insights_repository
        self.__structures_repository = structures_repository
        self.__account_journal_repository = account_journal_repository
        self.__structures_syncronizer = None
        self.__insights_syncronizer = None
        self.__reporter = None

    def set_insights_repository(self, insights_repository: TuringMongoRepository = None):
        self.__insights_repository = insights_repository
        return self

    def set_structures_repository(self, structures_repository: TuringMongoRepository = None):
        self.__structures_repository = structures_repository
        return self

    def set_account_journal_repository(self, account_journal_repository: TuringAdAccountJournalRepository = None):
        self.__account_journal_repository = account_journal_repository
        return self

    def set_reporter(self, reporter: typing.Any = None):
        self.__reporter = reporter
        return self

    def run(self, business_owner_id: typing.AnyStr = None, user_type: UserTypeEnum = None):
        start_sync_date = datetime.now()
        # get latest ad account state for all BO
        ad_accounts_details = self.__account_journal_repository.get_latest_accounts_active(
            business_owner_id=business_owner_id
        )

        # mark ad accounts currently being synced as sync_status = IN_PROGRESS
        self.__account_journal_repository.change_account_sync_status(
            ad_accounts_details, AdAccountSyncStatusEnum.IN_PROGRESS
        )

        # group ad accounts by business owner id
        business_owners = self.__group_by_business_owner_id(ad_accounts_details)

        # for each BO for each ad account, start a structures sync thread and an insights sync thread
        for business_owner_id, business_owner_details in business_owners.items():
            sync(
                self.__structures_repository.new_structures_repository(),
                self.__insights_repository.new_insights_repository(),
                self.__account_journal_repository.new_ad_account_journal_repository(),
                business_owner_details,
                user_type,
            )

            # # uncomment to test in sync
            # sync(self.__structures_repository.new_structures_repository(),
            #      self.__insights_repository.new_insights_repository(),
            #      self.__account_journal_repository.new_ad_account_journal_repository(),
            #      entry)

            # update ad account last sync time for current business owner based on the time when the insights sync
            # finished for each ad account.
            self.__account_journal_repository.update_last_sync_time_by_business_owner_id(business_owner_id)

            # publish message to Dexter Background tasks to start processing the data for the current business owner
            self.__publish_business_owner_synced_event(business_owner_id, start_sync_date)

        # compile and send sync status report
        if ad_accounts_details:
            self.__reporter = SyncStatusReporter(
                account_journal_repository=self.__account_journal_repository,
                structures_repository=self.__structures_repository,
            )

            sync_report = self.__reporter.compile_report()
            self.__reporter.commit_report(sync_report)

    @staticmethod
    def __group_by_business_owner_id(ad_accounts_details: typing.List[typing.Dict] = None) -> typing.Dict:
        business_owner_details = defaultdict(list)
        for entry in ad_accounts_details:
            business_owner_details[entry[MiscFieldsEnum.business_owner_id]].append(copy.deepcopy(entry))
        return business_owner_details

    def __publish_business_owner_synced_event(
            self, business_owner_id: typing.AnyStr = None, sync_start_date: datetime = None
    ) -> None:
        account_ids = self.__account_journal_repository.get_last_updated_accounts(business_owner_id, sync_start_date)
        business_owner_updated_details = UpdatedBusinessOwnersDetails(
            business_owner_facebook_id=business_owner_id, ad_account_ids=account_ids
        )
        business_owner_synced_event = FacebookTuringDataSyncCompletedEvent(
            business_owners=[business_owner_updated_details]
        )
        try:
            rabbitmq_adapter = fixtures.rabbitmq_adapter
            rabbitmq_adapter.publish(business_owner_synced_event)
            logger.info({"rabbitmq": rabbitmq_adapter.serialize_message(business_owner_synced_event)})
        except Exception as e:
            logger.exception(f"{business_owner_synced_event.message_type} || {repr(e)}")
