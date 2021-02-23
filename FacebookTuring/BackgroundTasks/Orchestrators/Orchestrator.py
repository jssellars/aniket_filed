import concurrent.futures
import copy
import logging
import os
import typing
from collections import defaultdict
from datetime import datetime
from itertools import chain
from time import sleep
from typing import Dict, List

from facebook_business.adobjects.business import Business
from facebook_business.exceptions import FacebookRequestError

from Core.Web.FacebookGraphAPI.GraphAPI.GraphAPISdkBase import GraphAPISdkBase
from Core.Web.FacebookGraphAPI.GraphAPIDomain.FacebookMiscFields import FacebookMiscFields
from Core.mongo_adapter import MongoOperator
from FacebookTuring.BackgroundTasks.Orchestrators.Synchronizer import sync
from FacebookTuring.BackgroundTasks.startup import fixtures, config
from FacebookTuring.Infrastructure.Domain.AdAccountSyncStatusEnum import AdAccountSyncStatusEnum
from FacebookTuring.Infrastructure.Domain.SyncStatusReporter import SyncStatusReporter
from FacebookTuring.Infrastructure.IntegrationEvents.FacebookTuringDataSyncCompletedEvent import (
    FacebookTuringDataSyncCompletedEvent,
    UpdatedBusinessOwnersDetails,
)
from FacebookTuring.Infrastructure.IntegrationEvents.MessageTypeEnum import UserTypeEnum
from FacebookTuring.Infrastructure.PersistenceLayer.TuringAdAccountJournalRepository import (
    TuringAdAccountJournalRepository,
)
from FacebookTuring.Infrastructure.PersistenceLayer.TuringMongoRepository import TuringMongoRepository

logger = logging.getLogger(__name__)

NUMBER_OF_WORKERS = (os.cpu_count() or 1) * 2
RATE_LIMIT_EXCEPTION_STATUS = 80000
SLEEP_ON_RATE_LIMIT_EXCEPTION = 3600


class Orchestrator:
    def __init__(self):
        self.__account_journal_repository = TuringAdAccountJournalRepository(
            config=config.mongo,
            database_name=config.mongo.accounts_journal_database_name,
            collection_name=config.mongo.accounts_journal_collection_name,
        )
        self.__insights_repository = TuringMongoRepository(
            config=config.mongo, database_name=config.mongo.insights_database_name
        )
        self.__structures_repository = TuringMongoRepository(
            config=config.mongo, database_name=config.mongo.structures_database_name
        )
        self.__business_owner_pages_repository = TuringMongoRepository(
            config=config.mongo,
            database_name=config.mongo.accounts_journal_database_name,
            collection_name=config.mongo.business_owner_pages_collection_name,
        )

        self.__structures_syncronizer = None
        self.__insights_syncronizer = None
        self.__reporter = None

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

        self.__delete_old_structures(business_owners)

        self.__sync_business_pages(business_owners)

        # for each BO for each ad account, start a structures sync thread and an insights sync thread
        for business_owner_id, business_owner_details in business_owners.items():
            permanent_token = fixtures.business_owner_repository.get_permanent_token(business_owner_id)
            with concurrent.futures.ThreadPoolExecutor() as executor:
                for business_owner in business_owner_details:
                    executor.submit(
                        sync,
                        self.__structures_repository.new_structures_repository(),
                        self.__insights_repository.new_insights_repository(),
                        self.__account_journal_repository.new_ad_account_journal_repository(),
                        [business_owner],
                        user_type,
                        permanent_token,
                    )

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

    def __sync_business_pages(self, business_owners: Dict):

        for business_owner_id, business_owner_details in business_owners.items():

            permanent_token = fixtures.business_owner_repository.get_permanent_token(business_owner_id)
            GraphAPISdkBase(config.facebook, permanent_token)

            business_ids = set()
            for business_owner in business_owner_details:
                business_ids.add(business_owner["business_facebook_id"])

            for business_id in business_ids:
                try:
                    business = Business(business_id)

                    # get owned pages
                    owned_pages = business.get_owned_pages()
                    # get client pages
                    client_pages = business.get_client_pages()
                    all_pages = chain(owned_pages, client_pages)

                    # Map and remove duplicates
                    ids = set()
                    pages = []
                    for page in all_pages:
                        if not page["id"] in ids:
                            ids.add(page["id"])
                            current_page = page.export_all_data()
                            current_page["business_id"] = business_id
                            pages.append(current_page)

                    self.__business_owner_pages_repository.delete_many({"business_id": business_id})
                    self.__business_owner_pages_repository.add_many(pages)

                except FacebookRequestError as fb_ex:
                    if fb_ex.http_status() == RATE_LIMIT_EXCEPTION_STATUS:
                        sleep(SLEEP_ON_RATE_LIMIT_EXCEPTION)
                    else:
                        continue

                except Exception:
                    continue

    @staticmethod
    def __group_by_business_owner_id(ad_accounts_details: typing.List[typing.Dict] = None) -> typing.Dict:
        business_owner_details = defaultdict(list)
        for entry in ad_accounts_details:
            business_owner_details[entry[FacebookMiscFields.business_owner_id]].append(copy.deepcopy(entry))
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

    def __delete_old_structures(self, business_owners: Dict) -> None:

        for business_owner_id, business_owner_details in business_owners.items():

            ad_account_ids = [business_owner[FacebookMiscFields.account_id] for business_owner in business_owner_details]

            query = {
                MongoOperator.AND.value: [
                    {
                        FacebookMiscFields.business_owner_facebook_id: business_owner_id
                    },
                    {
                        FacebookMiscFields.account_id: {MongoOperator.NOTIN.value: ad_account_ids}
                    }
                ]
            }

            structure_collections = self.__structures_repository.get_collections()
            for structure_collection in structure_collections:
                self.__structures_repository.collection = structure_collection
                self.__structures_repository.delete_many(query_filter=query)
