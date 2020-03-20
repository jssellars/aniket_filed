import typing
from string import Template


class GraphAPIRequestInstagram:
    __default_api_version = "v4.0"

    def __init__(self,
                 access_token: typing.AnyStr = None,
                 business_id: typing.AnyStr = None,
                 api_version: typing.AnyStr = None):
        self.__url = Template("https://graph.facebook.com/$api_version/$business_id?fields=instagram_accounts{id,username}&access_token=$access_token")

        self.__access_token = access_token
        self.__business_id = business_id
        self.__api_version = api_version if api_version else self.__default_api_version

    @property
    def url(self):
        url = self.__url
        url = url.substitute(api_version=self.__api_version,
                             access_token=self.__access_token,
                             business_id=self.__business_id)

        return url