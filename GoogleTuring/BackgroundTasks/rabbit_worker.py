# ====== CONFIGURE PATH TO SOLUTION - DO NOT DELETE ====== #
import os
import sys

path = os.environ.get("PYTHON_SOLUTION_PATH")
if path:
    sys.path.append(path)
# ====== END OF CONFIG SECTION ====== #
import json

from GoogleTuring.BackgroundTasks.startup import config, fixtures
from GoogleTuring.BackgroundTasks.IntegrationEvents.HandlersEnum import HandlersEnum
from GoogleTuring.BackgroundTasks.IntegrationEvents.MessageTypeEnum import RequestTypeEnum

import logging

logger = logging.getLogger(__name__)


def callback(ch, method, properties, body):
    try:
        ch.basic_ack(delivery_tag=method.delivery_tag)
        message_type = getattr(properties, "type", None)
        request_handler_name = RequestTypeEnum.get_by_value(message_type)
        request_handler = HandlersEnum.get_enum_by_name(request_handler_name).value
        message = json.loads(body)
        request_handler.handle(message)
    except Exception as e:
        logger.exception(repr(e))


def main():
    fixtures.rabbitmq_adapter.register_callback(callback).register_consumer(config.rabbitmq.consumer_name).start_consuming()


if __name__ == "__main__":
    main()
