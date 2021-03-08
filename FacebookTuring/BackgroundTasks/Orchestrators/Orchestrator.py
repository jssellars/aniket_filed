import concurrent.futures
import copy
import logging
import os
import typing
from collections import defaultdict
from datetime import datetime, timedelta
from itertools import chain
from time import sleep
from typing import Dict

from facebook_business.adobjects.business import Business
from facebook_business.exceptions import FacebookRequestError

from Core.mongo_adapter import MongoOperator
from Core.Web.FacebookGraphAPI.GraphAPI.GraphAPISdkBase import GraphAPISdkBase
from Core.Web.FacebookGraphAPI.GraphAPIDomain.FacebookMiscFields import FacebookMiscFields
from FacebookTuring.BackgroundTasks.Orchestrators.Synchronizer import sync
from FacebookTuring.BackgroundTasks.startup import config, fixtures
from FacebookTuring.Infrastructure.Domain.AdAccountSyncStatusEnum import AdAccountSyncStatusEnum
from FacebookTuring.Infrastructure.Domain.SyncStatusReporter import SyncStatusReporter
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
        self.__business_owner_pages_repository = TuringMongoRepository(
            config=config.mongo,
            database_name=config.mongo.accounts_journal_database_name,
            collection_name=config.mongo.business_owner_pages_collection_name,
        )
        self.__structures_repository = TuringMongoRepository(
            config=config.mongo, database_name=config.mongo.structures_database_name
        )

        self.__insights_repository = TuringMongoRepository(
            config=config.mongo, database_name=config.mongo.insights_database_name
        )

        self.__structures_syncronizer = None
        self.__insights_syncronizer = None
        self.__reporter = None

    def set_reporter(self, reporter: typing.Any = None):
        self.__reporter = reporter
        return self

    def run(self, business_owner_id: typing.AnyStr = None, user_type: UserTypeEnum = None):

        self.__update_in_progress_ad_accounts(business_owner_id)

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
                        self.__account_journal_repository,
                        [business_owner],
                        user_type,
                        permanent_token,
                    )

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
            if not permanent_token:
                continue

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

    def __delete_old_structures(self, business_owners: Dict) -> None:

        for business_owner_id, business_owner_details in business_owners.items():

            ad_account_ids = [
                business_owner[FacebookMiscFields.account_id] for business_owner in business_owner_details
            ]

            query = {
                MongoOperator.AND.value: [
                    {FacebookMiscFields.business_owner_facebook_id: business_owner_id},
                    {FacebookMiscFields.account_id: {MongoOperator.NOTIN.value: ad_account_ids}},
                ]
            }

            structure_collections = self.__structures_repository.get_collections()
            for structure_collection in structure_collections:
                self.__structures_repository.collection = structure_collection
                self.__structures_repository.delete_many(query_filter=query)

    def __update_in_progress_ad_accounts(self, business_owner_id: str):

        query = {
            MongoOperator.AND.value: [
                {
                    MongoOperator.OR.value: [
                        {FacebookMiscFields.structures_sync_status: AdAccountSyncStatusEnum.IN_PROGRESS.value},
                        {FacebookMiscFields.sync_status: AdAccountSyncStatusEnum.IN_PROGRESS.value},
                    ]
                },
                {FacebookMiscFields.business_owner_id: business_owner_id},
            ]
        }

        in_progress_ad_accounts = self.__account_journal_repository.get(query=query)
        account_ids = [entry[FacebookMiscFields.account_id] for entry in in_progress_ad_accounts]

        query = {
            MongoOperator.SET.value: {
                FacebookMiscFields.structures_sync_status: AdAccountSyncStatusEnum.PENDING.value,
                FacebookMiscFields.sync_status: AdAccountSyncStatusEnum.PENDING.value,
                FacebookMiscFields.last_synced_on: datetime.now() - timedelta(days=config.days_to_sync),
            }
        }

        query_filter = {FacebookMiscFields.account_id: {MongoOperator.IN.value: account_ids}}

        self.__account_journal_repository.update_many(query_filter, query)

        structure_collections = self.__structures_repository.get_collections()
        insights_collections = self.__insights_repository.get_collections()
        for structure_collection in structure_collections:
            self.__structures_repository.collection = structure_collection
            self.__structures_repository.delete_many(query_filter=query_filter)

        for insights_collection in insights_collections:
            self.__insights_repository.collection = insights_collection
            self.__insights_repository.delete_many(query_filter=query_filter)
