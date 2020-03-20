import json
import uuid

import pika
import typing

from pika import BasicProperties

from Core.Tools.Misc.ObjectSerializers import object_to_json


class RabbitMqClient:

    @classmethod
    def __serialize(cls, data: typing.Any) -> typing.Dict:
        return object_to_json(data)

    def __init__(self,
                 config: typing.Any,
                 exchange_name: typing.AnyStr,
                 outbound_routing_key: typing.AnyStr,
                 inbound_queue: typing.AnyStr = None):
        self.__config = config
        self.__exchange_name = exchange_name
        self.__inbound_queue = inbound_queue
        self.__outbound_routing_key = outbound_routing_key
        self.__callback = None

        self.consumer_started = False

        credentials = pika.credentials.PlainCredentials(username=self.__config.username, password=self.__config.password, erase_on_connect=False)
        self.__connection_parameters = pika.ConnectionParameters(host=self.__config.hostname,
                                                                 port=self.__config.port,
                                                                 virtual_host=self.__config.virtual_host,
                                                                 credentials=credentials,
                                                                 heartbeat=self.__config.heartbeat,
                                                                 blocked_connection_timeout=self.__config.connection_timeout)
        self.__channel = None

    def publish(self, message_body: typing.Any) -> typing.NoReturn:
        connection = pika.BlockingConnection(self.__connection_parameters)
        channel = connection.channel()

        message_properties = self.__generate_message_properties(message_body)
        message_body = json.dumps(RabbitMqClient.__serialize(message_body))

        channel.basic_publish(self.__exchange_name,
                              self.__outbound_routing_key,
                              message_body,
                              properties=message_properties)

        channel.close()
        connection.close()

    @staticmethod
    def __generate_message_properties(message_body: typing.Any) -> BasicProperties:
        message_properties = BasicProperties()
        message_properties.type = message_body.message_type
        message_properties.message_id = str(uuid.uuid4())
        message_properties.priority = 1
        message_properties.content_type = "application/json"
        message_properties.delivery_mode = 2

        return message_properties

    def register_callback(self, callback: typing.Callable) -> typing.Any:
        self.__callback = callback
        return self

    def register_consumer(self, consumer_tag: typing.AnyStr) -> typing.Any:
        """callback(ch, method, properties, body)"""
        if not self.__callback:
            raise ValueError("No callback provided. Try again by registering a callback first.")

        connection = pika.BlockingConnection(self.__connection_parameters)

        self.__channel = connection.channel()
        self.__channel.basic_consume(self.__inbound_queue, self.__callback, auto_ack=False, consumer_tag=consumer_tag)

        return self

    def start_consuming(self):
        if not self.__channel:
            raise ValueError("No channel was created. Try again by creating a channel and registering a consumer first.")

        self.consumer_started = True
        self.__channel.start_consuming()
