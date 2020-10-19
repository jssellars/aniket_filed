# ====== CONFIGURE PATH TO SOLUTION - DO NOT DELETE ====== #
import os
import sys

path = os.environ.get("PYTHON_SOLUTION_PATH")
if path:
    sys.path.append(path)
# ====== END OF CONFIG SECTION ====== #
import json

from Core.Tools.Logger.LoggerMessageBase import LoggerMessageBase, LoggerMessageTypeEnum
from Core.Tools.RabbitMQ.RabbitMqClient import RabbitMqClient
from PotterFacebookProductCatalogs.BackgroundTasks.Startup import rabbit_logger, logger, startup
from PotterFacebookProductCatalogs.Infrastructure.IntegrationEvents.HandlersEnum import HandlersEnum
from PotterFacebookProductCatalogs.Infrastructure.IntegrationEvents.MessageTypeEnum import RequestTypeEnum


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
        body = json.loads(body)
        request_handler.set_rabbit_logger(rabbit_logger).set_startup(startup).handle(body)
    except Exception as e:
        log = LoggerMessageBase(
            mtype=LoggerMessageTypeEnum.INTEGRATION_EVENT,
            name="Potter Facebook Product Catalogs Integration Error",
            description=str(e),
            extra_data={"message_type": getattr(properties, "type", None), "event_body": body},
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
