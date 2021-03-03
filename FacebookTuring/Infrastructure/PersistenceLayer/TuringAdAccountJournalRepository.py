import copy
from datetime import datetime, timedelta
from typing import Dict, List

from Core.mongo_adapter import MongoOperator, MongoProjectionState, MongoRepositoryBase
from Core.Tools.Misc.ObjectSerializers import object_to_json
from Core.Web.FacebookGraphAPI.GraphAPIDomain.FacebookMiscFields import FacebookMiscFields
from FacebookTuring.Infrastructure.Domain.AdAccountSyncStatusEnum import AdAccountSyncStatusEnum
from FacebookTuring.Infrastructure.Domain.StructureStatusEnum import StructureStatusEnum
from FacebookTuring.Infrastructure.Domain.SyncStatusReport import SyncStatusReport
from FacebookTuring.Infrastructure.IntegrationEvents.BusinessOwnerPreferencesChangedEvent import AdAccountDetails


class TuringAdAccountJournalRepository(MongoRepositoryBase):
    DEFAULT_DATETIME_FORMAT = "%Y-%m-%d"

    def __init__(self, *args, **kwargs):
        super(TuringAdAccountJournalRepository, self).__init__(*args, **kwargs)

    def update_business_owner(
        self,
        business_owner_id: str = None,
        ad_accounts: List[AdAccountDetails] = None,
        days_to_sync: int = FacebookMiscFields.last_three_months,
    ) -> None:
        existing_ad_accounts = self.get_ad_accounts_by_business_owner_id(business_owner_id)
        existing_ad_accounts_ids = [
            ad_account.get(FacebookMiscFields.account_id, None) for ad_account in existing_ad_accounts
        ]
        ad_accounts_ids = [ad_account.id.split("_")[1] for ad_account in ad_accounts]

        removed_ad_accounts = list(set(existing_ad_accounts_ids) - set(ad_accounts_ids))
        if removed_ad_accounts:
            self.update_ad_accounts_status(removed_ad_accounts, StructureStatusEnum.REMOVED.value)

        new_ad_accounts_ids = list(set(ad_accounts_ids) - set(existing_ad_accounts_ids))
        if new_ad_accounts_ids:
            new_ad_accounts = [
                ad_account for ad_account in ad_accounts if ad_account.id.split("_")[1] in new_ad_accounts_ids
            ]
            self.add_ad_accounts(business_owner_id, new_ad_accounts, days_to_sync)

    def get_ad_accounts_by_business_owner_id(self, business_owner_id: str = None):
        query = {
            MongoOperator.AND.value: [
                {
                    FacebookMiscFields.business_owner_id: {MongoOperator.EQUALS.value: business_owner_id},
                    FacebookMiscFields.status: {
                        MongoOperator.IN.value: [StructureStatusEnum.ACTIVE.value, StructureStatusEnum.REMOVED.value]
                    },
                }
            ]
        }
        return self.get(query=query)

    def get_latest_accounts_active(self, business_owner_id: str = None):
        query = {
            MongoOperator.AND.value: [
                {FacebookMiscFields.status: {MongoOperator.EQUALS.value: StructureStatusEnum.ACTIVE.value}},
                {
                    FacebookMiscFields.structures_sync_status: {
                        MongoOperator.IN.value: [
                            AdAccountSyncStatusEnum.COMPLETED.value,
                            AdAccountSyncStatusEnum.PENDING.value,
                            AdAccountSyncStatusEnum.COMPLETED_WITH_ERRORS.value,
                        ]
                    }
                },
                {
                    FacebookMiscFields.insights_sync_status: {
                        MongoOperator.IN.value: [
                            AdAccountSyncStatusEnum.COMPLETED.value,
                            AdAccountSyncStatusEnum.PENDING.value,
                            AdAccountSyncStatusEnum.COMPLETED_WITH_ERRORS.value,
                        ]
                    }
                },
            ]
        }
        if business_owner_id:
            query[MongoOperator.AND.value].append(
                {FacebookMiscFields.business_owner_id: {MongoOperator.EQUALS.value: business_owner_id}}
            )

        projection = {MongoOperator.GROUP_KEY.value: MongoProjectionState.OFF.value}
        results = self.get(query, projection)
        return results

    def get_last_updated_accounts(self, business_owner_id: str = None, last_updated_at: datetime = None) -> List[str]:
        query = {
            MongoOperator.AND.value: [
                {
                    FacebookMiscFields.business_owner_id: {MongoOperator.EQUALS.value: business_owner_id},
                    FacebookMiscFields.last_synced_on: {MongoOperator.GREATERTHANEQUAL.value: last_updated_at},
                    FacebookMiscFields.status: {MongoOperator.EQUALS.value: StructureStatusEnum.ACTIVE.value},
                }
            ]
        }
        projection = {
            FacebookMiscFields.account_id: MongoProjectionState.ON.value,
            MongoOperator.GROUP_KEY.value: MongoProjectionState.OFF.value,
        }
        account_ids = self.get(query, projection)
        return [account_id[FacebookMiscFields.account_id] for account_id in account_ids]

    def update_ad_accounts_status(self, ad_accounts: List[str] = None, new_status: StructureStatusEnum = None) -> None:
        query_filter = {FacebookMiscFields.account_id: {MongoOperator.IN.value: ad_accounts}}
        query = {
            MongoOperator.SET.value: {
                FacebookMiscFields.status: new_status,
            }
        }
        return self.update_many(query_filter, query)

    def update_last_sync_time(self, account_id: str = None):
        query_filter = {FacebookMiscFields.account_id: {MongoOperator.EQUALS.value: account_id}}
        query = {
            MongoOperator.SET.value: {
                FacebookMiscFields.last_synced_on: datetime.now().strftime(self.DEFAULT_DATETIME_FORMAT),
            }
        }
        self.update_one(query_filter, query)

    def update_last_sync_time_by_business_owner_id(self, business_owner_id: str = None) -> None:
        # get business owner details
        query = {FacebookMiscFields.business_owner_id: {MongoOperator.EQUALS.value: business_owner_id}}
        business_owner_details = self.get(query)

        # update last synced on to match the time when insights finished syncing for each ad account
        for detail in business_owner_details:
            update_last_sync_time_query_filter = {
                FacebookMiscFields.account_id: {MongoOperator.EQUALS.value: detail.get(FacebookMiscFields.account_id)}
            }
            update_last_sync_time_query = {
                MongoOperator.SET.value: {
                    FacebookMiscFields.last_synced_on: detail.get(FacebookMiscFields.insights_sync_end_date),
                    FacebookMiscFields.previous_last_synced_on: detail.get(FacebookMiscFields.last_synced_on),
                    FacebookMiscFields.sync_status: AdAccountSyncStatusEnum.COMPLETED.value,
                }
            }
            self.update_one(query_filter=update_last_sync_time_query_filter, query=update_last_sync_time_query)

    def add_ad_accounts(
        self,
        business_owner_id: str = None,
        ad_accounts: List[AdAccountDetails] = None,
        days_to_sync: int = FacebookMiscFields.last_one_months,
    ) -> None:
        new_accounts = []
        for ad_account in ad_accounts:
            entry = object_to_json(ad_account)
            entry[FacebookMiscFields.account_id] = entry.pop(FacebookMiscFields.id).split("_")[1]
            entry[FacebookMiscFields.business_owner_id] = business_owner_id
            entry[FacebookMiscFields.status] = StructureStatusEnum.ACTIVE.value
            entry[FacebookMiscFields.structures_sync_status] = AdAccountSyncStatusEnum.PENDING.value
            entry[FacebookMiscFields.insights_sync_status] = AdAccountSyncStatusEnum.PENDING.value
            entry[FacebookMiscFields.last_synced_on] = datetime.now() - timedelta(days=days_to_sync)
            entry[FacebookMiscFields.previous_last_synced_on] = None
            entry[FacebookMiscFields.insights_sync_start_date] = None
            entry[FacebookMiscFields.insights_sync_end_date] = None
            entry[FacebookMiscFields.structures_sync_start_date] = None
            entry[FacebookMiscFields.structures_sync_end_date] = None

            new_accounts.append(copy.deepcopy(entry))

        self.add_many(new_accounts)

    def change_account_sync_status(
        self, accounts_details: List[Dict] = None, sync_status: AdAccountSyncStatusEnum = None
    ) -> None:
        self.collection = self.config.accounts_journal_collection_name

        for entry in accounts_details:
            # create query to filter entries by business owner and ad account id and status
            query_filter = {
                MongoOperator.AND.value: [
                    {
                        FacebookMiscFields.business_owner_id: {
                            MongoOperator.EQUALS.value: entry[FacebookMiscFields.business_owner_id]
                        }
                    },
                    {FacebookMiscFields.account_id: {MongoOperator.EQUALS.value: entry[FacebookMiscFields.account_id]}},
                    {FacebookMiscFields.status: {MongoOperator.EQUALS.value: entry[FacebookMiscFields.status]}},
                ]
            }

            # create query to update entry status to sync_status
            query = {MongoOperator.SET.value: {FacebookMiscFields.sync_status: sync_status.value}}

            self.update_one(query_filter=query_filter, query=query)

    def change_account_sync_start_date(self, account_id: str = None) -> None:
        self.collection = self.config.accounts_journal_collection_name
        query_filter = {FacebookMiscFields.account_id: {MongoOperator.EQUALS.value: account_id}}
        query = {
            MongoOperator.SET.value: {
                FacebookMiscFields.sync_start_date: datetime.now(),
                FacebookMiscFields.sync_end_date: None,
                FacebookMiscFields.sync_status: AdAccountSyncStatusEnum.IN_PROGRESS.value,
                FacebookMiscFields.insights_sync_status: AdAccountSyncStatusEnum.IN_PROGRESS.value,
                FacebookMiscFields.structures_sync_status: AdAccountSyncStatusEnum.IN_PROGRESS.value,
            }
        }
        self.update_one(query_filter=query_filter, query=query)

    def change_account_structures_sync_status(
        self,
        account_id: str = None,
        new_status: AdAccountSyncStatusEnum = None,
        start_date: datetime = None,
        end_date: datetime = None,
    ) -> None:
        self.collection = self.config.accounts_journal_collection_name
        query_filter = {FacebookMiscFields.account_id: {MongoOperator.EQUALS.value: account_id}}

        query = {MongoOperator.SET.value: {FacebookMiscFields.structures_sync_status: new_status.value}}

        if start_date:
            query[MongoOperator.SET.value][FacebookMiscFields.structures_sync_start_date] = start_date
        if end_date:
            query[MongoOperator.SET.value][FacebookMiscFields.structures_sync_end_date] = end_date

        self.update_one(query_filter, query)

    def change_account_insights_sync_status(
        self,
        account_id: str = None,
        new_status: AdAccountSyncStatusEnum = None,
        start_date: datetime = None,
        end_date: datetime = None,
    ) -> None:
        self.collection = self.config.accounts_journal_collection_name
        query_filter = {FacebookMiscFields.account_id: {MongoOperator.EQUALS.value: account_id}}
        query = {MongoOperator.SET.value: {FacebookMiscFields.insights_sync_status: new_status.value}}
        if start_date:
            query[MongoOperator.SET.value][FacebookMiscFields.insights_sync_start_date] = start_date
        if end_date:
            query[MongoOperator.SET.value][FacebookMiscFields.insights_sync_end_date] = end_date

        self.update_one(query_filter, query)

    def save_sync_report(self, report: List[SyncStatusReport] = None, created_at: datetime = None) -> None:
        self.collection = self.config.accounts_journal_sync_reports_collection_name
        document = {
            FacebookMiscFields.created_at: created_at,
            FacebookMiscFields.report: [object_to_json(entry) for entry in report],
        }
        self.add_one(document)
