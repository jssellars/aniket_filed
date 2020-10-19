# ====== CONFIGURE PATH TO SOLUTION - DO NOT DELETE ====== #
import os
import sys

path = os.environ.get("PYTHON_SOLUTION_PATH")
if path:
    sys.path.append(path)
# ====== END OF CONFIG SECTION ====== #
import json
import traceback

from Core.Tools.RabbitMQ.RabbitMqClient import RabbitMqClient
from GoogleTuring.BackgroundTasks.Startup import startup
from GoogleTuring.Infrastructure.IntegrationEvents.HandlersEnum import HandlersEnum
from GoogleTuring.Infrastructure.IntegrationEvents.MessageTypeEnum import RequestTypeEnum
from GoogleTuring.BackgroundTasks.Startup import logger


def callback(ch, method, properties, body):
    try:
        ch.basic_ack(delivery_tag=method.delivery_tag)
        message_type = getattr(properties, "type", None)
        request_handler_name = RequestTypeEnum.get_by_value(message_type)
        request_handler = HandlersEnum.get_enum_by_name(request_handler_name).value
        message = json.loads(body)
        request_handler.handle(message, logger)
    except:
        traceback.print_exc()


def main():
    # TODO: normalize by adding the same config parsing as in the other projects
    RabbitMqClient(
        startup.rabbitmq_config,
        inbound_queue=startup.direct_inbound_queue.name,
    ).register_callback(callback).register_consumer("google.turing").start_consuming()


if __name__ == "__main__":
    main()
