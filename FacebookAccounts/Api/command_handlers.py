import typing

import requests
from facebook_business.adobjects.user import User

from Core.Web.FacebookGraphAPI.GraphAPI.GraphAPISdkBase import GraphAPISdkBase
from Core.Web.FacebookGraphAPI.GraphAPI.HTTPRequestBase import HTTPRequestBase
from Core.Web.Security.Authorization import add_bearer_token, generate_technical_token
from FacebookAccounts.Api.dtos import BusinessOwnerCreatedDto
from FacebookAccounts.Api.startup import config, fixtures
from FacebookAccounts.Infrastructure.GraphAPIHandlers.GraphAPIAdAccountHandler import GraphAPIAdAccountHandler
from FacebookAccounts.Infrastructure.GraphAPIRequests.PermanentTokenGraphAPIRequests import \
    get_exchange_temporary_token_url, get_generate_permanent_token_url
from FacebookAccounts.Infrastructure.IntegrationEvents.BusinessOwnerCreatedEvent import \
    BusinessOwnerCreatedEvent


import logging

logger = logging.getLogger(__name__)


class BusinessOwnerCreateCommandHandler:

    @classmethod
    def handle(cls, command):
        cls.generate_permanent_token(command)

        # call subscription that new user has been successfully added to the system
        cls.activate_new_user(command, config)

        # get businesses and publish ad accounts response to Facebook Accounts queue
        business = cls.get_businesses(command)

        # publish businesses details to facebook ad accounts queue
        response = BusinessOwnerCreatedEvent(facebook_id=business.facebook_id,
                                             filed_user_id=business.filed_user_id,
                                             name=business.name,
                                             email=business.email,
                                             requested_permissions=business.requested_permissions,
                                             businesses=business.businesses)

        cls.publish_response(response)

    @classmethod
    def activate_new_user(cls, command, config):
        try:
            technical_token = generate_technical_token(fixtures.technical_token_manager)

            headers = add_bearer_token(technical_token)

            body = {
                "UserId": command.filed_user_id,
                "BusinessOwnerFacebookId": command.facebook_id
            }

            _ = requests.put(config.external_services.subscription_update_business_owner_endpoint, json=body,
                             headers=headers)
        except Exception as e:
            raise e

    @classmethod
    def publish_response(cls, response):
        try:
            rabbitmq_adapter = fixtures.rabbitmq_adapter
            response.requested_permissions = ",".join(response.requested_permissions)
            rabbitmq_adapter.publish(response)
            logger.info(response.message_type, extra=dict(rabbitmq=rabbitmq_adapter.serialize_message(response)))
        except Exception as e:
            raise e

    @classmethod
    def generate_permanent_token(cls, command):
        try:
            temporary_token, _ = HTTPRequestBase.get(get_exchange_temporary_token_url(command.temporary_token, config))
            temporary_token = temporary_token.get("access_token")
        except Exception as e:
            raise e

        try:
            permanent_token_response, _ = HTTPRequestBase.get(
                get_generate_permanent_token_url(command.facebook_id, temporary_token, config)
            )
        except Exception as e:
            raise e

        try:
            for entry in permanent_token_response:
                fixtures.business_owner_repository.create_or_update_user(
                    business_owner_facebook_id=command.facebook_id,
                    name=command.name,
                    email=command.email,
                    token=entry["access_token"],
                    page_id=entry["id"])
        except Exception as e:
            raise e

    @classmethod
    def get_businesses(cls, command):
        try:
            permanent_token = fixtures.business_owner_repository.get_permanent_token(command.facebook_id)

            businesses = GraphAPIAdAccountHandler(permanent_token, config.facebook).get_business_owner_details(
                command.facebook_id)

            businesses = BusinessOwnerCreatedDto(facebook_id=command.facebook_id,
                                                 name=command.name,
                                                 email=command.email,
                                                 requested_permissions=command.requested_permissions,
                                                 filed_user_id=command.filed_user_id,
                                                 businesses=businesses)

        except Exception as e:
            raise e

        return businesses


class BusinessOwnerDeletePermissionsCommandHandler:

    @classmethod
    def handle(cls,
               business_owner_id: typing.AnyStr = None,
               permissions: typing.AnyStr = None) -> typing.Dict:

        permanent_token = fixtures.business_owner_repository.get_permanent_token(business_owner_id)

        # initialize GraphAPI SDK
        _ = GraphAPISdkBase(config.facebook, permanent_token)

        user = User(fbid=business_owner_id)
        response = {
            'successful': [],
            'failed': []
        }
        permissions = permissions.split(",")
        for permission in permissions:
            try:
                fb_response = user.delete_permissions(params={"permission": permission})
                if fb_response:
                    response['successful'].append(permission)
            except:
                response['failed'].append(permission)

        return response
