import json
import os
from datetime import datetime, timezone
from urllib.parse import urlencode
from flask import request
import requests

from woocommerce import API

from Core.Web.Security.JWTTools import decode_jwt_from_headers
from FiledEcommerce.Api.ImportIntegration.interface.ecommerce import Ecommerce
from FiledEcommerce.Infrastructure.PersistanceLayer.EcommerceMongoRepository import EcommerceMongoRepository
from FiledEcommerce.Infrastructure.PersistanceLayer.EcommerceSQLRepository import session_scope



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
    __install_return_url = "https://filedwoocommerce.000webhostapp.com/shop",
    __load_redirect_url = "http://82940f3e58e4.ngrok.io/wordpress",
    __install_redirect_url = "https://localhost:4200/#/catalog/ecommerce"

    @staticmethod
    def is_valid_shop(shop: str):
        """
        Method to check if a shop is valid
        @param shop: store/shop URL
        @return:
        """
        request = requests.get(shop)
        if request.status_code == 200:
            return {"msg": "OK"}
        else:
            return {"error": "Invalid shop URL"}

    @classmethod
    def pre_install(cls, data):
        """
        Receive data from FE, check if shop is valid.
        Then provide necessary details, save to DB and connect to store.
        @param data:
        @return: redirect_url. e.g:
        http://localhost/wordpress/wc-auth/v1/authorize?app_name=Filed&scope=read_write&user_id=204&return_url=http%3A%2F%2Flocalhost%2Fwordpress&callback_url=https%3A%2F%2F4b0919d9af56.ngrok.io%2Fwoo_commerce
        """
        shop: str = data["shop"]
        if not cls.is_valid_shop(shop):
            return cls.RESPONSE_ERROR_MESSAGE
        user_id = data["user_id"]
        email = data.get("email")
        params = {
            "app_name": "Filed",
            "scope": cls.WOOCOMMERCE_API_SCOPES,
            "user_id": user_id,
            "return_url": cls.__install_return_url,
            "callback_url": cls.__callback_url
        }
        query_string = urlencode(params)
        redirect_url = f"{shop}{cls.__install_endpoint}?{query_string}"

        mongo_db = MongoManager.oauth_collection()
        mongo_db.insert_one({"email": email, "userId": user_id, "shop": shop})

        return redirect_url

    @classmethod
    def app_install(cls, data) -> str:
        """
        Get credentials from the redirect_url, save credentials to db,
        then redirect user to the Ecommerce page.
        https://woocommerce.github.io/woocommerce-rest-api-docs/#rest-api-keys
        @param data:
        @return: Ecommerce URL
        """
        shop_url = data["shop"]
        user_id = data["user_id"]
        consumer_key = data["consumer_key"]
        consumer_secret = data["consumer_secret"]
        key_permissions = data["read-write"]

        mongo_db = MongoManager.oauth_collection()
        data = mongo_db.find_one({"shop": shop_url})

        details = {
            "shop": shop_url,
            "user_id": user_id,
            "consumer_key": consumer_key,
            "consumer_secret": consumer_secret,
            "key_permissions": key_permissions,
        }
        cls.write_details_to_db(details, data)

        return cls.__install_redirect_url

    @classmethod
    def app_load(cls, data):
        """
        Redirect users to Filed's authentication page
        @param data:
        @return: authentication page URL
        """
        user_id = data["user_id"]
        if cls.read_credentials_from_db(user_id) != "":
            return cls.__load_redirect_url
        else:
            return cls.RESPONSE_ERROR_MESSAGE

    @classmethod
    def app_uninstall(cls, data):
        pass


    @staticmethod
    def read_credentials_from_db(user_id):
        """
        Helper method to read required details from DB
        @param user_id:
        @return:
        """
        with SqlManager() as cursor:
            cursor.execute(
                f"SELECT Details FROM ExternalPlatforms WHERE FiledBusinessOwnerId = {user_id} AND PlatformId = 6"
            )
            row = cursor.fetchval()
        if not row:
            return ""
        else:
            return row

    @staticmethod
    def write_details_to_db(details, data):
        """
        Helper function to write details/credentials to DB
        @param details: credentials to save
        @param data:
        @return:
        """
        user_id = data["userId"]
        with SqlManager() as cursor:
            cursor.execute(
                "INSERT INTO ExternalPlatforms(CreatedAt, CreatedById, CreatedByFirstName, CreatedByLastName," +
                " FiledBusinessOwnerId, PlatformId, Details) VALUES(?, ?, ?, ?, ?, ?, ?)",
                datetime.now(), user_id, "John", "Doe", user_id, 6, json.dumps(details)
            )
            cursor.commit()

    @classmethod
    def get_product_variants(cls, body, p_id):
        """
        Helper function to get product variants from woocommerce
        https://woocommerce.github.io/woocommerce-rest-api-docs/#list-all-product-variations
        @param body:
        @param p_id: product ID
        @return: list of product variations
        """
        user_id = body["user_id"]
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
        variants_lst = wcapi.get("products/%s/variations" % p_id).json()

        return variants_lst