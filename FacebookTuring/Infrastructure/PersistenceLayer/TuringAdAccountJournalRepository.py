import copy
import typing
from datetime import datetime, timedelta

from Core.Tools.Misc.ObjectSerializers import object_to_json
from Core.Tools.MongoRepository.MongoOperator import MongoOperator
from Core.Tools.MongoRepository.MongoRepositoryBase import MongoRepositoryBase, MongoProjectionState
from FacebookTuring.Infrastructure.Domain.MiscFieldsEnum import MiscFieldsEnum
from FacebookTuring.Infrastructure.Domain.StructureStatusEnum import StructureStatusEnum
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
            self.update_ad_accounts_status(removed_ad_accounts, StructureStatusEnum.REMOVED)

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

    def get_latest_accounts_active(self):
        query = {
            MiscFieldsEnum.status: {
                MongoOperator.EQUALS.value: StructureStatusEnum.ACTIVE.value
            }
        }
        return self.get(query)

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
        # ad_accounts = [ad_account for ad_account in ad_accounts]
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

    def add_ad_accounts(self, business_owner_id: typing.AnyStr = None,
                        ad_accounts: typing.List[AdAccountDetails] = None) -> typing.NoReturn:
        new_accounts = []
        for ad_account in ad_accounts:
            entry = object_to_json(ad_account)
            entry[MiscFieldsEnum.account_id] = entry.pop(MiscFieldsEnum.id).split("_")[1]
            entry[MiscFieldsEnum.business_owner_id] = business_owner_id
            entry[MiscFieldsEnum.status] = StructureStatusEnum.ACTIVE.value
            #  todo: replace to last 3 months after we are sure everything works.
            #  It takes too long for 3months. Makes testing hard.
            entry[MiscFieldsEnum.last_synced_on] = (datetime.now() -
                                                    timedelta(days=MiscFieldsEnum.last_one_months))
            new_accounts.append(copy.deepcopy(entry))

        self.add_many(new_accounts)

    def new_ad_account_journal_repository(self):
        repository = TuringAdAccountJournalRepository(config=self.config,
                                                      database_name=self.config.accounts_journal_database_name,
                                                      collection_name=self.config.accounts_journal_collection_name)
        return repository
