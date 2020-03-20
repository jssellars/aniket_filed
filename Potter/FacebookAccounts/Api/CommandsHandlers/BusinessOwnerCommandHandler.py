from dataclasses import asdict

import requests

from Core.Tools.RabbitMQ.RabbitMqClient import RabbitMqClient
from Core.Web.BusinessOwnerRepository.BusinessOwnerRepository import BusinessOwnerRepository
from Core.Web.FacebookGraphAPI.GraphAPI.HTTPRequestBase import HTTPRequestBase
from Potter.FacebookAccounts.Infrastructure.GraphAPIRequests.PermanentTokenGraphAPIRequests import ExchangeTemporaryTokenGraphAPIRequest
from Potter.FacebookAccounts.Infrastructure.GraphAPIRequests.PermanentTokenGraphAPIRequests import GeneratePermanentTokenGraphAPIRequest
from Potter.FacebookAccounts.Infrastructure.GraphAPIRequests.PermanentTokenGraphAPIRequests import DeletePermissionsGraphAPIRequest
from Core.Web.Security.Authorization import add_bearer_token, generate_technical_token
from Potter.FacebookAccounts.Api.Dtos.BusinessOwnerCreatedDto import BusinessOwnerCreatedDto
from Potter.FacebookAccounts.Infrastructure.GraphAPIHandlers.GraphAPIAdAccountHandler import GraphAPIAdAccountHandler
from Potter.FacebookAccounts.Infrastructure.IntegrationEvents.BusinessOwnerCreatedEvent import BusinessOwnerCreatedEvent
from Potter.FacebookAccounts.Api.Startup import startup


class BusinessOwnerCreateCommandHandler:

    @classmethod
    def handle(cls, command):
        cls.generate_permanent_token(command)

        # call subscription that new user has been successfully added to the system
        cls.activate_new_user(command, startup)

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
    def activate_new_user(cls, command, startup):
        try:
            technical_token = generate_technical_token(startup)

            headers = add_bearer_token(technical_token)

            body = {
                "UserId": command.filed_user_id,
                "BusinessOwnerFacebookId": command.facebook_id
            }

            response = requests.put(startup.external_services.subscription_update_business_owner_endpoint, json=body, headers=headers)
        except Exception as e:
            raise e

    @classmethod
    def publish_response(cls, response):
        try:
            rabbitmq_client = RabbitMqClient(startup.rabbitmq_config, startup.exchange_details.name, startup.exchange_details.outbound_queue.key)
            rabbitmq_client.publish(response)
        except Exception as e:
            raise e

    @classmethod
    def generate_permanent_token(cls, command):
        try:
            exchange_token_url = ExchangeTemporaryTokenGraphAPIRequest.generate_url(command.temporary_token)
            temporary_token, _ = HTTPRequestBase.get(exchange_token_url)
            temporary_token = temporary_token.get("access_token")
        except Exception as e:
            raise e

        try:
            generate_permanent_token_url = GeneratePermanentTokenGraphAPIRequest.generate_url(command.facebook_id, temporary_token)
            permanent_token_response, _ = HTTPRequestBase.get(generate_permanent_token_url)
        except Exception as e:
            raise e

        try:
            for entry in permanent_token_response:
                BusinessOwnerRepository(startup.session).create_or_update_user(business_owner_facebook_id=command.facebook_id,
                                                                               name=command.name,
                                                                               email=command.email,
                                                                               token=entry["access_token"],
                                                                               page_id=entry["id"])
        except Exception as e:
            raise e

    @classmethod
    def get_businesses(cls, command):
        try:
            permanent_token = BusinessOwnerRepository(startup.session).get_permanent_token(command.facebook_id)

            businesses = GraphAPIAdAccountHandler(permanent_token, startup.facebook_config).get_business_owner_details(command.facebook_id)

            businesses = BusinessOwnerCreatedDto(facebook_id=command.facebook_id,
                                                 name=command.name,
                                                 email=command.email,
                                                 requested_permissions=command.requested_permissions,
                                                 filed_user_id=command.filed_user_id,
                                                 businesses=businesses)

        except Exception as e:
            raise e

        return businesses


class BusinessOwnerUpdateCommandHandler:
    """TODO: Finish implementation after discussion with Sebastian + Vlad on how it is best to do this"""
    @classmethod
    def handle(cls, command):
        try:
            business_owner_permanent_token = BusinessOwnerRepository(startup.session).get_permanent_token(command.facebook_id)
            delete_permissions_url = DeletePermissionsGraphAPIRequest.generate_url(command.facebook_id, business_owner_permanent_token)

            HTTPRequestBase.delete(delete_permissions_url)
        except Exception as e:
            raise e
