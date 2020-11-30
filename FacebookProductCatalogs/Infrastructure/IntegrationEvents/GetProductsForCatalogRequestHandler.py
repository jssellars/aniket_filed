import typing

from Core.Tools.RabbitMQ.RabbitMqClient import RabbitMqClient
from Core.Web.BusinessOwnerRepository.BusinessOwnerRepository import BusinessOwnerRepository
from FacebookProductCatalogs.Infrastructure.GraphAPIHandlers.GraphAPIProductsHandler import \
    GraphAPIProductsHandler
from FacebookProductCatalogs.Infrastructure.IntegrationEvents.GetAllProductIdsResponse import \
    GetAllProductIdsResponse
from FacebookProductCatalogs.Infrastructure.IntegrationEvents.GetProductsForCatalogRequest import \
    GetProductsForCatalogRequest
from FacebookProductCatalogs.Infrastructure.IntegrationEvents.GetProductsForCatalogRequestMapping import \
    GetProductsForCatalogRequestMapping
from FacebookProductCatalogs.Infrastructure.IntegrationEvents.GetProductsForCatalogResponse import \
    GetProductsForCatalogResponse


import logging

logger = logging.getLogger(__name__)


class GetProductsForCatalogRequestHandler:
    __startup = None

    @classmethod
    def set_startup(cls, startup: typing.Any = None):
        cls.__startup = startup
        return cls

    @classmethod
    def handle(cls, message_body: typing.Dict) -> typing.NoReturn:
        try:
            #  load message
            message_mapper = GetProductsForCatalogRequestMapping(target=GetProductsForCatalogRequest)
            message = message_mapper.load(message_body)

            #  get permanent token
            permanent_token = (BusinessOwnerRepository(cls.__startup.session).
                               get_permanent_token(message.business_owner_facebook_id))

            product_groups, errors = GraphAPIProductsHandler.handle(permanent_token=permanent_token,
                                                                    product_catalog_id=message.product_catalog_facebook_id,
                                                                    startup=cls.__startup)

            # Create & publish product batches of message.page_size
            for groups in cls.__get_fields_partitions(product_groups, message.page_size):
                response = GetProductsForCatalogResponse(
                    business_owner_facebook_id=message.business_owner_facebook_id,
                    business_facebook_id=message.business_facebook_id,
                    product_groups=groups,
                    product_catalog_facebook_id=message.product_catalog_facebook_id,
                    filed_user_id=message.filed_user_id,
                    errors=errors)
                cls.__publish(response)

            # Create & publish final product information GetAllProductIdsResponse
            get_all_product_ids_response = GetAllProductIdsResponse()
            get_all_product_ids_response.product_catalog_facebook_id = message.product_catalog_facebook_id
            get_all_product_ids_response.business_facebook_id = message.business_facebook_id
            get_all_product_ids_response.business_owner_facebook_id = message.business_facebook_id
            get_all_product_ids_response.filed_user_id = message.filed_user_id
            get_all_product_ids_response.product_group_ids = [product_group.id for product_group in product_groups]
            get_all_product_ids_response.product_ids = [product.id
                                                        for product_group in product_groups
                                                        for product in product_group.products]
            cls.__publish(get_all_product_ids_response)

        except Exception as e:
            raise e

    @staticmethod
    def __get_fields_partitions(groups, page_size):
        n = len(groups)
        indices = range(0, n, page_size)
        for index in indices:
            yield groups[index:index + page_size]

    @classmethod
    def __publish(cls, product_sets):
        try:
            rabbitmq_client = RabbitMqClient(cls.__startup.rabbitmq_config,
                                             cls.__startup.exchange_details.name,
                                             cls.__startup.exchange_details.outbound_queue.key)
            rabbitmq_client.publish(product_sets)
            logger.info({"rabbitmq": rabbitmq_client.serialize_message(product_sets)})
        except Exception as e:
            raise e
