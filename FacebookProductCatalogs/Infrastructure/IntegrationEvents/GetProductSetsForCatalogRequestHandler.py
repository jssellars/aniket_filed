import logging
from typing import Dict

from Core.fixtures import Fixtures
from Core.rabbitmq_adapter import RabbitMqAdapter
from Core.settings_models import Model
from FacebookProductCatalogs.Infrastructure.GraphAPIHandlers.GraphAPIProductSetsHandler import \
    GraphAPIProductSetsHandler
from FacebookProductCatalogs.Infrastructure.IntegrationEvents.GetProductSetsForCatalogRequest import \
    GetProductSetsForCatalogRequest
from FacebookProductCatalogs.Infrastructure.IntegrationEvents.GetProductSetsForCatalogRequestMapping import \
    GetProductSetsForCatalogRequestMapping
from FacebookProductCatalogs.Infrastructure.IntegrationEvents.GetProductSetsForCatalogResponse import \
    GetProductSetsForCatalogResponse

logger = logging.getLogger(__name__)


class GetProductSetsForCatalogRequestHandler:
    @classmethod
    def handle(cls, message_body: Dict, fixtures: Fixtures, config: Model) -> None:
        message_mapper = GetProductSetsForCatalogRequestMapping(target=GetProductSetsForCatalogRequest)
        message = message_mapper.load(message_body)

        permanent_token = fixtures.business_owner_repository.get_permanent_token(message.business_owner_facebook_id)

        product_sets, errors = GraphAPIProductSetsHandler.handle(
            permanent_token=permanent_token,
            product_catalog_id=message.product_catalog_facebook_id,
            config=config,
        )

        response = GetProductSetsForCatalogResponse(
            business_owner_facebook_id=message.business_owner_facebook_id,
            business_facebook_id=message.business_facebook_id,
            product_catalog_facebook_id=message.product_catalog_facebook_id,
            product_sets=product_sets,
            filed_user_id=message.filed_user_id,
            errors=errors,
        )

        cls.__publish(response, fixtures.rabbitmq_adapter)

    @classmethod
    def __publish(cls, product_sets: GetProductSetsForCatalogResponse, rabbitmq_adapter: RabbitMqAdapter):
        rabbitmq_adapter.publish(product_sets)
        logger.info({"rabbitmq": rabbitmq_adapter.serialize_message(product_sets)})
