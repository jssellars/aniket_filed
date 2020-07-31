import typing
from copy import deepcopy

from facebook_business.adobjects.productcatalog import ProductCatalog
from facebook_business.adobjects.productset import ProductSet as FacebookProductSet

from Core.Web.FacebookGraphAPI.GraphAPI.GraphAPISdkBase import GraphAPISdkBase
from Core.Web.FacebookGraphAPI.Tools import Tools
from Potter.FacebookProductCatalogs.Infrastructure.Domain.ProductSet import ProductSet
from Potter.FacebookProductCatalogs.Infrastructure.GraphAPIHandlers.GraphAPIProductFields import PRODUCT_SETS_FIELDS


class GraphAPIProductSetsHandler:
    @classmethod
    def handle(cls,
               permanent_token: typing.AnyStr = None,
               product_catalog_id: typing.AnyStr = None,
               startup: typing.Any = None) -> typing.Tuple[typing.List[typing.Any], typing.List[typing.Any]]:
        # initialize GraphAPI SDK
        _ = GraphAPISdkBase(startup.facebook_config, permanent_token)

        errors = []
        product_sets = []

        # get product sets
        try:
            product_catalog = ProductCatalog(fbid=product_catalog_id)
            facebook_product_sets = product_catalog.get_product_sets(fields=PRODUCT_SETS_FIELDS)

            product_sets = [cls.__map_facebook_sets(product_set) for product_set in facebook_product_sets]
        except Exception as e:
            errors.append(deepcopy(Tools.create_error(e, code="FB_GRAPH_API")))

        return product_sets, errors

    @classmethod
    def __map_facebook_sets(cls, facebook_product_set: typing.Any = None):
        facebook_product_set = Tools.convert_to_json(facebook_product_set)
        product_set = ProductSet()
        product_set.name = facebook_product_set[FacebookProductSet.Field.name]
        product_set.id = facebook_product_set[FacebookProductSet.Field.id]
        product_set.details = facebook_product_set

        return product_set
