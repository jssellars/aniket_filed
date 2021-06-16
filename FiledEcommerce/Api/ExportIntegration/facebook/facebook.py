import json
from dataclasses import asdict
from datetime import datetime, timezone
from copy import deepcopy
from Core.Web.FacebookGraphAPI.Tools import Tools
import humps
import requests
from flask import request
from sgqlc.operation import Operation
import urllib.parse
from Core.Web.Security.JWTTools import decode_jwt_from_headers
from FiledEcommerce.Api.ExportIntegration.interface.ecommerce import Ecommerce

from FiledEcommerce.Api.utils.models.filed_model import (
    FiledCustomProperties,
    FiledProduct,
    FiledVariant,
)
from facebook_business.adobjects.productitem import ProductItem as FacebookProductItem
from FiledEcommerce.Infrastructure.PersistanceLayer.FiledProducts.models import *

from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.productcatalog import ProductCatalog

from Core.Web.FacebookGraphAPI.GraphAPI.GraphAPISdkBase import GraphAPISdkBase

from Core.Web.Security.JWTTools import extract_business_owner_facebook_id
from FiledEcommerce.Api.startup import config, fb_fixtures
from facebook_business.adobjects.business import Business
from pydantic_sqlalchemy import sqlalchemy_to_pydantic
from FiledEcommerce.Infrastructure.PersistanceLayer.FiledProducts.FiledProductsSQLRepo import (
    FiledProductsSQLRepo,
)


class Facebook(Ecommerce):

    facebook_buisness_id = None
    errors = []
    mappings = {}
    request_json = {}
    _redirect_uri = urllib.parse.quote("https://dev3.filed.com")

    @classmethod
    def get_temporary_access_token_url(cls, config):
        return (
            f"https://www.facebook.com/{config.facebook.api_version}/dialog/oauth?client_id={config.facebook.app_id}"
            f"&redirect_uri={cls._redirect_uri}&state=abc&response_type=token"
        )

    @classmethod
    def handle(cls, request: request):
        cls.request_json = request.get_json(force=True)
        cls.facebook_buisness_id = extract_business_owner_facebook_id()
        # cls.facebook_buisness_id = cls.request_json["buisness_id"]
        permanent_token = cls.get_permanent_token(
            config.facebook.api_version,
            config.facebook.app_secret,
            cls.request_json["access_token"],
        )
        print(permanent_token)
        #we will refactor this later, once everything is up and running
        # permanent_token = fb_fixtures.business_owner_repository.get_permanent_token(
        #     cls.facebook_buisness_id
        # )
        _ = GraphAPISdkBase(config.facebook, permanent_token)
        cls.mappings = cls.request_json["mappings"]

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
        PydanticFiledCurrencies = sqlalchemy_to_pydantic(Currencies)

        products = []
        filed_set_id = cls.request_json["filed_set_id"]
        variants, set_name = FiledProductsSQLRepo.getFiledVariantsByFiledSetId(
            id=int(filed_set_id)
        )
        for variant in variants:
            single_product = {}
            pyndantic_variant = PydanticFiledVariants.from_orm(variant).dict()
            for mapping in cls.mappings["variants"]:
                mapping = dict(mapping)
                filedKey = mapping.get("filedKey")
                mappedTo = mapping.get("mappedTo")
                pyndantic_variant_keys = pyndantic_variant.keys()
                if filedKey in pyndantic_variant_keys:
                    single_product[mappedTo] = pyndantic_variant[filedKey]
                    if mappedTo == "price":
                        single_product[mappedTo] = int(pyndantic_variant[filedKey])

                    if filedKey == "Availability":
                        if int(pyndantic_variant[filedKey]) == 1:
                            single_product["availability"] = "in stock"
                        else:
                            single_product["availability"] = "out of stock"

                if mappedTo == FacebookProductItem.Field.Condition:
                    single_product[mappedTo] = pyndantic_variant[filedKey] or "new"

                if mappedTo == FacebookProductItem.Field.brand:
                    single_product[
                        mappedTo
                    ] = "Facebook"  # we don't have brand field in filed variants
            single_product[
                FacebookProductItem.Field.currency
            ] = PydanticFiledCurrencies["Name"]

            products.append(single_product)
        return products, set_name

    @classmethod
    def export(cls, request: request):
        cls.handle(request)
        products, catalog_name = cls.mapper()
        fb_catalog_id = cls.create_facebook_catalog(catalog_name)
        product_catalogs = [
            ProductCatalog(fbid=fb_catalog_id["id"]).create_product(params=product)
            for product in products
        ]
        return product_catalogs, cls.errors

    @classmethod
    def pre_install(cls, request: request):
        return cls.get_temporary_access_token_url(config)

    @classmethod
    def app_install(cls, request):
        pass

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
