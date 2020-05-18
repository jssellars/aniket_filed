import typing
from string import Template


class GraphAPIRequestBusiness:
    __default_api_version = "v5.0"

    def __init__(self,
                 access_token: typing.AnyStr = None,
                 account_id: typing.AnyStr = None,
                 api_version: typing.AnyStr = None):
        self.__url = Template(
            "https://graph.facebook.com/$api_version/$account_id?fields=business&access_token=$access_token")

        self.__access_token = access_token
        self.__account_id = account_id
        self.__api_version = api_version if api_version else self.__default_api_version

    @property
    def url(self):
        url = self.__url
        url = url.substitute(api_version=self.__api_version,
                             access_token=self.__access_token,
                             account_id=self.__account_id)

        return url
