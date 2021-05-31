import base64
import hashlib
import hmac
import json
import logging
import re
import uuid
from datetime import datetime, timezone
from typing import Match, Optional

import requests
from flask import request
from requests.exceptions import HTTPError

from Core.Web.Security.JWTTools import decode_jwt_from_headers
from FiledEcommerce.Api.ImportIntegration.interface.ecommerce import Ecommerce
from FiledEcommerce.Infrastructure.PersistanceLayer.EcommerceMongoRepository import EcommerceMongoRepository
from FiledEcommerce.Infrastructure.PersistanceLayer.EcommerceSQLRepository import session_scope


class Shopify(Ecommerce):
    # Runtime Constants
    ACCESS_MODE: str = "offline"
    SHOPIFY_API_VERSION = "2021-04"
    SHOPIFY_API_SCOPES = "read_products"
    RESPONSE_ERROR_MESSAGE = "Something went wrong!"

    # ENVIRONMENT Constants
    SHOPIFY_API_KEY = "5cab30a1fb0bd39a4704a39dbca7dce3"
    SHOPIFY_API_SECRET = "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"
    SHOPIFY_APP_URL = "https://ckqug0g7z8.execute-api.eu-west-1.amazonaws.com/dev"

    # private props
    __base_url = ""
    __access_token = "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"

    # endpoints
    __install_endpoint = "oauth/shopify/install"
    __uninstall_endpoint = "oauth/shopify/uninstall"
    __load_redirect_url = "https://localhost:4200/#/catalog"
    __install_redirect_url = "https://localhost:4200/#/catalog/ecommerce"

    @classmethod
    def generate_hmac_hex(cls, data: bytes) -> str:
        return hmac.new(cls.SHOPIFY_API_SECRET.encode("utf-8"), data, hashlib.sha256).hexdigest()

    @staticmethod
    def generate_utc_aware_datestring():
        return datetime.now(timezone.utc).replace(microsecond=0).isoformat()[:-6] + "Z"

    @staticmethod
    def verify_shopify_hmac(data: bytes, orig_hmac: str):
        return Shopify.generate_hmac_hex(data) == orig_hmac

    @staticmethod
    def is_valid_shop(shop: str) -> Optional[Match[str]]:
        # Shopify docs give regex with protocol required, but shop never includes protocol
        shopname_regex = r"[a-zA-Z0-9][a-zA-Z0-9\-]*\.myshopify\.com[\/]?"
        return re.match(shopname_regex, shop)

    @classmethod
    def verify_api_call(cls, request_query_params: dict) -> int:
        """ Verify if a call is genuine by checking the HMAC hex """

        received_hmac: str = request_query_params["hmac"]
        shop: str = request_query_params["shop"]

        data = "&".join([f"{key}={value}" for key, value in request_query_params.items() if key != "hmac"]).encode(
            "utf-8"
        )

        if not cls.verify_shopify_hmac(data, received_hmac):
            logging.error(f"HMAC could not be verified: \n\thmac {received_hmac}\n\tdata {data}")
            return 400

        if shop and not cls.is_valid_shop(shop):
            logging.error(f"Shop name received is invalid: \n\tshop {shop}")
            return 401

        # call is verified
        return 200

    @classmethod
    def verify_webhook_call(
        cls, encoded_shopify_hmac: str, request_body: bytes, received_topic: str, desired_topic: str
    ) -> int:
        """ Verify if a webhook call is genuine by checking the HMAC hex """

        hmac_hex = base64.b64decode(encoded_shopify_hmac).hex()

        if not cls.verify_shopify_hmac(request_body, hmac_hex):
            logging.error(f"HMAC could not be verified: \n\thmac {hmac_hex}\n\tdata {request_body}")
            return 401

        if received_topic != desired_topic:
            logging.error(f"Received wrong webhook topic: \n\treceived {received_topic} \n\t desired {desired_topic}")
            return 400

        # call is verified
        return 200

    @classmethod
    def get_access_token(cls, shop: str, code: str) -> tuple:
        """ Retrieve the access token from Shopify Admin OAuth. """

        url = f"https://{shop}/admin/oauth/access_token"
        payload = {"client_id": cls.SHOPIFY_API_KEY, "client_secret": cls.SHOPIFY_API_SECRET, "code": code}
        try:
            response = requests.post(url, json=payload)
            response.raise_for_status()
            data = response.json()
            return data["access_token"], 200
        except HTTPError as ex:
            logging.exception(str(ex))
            return "Authorization code expired", 400

    @classmethod
    def pre_install(cls):
        """When Front End sends the credentials, check if shop is valid.
        If yes, generate the app install url and store credentials in MongoDB for temporary matching.
        """
        token_data = decode_jwt_from_headers()
        shop: str = request.args.get("shop")
        if cls.is_valid_shop(shop):
            user_id = token_data["user_filed_id"]
            # NONCE is a single-use random value we send to Shopify so we know the next call from Shopify is valid.
            # https://en.wikipedia.org/wiki/Cryptographic_nonce
            nonce = uuid.uuid4().hex

            install_redirect_url = f"{cls.SHOPIFY_APP_URL}/{cls.__install_endpoint}"
            redirect_url = (
                f"https://{shop}/admin/oauth/authorize?"
                f"client_id={cls.SHOPIFY_API_KEY}&scope={cls.SHOPIFY_API_SCOPES}&"
                f"redirect_uri={install_redirect_url}&state={nonce}&grant_options[]={cls.ACCESS_MODE}"
            )

            # store the user credentials in Mongo for matching
            mongo_db = EcommerceMongoRepository()
            mongo_db.add_one({"userId": user_id, "nonce": nonce, "shop": shop})

            return redirect_url
        else:
            return cls.RESPONSE_ERROR_MESSAGE

    @classmethod
    def app_load(cls) -> str:
        """ From Shopify, new (or registered) user opens our app. Redirect them to Filed Platform to Sign Up/In. """

        # First we verify the call
        verification_status = cls.verify_api_call(request.args)
        if verification_status != 200:
            # call not verified
            return cls.RESPONSE_ERROR_MESSAGE

        return cls.__load_redirect_url

    @classmethod
    def app_install(cls) -> str:
        """When the app is installed, Shopify redirects us to this method. We will check the call and get the
        access token using the one time authorization code Shopify provides us. We will also create an webhook
        in Shopify for receiving notification when user uninstalls our app.

        Afterwards, we return a redirect url to lead user back to our platform.
        """
        data = request.args
        # First we verify the call
        verification_status = cls.verify_api_call(request.args)
        if verification_status != 200:
            # call not verified
            return cls.RESPONSE_ERROR_MESSAGE

        # Now we do the tasks
        shop: str = data.get("shop")
        code: str = data.get("code")
        state: str = data.get("state")

        # Shopify passes our NONCE as the `state` parameter and we need to ensure it matches!
        mongo_db = EcommerceMongoRepository()
        # if a record exists, state is valid
        record = mongo_db.get_first_by_key({"shop": shop, "nonce": state})
        if not record:
            logging.error(f"Invalid state received: \n\tstate {state}")
            return "Invalid `state` received"

        # Ok, NONCE matches, we get rid of it now (a nonce, by definition, should only be used once)
        mongo_db.delete_many({"shop": shop})

        # Using the `code` received from Shopify we can now generate an access token that is specific to
        # the specified `shop` with the ACCESS_MODE and SHOPIFY_API_SCOPES we have.
        cls.__access_token, token_status = cls.get_access_token(shop=shop, code=code)
        if token_status != 200:
            return cls.__access_token  # now a error message

        # Now we store the token in database
        user_id = record["userId"]
        details = {"shop_name": shop, "access_token": cls.__access_token}

        print(details)

        with session_scope() as cursor:
            cursor.execute(
                "INSERT INTO ExternalPlatforms(CreatedAt, CreatedById, CreatedByFirstName, CreatedByLastName, "
                + "FiledBusinessOwnerId, PlatformId, Details) VALUES(?, ?, ?, ?, ?, ?, ?)",
                cls.generate_utc_aware_datestring(),
                user_id,
                "Sandeepan",
                "B",
                user_id,
                2,
                json.dumps(details),
            )  # Shopify Platform is 2
            cursor.commit()

        # Now we register a webhook so Shopify will notify us when the app gets uninstalled
        # DEBUG NOTE: The webhooks DOES NOT WORK with localhost
        webhook_url = f"{cls.SHOPIFY_APP_URL}/{cls.__uninstall_endpoint}"
        cls.create_webhook(shop=shop, address=webhook_url, topic="app/uninstalled")

        # Now we redirect client back to our platform for catalog mapping
        return cls.__install_redirect_url

    @classmethod
    def app_uninstall(
        cls, encoded_shopify_hmac: str, webhook_topic: str, request_body: bytes, webhook_payload: dict
    ) -> tuple:
        """
        Webhook Processing for "app/uninstalled" Topic for when Shopify sends us notification that
        a user uninstalled our app. We will run some routine diagnostics and cleanup here.

        :param encoded_shopify_hmac: The Header String 'X-Shopify-Hmac-Sha256'
        :param webhook_topic: The Header String 'X-Shopify-Topic'
        :param request_body: UTF-8 encoded bytes object of the request body
        :param webhook_payload: Received JSON body data

        :return: A tuple of Response String and Status Code number
        """

        # verify_webhook_call
        verification_status = cls.verify_webhook_call(
            encoded_shopify_hmac, request_body, webhook_topic, "app/uninstalled"
        )

        if verification_status != 200:
            # call not verified
            return cls.RESPONSE_ERROR_MESSAGE, verification_status

        logging.info(f"webhook call received {webhook_topic}:\n{json.dumps(webhook_payload, indent=4)}")
        # NOTE the shop ACCESS_TOKEN is now void!
        # TODO: We need a SQL DELETE operation here to delete relevant credential record
        # cls.write_token_to_db(webhook_payload["domain"], "")

        return "OK", 200

    # https://shopify.dev/tutorials/add-gdpr-webhooks-to-your-app
    @classmethod
    def customer_redact(cls):
        """ Webhook Processing for "customers/redact" Topic."""
        pass

    @classmethod
    def shop_redact(cls):
        """ Webhook Processing for "shop/redact" Topic."""
        pass

    @classmethod
    def customer_data_req(cls):
        """ Webhook Processing for "customers/data_request" Topic."""
        pass

    @classmethod
    def authenticated_shopify_call(
        cls, shop: str, endpoint: str, params: dict = None, payload: dict = None, headers: dict = {}, query: str = ""
    ) -> dict:
        """ Make an authenticated Shopify Admin API call """

        cls.__base_url = f"https://{shop}/admin/api/{cls.SHOPIFY_API_VERSION}"
        url = f"{cls.__base_url}/{endpoint}.json"
        headers["X-Shopify-Access-Token"] = cls.__access_token

        try:
            if endpoint == "graphql":
                # later on only graphql to get all data
                response = requests.post(url, params=params, json={"query": query}, headers=headers)
            elif endpoint == "webhooks":
                # this REST endpoint is always needed for webhooks
                response = requests.post(url, params=params, json=payload, headers=headers)
            else:
                # REST method to get data
                response = requests.get(url, params=params, json=payload, headers=headers)

            response.raise_for_status()
            logging.debug(f"authenticated_shopify_call response:\n{json.dumps(response.json(), indent=4)}")
            return response.json()
        except HTTPError as ex:
            logging.exception(ex)
            return cls.RESPONSE_ERROR_MESSAGE

    @classmethod
    def create_webhook(cls, shop: str, address: str, topic: str) -> dict:
        """ Create a webhook in Shopify user shop """

        endpoint = "webhooks"
        payload = {"webhook": {"topic": topic, "address": address, "format": "json"}}
        return cls.authenticated_shopify_call(shop=shop, endpoint=endpoint, payload=payload)
