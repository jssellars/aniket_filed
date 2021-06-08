import http.client
import json
from dataclasses import asdict
from datetime import datetime, timezone

import humps
from flask import request
from sgqlc.operation import Operation

from Core.Web.Security.JWTTools import decode_jwt_from_headers
from FiledEcommerce.Api.ImportIntegration.bigcommerce.graphql import Query
from FiledEcommerce.Api.ImportIntegration.interface.ecommerce import Ecommerce
from FiledEcommerce.Api.utils.models.filed_model import FiledCustomProperties, FiledProduct, FiledVariant
from FiledEcommerce.Infrastructure.PersistanceLayer.EcommerceMongoRepository import EcommerceMongoRepository
from FiledEcommerce.Infrastructure.PersistanceLayer.EcommerceSQL_ORM_Model import engine, ext_plat_cols, cols, external_platforms


class BigCommerce(Ecommerce):
    client_id = "gzmqgnkolrpn1ymywjzrsbr9z8jnbxw"
    client_secret = "75ff5362495a9a720f4de0e737092cd5be4aaf2efdf1751c263c73cb8bcc5bb9"
    callback_url = "http://localhost:3000/oauth/bigcommerce/install"

    __marketplace_url = "https://store-pzuk9w46gs.mybigcommerce.com/manage/marketplace/apps/my-apps/drafts"
    __filed_ecom_url = "https://localhost:4200/#/catalog/ecommerce"

    @classmethod
    def pre_install(cls):
        data = request.args
        token_data = decode_jwt_from_headers()
        email = data.get("email")
        user_id = token_data.get("user_filed_id")

        mongo_db = EcommerceMongoRepository()
        mongo_db.add_one({"email": email, "userId": user_id})

        return cls.__marketplace_url

    @classmethod
    def app_install(cls):
        body = request.args
        code = body.get("code")
        context = body.get("context")
        scope = body.get("scope")

        print(code)
        print(context)
        print(scope)

        store_hash = context.split("/")[1]
        token_response = cls.get_access_token(code=code, context=context, scope=scope)
        print(token_response)

        access_token = token_response.get("access_token")
        user = token_response.get("user")
        email = user.get("email")
        storefront_token = cls.get_storefront_token(access_token=access_token, store_hash=store_hash)
        print(storefront_token)

        mongo_db = EcommerceMongoRepository()
        data = mongo_db.get_first_by_key("email", email)
        print(data)

        user_id = data.get("userId")
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

        return cls.__filed_ecom_url

    @classmethod
    def app_load(cls):
        pass

    @classmethod
    def app_uninstall(cls):
        pass

    @classmethod
    def get_access_token(cls, code, context, scope):
        conn = http.client.HTTPSConnection("login.bigcommerce.com")

        headers = {"Content-Type": "application/json"}
        payload = {
            "client_id": cls.client_id,
            "client_secret": cls.client_secret,
            "code": code,
            "context": context,
            "scope": scope,
            "grant_type": "authorization_code",
            "redirect_uri": cls.callback_url,
        }

        conn.request("POST", "/oauth2/token", json.dumps(payload), headers)

        raw_data = conn.getresponse()
        data = raw_data.read()
        response = json.loads(data.decode("utf-8"))

        return response

    @classmethod
    def get_storefront_token(cls, access_token, store_hash):
        conn = http.client.HTTPSConnection("api.bigcommerce.com")

        headers = {"Content-Type": "application/json", "Accept": "application/json", "X-Auth-Token": access_token}

        payload = {"channel_id": 1, "expires_at": 1643622707}

        conn.request("POST", f"/stores/{store_hash}/v3/storefront/api-token", json.dumps(payload), headers)

        raw_data = conn.getresponse()
        data = raw_data.read()
        response = json.loads(data.decode("utf-8"))

        return response["data"]["token"]

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

        print(details)
        data = json.loads(details)
        token = data["storefront_token"]
        store_hash = data["store_hash"]

        headers = {"Content-Type": "application/json", "Authorization": f"Bearer {token}"}

        after = None
        conn = http.client.HTTPSConnection(f"store-{store_hash}.mybigcommerce.com")

        while True:
            query = cls.get_query(after=after)
            payload = {"query": str(query)}

            conn.request("POST", "/graphql", json.dumps(payload), headers)
            res = conn.getresponse()
            data = res.read()

            json_data = json.loads(data.decode("utf-8"))
            print(json_data)
            if not json_data["data"]["site"]["products"]["pageInfo"]["hasNextPage"]:
                break

            after = json_data["data"]["site"]["products"]["pageInfo"]["endCursor"]
            yield humps.decamelize(json_data)

    @classmethod
    def mapper(cls, data, mapping):
        products_list = []
        imported_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat()[:-6] + "Z"

        edge = data["data"]["site"]["products"]["edges"]

        for product in edge:
            df = {}
            node = product["node"]
            for _map in mapping.get("product"):
                if _map["filed_key"] in FiledProduct.__annotations__:
                    df[_map["filed_key"]] = node[_map["mapped_to"]]

            pr = FiledProduct(
                product_id=node["entity_id"],
                title=node["name"],
                product_type=node["type"],
                vendor="Dummy-BC-Shop",
                description=node["plain_text_description"],
                tags=",".join([tag["node"]["name"] for tag in node["categories"]["edges"]]),
                sku=node["sku"],
                brand=node["brand"],
                availability=True,
                image_url=node["default_image"]["url"],
                created_at=imported_at,
                updated_at=imported_at,
                imported_at=imported_at,
                variants=[],
            )

            for variant in node["variants"]["edges"]:
                vdf = {"custom_fields": {}}
                vnode = variant["node"]
                for _map in mapping.get("variant"):
                    if _map["filed_key"] in FiledProduct.__annotations__:
                        vdf[_map["filed_key"]] = node[_map["mapped_to"]]
                    else:
                        custom = {_map["filed_key"]: node.get(_map["mapped_to"])}
                        vdf["custom_fields"].update(custom)

                vr = FiledVariant(
                    variant_id=vnode["entity_id"],
                    filed_product_id="",
                    display_name=node["name"],
                    price=vnode["prices"]["price"]["value"],  # Change to sale price
                    compare_at_price=vnode["prices"]["price"]["value"],  # Change to base price
                    availability=True,
                    url=node["add_to_cart_url"],
                    image_url=node["default_image"]["url"],
                    sku=vnode["sku"],
                    barcode="",
                    inventory_quantity=vnode["inventory"],
                    tags=",".join([tag["node"]["name"] for tag in node["categories"]["edges"]]),
                    description=node["plain_text_description"],
                    created_at=imported_at,
                    updated_at=imported_at,
                    imported_at=imported_at,
                    material="",
                    condition="",
                    color="",
                    size="",
                    custom_props=FiledCustomProperties(properties=vdf["custom_fields"])
                    if vdf["custom_fields"]
                    else None,
                )
                pr.variants.append(vr)

            products_list.append(asdict(pr))

        return {"products": products_list}
