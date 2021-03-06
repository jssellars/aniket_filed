import typing
from string import Template


class GraphAPIRequestProduct:
    __default_api_version = "v9.0"

    def __init__(
        self,
        access_token: typing.AnyStr = None,
        product_catalog_id: typing.AnyStr = None,
        api_version: typing.AnyStr = None,
        fields: typing.List[typing.AnyStr] = None,
    ):
        self.__url = Template(
            "https://graph.facebook.com/$api_version/$product_catalog_id/products?fields=$fields&access_token"
            "=$access_token"
        )

        self.__access_token = access_token
        self.__product_catalog_id = product_catalog_id
        self.__api_version = api_version if api_version else self.__default_api_version
        self.__fields = fields

    @property
    def url(self):
        url = self.__url
        url = url.substitute(
            api_version=self.__api_version,
            access_token=self.__access_token,
            product_catalog_id=self.__product_catalog_id,
            fields=self.__fields,
        )

        return url
