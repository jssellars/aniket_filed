import typing

from Core.logging_legacy import log_message_as_dict
from Core.Tools.RabbitMQ.RabbitMqClient import RabbitMqClient
from Core.Web.BusinessOwnerRepository.BusinessOwnerRepository import BusinessOwnerRepository
from FacebookProductCatalogs.Infrastructure.GraphAPIHandlers.GraphAPIProductCatalogsHandler import \
    GraphAPIProductCatalogsHandler
from FacebookProductCatalogs.Infrastructure.IntegrationEvents.GetProductCatalogsForBusinessRequest import \
    GetProductCatalogsForBusinessRequest
from FacebookProductCatalogs.Infrastructure.IntegrationEvents.GetProductCatalogsForBusinessRequestMapping import \
    GetProductCatalogsForBusinessRequestMapping
from FacebookProductCatalogs.Infrastructure.IntegrationEvents.GetProductCatalogsForBusinessResponse import \
    GetProductCatalogsForBusinessResponse


import logging

logger_native = logging.getLogger(__name__)


class GetProductCatalogsForBusinessRequestHandler:
    __rabbit_logger = None
    __startup = None

    @classmethod
    def set_rabbit_logger(cls, logger: typing.Any = None):
        cls.__rabbit_logger = logger
        return cls

    @classmethod
    def set_startup(cls, startup: typing.Any = None):
        cls.__startup = startup
        return cls

    @classmethod
    def handle(cls, message_body: typing.Dict) -> typing.NoReturn:
        try:
            #  load message
            message_mapper = GetProductCatalogsForBusinessRequestMapping(target=GetProductCatalogsForBusinessRequest)
            message = message_mapper.load(message_body)

            #  get permanent token
            permanent_token = (BusinessOwnerRepository(cls.__startup.session).
                               get_permanent_token(message.business_owner_facebook_id))

            product_catalogs, errors = GraphAPIProductCatalogsHandler.handle(permanent_token=permanent_token,
                                                                             business_id=message.business_facebook_id,
                                                                             startup=cls.__startup)

            response = GetProductCatalogsForBusinessResponse(
                business_owner_facebook_id=message.business_owner_facebook_id,
                business_facebook_id=message.business_facebook_id,
                product_catalogs=product_catalogs,
                filed_user_id=message.filed_user_id,
                errors=errors)

            cls.__publish(response)
        except Exception as e:
            raise e

    @classmethod
    def __publish(cls, product_catalogs):
        try:
            rabbitmq_client = RabbitMqClient(cls.__startup.rabbitmq_config,
                                             cls.__startup.exchange_details.name,
                                             cls.__startup.exchange_details.outbound_queue.key)
            rabbitmq_client.publish(product_catalogs)
            cls.__rabbit_logger.logger.info(log_message_as_dict(mtype=logging.INFO,
                                      name=product_catalogs.message_type,
                                      extra_data={"event_body": rabbitmq_client.serialize_message(product_catalogs)}))
        except Exception as e:
            raise e
