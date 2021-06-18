import json
from dataclasses import asdict
from datetime import datetime, timezone
from copy import deepcopy
from Core.Web.FacebookGraphAPI.Tools import Tools
import humps
import requests
from flask import request
import urllib.parse
from Core.Web.Security.JWTTools import decode_jwt_from_headers
from FiledEcommerce.Api.ExportIntegration.interface.ecommerce import Ecommerce

from facebook_business.adobjects.productitem import ProductItem as FacebookProductItem
from FiledEcommerce.Infrastructure.PersistanceLayer.FiledProducts.models import *

from facebook_business.adobjects.productcatalog import ProductCatalog

from Core.Web.FacebookGraphAPI.GraphAPI.GraphAPISdkBase import GraphAPISdkBase

from Core.Web.Security.JWTTools import (
    extract_business_owner_facebook_id,
    extract_user_filed_id,
)
from FiledEcommerce.Api.startup import config
from facebook_business.adobjects.business import Business
from pydantic_sqlalchemy import sqlalchemy_to_pydantic
from FiledEcommerce.Infrastructure.PersistanceLayer.FiledProducts.FiledProductsSQLRepo import (
    FiledProductsSQLRepo,
)
from FiledEcommerce.Infrastructure.PersistanceLayer.FiledProducts.FiledConstants import (
    PlatformsEnum,
)
from FiledEcommerce.Api.utils.tools.date_utils import get_utc_aware_date
from facebook_business.adobjects.user import User


class Facebook(Ecommerce):

    facebook_buisness_id = None
    errors = []
    mappings = {}
    request_json = {}
    _redirect_uri = urllib.parse.quote("https://dev3.filed.com")
    filed_business_id = None
    @classmethod
    def get_temporary_access_token_url(cls, config):
        return (
            f"https://www.facebook.com/{config.facebook.api_version}/dialog/oauth?client_id={config.facebook.app_id}"
            f"&redirect_uri={cls._redirect_uri}&state=abc&response_type=token"
        )

    @classmethod
    def _get_external_platform(cls):
        cls.filed_business_id = int(extract_user_filed_id())
        external_platform = FiledProductsSQLRepo.getExternalPlatformByFiledBussinessId(
            cls.filed_business_id, PlatformsEnum.FACEBOOK.value[1]
        )
        return external_platform
    @classmethod
    def handle(cls, request: request):
        cls.request_json = request.get_json(force=True)
        cls.facebook_buisness_id = extract_business_owner_facebook_id()
        # cls.facebook_buisness_id = cls.request_json["buisness_id"]
        external_platform = cls._get_external_platform()
        permanent_token = json.loads(external_platform.Details)["permanent_access_token"]
        _ = GraphAPISdkBase(config.facebook, permanent_token)
        cls.mappings = cls.request_json["mapping"]

    @classmethod
    def create_facebook_catalog(cls, catalog_name):
        fb_catalog = None
        try:
            business = Business(fbid=cls.facebook_buisness_id).get_business_users()
            fb_catalog = Business(
                fbid=str(business[0]["business"]["id"])
            ).create_owned_product_catalog(params={"name": catalog_name})
        except Exception as e:
            cls.errors.append(deepcopy(Tools.create_error(e, code="FB_GRAPH_API")))
        return fb_catalog

    @classmethod
    def mapper(cls):
        PydanticFiledVariants = sqlalchemy_to_pydantic(FiledVariants)

        Currencies = FiledProductsSQLRepo.getCurrencies()
        currency_map = {}
        for currency in Currencies:
            currency_map[currency.Id] = currency.Name

        products = []
        filed_set_id = cls.request_json.get("filed_set_id")
        filed_smartset_id = cls.request_json.get("filed_smartset_id")
        if filed_set_id:
            variants, set_name = FiledProductsSQLRepo.getFiledVariantsByFiledSetId(
                id=filed_set_id
            )
        elif filed_smartset_id:
            variants, set_name = FiledProductsSQLRepo.getFiledVariantsByFiledSmartSetId(
                id=filed_smartset_id
            )
        else:
            raise Exception("Please provide Filed set id or Filed smart set id")

        for variant in variants:
            single_product = {}
            pyndantic_variant = PydanticFiledVariants.from_orm(variant).dict()
            cls.filed_business_id = int(extract_user_filed_id())
            if pyndantic_variant['CreatedById'] != cls.filed_business_id:
                raise Exception("Filed set is not created by this account")
            for mapping in cls.mappings["variants"]:
                mapping = dict(mapping)
                filedKey = mapping.get("filedKey")
                mappedTo = mapping.get("mappedTo")
                pyndantic_variant_keys = pyndantic_variant.keys()
                if filedKey in pyndantic_variant_keys:
                    single_product[mappedTo] = pyndantic_variant[filedKey]
                    if mappedTo == FacebookProductItem.Field.price:
                        single_product[mappedTo] = int(pyndantic_variant[filedKey])

                    if filedKey == "Availability":
                        if int(pyndantic_variant[filedKey]) == 1:
                            single_product["availability"] = "in stock"
                        else:
                            single_product["availability"] = "out of stock"

                if mappedTo == FacebookProductItem.Field.condition:
                    single_product[mappedTo] = pyndantic_variant[filedKey] or "new"

                if mappedTo == FacebookProductItem.Field.brand:
                    single_product[
                        mappedTo
                    ] = "None"  # we don't have brand field in filed variants
            single_product[FacebookProductItem.Field.currency] = currency_map[
                variant.CurrencyId
            ]

            single_product[FacebookProductItem.Field.category] = "None"

            products.append(single_product)
        return products, set_name

    @classmethod
    def export(cls, request: request):
        cls.handle(request)
        products, catalog_name = cls.mapper()
        fb_catalog_id = cls.create_facebook_catalog(catalog_name)
        pushed_products = [
            ProductCatalog(fbid=fb_catalog_id["id"]).create_product(params=product)
            for product in products
        ]
        
        return fb_catalog_id["id"] if len(pushed_products) else f"Catalog created with id {fb_catalog_id['id']} but no products pushed to catalog"

    @classmethod
    def pre_install(cls, request: request):
        from facebook_business.exceptions import FacebookRequestError
        external_platform = cls._get_external_platform()
        if external_platform:
            permanent_token = json.loads(external_platform.Details)["permanent_access_token"]
            try:
                _ = GraphAPISdkBase(config.facebook, permanent_token)
                User("me").api_get()
                return None, permanent_token
            except FacebookRequestError:
                pass  # return the url to get the token in the last line

        return cls.get_temporary_access_token_url(config), None

    @classmethod
    def app_install(cls, request):
        cls.request_json = request.get_json(force=True)
        access_token = None
        try:
            access_token = cls.request_json["access_token"]
        except:
            pass  # skip if we already have permanent token
        if access_token:
            permanent_token = cls.get_permanent_token(
                config.facebook.app_id,
                config.facebook.app_secret,
                access_token,
            )
            details = {"permanent_access_token": permanent_token}
            now = get_utc_aware_date()
            user_id = extract_user_filed_id()
            platform_id =  PlatformsEnum.FACEBOOK.value[1]
            jwt_data = decode_jwt_from_headers()
            user_firstname = jwt_data.get("user_firstname")
            user_lastname = jwt_data.get("user_lastname")
            externalPlatform = ExternalPlatforms(
                CreatedByFirstName=user_firstname,
                CreatedByLastName=user_lastname,
                CreatedById=user_id,
                CreatedAt=now,
                FiledBusinessOwnerId=user_id,
                PlatformId=platform_id,
                Details=details,
            )
            return FiledProductsSQLRepo.createOrupdateExternalPlatform(externalPlatform)
        return 'app already installed'

    @classmethod
    def app_load(cls, request):
        pass

    @classmethod
    def app_uninstall(cls, request):
        pass

    @classmethod
    def get_permanent_token(cls, app_id, app_secret, fb_exchange_token):
        url = "https://graph.facebook.com/oauth/access_token"
        payload = {
            "grant_type": "fb_exchange_token",
            "client_id": app_id,
            "client_secret": app_secret,
            "fb_exchange_token": fb_exchange_token,
        }
        response = requests.post(url, params=payload)
        return response.json()["access_token"]
