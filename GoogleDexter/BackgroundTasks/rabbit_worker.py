# ====== CONFIGURE PATH TO SOLUTION - DO NOT DELETE ====== #
import os
import sys

path = os.environ.get("PYTHON_SOLUTION_PATH")
if path:
    sys.path.append(path)
# ====== END OF CONFIG SECTION ====== #
from Core.Dexter.PersistanceLayer.DexterJournalMongoRepository import DexterJournalMongoRepository
from Core.Dexter.PersistanceLayer.DexterRecommendationsMongoRepository import DexterRecommendationsMongoRepository
from Core.Tools.Logger.LoggerMessageBase import LoggerMessageBase, LoggerMessageTypeEnum
from Core.Tools.RabbitMQ.RabbitMqClient import RabbitMqClient
from GoogleDexter.BackgroundTasks.Startup import startup, rabbit_logger, logger
from GoogleDexter.Infrastructure.IntegrationEvents.HandlersEnum import HandlersEnum
from GoogleDexter.Infrastructure.IntegrationEvents.MessageTypeEnum import RequestTypeEnum


def callback(ch, method, properties, body):
    log = LoggerMessageBase(
        mtype=LoggerMessageTypeEnum.INTEGRATION_EVENT,
        name=getattr(properties, "type", None),
        extra_data={"event_body": body},
    )
    rabbit_logger.logger.info(log.to_dict())
    try:
        ch.basic_ack(delivery_tag=method.delivery_tag)
        message_type = getattr(properties, "type", None)
        request_handler_name = RequestTypeEnum.get_by_value(message_type)
        request_handler = HandlersEnum.get_enum_by_name(request_handler_name).value
    except:
        log = LoggerMessageBase(
            mtype=LoggerMessageTypeEnum.ERROR,
            name="Google Dexter Integration Error",
            description="Failed to initialise processing",
        )
        logger.logger.exception(log.to_dict())

        return

    try:
        # data_repository = GoogleDexterMongoRepository(config=startup.mongo_config)
        recommendations_repository = DexterRecommendationsMongoRepository(
            config=startup.mongo_config,
            database_name=startup.mongo_config.recommendations_database_name,
            collection_name=startup.mongo_config.recommendations_collection_name,
        )
        journal_repository = DexterJournalMongoRepository(
            config=startup.mongo_config,
            database_name=startup.mongo_config.journal_database_name,
            collection_name=startup.mongo_config.journal_collection_name,
        )
        (
            request_handler.set_startup(startup)
            # .set_data_repository(data_repository)
            .set_journal_repository(journal_repository)
            .set_recommendations_repository(recommendations_repository)
            .handle(body)
        )
    except Exception as e:
        log = LoggerMessageBase(
            mtype=LoggerMessageTypeEnum.INTEGRATION_EVENT,
            name="Google Dexter Integration Error",
            description=str(e),
            extra_data={"message_type": message_type, "integration_event_body": body},
        )
        logger.logger.exception(log.to_dict())


def main():
    RabbitMqClient(
        startup.rabbitmq_config,
        startup.exchange_details.name,
        startup.exchange_details.outbound_queue.key,
        startup.exchange_details.inbound_queue.name,
    ).register_callback(callback).register_consumer(startup.rabbitmq_config.consumer_name).start_consuming()


if __name__ == "__main__":
    main()
