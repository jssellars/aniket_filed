import typing

from Core.Web.BusinessOwnerRepository.BusinessOwnerRepository import BusinessOwnerRepository
from FacebookProductCatalogs.Infrastructure.GraphAPIHandlers.GraphAPIProductSetsHandler import \
    GraphAPIProductSetsHandler
from FacebookProductCatalogs.Infrastructure.IntegrationEvents.GetProductSetsForCatalogRequest import \
    GetProductSetsForCatalogRequest
from FacebookProductCatalogs.Infrastructure.IntegrationEvents.GetProductSetsForCatalogRequestMapping import \
    GetProductSetsForCatalogRequestMapping
from FacebookProductCatalogs.Infrastructure.IntegrationEvents.GetProductSetsForCatalogResponse import \
    GetProductSetsForCatalogResponse


import logging

logger = logging.getLogger(__name__)


class GetProductSetsForCatalogRequestHandler:
    _config = None

    @classmethod
    def set_config(cls, config: typing.Any = None):
        cls._config = config
        return cls

    @classmethod
    def handle(cls, message_body: typing.Dict) -> typing.NoReturn:
        try:
            message_mapper = GetProductSetsForCatalogRequestMapping(target=GetProductSetsForCatalogRequest)
            message = message_mapper.load(message_body)

            permanent_token = (BusinessOwnerRepository(cls._config.sql_db_session).
                               get_permanent_token(message.business_owner_facebook_id))

            product_sets, errors = GraphAPIProductSetsHandler.handle(permanent_token=permanent_token,
                                                                     product_catalog_id=message.product_catalog_facebook_id,
                                                                     config=cls._config)

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
            rabbitmq_adapter = cls._config.rabbitmq_adapter
            rabbitmq_adapter.publish(product_sets)
            logger.info({"rabbitmq": rabbitmq_adapter.serialize_message(product_sets)})
        except Exception as e:
            raise e
