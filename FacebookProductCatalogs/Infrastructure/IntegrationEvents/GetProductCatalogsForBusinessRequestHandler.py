import logging
from typing import Dict

from Core.fixtures import Fixtures
from Core.rabbitmq_adapter import RabbitMqAdapter
from Core.settings_models import Model
from FacebookProductCatalogs.Infrastructure.GraphAPIHandlers.GraphAPIProductCatalogsHandler import \
    GraphAPIProductCatalogsHandler
from FacebookProductCatalogs.Infrastructure.IntegrationEvents.GetProductCatalogsForBusinessRequest import \
    GetProductCatalogsForBusinessRequest
from FacebookProductCatalogs.Infrastructure.IntegrationEvents.GetProductCatalogsForBusinessRequestMapping import \
    GetProductCatalogsForBusinessRequestMapping
from FacebookProductCatalogs.Infrastructure.IntegrationEvents.GetProductCatalogsForBusinessResponse import \
    GetProductCatalogsForBusinessResponse

logger = logging.getLogger(__name__)


class GetProductCatalogsForBusinessRequestHandler:
    @classmethod
    def handle(cls, message_body: Dict, fixtures: Fixtures, config: Model) -> None:
        message_mapper = GetProductCatalogsForBusinessRequestMapping(target=GetProductCatalogsForBusinessRequest)
        message = message_mapper.load(message_body)

        permanent_token = fixtures.business_owner_repository.get_permanent_token(message.business_owner_facebook_id)

        product_catalogs, errors = GraphAPIProductCatalogsHandler.handle(
            permanent_token=permanent_token, business_id=message.business_facebook_id, config=config
        )

        response = GetProductCatalogsForBusinessResponse(
            business_owner_facebook_id=message.business_owner_facebook_id,
            business_facebook_id=message.business_facebook_id,
            product_catalogs=product_catalogs,
            filed_user_id=message.filed_user_id,
            errors=errors,
        )

        cls.__publish(response, fixtures.rabbitmq_adapter)

    @classmethod
    def __publish(cls, product_catalogs: GetProductCatalogsForBusinessResponse, rabbitmq_adapter: RabbitMqAdapter):
        rabbitmq_adapter.publish(product_catalogs)
        logger.info({"rabbitmq": rabbitmq_adapter.serialize_message(product_catalogs)})
