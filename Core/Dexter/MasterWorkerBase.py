import math
import time
import typing as typing
from threading import Thread

from Core.Dexter.Infrastructure.Domain.ChannelEnum import ChannelEnum
from Core.Dexter.PersistanceLayer import DexterJournalMongoRepository
from Core.Dexter.PersistanceLayer.DexterRecommendationsMongoRepository import DexterRecommendationsMongoRepository
from GoogleDexter.Infrastructure.PersistanceLayer.GoogleDexterMongoRepository import GoogleDexterMongoRepository

BATCH_SIZE = 0.25
SLEEP_TIME = 10


class MasterWorkerBase:

    def __init__(self):
        pass

    def start_algorithm_for_accounts_set(self,
                                         ad_account_ids: typing.List[typing.AnyStr] = None,
                                         business_owner_id: typing.AnyStr = None,
                                         startup: typing.Any = None,
                                         recommendations_repository: DexterRecommendationsMongoRepository = None,
                                         journal_repository: DexterJournalMongoRepository = None,
                                         channel: ChannelEnum = None):
        raise NotImplementedError

    def start_dexter_for_business_owner(self,
                                        business_owner_id: typing.AnyStr = None,
                                        business_owner_account_ids: typing.List = None,
                                        startup: typing.Any = None,
                                        recommendations_repository: DexterRecommendationsMongoRepository = None,
                                        journal_repository: DexterJournalMongoRepository = None,
                                        channel: ChannelEnum = None) -> typing.NoReturn:
        number_of_account_ids = len(business_owner_account_ids)
        batch_size = math.ceil((BATCH_SIZE * number_of_account_ids))

        for start in range(0, number_of_account_ids, batch_size):
            if start + batch_size < number_of_account_ids:
                child_thread = Thread(target=self.start_algorithm_for_accounts_set,
                                      args=(business_owner_account_ids[start:start + batch_size],
                                            business_owner_id,
                                            startup,
                                            recommendations_repository,
                                            journal_repository,
                                            channel))
                child_thread.start()
                time.sleep(SLEEP_TIME)

            else:
                child_thread = Thread(target=self.start_algorithm_for_accounts_set,
                                      args=(business_owner_account_ids[start:],
                                            business_owner_id,
                                            startup,
                                            recommendations_repository,
                                            journal_repository,
                                            channel))
                child_thread.start()
