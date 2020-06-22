# ====== CONFIGURE PATH TO SOLUTION - DO NOT DELETE ====== #
import os
import sys

path = os.environ.get("PYTHON_SOLUTION_PATH")
if path:
    sys.path.append(path)
else:
    sys.path.append("/Users/luchicla/Work/Filed/Source/Filed.Python/")
# ====== END OF CONFIG SECTION ====== #

from Core.Tools.Logger.LoggerMessageBase import LoggerMessageBase, LoggerMessageTypeEnum
from Core.Tools.RabbitMQ.RabbitMqClient import RabbitMqClient
from FacebookDexter.BackgroundTasks.Startup import startup, rabbit_logger, logger
from FacebookDexter.Infrastructure.IntegrationEvents.HandlersEnum import HandlersEnum
from FacebookDexter.Infrastructure.IntegrationEvents.MessageTypeEnum import RequestTypeEnum
from FacebookDexter.Infrastructure.PersistanceLayer.DexterJournalMongoRepository import DexterJournalMongoRepository
from FacebookDexter.Infrastructure.PersistanceLayer.DexterRecommendationsMongoRepository import \
    DexterRecommendationsMongoRepository


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
                                name="Facebook Dexter Integration Error",
                                description="Failed to initialise processing")
        logger.logger.exception(log.to_dict())
        return

    try:
        # initialize all repos
        recommendations_repository = DexterRecommendationsMongoRepository(config=startup.mongo_config,
                                                                          database_name=startup.mongo_config.recommendations_database_name,
                                                                          collection_name=startup.mongo_config.recommendations_collection_name)
        journal_repository = DexterJournalMongoRepository(config=startup.mongo_config,
                                                          database_name=startup.mongo_config.journal_database_name,
                                                          collection_name=startup.mongo_config.journal_collection_name)

        request_handler. \
            set_startup(startup). \
            set_journal_repository(journal_repository). \
            set_recommendations_repository(recommendations_repository). \
            handle(body)
    except Exception as e:
        log = LoggerMessageBase(mtype=LoggerMessageTypeEnum.INTEGRATION_EVENT,
                                name="Facebook Dexter Integration Error",
                                description=str(e),
                                extra_data={
                                    "message_type": message_type,
                                    "integration_event_body": body
                                })
        logger.logger.exception(log.to_dict())


if __name__ == "__main__":
    rabbitmq_client = RabbitMqClient(startup.rabbitmq_config,
                                     startup.exchange_details.name,
                                     startup.exchange_details.outbound_queue.key,
                                     inbound_queue=startup.exchange_details.inbound_queue.name)
    rabbitmq_client.register_callback(callback).register_consumer(
        consumer_tag=startup.rabbitmq_config.consumer_name).start_consuming()
