import copy
import math
import typing
from collections import defaultdict
from threading import Thread

from Core.Tools.Logger.LoggerMessageBase import LoggerMessageBase, LoggerMessageTypeEnum
from Core.Tools.RabbitMQ.RabbitMqClient import RabbitMqClient
from FacebookTuring.BackgroundTasks.Orchestrators.Synchronizer import sync
from FacebookTuring.BackgroundTasks.Startup import startup
from FacebookTuring.Infrastructure.Domain.MiscFieldsEnum import MiscFieldsEnum
from FacebookTuring.Infrastructure.IntegrationEvents.FacebookTuringDataSyncCompletedEvent import \
    UpdatedBusinessOwnersDetails, \
    FacebookTuringDataSyncCompletedEvent
from FacebookTuring.Infrastructure.PersistenceLayer.TuringAdAccountJournalRepository import \
    TuringAdAccountJournalRepository
from FacebookTuring.Infrastructure.PersistenceLayer.TuringMongoRepository import TuringMongoRepository


class Orchestrator:
    ACCOUNTS_PER_THREAD = 0.50

    def __init__(self,
                 insights_repository: TuringMongoRepository = None,
                 structures_repository: TuringMongoRepository = None,
                 account_journal_repository: TuringAdAccountJournalRepository = None):

        self.__insights_repository = insights_repository
        self.__structures_repository = structures_repository
        self.__account_journal_repository = account_journal_repository
        self.__structures_syncronizer = None
        self.__insights_syncronizer = None
        self.__logger = None
        self.__rabbit_logger = None

    def set_insights_repository(self, insights_repository: TuringMongoRepository = None):
        self.__insights_repository = insights_repository
        return self

    def set_structures_repository(self, structures_repository: TuringMongoRepository = None):
        self.__structures_repository = structures_repository
        return self

    def set_account_journal_repository(self, account_journal_repository: TuringAdAccountJournalRepository = None):
        self.__account_journal_repository = account_journal_repository
        return self

    def set_logger(self, logger: typing.Any):
        self.__logger = logger
        return self

    def set_rabbit_logger(self, logger: typing.Any):
        self.__rabbit_logger = logger
        return self

    def run(self, business_owner_id: typing.AnyStr = None):
        # get latest ad account state for all BO
        ad_accounts_details = self.__account_journal_repository.get_latest_accounts_active(
            business_owner_id=business_owner_id)
        business_owners = self.__group_by_business_owner_id(ad_accounts_details)

        # for each BO for each ad account, start a structures sync thread and an insights sync thread
        for business_owner_id, business_owner_details in business_owners.items():
            tasks = list()
            step = math.ceil(self.ACCOUNTS_PER_THREAD * len(business_owner_details))
            for index in range(0, len(business_owner_details), step):
                entry = business_owner_details[index:index + step]
                tasks.append(Thread(target=sync,
                                    args=(self.__structures_repository.new_structures_repository(),
                                          self.__insights_repository.new_insights_repository(),
                                          self.__account_journal_repository.new_ad_account_journal_repository(),
                                          entry)))
            for task in tasks:
                task.start()
            #  publish event with updated ad accounts to Facebook Dexter
            # this publish event can be modified to publish one update for all BOs available. It makes more sense to
            # publish as they come to minimise the
            # waiting time for Dexter to run and the computation volume.
            for task in tasks:
                task.join()

            # # uncomment to test in sync
            # sync(self.__structures_repository.new_structures_repository(),
            #      self.__insights_repository.new_insights_repository(),
            #      self.__account_journal_repository.new_ad_account_journal_repository(),
            #      entry)

            self.__publish_business_owner_synced_event(business_owner_id)

    @staticmethod
    def __group_by_business_owner_id(ad_accounts_details: typing.List[typing.Dict] = None) -> typing.Dict:
        business_owner_details = defaultdict(list)
        for entry in ad_accounts_details:
            business_owner_details[entry[MiscFieldsEnum.business_owner_id]].append(copy.deepcopy(entry))
        return business_owner_details

    def __publish_business_owner_synced_event(self,
                                              business_owner_id: typing.AnyStr = None) -> typing.NoReturn:
        account_ids = self.__account_journal_repository.get_last_updated_accounts(business_owner_id)
        business_owner_updated_details = UpdatedBusinessOwnersDetails(business_owner_facebook_id=business_owner_id,
                                                                      ad_account_ids=account_ids)
        business_owner_synced_event = FacebookTuringDataSyncCompletedEvent(
            business_owners=[business_owner_updated_details])
        try:
            rabbitmq_client = RabbitMqClient(startup.rabbitmq_config,
                                             startup.exchange_details.name,
                                             startup.exchange_details.outbound_queue.key)
            rabbitmq_client.publish(business_owner_synced_event)
            log = LoggerMessageBase(mtype=LoggerMessageTypeEnum.INTEGRATION_EVENT,
                                    name=business_owner_synced_event.message_type,
                                    extra_data={
                                        "event_body": rabbitmq_client.serialize_message(business_owner_synced_event)
                                    })
            self.__rabbit_logger.logger.info(log.to_dict())
        except Exception as e:
            log = LoggerMessageBase(mtype=LoggerMessageTypeEnum.ERROR,
                                    name=business_owner_synced_event.message_type,
                                    description=str(e))
            self.__logger.logger.exception(log.to_dict())
