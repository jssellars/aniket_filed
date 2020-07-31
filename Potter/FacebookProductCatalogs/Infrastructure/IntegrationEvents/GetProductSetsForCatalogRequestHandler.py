import typing

from Core.Tools.Logger.LoggerMessageBase import LoggerMessageBase, LoggerMessageTypeEnum
from Core.Tools.RabbitMQ.RabbitMqClient import RabbitMqClient
from Core.Web.BusinessOwnerRepository.BusinessOwnerRepository import BusinessOwnerRepository
from Potter.FacebookProductCatalogs.Infrastructure.GraphAPIHandlers.GraphAPIProductSetsHandler import \
    GraphAPIProductSetsHandler
from Potter.FacebookProductCatalogs.Infrastructure.IntegrationEvents.GetProductSetsForCatalogRequest import \
    GetProductSetsForCatalogRequest
from Potter.FacebookProductCatalogs.Infrastructure.IntegrationEvents.GetProductSetsForCatalogRequestMapping import \
    GetProductSetsForCatalogRequestMapping
from Potter.FacebookProductCatalogs.Infrastructure.IntegrationEvents.GetProductSetsForCatalogResponse import \
    GetProductSetsForCatalogResponse


class GetProductSetsForCatalogRequestHandler:
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
            message_mapper = GetProductSetsForCatalogRequestMapping(target=GetProductSetsForCatalogRequest)
            message = message_mapper.load(message_body)

            #  get permanent token
            permanent_token = (BusinessOwnerRepository(cls.__startup.session).
                               get_permanent_token(message.business_owner_facebook_id))

            product_sets, errors = GraphAPIProductSetsHandler.handle(permanent_token=permanent_token,
                                                                     product_catalog_id=message.product_catalog_facebook_id,
                                                                     startup=cls.__startup)

            response = GetProductSetsForCatalogResponse(
                business_owner_facebook_id=message.business_owner_facebook_id,
                business_facebook_id=message.business_facebook_id,
                product_catalog_facebook_id=message.product_catalog_facebook_id,
                product_sets=product_sets,
                filed_user_id=message.filed_user_id,
                errors=errors)

            cls.__publish(response)
        except Exception as e:
            raise e

    @classmethod
    def __publish(cls, product_sets):
        try:
            rabbitmq_client = RabbitMqClient(cls.__startup.rabbitmq_config,
                                             cls.__startup.exchange_details.name,
                                             cls.__startup.exchange_details.outbound_queue.key)
            rabbitmq_client.publish(product_sets)
            log = LoggerMessageBase(mtype=LoggerMessageTypeEnum.INTEGRATION_EVENT,
                                    name=product_sets.message_type,
                                    extra_data={"event_body": rabbitmq_client.serialize_message(product_sets)})
            cls.__rabbit_logger.logger.info(log.to_dict())
        except Exception as e:
            raise e
