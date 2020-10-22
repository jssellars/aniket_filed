import typing
from string import Template


class GraphAPIRequestAdAccountSpent:
    __default_api_version = "v7.0"

    def __init__(self,
                 access_token: typing.AnyStr = None,
                 business_owner_facebook_id: typing.AnyStr = None,
                 account_id: typing.AnyStr = None,
                 since: typing.AnyStr = None,
                 until: typing.AnyStr = None,
                 api_version: typing.AnyStr = None):
        self.__url = Template(
            "https://graph.facebook.com/$api_version/$business_owner_facebook_id/adaccounts?fields=account_id,currency,business,insights.time_range({'since':'$since','until':'$until'})&access_token=$access_token&filtering=[{field: 'account_id',operator:'EQUAL', value: '$account_id'}]")
        self.__access_token = access_token
        self.__business_owner_facebook_id = business_owner_facebook_id
        self.__account_id = account_id
        self.__since = since
        self.__until = until
        self.__api_version = api_version if api_version else self.__default_api_version

    @property
    def url(self):
        url = self.__url
        url = url.substitute(api_version=self.__api_version,
                             business_owner_facebook_id=self.__business_owner_facebook_id,
                             access_token=self.__access_token,
                             account_id=self.__account_id,
                             since=self.__since,
                             until=self.__until)

        return url
