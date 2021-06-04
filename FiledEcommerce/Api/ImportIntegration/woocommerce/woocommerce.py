import json
import os
from datetime import datetime
from urllib.parse import urlencode

import requests
from flask import request

from Core.Web.Security.JWTTools import decode_jwt_from_headers
from FiledEcommerce.Api.ImportIntegration.interface.ecommerce import Ecommerce
from FiledEcommerce.Infrastructure.PersistanceLayer.EcommerceMongoRepository import EcommerceMongoRepository
from FiledEcommerce.Infrastructure.PersistanceLayer.EcommerceSQLRepository import SqlManager


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
    __install_return_url = "https://localhost:4200/#/catalog/ecommerce"
    __load_redirect_url = "https://005f22fd530c.ngrok.io/wordpress"
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

        with SqlManager() as cursor:
            cursor.execute("SELECT Name FROM FiledBusinessOwners WHERE FiledBusinessOwnerId = ?", user_id)
            user_name = cursor.fetchval()
        temp_nl = user_name.split(" ", 1)
        if len(temp_nl) == 2:
            user_first_name, user_last_name = temp_nl[0], temp_nl[1]
        else:
            user_first_name, user_last_name = temp_nl[0], ""

        with SqlManager() as cursor:
            cursor.execute(
                "INSERT INTO ExternalPlatforms(CreatedAt, CreatedById, CreatedByFirstName, CreatedByLastName," +
                " FiledBusinessOwnerId, PlatformId, Details) VALUES(?, ?, ?, ?, ?, ?, ?)",
                datetime.now(), user_id, user_first_name, user_last_name, user_id, 6, json.dumps(details)
            )
            cursor.commit()

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
        if cls.read_credentials_from_db(user_id) != "":
            return cls.__install_redirect_url
        else:
            return cls.RESPONSE_ERROR_MESSAGE

    @classmethod
    def app_uninstall(cls):
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
