# ====== CONFIGURE PATH TO SOLUTION - DO NOT DELETE ====== #
import os
import sys

path = os.environ.get("PYTHON_SOLUTION_PATH")
if path:
    sys.path.append(path)
# ====== END OF CONFIG SECTION ====== #
from Core.Dexter.PersistanceLayer.DexterJournalMongoRepository import DexterJournalMongoRepository
from Core.Dexter.PersistanceLayer.DexterRecommendationsMongoRepository import DexterRecommendationsMongoRepository
from Core.logging_legacy import log_message_as_dict
from Core.Tools.RabbitMQ.RabbitMqClient import RabbitMqClient
from FacebookDexter.BackgroundTasks.Startup import startup, rabbit_logger, logger
from FacebookDexter.Infrastructure.IntegrationEvents.HandlersEnum import HandlersEnum
from FacebookDexter.Infrastructure.IntegrationEvents.MessageTypeEnum import RequestTypeEnum


import logging

logger_native = logging.getLogger(__name__)


def callback(ch, method, properties, body):
    rabbit_logger.logger.info(log_message_as_dict(mtype=logging.INFO,
        name=getattr(properties, "type", None),
        extra_data={"event_body": body},
    ))

    try:
        ch.basic_ack(delivery_tag=method.delivery_tag)
        message_type = getattr(properties, "type", None)
        request_handler_name = RequestTypeEnum.get_by_value(message_type)
        request_handler = HandlersEnum.get_enum_by_name(request_handler_name).value
    except:
        logger.logger.exception(log_message_as_dict(mtype=logging.ERROR,
            name="Facebook Dexter Integration Error",
            description="Failed to initialise processing",
        ))

        return

    try:
        recommendations_repository = DexterRecommendationsMongoRepository(
            config=startup.mongo_config,
            database_name=startup.mongo_config.recommendations_database_name,
            collection_name=startup.mongo_config.recommendations_collection_name,
            logger=logger,
        )
        journal_repository = DexterJournalMongoRepository(
            config=startup.mongo_config,
            database_name=startup.mongo_config.journal_database_name,
            collection_name=startup.mongo_config.journal_collection_name,
            logger=logger,
        )
        (
            request_handler.set_startup(startup)
            .set_journal_repository(journal_repository)
            .set_recommendations_repository(recommendations_repository)
            .handle(body)
        )
    except Exception as e:
        logger.logger.exception(log_message_as_dict(mtype=logging.INFO,
            name="Facebook Dexter Integration Error",
            description=str(e),
            extra_data={"message_type": message_type, "integration_event_body": body},
        ))


def main():
    _PREFETCH_COUNT = 50
    RabbitMqClient(
        startup.rabbitmq_config,
        startup.exchange_details.name,
        startup.exchange_details.outbound_queue.key,
        startup.exchange_details.inbound_queue.name,
        _PREFETCH_COUNT,
    ).register_callback(callback).register_consumer(startup.rabbitmq_config.consumer_name).start_consuming()


if __name__ == "__main__":
    main()
