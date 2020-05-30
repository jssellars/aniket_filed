import typing
from string import Template


class GraphAPIRequestAudienceSize:
    __default_api_version = "v5.0"

    def __init__(self,
                 access_token: typing.AnyStr = None,
                 account_id: typing.AnyStr = None,
                 audience_details: typing.Dict = None,
                 api_version: typing.AnyStr = None):
        self.__url = Template(
            "https://graph.facebook.com/$api_version/$account_id/delivery_estimate?"
            "fields=estimate_mau&targeting_spec=$targeting_spec&optimization_goal=$optimization_goal&"
            "access_token=$access_token")

        self.__access_token = access_token
        self.__account_id = account_id
        self.__audience_details = audience_details
        self.__api_version = api_version if api_version else self.__default_api_version

    @property
    def url(self):
        url = self.__url
        url = url.substitute(api_version=self.__api_version,
                             access_token=self.__access_token,
                             targeting_spec=self.__audience_details['targeting_spec'],
                             optimization_goal=self.__audience_details['optimization_goal'],
                             account_id=self.__account_id)

        return url
