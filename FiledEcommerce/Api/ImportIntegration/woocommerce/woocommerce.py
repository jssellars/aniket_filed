import json
from datetime import datetime, timezone
from urllib.parse import urlencode

import humps
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
    __callback_url_local = "https://20cba55562e2.ngrok.io/api/v1/oauth/woocommerce/install"
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
            "return_url": cls.get_redirect_url(),
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
        cls.write_to_db(details, data)

        mongo_db.delete_many({"userId": user_id})
        return cls.get_redirect_url()

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
        @param data: list of products
        @param mapping: dict of mapping
        @return: dict of mapped products
        """
        token_data = decode_jwt_from_headers()
        body = token_data.get("user_filed_id")
        filed_product_list = []
        imported_at = datetime.now(timezone.utc).replace(
            microsecond=0).isoformat()[:-6] + 'Z'
        product_id = []

        # process the mapping to get only mapped products
        for wcp in data:
            df = {}
            for p_map in mapping.get("product"):
                if p_map["filed_key"] in FiledProduct.__annotations__:
                    df[p_map['filed_key']] = wcp[p_map["mapped_to"]]

            # map the product to Filed's Product model
            filed_product = FiledProduct(
                product_id=wcp["id"],
                title=wcp["name"],
                product_type=wcp["type"],
                vendor="",
                description=wcp["description"],
                tags=", ".join([tag["name"] for tag in wcp["tags"]]),
                sku=wcp["sku"],
                image_url=", ".join([img["src"] for img in wcp["images"]]),
                created_at=wcp["date_created"],
                updated_at=wcp["date_modified"],
                imported_at=imported_at,
                variants=[],
                brand="",
                availability=wcp["purchasable"]
            )

            if len(wcp.get("variations")) != 0:
                # get the product_id, variation_id, and make a call to the variant endpoint
                product_id.append(wcp["id"])
                for p_id in product_id:
                    variants_lst = cls.get_product_variants(body, p_id)

                # loop through the variants
                for variant in variants_lst:
                    color_flg, size_flg = 0, 0
                    for variant_attribute in variant["attributes"]:
                        if variant_attribute["name"] == "color":
                            color_flg = 1
                        elif variant_attribute["name"] == "size":
                            size_flg = 1
                        variant_map = {
                            "custom_fields": {}
                        }
                        # process the mapping to get only mapped products
                        for v_map in mapping["variant"]:
                            if v_map["filed_key"] in FiledVariant.__annotations__:
                                variant_map[v_map["filed_key"]] = variant[v_map["mapped_to"]]
                            else:
                                custom = {v_map["filed_key"]: variant.get(v_map["mapped_to"])}
                                variant_map["custom_fields"].update(custom)

                        # map the product to Filed's Variant model
                        filed_variant = FiledVariant(
                            variant_id=variant["id"],
                            filed_product_id="",
                            display_name=filed_product.title,
                            price=variant["sale_price"],
                            compare_at_price=variant["price"],
                            availability=variant["purchasable"],
                            url=variant["permalink"],
                            image_url=variant["image"].get("src"),
                            sku=variant["sku"],
                            barcode="",
                            inventory_quantity=variant["stock_quantity"],
                            tags=filed_product.tags,
                            description=variant["description"],
                            created_at=variant.get("date_created", imported_at),
                            updated_at=variant["date_modified"],
                            imported_at=imported_at,
                            material="",
                            condition="",
                            color=variant_attribute["option"] if color_flg == 1 else "",
                            size=variant_attribute["option"] if size_flg == 1 else "",
                            custom_props=FiledCustomProperties(
                                properties=variant_map["custom_fields"]
                            ) if variant_map["custom_fields"] else None,
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

        yield humps.decamelize(json_data)

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
                    .order_by(ext_plat_cols.CreatedAt.desc())
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

    @staticmethod
    def write_to_db(details: dict, data):
        """
        Helper method to save details to the db
        @param details: dict- e.g username, key, url, etc
        @param data: needed to fetch user_id
        @return: none
        """
        user_id = user_id = data.get("user_id")
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
