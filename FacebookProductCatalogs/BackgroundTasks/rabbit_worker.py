# ====== CONFIGURE PATH TO SOLUTION - DO NOT DELETE ====== #
import os
import sys

path = os.environ.get("PYTHON_SOLUTION_PATH")
if path:
    sys.path.append(path)
# ====== END OF CONFIG SECTION ====== #
import json

from Core.Tools.RabbitMQ.RabbitMqClient import RabbitMqClient
from FacebookProductCatalogs.BackgroundTasks.Startup import startup
from FacebookProductCatalogs.Infrastructure.IntegrationEvents.HandlersEnum import HandlersEnum
from FacebookProductCatalogs.Infrastructure.IntegrationEvents.MessageTypeEnum import RequestTypeEnum


import logging

logger = logging.getLogger(__name__)


def callback(ch, method, properties, body):
    logger.info(getattr(properties, "type", None), extra={"rabbitmq": body})

    try:
        ch.basic_ack(delivery_tag=method.delivery_tag)
        message_type = getattr(properties, "type", None)
        request_handler_name = RequestTypeEnum.get_by_value(message_type)
        request_handler = HandlersEnum.get_enum_by_name(request_handler_name).value
        body = json.loads(body)
        request_handler.set_startup(startup).handle(body)
    except Exception as e:
        logger.exception(repr(e), extra={"message_type": getattr(properties, "type", None), "event_body": body})


def main():
    RabbitMqClient(
        startup.rabbitmq_config,
        startup.exchange_details.name,
        startup.exchange_details.outbound_queue.key,
        startup.exchange_details.inbound_queue.name,
    ).register_callback(callback).register_consumer(startup.rabbitmq_config.consumer_name).start_consuming()


if __name__ == "__main__":
    main()
