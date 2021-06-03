import http.client
import json
from datetime import datetime
from flask import request
import requests
import jwt
from Core.Web.Security.JWTTools import decode_jwt_from_headers
from FiledEcommerce.Api.ImportIntegration.interface.ecommerce import Ecommerce
from FiledEcommerce.Infrastructure.PersistanceLayer.EcommerceMongoRepository import EcommerceMongoRepository
from FiledEcommerce.Infrastructure.PersistanceLayer.EcommerceSQLRepository import SqlManager

class Magento(Ecommerce):
    RESPONSE_ERROR_MESSAGE = {"error": "Something went wrong!"}
    __filed_ecom_url = "https://dev3.filed.com/#/catalog/ecommerce"

    @classmethod
    def app_load(cls):
        # request_query_params:  user_id
        """ Checks the Install with the value stored in db.
            Args:
                body (dict): Has user_id 
            Calls:
                cls.read_token_from_db(host_url) : read the token from database.
            Returns:
                "You already have this app", 202
        """
        body = request.args
        token_data = decode_jwt_from_headers()
        user_id = token_data["user_filed_id"]
        try:
            if cls.read_token_from_db(user_id) != "":
                return cls.__filed_ecom_url
        except Exception as e:
            raise e

    @classmethod
    def pre_install(cls):
        """ Verifies the store calling the store_info_resolver, calls the get_token function, calls the write_token_to_db.
            Args:
                data (dict): Holds value for email, user_id, host_url, username, password.
            Calls:
                get_token(host_url, username, password) : To get the Admin Access Token as str.
                store_info_resolver(host_url, token) : To get the store information for the given host_url.
                write_token_to_db(host_url, store_code, token): To write the generated Admin Access token into db.
            Returns:
                Success
        """ 
        data = request.args
        email = data.get("email")
        token_data = decode_jwt_from_headers()
        user_id = token_data["user_filed_id"]
        host_url = data.get("host_url")
        username = data.get("username")
        password = data.get("password")
        mongo_db = EcommerceMongoRepository()
        mongo_db.add_one({"host_url": host_url, "email": email, "user_id": user_id})
        body = {"host_url": host_url, "username": username, "password": password}
        return cls.app_install_helper(body)

    @classmethod
    def app_install_helper(cls, body):
        """
        """
        host_url =  body.get("host_url")
        username = body.get("username")
        password = body.get("password")

        try:
            token = cls.get_token(host_url, username, password)
            store_response = cls.store_info_resolver(host_url, token)
            if not store_response:
                return "Sorry! No Store Found"
            else:
                store_code = "default"
                mongo_db = EcommerceMongoRepository()
                data = mongo_db.get_first_by_key("host_url",host_url)
                deets = {
                    "token" : token,
                    "store_code" : store_code,
                    "host_url" : host_url
                }
                cls.write_token_to_db(deets, data)
                return cls.__filed_ecom_url
        except Exception as e:
            raise e

    @classmethod
    def app_install(cls):
        """ Install the app and calls get_token, store_info_resolver, write_token_to_db
            Args:
                body (dict): Holds value for host_url, username, password. 
            Calls:
                get_token(host_url, username, password) : To get the Admin Access Token as str.
                store_info_resolver(host_url, token) : To get the store information for the given host_url.
                write_token_to_db(host_url, store_code, token): To write the generated Admin Access token into db.
            Returns:
                cls.__filed_ecom_url
        """ 
        body = request.args
        host_url =  body.get("host_url")
        username = body.get("username")
        password = body.get("password")

        try:
            token = cls.get_token(host_url, username, password)
            store_response = cls.store_info_resolver(host_url, token)
            if not store_response:
                return "Sorry! No Store Found"
            else:
                store_code = "default"
                mongo_db = EcommerceMongoRepository()
                data = mongo_db.get_first_by_key("host_url", host_url)
                deets = {
                    "token" : token,
                    "store_code" : store_code,
                    "host_url" : host_url
                }
                cls.write_token_to_db(deets, data)
                return cls.__filed_ecom_url
        except Exception as e:
            raise e

    @classmethod
    def app_uninstall(cls):
        # Delete Token from the db 
        pass

    @classmethod
    def store_info_resolver(cls, host_url: str, token: str):
        """ Retrieve the Store Information for a Magento Account.
            Args:
                host_url (str): Url of the store(ex: www.abcstore.com).
                username (str): Admin username of the store.
                password (str): Admin password of the store.
            Returns:
                result (list): list of store information as dict with (key, value) as (base_url, code)
        """
        result = []
        headers = {
            'accept': 'application/json',
            'Authorization': f'Bearer {token}',
        }
        response = requests.get(f"http://{host_url}/rest/all/V1/store/storeConfigs", headers=headers)
        if response.status_code == 200:
            for store in response.json():
                k ={store["base_url"]:store["code"]}
            result.append(k)
        return result

    @classmethod
    def get_token(cls, host_url: str ,username: str, password: str) -> str:     
        """ Retrieve the access token from Magento Admin. 
            Args:
                host_url (str): Url of the store(ex: www.abcstore.com).
                username (str): Admin username of the store.
                password (str): Admin password of the store.
            Returns:
                response.json(): Access Token as string
        """
        headers = {
            'accept': 'application/json',
            'Content-Type': 'application/json',
        }
        #data = '{ "username": "admin", "password": "anuranjan007@"}'

        data = {"username": f"{username}", "password": f"{password}"}
        data = json.dumps(data)
        token_url = f"http://{host_url}/rest/all/V1/integration/admin/token"
        
        response = requests.post(token_url, data=data, headers=headers)
        return response.json()

    @staticmethod
    def read_token_from_db(user_id):
        """ Reads the token from the db
            Args:
                user_id: user_id
            Calls:
                None
            Returns:
                returns row of db as json 
        """
        with SqlManager() as cursor:
            cursor.execute("SELECT Details FROM ExternalPlatforms WHERE FiledBusinessOwnerId = ? AND PlatformId = ?", user_id, 5)
            row = cursor.fetchval()
        if not json.loads(row):
            return ""
        else:
            return json.loads(row)


    @staticmethod
    def write_token_to_db(deets: dict, data):
        """ Writes the token to the db
            Args:
                deets (dict) : deets having email, token , username, password etc
                data (dict) : user_id
            Calls:
                None
            Returns:
                None
        """
        user_id = data.get("user_id")
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
                5,
                json.dumps(deets)
            )
            cursor.commit()