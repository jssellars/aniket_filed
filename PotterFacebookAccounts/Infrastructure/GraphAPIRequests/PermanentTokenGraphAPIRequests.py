from dataclasses import dataclass
from string import Template

from PotterFacebookAccounts.Api.Startup import startup


@dataclass
class PermanentTokenGraphAPIRequestBase:
    _api_version = startup.facebook_config.api_version
    _app_id = startup.facebook_config.app_id
    _app_secret = startup.facebook_config.app_secret


class ExchangeTemporaryTokenGraphAPIRequest(PermanentTokenGraphAPIRequestBase):

    @classmethod
    def generate_url(cls, temporary_token):
        url = Template(
            "https://graph.facebook.com/$api_version/oauth/access_token?grant_type=fb_exchange_token&client_id=$app_id&client_secret=$app_secret&fb_exchange_token=$temporary_token")
        url = url.substitute(api_version=cls._api_version, app_id=cls._app_id, app_secret=cls._app_secret,
                             temporary_token=temporary_token)

        return url


class GeneratePermanentTokenGraphAPIRequest(PermanentTokenGraphAPIRequestBase):

    @classmethod
    def generate_url(cls, business_owner_facebook_id, exchangedToken):
        url = Template(
            "https://graph.facebook.com/$api_version/$business_owner_facebook_id/accounts?access_token=$exchangedToken")
        url = url.substitute(api_version=cls._api_version, business_owner_facebook_id=business_owner_facebook_id,
                             exchangedToken=exchangedToken)

        return url


class DeletePermissionsGraphAPIRequest(PermanentTokenGraphAPIRequestBase):

    @classmethod
    def generate_url(cls, business_owner_facebook_id, business_owner_permanent_token):
        url = Template(
            "https://graph.facebook.com/$api_version/$business_owner_facebook_id/permissions&access_tokne=$business_owner_permanent_token")
        url = url.substitute(api_version=cls._api_version, business_owner_facebook_id=business_owner_facebook_id,
                             business_owner_permanent_token=business_owner_permanent_token)

        return url
