# ====== CONFIGURE PATH TO SOLUTION - DO NOT DELETE ====== #
import os
import sys
from threading import Thread
from time import sleep

import schedule

path = os.environ.get("PYTHON_SOLUTION_PATH")
if path:
    sys.path.append(path)
else:
    sys.path.append("/Users/luchicla/Work/Filed/Source/Filed.Python/")
# ====== END OF CONFIG SECTION ====== #

from Core.Tools.Logger.LoggerMessageBase import LoggerMessageBase, LoggerMessageTypeEnum
from Core.Tools.RabbitMQ.RabbitMqClient import RabbitMqClient
from FacebookTuring.BackgroundTasks.Orchestrators.Orchestrator import Orchestrator
from FacebookTuring.BackgroundTasks.Startup import startup, logger, rabbit_logger
from FacebookTuring.Infrastructure.IntegrationEvents.HandlersEnum import HandlersEnum
from FacebookTuring.Infrastructure.IntegrationEvents.MessageTypeEnum import RequestTypeEnum
from FacebookTuring.Infrastructure.PersistenceLayer.TuringAdAccountJournalRepository import \
    TuringAdAccountJournalRepository
from FacebookTuring.Infrastructure.PersistenceLayer.TuringMongoRepository import TuringMongoRepository
from FacebookTuring.BackgroundTasks.DailySyncronizer import run_daily_sync


def callback(ch, method, properties, body):
    # log message
    log = LoggerMessageBase(mtype=LoggerMessageTypeEnum.INTEGRATION_EVENT,
                            name=getattr(properties, "type", None),
                            extra_data={"event_body": body})
    rabbit_logger.logger.info(log.to_dict())

    try:
        ch.basic_ack(delivery_tag=method.delivery_tag)
        message_type = getattr(properties, "type", None)
        request_handler_name = RequestTypeEnum.get_by_value(message_type)
        request_handler = HandlersEnum.get_enum_by_name(request_handler_name).value
    except:
        log = LoggerMessageBase(mtype=LoggerMessageTypeEnum.ERROR,
                                name="Facebook Turing Integration Error",
                                description="Failed to initialise processing")
        logger.logger.exception(log.to_dict())
        return

    try:
        #  Initialize mongo repositories for accounts journal, insights and structures
        account_journal_repository = TuringAdAccountJournalRepository(config=startup.mongo_config,
                                                                      database_name=startup.mongo_config.accounts_journal_database_name,
                                                                      collection_name=startup.mongo_config.accounts_journal_collection_name)
        insights_repository = TuringMongoRepository(config=startup.mongo_config,
                                                    database_name=startup.mongo_config.insights_database_name)
        structures_repository = TuringMongoRepository(config=startup.mongo_config,
                                                      database_name=startup.mongo_config.structures_database_name)

        #  initialize orchestrator
        orchestrator = (Orchestrator().
                        set_account_journal_repository(account_journal_repository).
                        set_insights_repository(insights_repository).
                        set_structures_repository(structures_repository).
                        set_logger(logger).
                        set_rabbit_logger(rabbit_logger))

        # handle message
        (request_handler.
         set_mongo_repository(account_journal_repository).
         set_orchestrator(orchestrator).
         set_logger(logger).
         handle(body))

        # terminate db connections
        account_journal_repository.close()
        insights_repository.close()
        structures_repository.close()
    except Exception as e:
        log = LoggerMessageBase(mtype=LoggerMessageTypeEnum.INTEGRATION_EVENT,
                                name="Facebook Turing Integration Error",
                                description=str(e),
                                extra_data={
                                    "message_type": message_type,
                                    "integration_event_body": body
                                })
        logger.logger.exception(log.to_dict())


if __name__ == "__main__":
    SLEEP_TIME = 5

    rabbitmq_client = RabbitMqClient(startup.rabbitmq_config,
                                     startup.exchange_details.name,
                                     startup.exchange_details.outbound_queue.key,
                                     inbound_queue=startup.exchange_details.inbound_queue.name)

    schedule.every().day.at("00:05").do(run_daily_sync)

    rabbit_thread = Thread(target=rabbitmq_client.register_callback(callback)
                           .register_consumer(consumer_tag=startup.rabbitmq_config.consumer_name)
                           .start_consuming)
    rabbit_thread.start()

    while True:
        schedule.run_pending()
        sleep(SLEEP_TIME)
