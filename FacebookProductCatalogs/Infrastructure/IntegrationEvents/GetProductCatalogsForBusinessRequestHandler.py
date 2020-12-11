import typing

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

logger = logging.getLogger(__name__)


class GetProductCatalogsForBusinessRequestHandler:
    _config = None

    @classmethod
    def set_config(cls, config: typing.Any = None):
        cls._config = config
        return cls

    @classmethod
    def handle(cls, message_body: typing.Dict) -> typing.NoReturn:
        try:
            message_mapper = GetProductCatalogsForBusinessRequestMapping(target=GetProductCatalogsForBusinessRequest)
            message = message_mapper.load(message_body)

            permanent_token = (BusinessOwnerRepository(cls._config.sql_db_session).
                               get_permanent_token(message.business_owner_facebook_id))

            product_catalogs, errors = GraphAPIProductCatalogsHandler.handle(permanent_token=permanent_token,
                                                                             business_id=message.business_facebook_id,
                                                                             config=cls._config)

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
            rabbitmq_adapter = cls._config.rabbitmq_adapter
            rabbitmq_adapter.publish(product_catalogs)
            logger.info({"rabbitmq": rabbitmq_adapter.serialize_message(product_catalogs)})
        except Exception as e:
            raise e
