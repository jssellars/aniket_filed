import typing
from copy import deepcopy

from facebook_business.adobjects.productcatalog import ProductCatalog
from facebook_business.adobjects.productgroup import ProductGroup as FacebookProductGroup
from facebook_business.adobjects.productitem import ProductItem as FacebookProductItem

from Core.Web.FacebookGraphAPI.GraphAPI.GraphAPIClientBase import GraphAPIClientBase
from Core.Web.FacebookGraphAPI.GraphAPI.GraphAPIClientConfig import GraphAPIClientBaseConfig
from Core.Web.FacebookGraphAPI.GraphAPI.GraphAPISdkBase import GraphAPISdkBase
from Core.Web.FacebookGraphAPI.Tools import Tools
from PotterFacebookProductCatalogs.Infrastructure.Domain.Product import Product
from PotterFacebookProductCatalogs.Infrastructure.Domain.ProductGroup import ProductGroup
from PotterFacebookProductCatalogs.Infrastructure.GraphAPIHandlers.GraphAPIProductFields import PRODUCT_FIELDS, \
    PRODUCT_GROUPS_FIELDS, PRODUCT_SETS_FIELD_BY_PRODUCT
from PotterFacebookProductCatalogs.Infrastructure.GraphAPIRequests.GraphAPIRequestProducts import \
    GraphAPIRequestProduct


class GraphAPIProductsHandler:

    @classmethod
    def handle(cls,
               permanent_token: typing.AnyStr = None,
               product_catalog_id: typing.AnyStr = None,
               startup: typing.Any = None) -> typing.Tuple[typing.List[typing.Any],
                                                           typing.List[typing.Any]]:
        # initialize GraphAPI SDK
        _ = GraphAPISdkBase(startup.facebook_config, permanent_token)

        errors = []

        # get product groups
        product_groups = []
        try:
            product_catalog = ProductCatalog(fbid=product_catalog_id)

            product_groups = product_catalog.get_product_groups(fields=PRODUCT_GROUPS_FIELDS)
        except Exception as e:
            errors.append(deepcopy(Tools.create_error(e, code="FB_GRAPH_API")))

        # get products
        products = []
        try:
            config = GraphAPIClientBaseConfig()
            config.request = GraphAPIRequestProduct(api_version=startup.facebook_config.api_version,
                                                    access_token=permanent_token,
                                                    product_catalog_id=product_catalog_id,
                                                    fields=PRODUCT_FIELDS)
            graph_api_client = GraphAPIClientBase(business_owner_permanent_token=permanent_token, config=config)
            response, _ = graph_api_client.call_facebook()
            if isinstance(products, Exception):
                errors.append(deepcopy(Tools.create_error(response, code="FB_GRAPH_API")))
                product_groups = []
                products = []
            else:
                products = response
        except Exception as e:
            errors.append(deepcopy(Tools.create_error(e, code="FB_GRAPH_API")))

        if products:
            products = [cls.__map_facebook_product(product) for product in products]

        if product_groups:
            product_groups = [cls.__map_facebook_group(product_group, products) for product_group in product_groups]

        return product_groups, errors

    @classmethod
    def __get_products_by_product_group_id(cls,
                                           product_group_id: typing.AnyStr = None,
                                           products: typing.List[Product] = None):
        relevant_products = [product for product in products
                             if product.facebook_product_group_id == product_group_id]
        return relevant_products

    @classmethod
    def __map_facebook_group(cls, facebook_product_group: typing.Any = None, products: typing.List[Product] = None):
        facebook_product_group = Tools.convert_to_json(facebook_product_group)
        product_group = ProductGroup()
        product_group.id = facebook_product_group[FacebookProductGroup.Field.id]
        product_group.retailer_id = facebook_product_group[FacebookProductGroup.Field.retailer_id]
        product_group.products = cls.__get_products_by_product_group_id(product_group.id, products)
        return product_group

    @classmethod
    def __map_facebook_product(cls, facebook_product: typing.Any = None):
        if not isinstance(facebook_product, dict):
            facebook_product = Tools.convert_to_json(facebook_product)
        product = Product()
        product.id = facebook_product.get(FacebookProductItem.Field.id)
        product.currency = facebook_product.get(FacebookProductItem.Field.currency)
        product.description = facebook_product.get(FacebookProductItem.Field.description)
        product.url = facebook_product.get(FacebookProductItem.Field.url)
        product.image_url = facebook_product.get(FacebookProductItem.Field.image_url)
        product.details = facebook_product
        product.availability = facebook_product.get(FacebookProductItem.Field.availability)
        product.name = facebook_product.get(FacebookProductItem.Field.name)
        product.price = facebook_product.get(FacebookProductItem.Field.price)
        facebook_product_group_id = facebook_product.get(FacebookProductItem.Field.product_group)
        product.facebook_product_group_id = facebook_product_group_id["id"]
        product.category = facebook_product.get(FacebookProductItem.Field.category)
        product.type = facebook_product.get(FacebookProductItem.Field.product_type)
        product.short_description = facebook_product.get(FacebookProductItem.Field.short_description)
        product.custom_data = cls.__map_custom_data(facebook_product.get(FacebookProductItem.Field.custom_data))
        product.custom_label_0 = facebook_product.get(FacebookProductItem.Field.custom_label_0)
        product.custom_label_1 = facebook_product.get(FacebookProductItem.Field.custom_label_1)
        product.custom_label_2 = facebook_product.get(FacebookProductItem.Field.custom_label_2)
        product.custom_label_3 = facebook_product.get(FacebookProductItem.Field.custom_label_3)
        product.custom_label_4 = facebook_product.get(FacebookProductItem.Field.custom_label_4)
        product.facebook_product_set_ids = cls.__get_product_set_ids_from_product(facebook_product.get(PRODUCT_SETS_FIELD_BY_PRODUCT, []))

        return product

    @staticmethod
    def __map_custom_data(raw_custom_data: typing.List[typing.Dict]) -> typing.Dict:
        mapped_custom_data = {}
        if raw_custom_data:
            for entry in raw_custom_data:
                mapped_custom_data[entry['key']] = entry['value']
        return mapped_custom_data

    @classmethod
    def __get_product_set_ids_from_product(cls, product_sets: typing.Dict = None) -> typing.List[typing.AnyStr]:
        if not product_sets:
            return []
        product_sets = product_sets.get('data')
        product_set_ids = []
        if product_sets:
            product_set_ids = [product_set.get('id') for product_set in product_sets]
        return product_set_ids
