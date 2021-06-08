import json
import os
from datetime import datetime, timezone
from urllib.parse import urlencode

import requests
from flask import request
from woocommerce import API

from Core.Web.Security.JWTTools import decode_jwt_from_headers
from FiledEcommerce.Api.ImportIntegration.interface.ecommerce import Ecommerce
from FiledEcommerce.Api.utils.models.filed_model import FiledCustomProperties, FiledProduct, FiledVariant
from FiledEcommerce.Infrastructure.PersistanceLayer.EcommerceMongoRepository import EcommerceMongoRepository
from FiledEcommerce.Infrastructure.PersistanceLayer.EcommerceSQL_ORM_Model import *


class WooCommerce(Ecommerce):
    # Runtime Constants
    WOOCOMMERCE_API_VERSION = "wc/v3"
    WOOCOMMERCE_API_SCOPES = "read_write"
    RESPONSE_ERROR_MESSAGE = "Something went wrong!"

    # ENVIRONMENT Constants
    WOOCOMMERCE_API_KEY = os.environ.get('CONSUMER_API_KEY')
    WOOCOMMERCE_API_SECRET = os.environ.get('CONSUMER_API_SECRET')

    # endpoints
    __callback_url = "https://httpbin.org/anything"
    __install_endpoint = "/wc-auth/v1/authorize"
    __install_return_url = "https://filedwoocommerce.000webhostapp.com/shop"
    __load_redirect_url = "http://82940f3e58e4.ngrok.io/wordpress"
    __install_redirect_url = "https://localhost:4200/#/catalog/ecommerce"

    @staticmethod
    def is_valid_shop(shop: str):
        """
        Method to check if a shop is valid
        @param shop: store/shop URL
        @return:
        """
        req = requests.get(shop)
        if req.status_code == 200:
            return {"msg": "OK"}
        else:
            return {"error": "Invalid shop URL"}

    @classmethod
    def pre_install(cls):
        """
        Receive data from FE, check if shop is valid.
        Then provide necessary details, save to DB and connect to store.
        @param data:
        @return: redirect_url. e.g:
        http://localhost/wordpress/wc-auth/v1/authorize?app_name=Filed&scope=read_write&user_id=204&return_url=http%3A%2F%2Flocalhost%2Fwordpress&callback_url=https%3A%2F%2F4b0919d9af56.ngrok.io%2Fwoo_commerce
        """
        token_data = decode_jwt_from_headers()
        data = request.args
        shop: str = data.get("shop")
        if not cls.is_valid_shop(shop):
            return cls.RESPONSE_ERROR_MESSAGE
        user_id = token_data["user_filed_id"]
        params = {
            "app_name": "Filed",
            "scope": cls.WOOCOMMERCE_API_SCOPES,
            "user_id": user_id,
            "return_url": cls.__install_return_url,
            "callback_url": cls.__callback_url
        }
        query_string = urlencode(params)
        redirect_url = "%s%s?%s" % (shop, cls.__install_endpoint, query_string)

        mongo_db = EcommerceMongoRepository()
        mongo_db.add_one({"userId": user_id, "shop": shop})

        return redirect_url

    @classmethod
    def app_install(cls):
        """
        Get credentials from the redirect_url, save credentials to db,
        then redirect user to the Ecommerce page.
        https://woocommerce.github.io/woocommerce-rest-api-docs/#rest-api-keys
        @param data:
        @return: Ecommerce URL
        """
        data = request.args
        token_data = decode_jwt_from_headers()
        shop_url = data.get("shop")
        user_id = token_data["user_filed_id"]
        consumer_key = data.get("consumer_key")
        consumer_secret = data.get("consumer_secret")
        key_permissions = data.get("key_permissions")

        mongo_db = EcommerceMongoRepository()
        data = mongo_db.get_first_by_key("shop", shop_url)

        details = {
            "shop": shop_url,
            "user_id": user_id,
            "consumer_key": consumer_key,
            "consumer_secret": consumer_secret,
            "key_permissions": key_permissions,
        }
        flag = 0
        with engine.connect() as conn:
            query = (
                select([cols.Name])
                    .where(cols.FiledBusinessOwnerId == user_id)
                    .limit(1)
            )
            for row in conn.execute(query):
                try:
                    user_name = row[0]
                    flag = 1
                except Exception:
                    raise cls.RESPONSE_ERROR_MESSAGE_NOT_FOUND
        if flag == 1:
            temp_nl = user_name.split(" ", 1)
            if len(temp_nl) == 2:
                user_first_name, user_last_name = temp_nl[0], temp_nl[1]
            else:
                user_first_name, user_last_name = temp_nl[0], ""

        with engine.connect() as conn:
            ins = external_platforms.insert().values(
                CreatedAt=datetime.now(),
                CreatedById=user_id,
                CreatedByFirstName=user_first_name,
                CreatedByLastName=user_last_name,
                FiledBusinessOwnerId=user_id,
                PlatformId=6,
                Details=json.dumps(details)
            )
            result = conn.execute(ins)

        return cls.__install_redirect_url

    @classmethod
    def app_load(cls):
        """
        Redirect users to Filed's authentication page
        @param data:
        @return: authentication page URL
        """
        token_data = decode_jwt_from_headers()
        user_id = token_data["user_filed_id"]
        if cls.read_shop_from_db(user_id) != "":
            return cls.__install_redirect_url
        else:
            return cls.RESPONSE_ERROR_MESSAGE

    @classmethod
    def app_uninstall(cls):
        pass

    @staticmethod
    def read_shop_from_db(user_id):
        """
        Helper method to read required details from DB
        @param user_id:
        @return:
        """
        flag = 0
        with engine.connect() as conn:
            query = (
                select([ext_plat_cols.Details])
                    .where(ext_plat_cols.FiledBusinessOwnerId == user_id)
                    .where(ext_plat_cols.PlatformId == 6)
                    .limit(1)
            )
            for row in conn.execute(query):
                try:
                    details = json.loads(row["Details"])
                    shop = details.get("shop")
                    flag = 1
                except Exception as e:
                    raise e
        if flag == 1:
            return shop
        else:
            return ""

    @classmethod
    def mapper(cls, data, mapping):
        """
        Mapping of platform's data to Filed's models
        @param data:
        @param mapping: list of products with the right mapping
        @return:
        """
        body = data[1]
        data = data[0]
        filed_product_list = []
        imported_at = datetime.now(timezone.utc).replace(
            microsecond=0).isoformat()[:-6] + 'Z'

        product_id = []
        df = {}
        # process the mapping to get only mapped products
        for p_map in mapping["mapping"]["product"]:
            df[p_map["mapped_to"]] = data[p_map["name"]]
            df[p_map["filed_key"]] = df[p_map["mapped_to"]]

        # map the product to Filed's Product model
        filed_product = FiledProduct(
            product_id=df["product_id"],
            title=df["title"],
            product_type=df["product_type"],
            vendor="",
            description=df["description"],
            tags=",".join(df["tags"]),
            sku="",
            image_url=",".join(img["src"] for img in data["images"]),
            created_at=data["date_created"],
            updated_at=data["date_modified"],
            imported_at=imported_at,
            variants=[],
            brand="",
            availability=True
        )

        if len(data.get("variations")) != 0:
            # get the product_id, variation_id, and make a call to the variant endpoint
            product_id.append(data["id"])
            for p_id in product_id:
                variants_lst = cls.get_product_variants(body, p_id)

            # loop through the variants
            for variant in variants_lst:
                variant_map = {
                    "custom_fields": {}
                }
                # process the mapping to get only mapped products
                for v_map in mapping["mapping"]["variant"]:
                    if v_map["filed_key"] in FiledVariant.__annotations__:
                        variant_map[v_map["mapped_to"]] = variant[v_map["name"]]
                        variant_map[v_map["filed_key"]] = variant_map[v_map["mapped_to"]]

                # map the product to Filed's Variant model
                filed_variant = FiledVariant(
                    variant_id="",
                    filed_product_id="",
                    display_name="",
                    price=variant_map["price"],
                    compare_at_price=variant_map["compare_at_price"],
                    availability=variant_map["availability"],
                    url=variant_map["url"],
                    image_url="",
                    sku=variant_map["sku"],
                    barcode="",
                    inventory_quantity=variant_map["inventory_quantity"],
                    tags="",
                    description=variant_map["description"],
                    created_at=variant.get("created_at", imported_at),
                    updated_at=variant["date_modified"],
                    imported_at=imported_at,
                    material="",
                    condition="",
                    color="",
                    size="",
                    custom_props=FiledCustomProperties(
                        properties=variant_map["custom_fields"]
                    ) if variant_map["custom_fields"] else None
                )
                filed_product.variants.append(filed_variant.__dict__)
        filed_product_list.append(filed_product.__dict__)

        return filed_product_list

    @classmethod
    def get_products(cls, body):
        """
        Get all products from the user's store
        # https://woocommerce.github.io/woocommerce-rest-api-docs/?python#list-all-products
        @param body:
        @return: list of WC products
        """
        user_id = body.get("user_filed_id")
        credentials = cls.read_credentials_from_db(user_id)
        data = json.loads(credentials)
        shop_url = data["shop"]
        consumer_key = data["consumer_key"]
        consumer_secret = data["consumer_secret"]
        wcapi = API(
            url=shop_url,
            consumer_key=consumer_key,
            consumer_secret=consumer_secret,
            version=cls.WOOCOMMERCE_API_VERSION
        )
        json_data = wcapi.get("products").json()

        return json_data, body

    @staticmethod
    def read_credentials_from_db(user_id):
        """
        Helper method to read required details from DB
        @param user_id:
        @return:
        """
        flag = 0
        with engine.connect() as conn:
            query = (
                select([ext_plat_cols.Details])
                    .where(ext_plat_cols.FiledBusinessOwnerId == user_id)
                    .where(ext_plat_cols.PlatformId == 6)
                    .limit(1)
            )
            for row in conn.execute(query):
                if not row:
                    return ""
            return row

    @classmethod
    def get_product_variants(cls, body, p_id):
        """
        Helper function to get product variants from woocommerce
        https://woocommerce.github.io/woocommerce-rest-api-docs/#list-all-product-variations
        @param body:
        @param p_id: product ID
        @return: list of product variations
        """
        user_id = body.get("user_filed_id")
        credentials = cls.read_credentials_from_db(user_id)
        data = json.loads(credentials)
        shop_url = data["shop"]
        consumer_key = data["consumer_key"]
        consumer_secret = data["consumer_secret"]
        wcapi = API(
            url=shop_url,
            consumer_key=consumer_key,
            consumer_secret=consumer_secret,
            version=cls.WOOCOMMERCE_API_VERSION
        )
        return wcapi.get("products/%s/variations" % p_id).json()