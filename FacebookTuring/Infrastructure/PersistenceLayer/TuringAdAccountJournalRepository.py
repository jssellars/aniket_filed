import copy
import typing
from datetime import datetime, timedelta

from Core.Tools.Misc.ObjectSerializers import object_to_json
from Core.Tools.MongoRepository.MongoOperator import MongoOperator
from Core.Tools.MongoRepository.MongoRepositoryBase import MongoRepositoryBase, MongoProjectionState
from FacebookTuring.Infrastructure.Domain.AdAccountSyncStatusEnum import AdAccountSyncStatusEnum
from FacebookTuring.Infrastructure.Domain.MiscFieldsEnum import MiscFieldsEnum
from FacebookTuring.Infrastructure.Domain.StructureStatusEnum import StructureStatusEnum
from FacebookTuring.Infrastructure.Domain.SyncStatusReport import SyncStatusReport
from FacebookTuring.Infrastructure.IntegrationEvents.BusinessOwnerPreferencesChangedEvent import AdAccountDetails


class TuringAdAccountJournalRepository(MongoRepositoryBase):
    DEFAULT_DATETIME_FORMAT = "%Y-%m-%d"

    def __init__(self, *args, **kwargs):
        super(TuringAdAccountJournalRepository, self).__init__(*args, **kwargs)

    def update_business_owner(self,
                              business_owner_id: typing.AnyStr = None,
                              ad_accounts: typing.List[AdAccountDetails] = None) -> typing.NoReturn:
        existing_ad_accounts = self.get_ad_accounts_by_business_owner_id(business_owner_id)
        existing_ad_accounts_ids = [ad_account.get(MiscFieldsEnum.account_id, None) for ad_account in
                                    existing_ad_accounts]
        ad_accounts_ids = [ad_account.id.split("_")[1] for ad_account in ad_accounts]

        removed_ad_accounts = list(set(existing_ad_accounts_ids) - set(ad_accounts_ids))
        if removed_ad_accounts:
            self.update_ad_accounts_status(removed_ad_accounts, StructureStatusEnum.REMOVED.value)

        new_ad_accounts_ids = list(set(ad_accounts_ids) - set(existing_ad_accounts_ids))
        if new_ad_accounts_ids:
            new_ad_accounts = [ad_account for ad_account in ad_accounts if
                               ad_account.id.split("_")[1] in new_ad_accounts_ids]
            self.add_ad_accounts(business_owner_id, new_ad_accounts)

    def get_ad_accounts_by_business_owner_id(self, business_owner_id: typing.AnyStr = None):
        query = {
            MongoOperator.AND.value: [{
                MiscFieldsEnum.business_owner_id: {
                    MongoOperator.EQUALS.value: business_owner_id
                },
                MiscFieldsEnum.status: {
                    MongoOperator.IN.value: [StructureStatusEnum.ACTIVE.value,
                                             StructureStatusEnum.REMOVED.value]
                }
            }]
        }
        return self.get(query=query)

    def get_latest_accounts_active(self, business_owner_id: typing.AnyStr = None):
        query = {
            MongoOperator.AND.value: [
                {
                    MiscFieldsEnum.status: {
                        MongoOperator.EQUALS.value: StructureStatusEnum.ACTIVE.value
                    }
                },
                {
                    MiscFieldsEnum.structures_sync_status: {
                        MongoOperator.IN.value: [AdAccountSyncStatusEnum.COMPLETED.value,
                                                 AdAccountSyncStatusEnum.PENDING.value,
                                                 AdAccountSyncStatusEnum.COMPLETED_WITH_ERRORS.value]
                    }
                },
                {
                    MiscFieldsEnum.insights_sync_status: {
                        MongoOperator.IN.value: [AdAccountSyncStatusEnum.COMPLETED.value,
                                                 AdAccountSyncStatusEnum.PENDING.value,
                                                 AdAccountSyncStatusEnum.COMPLETED_WITH_ERRORS.value]
                    }
                }
            ]
        }
        if business_owner_id:
            query[MongoOperator.AND.value].append({MiscFieldsEnum.business_owner_id:
                {
                    MongoOperator.EQUALS.value: business_owner_id
                }
            })

        projection = {
            MongoOperator.GROUP_KEY.value: MongoProjectionState.OFF.value
        }
        results = self.get(query, projection)
        return results

    def get_last_updated_accounts(self, business_owner_id: typing.AnyStr = None) -> typing.List[typing.AnyStr]:
        query = {
            MongoOperator.AND.value: [
                {
                    MiscFieldsEnum.business_owner_id: {
                        MongoOperator.EQUALS.value: business_owner_id
                    },
                    MiscFieldsEnum.last_synced_on: {
                        MongoOperator.EQUALS.value: datetime.now().strftime(self.DEFAULT_DATETIME_FORMAT)
                    },
                    MiscFieldsEnum.status: {
                        MongoOperator.EQUALS.value: StructureStatusEnum.ACTIVE.value
                    }
                }
            ]
        }
        projection = {
            MiscFieldsEnum.account_id: MongoProjectionState.ON.value,
            MongoOperator.GROUP_KEY.value: MongoProjectionState.OFF.value
        }
        account_ids = self.get(query, projection)
        return [account_id[MiscFieldsEnum.account_id] for account_id in account_ids]

    def update_ad_accounts_status(self, ad_accounts: typing.List[typing.AnyStr] = None,
                                  new_status: StructureStatusEnum = None) -> typing.NoReturn:
        query_filter = {
            MiscFieldsEnum.account_id: {
                MongoOperator.IN.value: ad_accounts
            }
        }
        query = {
            MongoOperator.SET.value: {
                MiscFieldsEnum.status: new_status,
            }
        }
        return self.update_many(query_filter, query)

    def update_last_sync_time(self, account_id: typing.AnyStr = None):
        query_filter = {
            MiscFieldsEnum.account_id: {
                MongoOperator.EQUALS.value: account_id
            }
        }
        query = {
            MongoOperator.SET.value: {
                MiscFieldsEnum.last_synced_on: datetime.now().strftime(self.DEFAULT_DATETIME_FORMAT),
            }
        }
        self.update_one(query_filter, query)

    def update_last_sync_time_by_business_owner_id(self, business_owner_id: typing.AnyStr = None) -> typing.NoReturn:
        # get business owner details
        query = {
            MiscFieldsEnum.business_owner_id: {
                MongoOperator.EQUALS.value: business_owner_id
            }
        }
        business_owner_details = self.get(query)

        # update last synced on to match the time when insights finished syncing for each ad account
        for detail in business_owner_details:
            update_last_sync_time_query_filter = {
                MiscFieldsEnum.account_id: {
                    MongoOperator.EQUALS.value: detail.get(MiscFieldsEnum.account_id)
                }
            }
            update_last_sync_time_query = {
                MongoOperator.SET.value: {
                    MiscFieldsEnum.last_synced_on: detail.get(MiscFieldsEnum.insights_sync_end_date),
                    MiscFieldsEnum.previous_last_synced_on: detail.get(MiscFieldsEnum.last_synced_on)
                }
            }
            self.update_one(query_filter=update_last_sync_time_query_filter, query=update_last_sync_time_query)

    def add_ad_accounts(self, business_owner_id: typing.AnyStr = None,
                        ad_accounts: typing.List[AdAccountDetails] = None) -> typing.NoReturn:
        new_accounts = []
        for ad_account in ad_accounts:
            entry = object_to_json(ad_account)
            entry[MiscFieldsEnum.account_id] = entry.pop(MiscFieldsEnum.id).split("_")[1]
            entry[MiscFieldsEnum.business_owner_id] = business_owner_id
            entry[MiscFieldsEnum.status] = StructureStatusEnum.ACTIVE.value
            entry[MiscFieldsEnum.structures_sync_status] = AdAccountSyncStatusEnum.PENDING.value
            entry[MiscFieldsEnum.insights_sync_status] = AdAccountSyncStatusEnum.PENDING.value
            entry[MiscFieldsEnum.last_synced_on] = (datetime.now() -
                                                    timedelta(days=MiscFieldsEnum.last_one_months))
            entry[MiscFieldsEnum.previous_last_synced_on] = None
            entry[MiscFieldsEnum.insights_sync_start_date] = None
            entry[MiscFieldsEnum.insights_sync_end_date] = None
            entry[MiscFieldsEnum.structures_sync_start_date] = None
            entry[MiscFieldsEnum.structures_sync_end_date] = None

            new_accounts.append(copy.deepcopy(entry))

        self.add_many(new_accounts)

    def change_account_sync_status(self,
                                   accounts_details: typing.List[typing.Dict] = None,
                                   sync_status: AdAccountSyncStatusEnum = None) -> typing.NoReturn:
        self.set_collection(self.config.accounts_journal_collection_name)

        for entry in accounts_details:
            # create query to filter entries by business owner and ad account id and status
            query_filter = {
                MongoOperator.AND.value: [
                    {
                        MiscFieldsEnum.business_owner_id: {
                            MongoOperator.EQUALS.value: entry[MiscFieldsEnum.business_owner_id]
                        }
                    },
                    {
                        MiscFieldsEnum.account_id: {
                            MongoOperator.EQUALS.value: entry[MiscFieldsEnum.account_id]
                        }
                    },
                    {
                        MiscFieldsEnum.status: {
                            MongoOperator.EQUALS.value: entry[MiscFieldsEnum.status]
                        }
                    }
                ]
            }

            # create query to update entry status to sync_status
            query = {
                MongoOperator.SET.value: {
                    MiscFieldsEnum.sync_status: sync_status.value
                }
            }

            self.update_one(query_filter=query_filter, query=query)

    def change_account_sync_start_date(self, account_id: typing.AnyStr = None) -> typing.NoReturn:
        self.set_collection(self.config.accounts_journal_collection_name)
        query_filter = {
            MiscFieldsEnum.account_id: {
                MongoOperator.EQUALS.value: account_id
            }
        }
        query = {
            MongoOperator.SET.value: {
                MiscFieldsEnum.sync_start_date: datetime.now(),
                MiscFieldsEnum.sync_end_date: None,
                MiscFieldsEnum.sync_status: AdAccountSyncStatusEnum.IN_PROGRESS.value,
                MiscFieldsEnum.insights_sync_status: AdAccountSyncStatusEnum.IN_PROGRESS.value,
                MiscFieldsEnum.structures_sync_status: AdAccountSyncStatusEnum.IN_PROGRESS.value
            }
        }
        self.update_one(query_filter=query_filter, query=query)

    def change_account_structures_sync_status(self,
                                              account_id: typing.AnyStr = None,
                                              new_status: AdAccountSyncStatusEnum = None,
                                              start_date: datetime = None,
                                              end_date: datetime = None) -> typing.NoReturn:
        self.set_collection(self.config.accounts_journal_collection_name)
        query_filter = {
            MiscFieldsEnum.account_id: {
                MongoOperator.EQUALS.value: account_id
            }
        }

        query = {
            MongoOperator.SET.value: {
                MiscFieldsEnum.structures_sync_status: new_status.value
            }
        }

        if start_date:
            query[MongoOperator.SET.value][MiscFieldsEnum.structures_sync_start_date] = start_date
        if end_date:
            query[MongoOperator.SET.value][MiscFieldsEnum.structures_sync_end_date] = end_date

        self.update_one(query_filter, query)

    def change_account_insights_sync_status(self,
                                            account_id: typing.AnyStr = None,
                                            new_status: AdAccountSyncStatusEnum = None,
                                            start_date: datetime = None,
                                            end_date: datetime = None) -> typing.NoReturn:
        self.set_collection(self.config.accounts_journal_collection_name)
        query_filter = {
            MiscFieldsEnum.account_id: {
                MongoOperator.EQUALS.value: account_id
            }
        }
        query = {
            MongoOperator.SET.value: {
                MiscFieldsEnum.insights_sync_status: new_status.value
            }
        }
        if start_date:
            query[MongoOperator.SET.value][MiscFieldsEnum.insights_sync_start_date] = start_date
        if end_date:
            query[MongoOperator.SET.value][MiscFieldsEnum.insights_sync_end_date] = end_date

        self.update_one(query_filter, query)

    def save_sync_report(self,
                         report: typing.List[SyncStatusReport] = None,
                         created_at: datetime = None) -> typing.NoReturn:
        self.set_collection(self.config.sync_reports_collection)
        document = {
            MiscFieldsEnum.created_at: created_at,
            MiscFieldsEnum.report: object_to_json(report)
        }
        self.add_one(document)

    def new_ad_account_journal_repository(self):
        repository = TuringAdAccountJournalRepository(config=self.config,
                                                      database_name=self.config.accounts_journal_database_name,
                                                      collection_name=self.config.accounts_journal_collection_name)
        return repository
