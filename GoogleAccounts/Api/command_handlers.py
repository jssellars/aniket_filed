import json
import logging
import os
import sys
from typing import Dict, List

import google.oauth2.credentials
import google_auth_oauthlib.flow
import httplib2
import requests
from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException
from oauth2client import GOOGLE_TOKEN_URI, client
from requests_oauthlib import OAuth2Session

import GoogleAccounts.Api.mappings
from Core.settings import Default
from GoogleAccounts.Api.commands import GoogleHeaders

# Oauth2 requires SSL which is not present in local testing, so disable SSl check
# https://stackoverflow.com/questions/27785375/testing-flask-oauthlib-locally-without-https
# TODO disable check only in development configuration not in production
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

logger = logging.getLogger(__name__)


class GetAccountsTreeCommandHandler:
    @classmethod
    def handle(cls, command):
        headers = cls.get_refresh_token(command)
        token = cls.get_token_from_refresh_token(headers.refresh_token)
        headers.token = token["access_token"]

        google_ads_client = GoogleAdsClient.load_from_storage(path="googleads.yaml", version="v6")
        try:
            return cls.get_account_tree(google_ads_client)
        except GoogleAdsException as ex:
            logger.error(f"Request with ID '{ex.request_id}' failed with status {ex.error.code().name}")
            raise Exception(f"Request with ID '{ex.request_id}' failed with status {ex.error.code().name}")

    @classmethod
    def get_refresh_token(cls, command):
        # TODO get info from config (Core.Default.Google) instead of .json
        google_config = Default.google
        refresh_token = (
            "1//0cgG4P2mKtjsMCgYIARAAGAwSNwF-L9Ir0Vl_1PxJPDAfNBcJerYGQEtxvAPuVoecfoJpsm3zedWUdyPRkG-NJk5i-iOFW5uaKaE"
        )

        flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
            "client_secret.json", scopes=google_config.scopes, redirect_uri=google_config.redirect_uri
        )

        try:
            flow.fetch_token(code=command.authorization_code)
            credentials = flow.credentials

            headers = GoogleHeaders(
                client_id=credentials.client_id,
                client_secret=credentials.client_secret,
                token=credentials.token,
                refresh_token=credentials.refresh_token,
                scopes=credentials.scopes,
            )
            return headers

        except Exception as e:
            logger.exception(f"Failed to get refresh_token. Error {repr(e)}")
            # TODO remove this hardcoded logic later when 2fa is sorted out

            headers = GoogleHeaders(
                client_id=google_config.client_id,
                client_secret=google_config.client_secret,
                token="access_token",
                refresh_token=refresh_token,
                scopes=google_config.scopes,
            )

            return headers

    @classmethod
    def get_token_from_refresh_token(cls, refresh_token):
        google_config = Default.google

        # if scopes are not known, pass scopes=None
        flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
            "client_secret.json", scopes=google_config.scopes, redirect_uri=google_config.redirect_uri
        )

        token = flow.oauth2session.refresh_token(
            token_url=google_config.token_url,
            refresh_token=refresh_token,
            client_id=google_config.client_id,
            client_secret=google_config.client_secret,
        )
        return token

    @classmethod
    def get_account_tree(cls, google_ads_client):
        response = list()

        googleads_service = google_ads_client.get_service("GoogleAdsService")
        customer_service = google_ads_client.get_service("CustomerService")

        # A collection of customer IDs to handle.
        customer_ids = []

        # query to retrieve all child accounts of a manager account.
        query = """
                   SELECT
                     customer_client.client_customer,
                     customer_client.level,
                     customer_client.manager,
                     customer_client.descriptive_name,
                     customer_client.currency_code,
                     customer_client.time_zone,
                     customer_client.id
                   FROM customer_client
                   WHERE customer_client.level <= 1"""

        customer_resource_names = customer_service.list_accessible_customers().resource_names

        for customer_resource_name in customer_resource_names:
            try:
                customer = customer_service.get_customer(resource_name=customer_resource_name)
                customer_ids.append(customer.id)
            except Exception as e:
                logger.exception(f"Customer ID is cancelled, {repr(e)}")

        customer_ids = [str(id_) for id_ in customer_ids]

        for customer_id in customer_ids:
            # Performs a breadth-first search to build a Dictionary that maps
            # managers to their child accounts (customerIdsToChildAccounts).
            unprocessed_customer_ids = [customer_id]
            customer_ids_to_child_accounts = dict()
            root_customer_client = None

            while unprocessed_customer_ids:
                customer_id = unprocessed_customer_ids.pop(0)
                customers = googleads_service.search(customer_id=customer_id, query=query)

                # Iterates over all rows in all pages to get all customer
                # clients under the specified customer's hierarchy.
                for googleads_row in customers:
                    customer_client = googleads_row.customer_client

                    # The customer client that with level-0 is the specified customer.
                    if customer_client.level == 0:
                        if root_customer_client is None:
                            root_customer_client = customer_client
                        continue

                    # For all level-1 (direct child) accounts that are a
                    # manager account, the above query will be run against them
                    # to create a Dictionary of managers mapped to their child
                    # accounts for printing the hierarchy afterwards.
                    if customer_id not in customer_ids_to_child_accounts:
                        customer_ids_to_child_accounts[customer_id] = []

                    customer_ids_to_child_accounts[customer_id].append(customer_client)

                    if customer_client.manager:
                        # A customer can be managed by multiple managers, so to
                        # prevent visiting the same customer many times, we
                        # need to check if it's already in the Dictionary.
                        if customer_client.id not in customer_ids_to_child_accounts and customer_client.level == 1:
                            unprocessed_customer_ids.append(customer_client.id)

            if root_customer_client is not None:
                result = list()
                cls.create_account_hierarchy(result, root_customer_client, customer_ids_to_child_accounts, 0)
                response.extend(result)
            else:
                raise UserWarning(
                    "CustomerID is likely a test account, so its customer client information cannot be retrieved."
                )

        return response

    @classmethod
    def create_account_hierarchy(cls, response, customer_client, customer_ids_to_child_accounts, depth):
        customer_id = str(customer_client.id)

        customer_info = {
            "customer_id": customer_client.id,
            "name": customer_client.descriptive_name,
            "currency_code": customer_client.currency_code,
            "time_zone": customer_client.time_zone,
            "is_manager": customer_client.manager,
            "children": [],
        }

        response.append(customer_info)

        # Recursively call this function for all child accounts of customer_client.
        if customer_id in customer_ids_to_child_accounts:
            for child_account in customer_ids_to_child_accounts[customer_id]:
                cls.create_account_hierarchy(
                    response[-1]["children"], child_account, customer_ids_to_child_accounts, depth + 1
                )
