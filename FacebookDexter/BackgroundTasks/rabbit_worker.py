# ====== CONFIGURE PATH TO SOLUTION - DO NOT DELETE ====== #
import os
import sys

from Core.mongo_adapter import MongoRepositoryBase
from FacebookDexter.Infrastructure.PersistanceLayer.StrategyJournalMongoRepository import StrategyJournalMongoRepository

path = os.environ.get("PYTHON_SOLUTION_PATH")
if path:
    sys.path.append(path)
# ====== END OF CONFIG SECTION ====== #
from Core.Dexter.PersistanceLayer.DexterJournalMongoRepository import DexterJournalMongoRepository
from Core.Dexter.PersistanceLayer.DexterRecommendationsMongoRepository import DexterRecommendationsMongoRepository
from FacebookDexter.BackgroundTasks.startup import config, fixtures
from FacebookDexter.Infrastructure.IntegrationEvents.HandlersEnum import HandlersEnum
from FacebookDexter.Infrastructure.IntegrationEvents.MessageTypeEnum import RequestTypeEnum


import logging

logger = logging.getLogger(__name__)


def callback(ch, method, properties, body):
    logger.info(getattr(properties, "type", None), extra={"rabbitmq": body})

    try:
        ch.basic_ack(delivery_tag=method.delivery_tag)
        message_type = getattr(properties, "type", None)
        request_handler_name = RequestTypeEnum.get_by_value(message_type)
        request_handler = HandlersEnum.get_enum_by_name(request_handler_name).value
    except Exception as e:
        logger.exception(f"Failed to initialise processing || {repr(e)}")

        return

    try:
        recommendations_repository = MongoRepositoryBase(
            config=config.mongo,
            database_name=config.mongo.recommendations_database_name,
            collection_name=config.mongo.recommendations_collection_name,
        )
        journal_repository = StrategyJournalMongoRepository(
            config=config.mongo,
            database_name=config.mongo.journal_database_name,
            collection_name=config.mongo.journal_collection_name,
        )

        request_handler(
            journal_repository=journal_repository,
            recommendations_repository=recommendations_repository,
        ).handle(body)

    except Exception as e:
        logger.exception(repr(e), extra={"message_type": message_type, "integration_event_body": body})


def main():
    fixtures.rabbitmq_adapter.register_callback(callback).register_consumer(config.rabbitmq.consumer_name).start_consuming()


if __name__ == "__main__":
    main()
