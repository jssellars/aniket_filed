import http.client
import json
from datetime import datetime

from flask import request

from Core.Web.Security.JWTTools import decode_jwt_from_headers
from FiledEcommerce.Api.ImportIntegration.interface.ecommerce import Ecommerce
from FiledEcommerce.Infrastructure.PersistanceLayer.EcommerceMongoRepository import EcommerceMongoRepository
from FiledEcommerce.Infrastructure.PersistanceLayer.EcommerceSQLRepository import SqlManager


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
                "INSERT INTO ExternalPlatforms(CreatedAt, CreatedById, CreatedByFirstName, CreatedByLastName, FiledBusinessOwnerId, PlatformId, Details) VALUES(?, ?, ?, ?, ?, ?, ?)",
                datetime.now(),
                user_id,
                user_first_name,
                user_last_name,
                user_id,
                4,
                json.dumps(deets),
            )
            cursor.commit()

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
