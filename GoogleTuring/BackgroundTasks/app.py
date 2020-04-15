import json
import time
from threading import Thread

import schedule

from Core.Tools.RabbitMQ.RabbitMqClient import RabbitMqClient
from GoogleTuring.BackgroundTasks.DailySyncJob import daily_sync_job
from GoogleTuring.BackgroundTasks.Startup import startup
from GoogleTuring.Infrastructure.IntegrationEvents.HandlersEnum import HandlersEnum
from GoogleTuring.Infrastructure.IntegrationEvents.MessageTypeEnum import RequestTypeEnum


def sync_callback(ch, method, properties, body):
    try:
        ch.basic_ack(delivery_tag=method.delivery_tag)
        message_type = getattr(properties, "type", None)
        request_handler_name = RequestTypeEnum.get_by_value(message_type)
        request_handler = HandlersEnum.get_enum_by_name(request_handler_name).value
        message = json.loads(body)
        request_handler.handle(message)
    except Exception as e:
        # TODO: log exception
        print(e.__str__())


rabbitmq_client = RabbitMqClient(startup.rabbitmq_config,
                                 inbound_queue=startup.direct_inbound_queue.name)

schedule.every().day.at("00:05").do(daily_sync_job)
rabbit_thread = Thread(target=rabbitmq_client.register_callback(sync_callback)
                                             .register_consumer(consumer_tag="google.turing")
                                             .start_consuming)
rabbit_thread.start()

while True:
    schedule.run_pending()
    time.sleep(1)
