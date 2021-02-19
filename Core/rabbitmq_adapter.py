import json
import uuid
from typing import Any, Dict, Callable

import pika

from Core import settings
from Core.Tools.Misc.ObjectSerializers import object_to_json


class RabbitMqAdapter:
    @classmethod
    def serialize_message(cls, data: Any) -> Dict:
        return object_to_json(data)

    def __init__(
        self,
        config: settings.RabbitMq,
        exchange: settings.Exchange,
        secondary_exchange: settings.Exchange,
        prefetch_count: int = 50,
    ) -> None:
        self._config = config
        self._exchange = exchange
        self._secondary_exchange = secondary_exchange
        self._prefetch_count = prefetch_count
        self._callback = None
        self._channel = None

        self.consumer_started = False

        self._connection_parameters = pika.ConnectionParameters(
            host=self._config.hostname,
            port=self._config.port,
            virtual_host=self._config.virtual_host,
            credentials=(
                pika.credentials.PlainCredentials(
                    username=self._config.username, password=self._config.password, erase_on_connect=False
                )
            ),
            heartbeat=self._config.heartbeat,
            blocked_connection_timeout=self._config.connection_timeout,
        )

    def publish(self, message_body: Any, on_secondary: bool = False) -> None:
        if on_secondary:
            exchange_name = self._secondary_exchange.name
            outbound_key = self._secondary_exchange.outbound_queue.key
        else:
            exchange_name = self._exchange.name
            outbound_key = self._exchange.outbound_queue.key

        with pika.BlockingConnection(self._connection_parameters) as connection:
            with connection.channel() as channel:
                channel.basic_publish(
                    exchange_name,
                    outbound_key,
                    json.dumps(RabbitMqAdapter.serialize_message(message_body)),
                    properties=pika.BasicProperties(
                        type=message_body.message_type,
                        message_id=str(uuid.uuid4()),
                        priority=1,
                        content_type="application/json",
                        delivery_mode=2,
                    ),
                )

    def register_callback(self, callback: Callable) -> "RabbitMqAdapter":
        """callback(ch, method, properties, body)"""
        self._callback = callback

        return self

    def register_consumer(self, consumer_tag: str) -> "RabbitMqAdapter":
        if not self._callback:
            raise ValueError("No callback provided. Try registering a callback first.")

        connection = pika.BlockingConnection(self._connection_parameters)
        self._channel = connection.channel()
        self._channel.basic_qos(prefetch_count=self._prefetch_count)
        self._channel.basic_consume(
            self._exchange.inbound_queue.name, self._callback, auto_ack=False, consumer_tag=consumer_tag
        )

        return self

    def start_consuming(self) -> None:
        if not self._channel:
            raise ValueError("No channel was created. Try creating a channel and registering a consumer first.")

        self.consumer_started = True
        self._channel.start_consuming()
