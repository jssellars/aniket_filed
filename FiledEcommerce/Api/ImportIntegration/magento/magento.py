import re
import requests
import json, logging, base64, hashlib
import http.client
from datetime import datetime, timezone
from urllib.parse import urlparse 
from flask import request
import requests
import jwt
from sgqlc.types import Enum, non_null, Arg, String, Float, Type, Int, Field, list_of, Boolean, ArgDict ,Interface, Union, Input, Schema
from FiledEcommerce.Api.utils.models.filed_model import FiledProduct, FiledVariant, FiledCustomProperties
from requests.exceptions import HTTPError
from sgqlc.operation import Operation
from Core.Web.Security.JWTTools import decode_jwt_from_headers
from FiledEcommerce.Api.ImportIntegration.interface.ecommerce import Ecommerce
from FiledEcommerce.Infrastructure.PersistanceLayer.EcommerceMongoRepository import EcommerceMongoRepository
from FiledEcommerce.Infrastructure.PersistanceLayer.EcommerceSQL_ORM_Model import engine, ext_plat_cols, cols, external_platforms
from FiledEcommerce.Api.ImportIntegration.magento.graphql import MagentoQuery
from FiledEcommerce.Api.ImportIntegration.magento.graphql import ConfigurableProduct

class Magento(Ecommerce):
    RESPONSE_ERROR_MESSAGE = {"error": "Something went wrong!"}
    RESPONSE_ERROR_MESSAGE_NOT_FOUND = {"error": "No Record Found"}
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
        flag = 0
        with engine.connect() as conn:
            query = (
                select([ext_plat_cols.Details])
                        .where(ext_plat_cols.FiledBusinessOwnerId==user_id)
                        .where(ext_plat_cols.PlatformId==5)
                        .limit(1)        
            )
            for row in conn.execute(query):
                try:
                    details = json.loads(row["Details"])
                    token = details.get("token") 
                    flag = 1
                except Exception as e:
                    raise e
        if flag == 1:
            return token
        else:
            return ""


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
                PlatformId=5,
                Details=json.dumps(deets)
                )
            result = conn.execute(ins)
    @classmethod
    def mapper(cls, data, mapping):
        # data : user_id 
        """ Calls the function to map the product data to the filed model. 
            Args:
                data (list):#list of products
            Calls:
                map_data(mapper,variants_mapper, host_url) : Maps the product data + Variants data to the Filed Model considering the given mapping from FE.
            Returns:
                mapped_data (List[FiledProduct]): list of data as FiledProduct.
        """  
        mapped_ob = mapping["mapping"]["product"]
        variant_mapped_ob = mapping["mapping"]["variant"]
        mapped_data = cls.map_data(mapped_ob, variant_mapped_ob, data)
        return mapped_data
        
    @classmethod
    def get_products(cls, body):
        """ Calls the get_products_helper to get product information page by page. 
            Args:
                body (dict) : user_id
            Calls:
                read_token_from_db(host_url,store_code) : reads the token from the db for a given host_url or store_code.
                get_products_helper(host_url) : gets the product information.
            Returns:
                filed_ob_list (List[FiledProduct]): list of data as FiledProduct.
        """
        user_id = body.get("user_filed_id")
        details = cls.read_token_from_db(user_id)
        host_url = details["host_url"]
        store_code = details["store_code"]
        token = details["token"]

        #host_url = "ec2-44-192-108-29.compute-1.amazonaws.com:8002"
        #store_code = "default"
        #token = "3a9vlgjl5zy44y09hnizblpin8f3cyzo" 
        
        if token == "":
            return "Sorry, App not Installed cannot resolve Token"
        else:
            products = []
            response = cls.get_products_helper(token, host_url, current_page = 1)
            products.append(response)
            total_pages = response["data"]["products"]["page_info"]["total_pages"]
            current_page = 2
            while current_page <= total_pages:
                response = cls.get_products_helper(token, host_url , current_page)
                products.append(response)
                current_page += 1
        return products

    @classmethod
    def get_query(cls, current_page: int):
        """ Returns the GraphQL query as str for retrieving the products. 
            Args:
                current_page (int): For generating query for current_page.
            Calls:
                change_case(str(query)) : for changing the case of query.
            Returns:
                replaced (str): String as graphql query.
        """        
        query = Operation(MagentoQuery)
        query.products(filter= {}, pageSize = 3, currentPage = current_page)
        query.products.total_count
        query.products.items.__fields__()
        query.products.items.categories.__fields__()
        query.products.items.categories.breadcrumbs.__fields__()
        query.products.items.description.__fields__()
        query.products.items.short_description.__fields__()
        query.products.items.image.__fields__()
        query.products.items.price.regularPrice.amount.__fields__()
        query.products.items.price.maximalPrice.amount.__fields__()
        query.products.items.price.minimalPrice.amount.__fields__()
        query.products.items.small_image.__fields__()
        query.products.items.thumbnail.__fields__()
        query.products.items.__as__(ConfigurableProduct).configurable_options()
        query.products.items.__as__(ConfigurableProduct).variants()
        query.products.page_info.__fields__()
        #print(str(query))
        return str(query)


    @classmethod
    def get_products_helper(cls, token: str, host_url: str , current_page: int):    #get_Products
        """ Gets all the products Info for the called query. 
            Args:
                token (str): Admin access token.
                host_url (str): Url of the store(ex: www.abcstore.com).
                current_page (int): For getting the products info for current_page.
            Calls:
                get_query(current_page) : To get the query for particular current_page.
            Returns:
                response.json() : products information from graphql query.
        """
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {token}',
        }
        query = cls.get_query(current_page)
        payload = {"query": f'{query}'}
        payload = json.dumps(payload)
        req_url = f"http://{host_url}/graphql"
        response = requests.post(req_url, data = payload, headers = headers) 
        return response.json()

    @classmethod
    def map_data(cls, mapper, variants_mapper, data):                
        """ Maps the product data to the filed model. 
            Args:
                mapper (dict): key value of filed attribute, ecommerce attribute.
                variants_mapper (dict) : key value of filed attribute, ecommerce variant attribute.
                host_url (str): Url of the store(ex: www.abcstore.com).
            Calls:
                get_products(body) : gets the product information.
            Returns:
                filed_ob_list (List[FiledProduct]): list of data as FiledProduct.
        """
        imported_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat()[:-6] + 'Z'
        filed_product_list = []
        products = data                 # one page of products
        for item in products["data"]["products"]["items"]:
            df = {}
            #print(item)
            for _map in mapper:
                if _map["filed_key"] in FiledProduct.__annotations__:
                    df[_map["filed_key"]] = item[_map["mapped_to"]]
            
            pr = FiledProduct(
                product_id=item["id"],
                title=item["name"],
                product_type=", ".join([category["name"] for category in item["categories"]]),
                vendor="Dummy-Magento-Shop",
                description=item["description"]["html"],
                tags=item["meta_keyword"],
                sku=item["sku"],
                image_url=item["image"]["url"],
                created_at=item["created_at"],
                updated_at=item["updated_at"],
                imported_at=imported_at,
                brand="",
                availability=True if item["stock_status"] == "IN_STOCK" else False,
                variants=[]               
            )

            if item["__typename"] == "ConfigurableProduct": 
                for variant_item in item["variants"]["product"]:
                    vdf = {
                        "custom_fields": {}
                    }
                    for _map in variants_mapper:
                        if _map["filed_key"] in FiledProduct.__annotations__:
                            vdf[_map["filed_key"]] = variant_item[_map["mapped_to"]]
                        else:
                            custom = {_map["filed_key"]: variant_item.get(_map["mapped_to"])}
                            vdf["custom_fields"].update(custom)

                    vr = FiledVariant(
                        variant_id=variant_item["id"],
                        filed_product_id=item["id"],
                        display_name=variant_item["name"],
                        price=variant_item["price"]["regularPrice"]["amount"]["value"],  
                        compare_at_price="", 
                        availability=True if variant_item["stock_status"] == "IN_STOCK" else False,
                        url=variant_item["canonical_url"],
                        image_url=variant_item["image"]["url"],
                        sku=variant_item["sku"],
                        barcode="",
                        inventory_quantity="",
                        tags=variant_item["meta_keyword"],
                        description=variant_item["description"]["html"],
                        created_at=variant_item["created_at"],
                        updated_at=variant_item["updated_at"],
                        imported_at=imported_at,
                        material="",
                        condition="",
                        color="",
                        size="",
                        custom_props=FiledCustomProperties(
                            properties=vdf["custom_fields"]
                        )if vdf["custom_fields"] else None
                    )
                    pr.variants.append(vr)
            filed_product_list.append(pr.__dict__)
        return filed_product_list