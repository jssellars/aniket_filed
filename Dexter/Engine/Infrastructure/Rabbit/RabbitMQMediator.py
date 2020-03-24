import datetime
import json

import pika

from Algorithms.Tools.RemoveActorPrefix import remove_actor_prefix
from Infrastructure.Mongo.Mongo import MongoMediator
from Infrastructure.Rabbit.RabbitMQSettings import RabbitMQProducerSettings, RabbitMQConsumerSettings, \
    InsightsMessageFields


class RabbitMqMediator:
    mongo = MongoMediator()

    def __init__(self):
        pass

    def send_recommendations(self, recommendations):

        for i, recommendation in enumerate(recommendations):

            saving_recommendation = recommendation
            saving_recommendation.createdAt = datetime.datetime.now()

            # if recommendation.campaignId is None:
            #     info = self.mongo.get_parent_and_campaign_id(recommendation.structureId)
            #     recommendation.campaignId = info['campaign_id']
            #     if info['ParentId'].find('act_') > 0:
            #         recommendation.parentId = info['ParentId']
            #     else:
            #         recommendation.parentId = remove_actor_prefix(info['ParentId'])
            #
            # recommendation.structureId = remove_actor_prefix(recommendation.structureId)
            saving_recommendation_dict = saving_recommendation.__dict__
            saving_recommendation_dict['applicationDetails'] = json.dumps(recommendation.applicationDetails)
            self.mongo.log_recommendation(saving_recommendation_dict)

            print(f"Sent recommendation:", saving_recommendation_dict)

    def ListenForMessages(self, callback=None):

        credentials = pika.credentials.PlainCredentials(RabbitMQConsumerSettings.USERNAME.value,
                                                        RabbitMQConsumerSettings.PASSWORD.value)

        parameters = pika.ConnectionParameters(host=RabbitMQConsumerSettings.HOSTNAME.value,
                                               port=RabbitMQConsumerSettings.PORT.value,
                                               virtual_host=RabbitMQConsumerSettings.VIRTUAL_HOST.value,
                                               credentials=credentials,
                                               heartbeat=RabbitMQProducerSettings.HEARTBEAT.value,
                                               socket_timeout=RabbitMQProducerSettings.CONNECTION_TIMEOUT.value
                                               )

        connection = pika.BlockingConnection(parameters)
        channel = connection.channel()
        channel.queue_declare(queue=RabbitMQConsumerSettings.INBOUND_QUEUE.value, durable=True)

        def consume_function(ch, method, properties, body):
            print("Consuming Message")
            print(" [x] body: %r" % body)

        if callback is None:
            callback = consume_function

        channel.basic_consume(queue=RabbitMQConsumerSettings.INBOUND_QUEUE.value, on_message_callback=callback,
                              auto_ack=True)
        print("Waiting for messages")
        channel.start_consuming()

    # ThrowAway Code
    # Will be deleted when we can consume messages from Campaign Insights
    def send_test_messages(self, number, date_range, ad_account_id):
        credentials = pika.credentials.PlainCredentials(RabbitMQConsumerSettings.USERNAME.value,
                                                        RabbitMQConsumerSettings.PASSWORD.value)

        parameters = pika.ConnectionParameters(host=RabbitMQConsumerSettings.HOSTNAME.value,
                                               port=RabbitMQConsumerSettings.PORT.value,
                                               virtual_host=RabbitMQConsumerSettings.VIRTUAL_HOST.value,
                                               credentials=credentials,
                                               heartbeat=RabbitMQConsumerSettings.HEARTBEAT.value,
                                               socket_timeout=RabbitMQConsumerSettings.CONNECTION_TIMEOUT.value)

        connection = pika.BlockingConnection(parameters)
        channel = connection.channel()

        channel.queue_declare(queue=RabbitMQConsumerSettings.INBOUND_QUEUE.value, durable=True)

        date_range_dict = {
            InsightsMessageFields.AD_ACCOUNT_ID.value: ad_account_id,
            InsightsMessageFields.START_TIME.value: date_range.get_start_date_string(),
            InsightsMessageFields.END_TIME.value: date_range.get_end_date_string()
        }

        turing_sync = 'TuringSyncCompletedEvent'

        for i in range(1, number + 1):
            mbody = json.dumps(date_range_dict)
            channel.basic_publish(exchange=RabbitMQConsumerSettings.EXCHANGE_NAME.value,
                                  routing_key=RabbitMQConsumerSettings.INBOUND_QUEUE_ROUTING_KEY.value, body=mbody,
                                  properties=pika.BasicProperties(priority=1, message_id='1', type=turing_sync,
                                                                  content_type='application/json', delivery_mode=2))

            print(f"Sent test {i}")
