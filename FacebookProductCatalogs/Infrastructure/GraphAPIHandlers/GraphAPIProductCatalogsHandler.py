from copy import deepcopy
from enum import Enum
from typing import Tuple, List, Any

from facebook_business.adobjects.business import Business
from facebook_business.adobjects.productcatalog import ProductCatalog as FacebookProductCatalog

from Core.Web.FacebookGraphAPI.GraphAPI.GraphAPISdkBase import GraphAPISdkBase
from Core.Web.FacebookGraphAPI.Tools import Tools
from Core.settings_models import Model
from FacebookProductCatalogs.Infrastructure.Domain.ProductCatalog import ProductCatalog
from FacebookProductCatalogs.Infrastructure.GraphAPIHandlers.GraphAPIProductFields import \
    PRODUCT_CATALOGS_FIELDS


class GraphAPIProductCatalogsTypeEnum(Enum):
    OWNED = "Owned Catalog"
    CLIENT = "Client Catalog"


class GraphAPIProductCatalogsHandler:

    @classmethod
    def handle(cls,
               permanent_token: str = None,
               business_id: str = None,
               config: Model = None) -> Tuple[List[Any], List[Any]]:
        # initialize GraphAPI SDK
        _ = GraphAPISdkBase(config.facebook, permanent_token)

        errors = []
        product_catalogs = []
        # create business
        business = Business(fbid=business_id)

        # get owned catalogs
        try:
            owned_catalogs = business.get_owned_product_catalogs(fields=PRODUCT_CATALOGS_FIELDS)
            product_catalogs = [cls.__map_facebook_catalog(catalog, GraphAPIProductCatalogsTypeEnum.OWNED.value)
                                for catalog in owned_catalogs]
        except Exception as e:
            errors.append(deepcopy(Tools.create_error(e, code="FB_GRAPH_API")))

        # get facebook catalogs
        try:
            client_catalogs = business.get_client_product_catalogs(fields=PRODUCT_CATALOGS_FIELDS)
            product_catalogs += [cls.__map_facebook_catalog(catalog, GraphAPIProductCatalogsTypeEnum.CLIENT.value)
                                 for catalog in client_catalogs]
        except Exception as e:
            errors.append(deepcopy(Tools.create_error(e, code="FB_GRAPH_API")))

        return product_catalogs, errors

    @classmethod
    def __map_facebook_catalog(cls, facebook_product_catalog: Any = None, catalog_type: str = None):
        facebook_product_catalog = Tools.convert_to_json(facebook_product_catalog)
        product_catalog = ProductCatalog()
        product_catalog.name = facebook_product_catalog[FacebookProductCatalog.Field.name]
        product_catalog.id = facebook_product_catalog[FacebookProductCatalog.Field.id]
        product_catalog.vertical = facebook_product_catalog[FacebookProductCatalog.Field.vertical]
        product_catalog.type = catalog_type
        product_catalog.details = facebook_product_catalog

        return product_catalog
