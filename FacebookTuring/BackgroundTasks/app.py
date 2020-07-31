# ====== CONFIGURE PATH TO SOLUTION - DO NOT DELETE ====== #
import os
import sys

path = os.environ.get("PYTHON_SOLUTION_PATH")
if path:
    sys.path.append(path)
else:
    sys.path.append("/Users/luchicla/Work/Filed/Source/Filed.Python/")
# ====== END OF CONFIG SECTION ====== #
from threading import Thread
from time import sleep

import schedule

from Core.Tools.Logger.LoggerMessageBase import LoggerMessageBase, LoggerMessageTypeEnum
from Core.Tools.RabbitMQ.RabbitMqClient import RabbitMqClient
from FacebookTuring.BackgroundTasks.FacebookTuringHandlers import FACEBOOK_TURING_HANDLERS
from FacebookTuring.BackgroundTasks.Startup import startup, logger, rabbit_logger
from FacebookTuring.Infrastructure.IntegrationEvents.HandlersEnum import HandlersEnum
from FacebookTuring.Infrastructure.IntegrationEvents.MessageTypeEnum import RequestTypeEnum
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
        handler = FACEBOOK_TURING_HANDLERS.get(message_type, None)
        handler(request_handler, body, startup, logger, rabbit_logger)
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

    schedule.every().day.at("15:35").do(run_daily_sync)

    rabbit_thread = Thread(target=rabbitmq_client.register_callback(callback)
                           .register_consumer(consumer_tag=startup.rabbitmq_config.consumer_name)
                           .start_consuming)
    rabbit_thread.start()

    while True:
        schedule.run_pending()
        sleep(SLEEP_TIME)
