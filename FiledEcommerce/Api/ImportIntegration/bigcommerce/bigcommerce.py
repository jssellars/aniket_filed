import json
from dataclasses import asdict
from datetime import datetime

import humps
import requests
from flask import request
from sgqlc.operation import Operation

from Core.Web.Security.JWTTools import decode_jwt_from_headers
from FiledEcommerce.Api.ImportIntegration.bigcommerce.graphql import Query
from FiledEcommerce.Api.ImportIntegration.interface.ecommerce import Ecommerce
from FiledEcommerce.Api.utils.models.filed_model import FiledCustomProperties, FiledProduct, FiledVariant
from FiledEcommerce.Api.utils.tools.date_utils import get_utc_aware_date
from FiledEcommerce.Infrastructure.CurrencyEnum import CurrencyEnum
from FiledEcommerce.Infrastructure.PersistanceLayer.EcommerceMongoRepository import EcommerceMongoRepository
from FiledEcommerce.Infrastructure.PersistanceLayer.EcommerceSQL_ORM_Model import *


class BigCommerce(Ecommerce):
    client_id = "gzmqgnkolrpn1ymywjzrsbr9z8jnbxw"
    client_secret = "75ff5362495a9a720f4de0e737092cd5be4aaf2efdf1751c263c73cb8bcc5bb9"
    # callback_url = "http://localhost:47650/api/v1/oauth/bigcommerce/install"
    callback_url = "https://py-filed-ecommerce-api.dev3.filed.com/api/v1/oauth/bigcommerce/install"
    __marketplace_url = "https://store-pzuk9w46gs.mybigcommerce.com/manage/marketplace/apps/my-apps/drafts"

    @classmethod
    def get_redirect_url(cls, test_flg):
        return (
            "https://localhost:4200/#/catalog/ecommerce"
            if test_flg == 1
            else "https://ecommerce.filed.com/#/catalog/ecommerce"
        )

    @classmethod
    def pre_install(cls):
        data = request.args
        token_data = decode_jwt_from_headers()
        email = data.get("email")
        user_id = token_data.get("user_filed_id")
        if request.host.startswith("localhost") or request.host.startswith("127.0.0.1"):
            test_flg = 1 
        else: 
            test_flg = 0
        mongo_db = EcommerceMongoRepository()
        mongo_db.add_one({"email": email, "user_id": user_id, "test": test_flg})

        return "true" , cls.__marketplace_url

    @classmethod
    def app_install(cls):
        body = request.args
        code = body.get("code")
        context = body.get("context")
        scope = body.get("scope")

        store_hash = context.split("/")[1]
        token_response = cls.get_access_token(code=code, context=context, scope=scope)

        access_token = token_response.get("access_token")
        user = token_response.get("user")
        email = user.get("email")
        storefront_token = cls.get_storefront_token(access_token=access_token, store_hash=store_hash)

        mongo_db = EcommerceMongoRepository()
        data = mongo_db.get_first_by_key("email", email)

        user_id = data.get("user_id")
        deets = {
            "access_token": access_token,
            "storefront_token": storefront_token,
            "store_hash": store_hash,
            "scope": scope,
            "store_email": email,
        }
        flag = 0
        with engine.connect() as conn:
            query = select([cols.Name]).where(cols.FiledBusinessOwnerId == user_id).limit(1)
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
                PlatformId=4,
                Details=json.dumps(deets),
            )
            result = conn.execute(ins)
        test_flg = data.get("test")
        mongo_db.delete_many({"email": email})
        return cls.get_redirect_url(test_flg)

    @classmethod
    def app_load(cls):
        pass

    @classmethod
    def app_uninstall(cls):
        with engine.connect() as conn:
            query = external_platforms.delete().where(ext_plat_cols.FiledBusinessOwnerId == 105).where(ext_plat_cols.PlatformId == 4).limit(1)
            conn.execute(query) #TODO: change 105 to user_id
        return 200

    @classmethod
    def get_access_token(cls, code, context, scope):
        url = "https://login.bigcommerce.com/oauth2/token"

        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        payload = {
            "client_id": cls.client_id,
            "client_secret": cls.client_secret,
            "code": code,
            "context": context,
            "scope": scope,
            "grant_type": "authorization_code",
            "redirect_uri": cls.callback_url,
        }

        data = requests.post(url, data=payload, headers=headers)
        return data.json()

    @classmethod
    def get_storefront_token(cls, access_token, store_hash):
        url = f"https://api.bigcommerce.com/stores/{store_hash}/v3/storefront/api-token"
        headers = {"Content-Type": "application/json", "X-Auth-Token": access_token}
        payload = {"channel_id": 1, "expires_at": 1624127400, "allowed_cors_origins": ["http://localhost:4200"]}

        data = requests.post(url, data=json.dumps(payload), headers=headers)
        return data.json()["data"]["token"]

    @classmethod
    def get_query(cls, after: str):
        query = Operation(Query)
        query.site.products(first=10, after=after)
        query.site.products.__fields__()
        query.site.products.edges.node.__fields__()
        query.site.products.edges.node.options.edges.node.__fields__()
        query.site.products.edges.node.categories.edges.node.__fields__()
        query.site.products.edges.node.customFields.edges.node.__fields__()
        query.site.products.edges.node.brand.__fields__()
        query.site.products.edges.node.defaultImage.url(width=1280)
        query.site.products.edges.node.brand.defaultImage.url(width=1280)
        query.site.products.edges.node.categories.edges.node.defaultImage.url(width=1280)
        query.site.products.edges.node.variants.edges.node.defaultImage.url(width=1280)
        query.site.products.edges.node.variants.edges.node.__fields__()
        query.site.products.edges.node.variants.edges.node.options.edges.node.__fields__()
        query.site.products.edges.node.variants.edges.node.inventory.byLocation.edges.node.__fields__()
        query.site.products.edges.node.variants.edges.node.inventory.__fields__()
        query.site.products.edges.node.variants.edges.node.prices.salePrice.__fields__()
        query.site.products.edges.node.variants.edges.node.prices.basePrice.__fields__()
        query.site.settings.storeName()
        return query

    @classmethod
    def get_products(cls, body):
        user_id = body.get("user_filed_id")

        with engine.connect() as conn:
            query = (
                select([ext_plat_cols.Details])
                .where(ext_plat_cols.FiledBusinessOwnerId == user_id)
                .where(ext_plat_cols.PlatformId == 4)
                .limit(1)
            )
            for record in conn.execute(query):
                details = record["Details"]

        data = json.loads(details)
        token = data["storefront_token"]
        store_hash = data["store_hash"]

        headers = {"Content-Type": "application/json", "Authorization": f"Bearer {token}"}

        after = None
        url = f"https://store-{store_hash}.mybigcommerce.com/graphql"

        while True:
            query = cls.get_query(after=after)
            payload = {"query": str(query)}

            data = requests.post(url, data=json.dumps(payload), headers=headers)

            json_data = data.json()
            if not json_data["data"]["site"]["products"]["pageInfo"]["hasNextPage"]:
                break

            after = json_data["data"]["site"]["products"]["pageInfo"]["endCursor"]
            yield humps.decamelize(json_data)

    @classmethod
    def mapper(cls, data, mapping):
        products_list = []
        imported_at = get_utc_aware_date()

        def _get_tags(mapped_data):
            if isinstance(mapped_data, dict):
                # tags is mapped to categories object as default
                return ",".join([tag["node"]["name"] for tag in mapped_data["tags"]["edges"]])
            elif isinstance(mapped_data, str):
                return mapped_data
            elif isinstance(mapped_data, list):
                return ",".join(mapped_data)
            else:
                return ""

        def _get_store_name(data: dict):
            try:
                store_name = data["data"]["site"]["settings"]["store_name"]
            except (KeyError, TypeError):
                return ""
            else:
                return store_name

        edge = data["data"]["site"]["products"]["edges"]
        already_mapped_fields = {"variants"}

        for product in edge:
            df = {}
            node = product["node"]
            for _map in mapping.get("product"):
                if _map["filed_key"] in FiledProduct.__annotations__:
                    try:
                        df[_map["filed_key"]] = node[_map["mapped_to"]]
                    except KeyError:
                        continue
                    else:
                        already_mapped_fields.add(_map["mapped_to"])

            currency_code = next(money["currency_code"] for money in node["prices"].values() if money)

            pr = FiledProduct(
                product_id=df["product_id"],
                title=df["title"],
                product_type=df["product_type"],
                vendor=_get_store_name(data),
                description=df["description"],
                tags=_get_tags(df) if df.get("tags") else "",
                sku=df["sku"],
                brand=df["brand"]["name"] if df.get("brand") else None,
                availability=True,
                image_url=df["image_url"]["url"] if df.get("image_url") else None,
                created_at=imported_at,
                updated_at=imported_at,
                imported_at=imported_at,
                variants=[],
                custom_props=FiledCustomProperties(
                    properties={field: value for field, value in node.items() if field not in already_mapped_fields}
                ),
            )

            for variant in node["variants"]["edges"]:
                vdf = {"custom_fields": {}}
                vnode = variant["node"]
                for _map in mapping.get("variant"):
                    filed_key = _map["filed_key"]
                    mapped_to = _map["mapped_to"]
                    if filed_key in {"tags", "display_name", "description", "url"}:
                        continue
                    if filed_key in {"price", "compare_at_price"}:
                        vdf[filed_key] = vnode["prices"][mapped_to]
                    elif filed_key in FiledVariant.__annotations__:
                        try:
                            vdf[filed_key] = vnode[mapped_to]
                        except KeyError:
                            continue
                    else:
                        custom = {filed_key: vnode.get(mapped_to)}
                        vdf["custom_fields"].update(custom)

                vr = FiledVariant(
                    variant_id=vdf["variant_id"],
                    filed_product_id="",
                    display_name=node["name"],
                    price=vdf["price"]["value"] if vdf.get("price") else None,
                    compare_at_price=vdf["compare_at_price"]["value"] if vdf.get("compare_at_price") else None,
                    availability=True,
                    url=node["add_to_cart_url"],
                    image_url=vdf["image_url"]["url"] if vdf.get("image_url") else pr.image_url,
                    sku=vnode["sku"],
                    barcode="",
                    inventory_quantity=vnode["inventory"],
                    tags=_get_tags(df) if df.get("tags") else "",
                    description=df["description"],
                    created_at=imported_at,
                    updated_at=imported_at,
                    imported_at=imported_at,
                    currency_id=CurrencyEnum[currency_code].value,
                    material=vdf.get("material", ""),
                    condition=vdf.get("condition", ""),
                    color=vdf.get("color", ""),
                    size=vdf.get("size", ""),
                    custom_props=FiledCustomProperties(properties=vdf.get("custom_fields")),
                )
                # Set image_url of product to variant if no product image
                if not pr.image_url:
                    pr.image_url = vr.image_url

                pr.variants.append(vr)
            products_list.append(asdict(pr))

        return {"products": products_list}
