import logging
import os
from dataclasses import asdict

import google_auth_oauthlib.flow
from google.ads.googleads.errors import GoogleAdsException

from Core.mongo_adapter import MongoRepositoryBase
from Core.settings import Default
from GoogleAccounts.Api.Commands.commands import GoogleHeaders
from GoogleAccounts.Api.startup import config
from GoogleAccounts.Infrastructure.GoogleAdsAPI.AdAccountsTreeClient import AdAccountsTreeClient

# Oauth2 requires SSL which is not present in local testing, so disable SSl check
# https://stackoverflow.com/questions/27785375/testing-flask-oauthlib-locally-without-https
# TODO disable check only in development configuration not in production
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

logger = logging.getLogger(__name__)


class GetAdAccountsTreeCommandHandler:
    accounts_repository = MongoRepositoryBase(
        config=config.mongo,
        database_name=config.mongo.google_accounts_database_name,
        collection_name=config.mongo.accounts_collection_name,
    )

    @classmethod
    def _build_client(cls, google_config, refresh_token):
        client = AdAccountsTreeClient(config=google_config, refresh_token=refresh_token)
        # TODO look into setting login_customer_id method in ads API
        # ads_client.set_client_customer_id(int(manager_id))
        return client

    @classmethod
    def handle(cls, google_config, command):
        refresh_token = cls.get_refresh_token(google_config, command)
        ad_account_tree_client = cls._build_client(google_config, refresh_token)

        try:
            return ad_account_tree_client.get_account_tree()
        except GoogleAdsException as ex:
            logger.exception(f"Request with ID '{ex.request_id}' failed with status {ex.error.code().name}")

    @classmethod
    def get_refresh_token(cls, google_config, command):
        # TODO get info from config (Core.Default.Google) instead of .json

        flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
            client_secrets_file="client_secret.json",
            scopes=google_config.scopes,
            redirect_uri=google_config.redirect_uri,
        )

        try:
            flow.fetch_token(code=command.authorization_code)
            credentials = flow.credentials

            headers = GoogleHeaders(
                business_owner_google_id="andrew@filed.com",
                client_id=credentials.client_id,
                client_secret=credentials.client_secret,
                token=credentials.token,
                refresh_token=credentials.refresh_token,
                scopes=credentials.scopes,
            )

            GetAdAccountsTreeCommandHandler.accounts_repository.add_one(asdict(headers))
            return headers.refresh_token

        except Exception as e:
            logger.exception(f"Failed to get refresh_token. Error {repr(e)}")

            # TODO remove this hardcoded logic later when 2fa is sorted out
            refresh_token = "1//0cgG4P2mKtjsMCgYIARAAGAwSNwF-L9Ir0Vl_1PxJPDAfNBcJerYGQEtxvAPuVoecfoJpsm3zedWUdyPRkG-NJk5i-iOFW5uaKaE"
            headers = GoogleHeaders(
                business_owner_google_id="andrew@filed.com",
                client_id=google_config.client_id,
                client_secret=google_config.client_secret,
                token="access_token",
                refresh_token=refresh_token,
                scopes=google_config.scopes,
            )

            GetAdAccountsTreeCommandHandler.accounts_repository.add_one(asdict(headers))

            return headers.refresh_token

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
