import json
import secrets
from copy import deepcopy

from Core.Web.FacebookGraphAPI.Tools import Tools
import requests
from flask import request
import urllib.parse as urlparse

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
from FiledEcommerce.Api.Dtos.ExportIntegrationMappingDto import (
    ExportIntegrationMappingDto,
)


class Facebook(Ecommerce):

    facebook_buisness_id:str = None
    errors:dict = []
    mappings:dict = {}
    request_json:dict = {}
    _callback_url:str = urlparse.quote(
        "https://py-filed-ecommerce-api.dev3.filed.com/api/v1/export/oauth/facebook/install/"
    )
    filed_user_id:str = None

    @classmethod
    def get_temporary_access_token_url(
        cls, config: config, state: str
    ):
        return (
            f"https://www.facebook.com/{config.facebook.api_version}/dialog/oauth?client_id={config.facebook.app_id}"
            f"&redirect_uri={cls._callback_url}&state={state}&response_type=token"
        )

    @classmethod
    def _get_external_platform(cls):
        cls.filed_user_id = int(extract_user_filed_id())
        external_platform = FiledProductsSQLRepo.getExternalPlatformByFiledBussinessId(
            cls.filed_user_id,
            FiledProductsSQLRepo.getPlatformByValue(PlatformsEnum.FACEBOOK.value).Id,
        )
        return external_platform

    @classmethod
    def get_mappings(cls, request: request, platform: str):
        externalPlatform = cls._get_external_platform()
        if externalPlatform and externalPlatform.MappingPreferences:
            return json.loads(externalPlatform.MappingPreferences)
        return ExportIntegrationMappingDto.get(platform=platform)

    @classmethod
    def handle(cls, request: request):
        cls.request_json = request.get_json(force=True)
        cls.facebook_buisness_id = extract_business_owner_facebook_id()
        # cls.facebook_buisness_id = cls.request_json["buisness_id"]
        external_platform = cls._get_external_platform()
        permanent_token = json.loads(external_platform.Details)[
            "permanent_access_token"
        ]
        _ = GraphAPISdkBase(config.facebook, permanent_token)
        mapping_preference = json.loads(external_platform.MappingPreferences)
        cls.mappings = mapping_preference if mapping_preference else None

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
            pydantic_variant = PydanticFiledVariants.from_orm(variant).dict()
            cls.filed_user_id = int(extract_user_filed_id())
            if pydantic_variant["CreatedById"] != cls.filed_user_id:
                raise Exception("Filed set is not created by this account")
            for mapping in cls.mappings["variants"]:
                mapping = dict(mapping)
                filedKey = mapping.get("filedKey")
                mappedTo = mapping.get("mappedTo")
                pydantic_variant_keys = pydantic_variant.keys()
                if filedKey in pydantic_variant_keys:
                    single_product[mappedTo] = pydantic_variant[filedKey]
                    if mappedTo == FacebookProductItem.Field.price:
                        single_product[mappedTo] = int(pydantic_variant[filedKey])

                    if filedKey == "Availability":
                        if int(pydantic_variant[filedKey]) == 1:
                            single_product["availability"] = "in stock"
                        else:
                            single_product["availability"] = "out of stock"

                if mappedTo == FacebookProductItem.Field.condition:
                    single_product[mappedTo] = pydantic_variant[filedKey] or "new"

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

        if len(pushed_products):
            return fb_catalog_id["id"]
        else:
            raise Exception(f"Catalog created with id {fb_catalog_id['id']} but no products pushed to catalog")

    @classmethod
    def pre_install(cls, request: request):
        from facebook_business.exceptions import FacebookRequestError

        state = secrets.token_hex(nbytes=8)
        external_platform = cls._get_external_platform()
        request_json = request.get_json()
        redirect_url = request_json.get("redirect_url")
        details = {"redirect_url": redirect_url, "state": state}
        if external_platform and False:
            external_platform_details = json.loads(external_platform.Details)
            if "permanent_access_token" in external_platform_details.keys():
                permanent_token = external_platform_details["permanent_access_token"]
                try:
                    _ = GraphAPISdkBase(config.facebook, permanent_token)
                    User("me").api_get()
                    return None
                except FacebookRequestError:
                    pass  # return the url to get the token in the last line
        else:
            externalPlatform = cls._create_external_platform()
            externalPlatform.Details = details
            FiledProductsSQLRepo.createOrupdateExternalPlatform(externalPlatform)
        return cls.get_temporary_access_token_url(config, state)

    @classmethod
    def app_install(cls, request: request):
        cls.request_json = request.get_json(force=True)
        data = request.args
        state = data.get("state")
        access_token = data.get("access_token")
        external_platform = cls._get_external_platform()
        external_platform_details = json.loads(external_platform.Details)
        if access_token and external_platform_details["state"] == state:
            permanent_token = cls.get_permanent_token(
                config.facebook.app_id,
                config.facebook.app_secret,
                access_token,
            )
            details = {"permanent_access_token": permanent_token}
            externalPlatform = cls._create_external_platform()
            externalPlatform.Details = details
            FiledProductsSQLRepo.createOrupdateExternalPlatform(externalPlatform)
            return external_platform_details["redirect_url"]
        return None

    @classmethod
    def app_load(cls, request: request):
        pass

    @classmethod
    def app_uninstall(cls, request: request):
        pass

    @classmethod
    def _create_external_platform(cls):
        now = get_utc_aware_date()
        user_id = extract_user_filed_id()
        platform_id = FiledProductsSQLRepo.getPlatformByValue(
            PlatformsEnum.FACEBOOK.value
        ).Id
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
        )
        return externalPlatform

    @classmethod
    def save_mappings(cls, request: request):
        cls.request_json = request.get_json(force=True)
        mapping = cls.request_json.get("mapping")
        externalPlatform = cls._create_external_platform()
        externalPlatform.MappingPreferences = json.dumps(mapping)
        return FiledProductsSQLRepo.createOrupdateExternalPlatform(externalPlatform)

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
