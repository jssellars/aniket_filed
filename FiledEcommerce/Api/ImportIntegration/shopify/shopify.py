import base64
import hashlib
import hmac
import json
import logging
import uuid
from dataclasses import asdict
from typing import List, Dict
import humps
import requests
import re
from datetime import datetime, timezone
from typing import Match, Optional
from sgqlc.operation import Operation
import requests
from flask import request
from requests.exceptions import HTTPError
from FiledEcommerce.Api.ImportIntegration.shopify.graphql import shopify_schema
from FiledEcommerce.Api.utils.models.filed_model import FiledProduct, FiledVariant, FiledCustomProperties
from Core.Web.Security.JWTTools import decode_jwt_from_headers
from FiledEcommerce.Api.utils.tools.date_utils import get_utc_aware_date
from FiledEcommerce.Api.ImportIntegration.interface.ecommerce import Ecommerce
from FiledEcommerce.Infrastructure.PersistanceLayer.EcommerceMongoRepository import EcommerceMongoRepository
from FiledEcommerce.Infrastructure.PersistanceLayer.EcommerceSQL_ORM_Model import *

class Shopify(Ecommerce):
    # Runtime Constants
    ACCESS_MODE: str = "offline"
    SHOPIFY_API_VERSION = "2021-04"
    SHOPIFY_API_SCOPES = "read_products"
    RESPONSE_ERROR_MESSAGE = "Something went wrong!"

    # ENVIRONMENT Constants
    SHOPIFY_API_KEY = "5cab30a1fb0bd39a4704a39dbca7dce3"
    SHOPIFY_API_SECRET = "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"
    SHOPIFY_APP_URL = "https://py-filed-ecommerce-api.dev3.filed.com/api/v1"


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
        record = mongo_db.get_first_by_key("nonce",state)
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
        flag = 0
        with engine.connect() as conn:
            query = (
                select([cols.Name])
                        .where(cols.FiledBusinessOwnerId==user_id)
                        .limit(1)        
            )
            for row in conn.execute(query):
                try:
                    user_name = row[0]
                    flag = 1
                except Exception as e:
                    logging.exception(str(e))
        if flag == 1:
            temp_nl = user_name.split(" ", 1)
            if len(temp_nl) == 2:
                user_first_name, user_last_name = temp_nl[0], temp_nl[1]
            else:
                user_first_name, user_last_name = temp_nl[0], ""

        with engine.connect() as conn:
            ins = external_platforms.insert().values(
                CreatedAt=cls.generate_utc_aware_datestring(),
                CreatedById=user_id,
                CreatedByFirstName=user_first_name,
                CreatedByLastName=user_last_name,
                FiledBusinessOwnerId=user_id,
                PlatformId=2,
                Details=json.dumps(details)
                )
            result = conn.execute(ins)

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
    @classmethod
    def mapper(cls, data: List[dict], mapping: Dict) -> Dict[str, list]:
        """Mapping of data"""
        filed_product_list = []

        def _get_id_from_gid(gid: str) -> str:
            """Takes 'gid://shopify/Product/{ID}' and returns only the numeric string ID"""
            return gid.replace("gid://shopify/Product/", "")

        for p in data:
            node = p["node"]
            # only map active products
            if node["status"] != "ACTIVE":
                continue

            product_map = {}

            node["tags"] = ", ".join(node["tags"])

            # Added variants, so we would not add it to custom properties
            already_mapped_fields = ["variants"]

            for _map in mapping["product"]:
                if _map["filed_key"] in FiledProduct.__annotations__:
                    product_map[_map["filed_key"]] = node[_map["mapped_to"]]
                    already_mapped_fields.append(_map["mapped_to"])

            imported_at = get_utc_aware_date()

            # first we process the products
            filed_product = FiledProduct(
                product_id=_get_id_from_gid(product_map["product_id"]),
                title=product_map["title"],
                product_type=product_map["product_type"],
                description=product_map["description"],
                vendor=product_map["vendor"],
                tags=product_map["tags"],
                image_url=product_map["image_url"]["original_src"],
                # TODO: Discuss SKU auto-generation
                # SKU Format recommendations: https://help.shopify.com/en/manual/products/details/sku
                # As of now, SKU is generated by using uuid
                sku=str(uuid.uuid3(uuid.NAMESPACE_DNS, "filed.com")),
                created_at=product_map["created_at"],
                updated_at=product_map["updated_at"],
                imported_at=imported_at,
                variants=[],
                custom_props=FiledCustomProperties(
                    {field: value for field, value in node.items() if field not in already_mapped_fields}
                ),
            )

            # then we process the variants
            product_variants = [e["node"] for e in node["variants"]["edges"]]
            for pv in product_variants:
                for so in pv.pop("selected_options"):
                    pv.update({so["name"].lower(): so["value"]})

                variant_map = {"custom_fields": {}}

                for _map in mapping["variant"]:
                    if _map["filed_key"] in FiledVariant.__annotations__:
                        variant_map[_map["filed_key"]] = pv.get(_map["mapped_to"], node.get(_map["mapped_to"]))
                    else:
                        custom = {_map["filed_key"]: pv.get(_map["mapped_to"])}
                        variant_map["custom_fields"].update(custom)

                custom_props = set([prop for prop in pv.keys() if prop not in FiledVariant.__annotations__]) - {
                    "available_for_sale",
                    "title",
                    "image",
                    "id",
                    "created_at",
                    "updated_at",
                }

                for prop in custom_props:
                    variant_map["custom_fields"].update({prop: pv[prop]})

                filed_variant = FiledVariant(
                    variant_id=pv["id"][29:],  # removing "gid://shopify/ProductVariant/"
                    filed_product_id="",
                    price=variant_map["price"],
                    compare_at_price=variant_map["compare_at_price"],
                    availability=variant_map["availability"],
                    url=variant_map["url"],
                    display_name=variant_map["display_name"],
                    image_url=pv["image"]["original_src"] if pv["image"] else node["featured_image"]["original_src"],
                    sku=variant_map["sku"],
                    barcode=variant_map["barcode"],
                    inventory_quantity=variant_map["inventory_quantity"],
                    tags=variant_map["tags"],
                    description=variant_map["description"],
                    created_at=pv.get("created_at", imported_at),
                    updated_at=pv.get("updated_at"),
                    imported_at=imported_at,
                    material=pv.get("material"),
                    condition=pv.get("condition"),
                    brand=pv.get("brand"),
                    color=pv.get("color"),
                    size=pv.get("size"),
                    custom_props=FiledCustomProperties(properties=variant_map["custom_fields"])
                    if variant_map["custom_fields"]
                    else None,
                )

                filed_product.variants.append(filed_variant)

            filed_product_list.append(asdict(filed_product))

        return {"products": filed_product_list}

    @classmethod
    def get_products(cls, body):
        """Get Products data from GraphQL using pagination"""

        user_id = body["user_filed_id"]
        shop, cls.__access_token = cls.read_credentials_from_db(user_id)

        query = cls.query_get_product_list()
        res = cls.authenticated_shopify_call(shop=shop, endpoint="graphql", query=query)

        if res == cls.RESPONSE_ERROR_MESSAGE:
            return "Call to the API failed."

        product_list = res.get("data").get("products").get("edges")
        next_page = res.get("data").get("products").get("pageInfo").get("hasNextPage")
        call_count = 1

        # Now get remaining products list
        while next_page:
            query = cls.query_get_product_list(after=product_list[-1]["cursor"])
            res = cls.authenticated_shopify_call(shop=shop, endpoint="graphql", query=query)
            for el in res.get("data").get("products").get("edges"):
                product_list.append(el)
            next_page = res.get("data").get("products").get("pageInfo").get("hasNextPage")
            call_count += 1

        print(call_count)

        # Now we get each product info
        for p in product_list:
            query = cls.query_get_product_info(p["node"]["id"])
            res = cls.authenticated_shopify_call(shop=shop, endpoint="graphql", query=query)
            p["node"] = res.get("data").get("product")
            call_count += 1

        print(call_count)

        yield humps.decamelize(product_list)

    @staticmethod
    def query_get_product_list(first: int = 250, after: str = None):
        _op = Operation(shopify_schema.query_type)
        _op_products = _op.products(first=first, after=after)

        _op_products.page_info.__fields__("has_next_page")
        _op_products_cursor = _op_products.edges.cursor()
        _op_products_node = _op_products.edges.node()

        _op_products_node.id()

        return str(_op)

    @staticmethod
    def query_get_product_info(product_id: str):
        _op = Operation(shopify_schema.query_type)
        _op_products = _op.product(id=product_id)

        _op_products.__fields__(
            "id",
            "created_at",
            "description",
            "online_store_url",
            "options",
            "product_type",
            "published_at",
            "seo",
            "status",
            "tags",
            "title",
            "updated_at",
            "vendor",
        )
        _op_products.featured_image.__fields__("original_src")

        _op_products_variants = _op_products.variants(first=100)
        _op_products_variants_node = _op_products_variants.edges.node()

        _op_products_variants_node.__fields__(
            "id",
            "available_for_sale",
            "barcode",
            "compare_at_price",
            "created_at",
            "display_name",
            "inventory_quantity",
            "price",
            "selected_options",
            "sku",
            "tax_code",
            "title",
            "updated_at",
            "weight",
            "weight_unit",
        )
        _op_products_variants_node.image.__fields__("original_src")

        return str(_op)
        
    @staticmethod
    def read_credentials_from_db(user_id: str):
        with engine.connect() as conn:
            query = (
                select([ext_plat_cols.Details])
                        .where(ext_plat_cols.FiledBusinessOwnerId==user_id)
                        .where(ext_plat_cols.PlatformId==2)
                        .limit(1)        
            )
            for record in conn.execute(query):
                row = record["Details"]

            details = json.loads(row)
            return details["shop_name"], details["access_token"]