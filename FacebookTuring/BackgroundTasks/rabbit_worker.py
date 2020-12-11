# ====== CONFIGURE PATH TO SOLUTION - DO NOT DELETE ====== #
import os
import sys

path = os.environ.get("PYTHON_SOLUTION_PATH")
if path:
    sys.path.append(path)
# ====== END OF CONFIG SECTION ====== #
from FacebookTuring.BackgroundTasks.startup import config, fixtures
from FacebookTuring.BackgroundTasks.FacebookTuringHandlers import FACEBOOK_TURING_HANDLERS
from FacebookTuring.Infrastructure.IntegrationEvents.HandlersEnum import HandlersEnum
from FacebookTuring.Infrastructure.IntegrationEvents.MessageTypeEnum import RequestTypeEnum


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
        handler = FACEBOOK_TURING_HANDLERS.get(message_type, None)
        handler(request_handler, body, config)
    except Exception as e:
        logger.exception(repr(e), extra={"message_type": message_type, "integration_event_body": body})


def main():
    fixtures.rabbitmq_adapter.register_callback(callback).register_consumer(config.rabbitmq.consumer_name).start_consuming()


if __name__ == "__main__":
    main()
