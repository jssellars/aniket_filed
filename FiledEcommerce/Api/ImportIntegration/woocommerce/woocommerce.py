import json
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
    __callback_url = "https://py-filed-ecommerce-api.dev3.filed.com/api/v1/oauth/woocommerce/install"
    __callback_url_local = "https://3a8c92293e9e.ngrok.io/api/v1/oauth/woocommerce/install"
    __pre_install_endpoint = "/wc-auth/v1/authorize"


    @classmethod
    def get_redirect_url(cls):
        return (
            "https://localhost:4200/#/catalog/ecommerce"
            if request.host.startswith("localhost")
            else "https://ecommerce.filed.com/#/catalog/ecommerce"
        )

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
            "return_url": cls.get_redirect_url,
            "callback_url": cls.__callback_url
        }
        query_string = urlencode(params)
        redirect_url = "%s%s?%s" % (shop, cls.__pre_install_endpoint, query_string)

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
        data = request.get_json()
        user_id = data.get("user_id")
        mongo_db = EcommerceMongoRepository()
        record = mongo_db.get_first_by_key("userId", user_id)
        shop_url = record.get("shop")
        consumer_key = data.get("consumer_key")
        consumer_secret = data.get("consumer_secret")
        key_permissions = data.get("key_permissions")

        details = {
            "shop": shop_url,
            "user_id": user_id,
            "consumer_key": consumer_key,
            "consumer_secret": consumer_secret,
            "key_permissions": key_permissions,
        }
        # cls.write_token_to_db(details, data)
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
                except Exception as e:
                    raise e
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

        mongo_db.delete_many({"userId" : user_id})
        return cls.get_redirect_url

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
            return cls.get_redirect_url()
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
        token_data = decode_jwt_from_headers()
        body = token_data.get("user_filed_id")
        filed_product_list = []
        imported_at = datetime.now(timezone.utc).replace(
            microsecond=0).isoformat()[:-6] + 'Z'

        product_id = []
        df = {}
        # process the mapping to get only mapped products
        for p_map in mapping["product"]:
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
                for v_map in mapping["variant"]:
                    if v_map["filed_key"] in FiledVariant.__annotations__:
                        variant_map[v_map["mapped_to"]] = variant[v_map["name"]]
                        variant_map[v_map["filed_key"]] = variant_map[v_map["mapped_to"]]
                    else:
                        variant_map[v_map["mapped_to"]] = variant[v_map["name"]]
                        custom = {v_map["filed_key"]: variant_map[v_map["mapped_to"]]}
                        variant_map["custom_fields"].update(custom)

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

        return {"products": filed_product_list}

    @classmethod
    def get_products(cls, body):
        """
        Get all products from the user's store
        # https://woocommerce.github.io/woocommerce-rest-api-docs/?python#list-all-products
        @param body:
        @return: list of WC products
        """
        user_id = body.get("user_filed_id")
        data = cls.read_credentials_from_db(user_id)
        shop_url = data[0]
        consumer_key = data[1]
        consumer_secret = data[2]
        wcapi = API(
            url=shop_url,
            consumer_key=consumer_key,
            consumer_secret=consumer_secret,
            wp_api=True,
            version=cls.WOOCOMMERCE_API_VERSION
        )
        json_data = wcapi.get("products").json()

        return json_data

    @staticmethod
    def read_credentials_from_db(user_id):
        """
        Helper method to read required details from DB
        @param user_id:
        @return:
        """
        with engine.connect() as conn:
            query = (
                select([ext_plat_cols.Details])
                    .where(ext_plat_cols.FiledBusinessOwnerId == user_id)
                    .where(ext_plat_cols.PlatformId == 6)
                    .limit(1)
            )
            for record in conn.execute(query):
                row = record["Details"]

            details = json.loads(row)
            return details["shop"], details["consumer_key"], details["consumer_secret"]

    @classmethod
    def get_product_variants(cls, body, p_id):
        """
        Helper function to get product variants from woocommerce
        https://woocommerce.github.io/woocommerce-rest-api-docs/#list-all-product-variations
        @param body:
        @param p_id: product ID
        @return: list of product variations
        """
        data = cls.read_credentials_from_db(body)
        shop_url = data[0]
        consumer_key = data[1]
        consumer_secret = data[2]
        wcapi = API(
            url=shop_url,
            consumer_key=consumer_key,
            consumer_secret=consumer_secret,
            version=cls.WOOCOMMERCE_API_VERSION
        )
        return wcapi.get("products/%s/variations" % p_id).json()
