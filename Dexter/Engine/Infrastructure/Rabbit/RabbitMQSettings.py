from enum import Enum


class RabbitMQProducerSettings(Enum):
    USERNAME = "ntvkpamp"
    PASSWORD = "k5TYym9Z7sp18wNPd4U6VAyH2C99-HPH"
    HOSTNAME = "juicy-mosquito.rmq.cloudamqp.com"
    PORT = 5672
    VIRTUAL_HOST = "ntvkpamp"
    EXCHANGE_NAME = "filed-direct"
    EXCHANGE_TYPE = "direct"
    OUTBOUND_QUEUE = "filed.test6.outbound"
    OUTBOUND_QUEUE_ROUTING_KEY = "filed.test6.outbound.key"
    PUBLISH_INTERVAL = 1
    HEARTBEAT = 0
    CONNECTION_TIMEOUT = 300


class RabbitMQConsumerSettings(Enum):
    USERNAME = "ntvkpamp"
    PASSWORD = "k5TYym9Z7sp18wNPd4U6VAyH2C99-HPH"
    HOSTNAME = "juicy-mosquito.rmq.cloudamqp.com"
    PORT = 5672
    VIRTUAL_HOST = "ntvkpamp"
    EXCHANGE_NAME = "filed-direct"
    EXCHANGE_TYPE = "direct"
    INBOUND_QUEUE = "filed.dexter.inbound"
    INBOUND_QUEUE_ROUTING_KEY = "filed.dexter.inbound.key"
    PUBLISH_INTERVAL = 1
    HEARTBEAT = 0
    CONNECTION_TIMEOUT = 300


class InsightsMessageFields(Enum):
    AD_ACCOUNT_ID = "ad_account_facebook_id"
    START_TIME = "since"
    END_TIME = "until"
    TOKEN = "technical_background_token"
