import json
import sys
sys.path.append("/Users/luchicla/Work/Filed/Source/Filed.Python")

from Core.Tools.RabbitMQ.RabbitMqClient import RabbitMqClient
from Potter.FacebookApps.BackgroundTasks.Startup import startup
from Potter.FacebookApps.Infrastructure.IntegrationEvents.HandlersEnum import HandlersEnum
from Potter.FacebookApps.Infrastructure.IntegrationEvents.MessageTypeEnum import RequestTypeEnum


def callback(ch, method, properties, body):
    try:
        ch.basic_ack(delivery_tag=method.delivery_tag)
        message_type = getattr(properties, "type", None)
        request_handler_name = RequestTypeEnum.get_by_value(message_type)
        request_handler = HandlersEnum.get_enum_by_name(request_handler_name).value

        body = json.loads(body)
        request_handler.handle(body)
    except Exception as e:
        # todo: log error
        print(e)


rabbitmq_client = RabbitMqClient(startup.rabbitmq_config,
                                 startup.exchange_details.name,
                                 startup.exchange_details.outbound_queue.key,
                                 inbound_queue=startup.exchange_details.inbound_queue.name)

while True:
    if not rabbitmq_client.consumer_started:
        rabbitmq_client.register_callback(callback).register_consumer(consumer_tag=startup.rabbitmq_config.consumer_name).start_consuming()
