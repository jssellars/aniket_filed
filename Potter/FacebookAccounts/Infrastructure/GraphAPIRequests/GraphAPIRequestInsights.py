import typing
from string import Template


class GraphAPIRequestInsights:

    __default_api_version = "v5.0"

    def __init__(self,
                 access_token: typing.AnyStr = None,
                 business_owner_facebook_id: typing.AnyStr = None,
                 since: typing.AnyStr = None,
                 until: typing.AnyStr = None,
                 api_version: typing.AnyStr = None):

        self.__url = Template("https://graph.facebook.com/$api_version/$business_owner_facebook_id/adaccounts?fields="
                              # "name,id,account_status,currency,amount_spent,business,campaigns{effective_status}," # required if we want no. active campaigns
                              "name,id,account_status,currency,amount_spent,business,"
                              "insights.time_range({'since':'$since','until':'$until'})."
                              "action_breakdowns(['action_type'])"
                              "{cpc,cpm,cpp,ctr,unique_clicks,unique_ctr,clicks,impressions,actions}"
                              "&access_token=$access_token")

        self.__access_token = access_token
        self.__business_owner_facebook_id = business_owner_facebook_id
        self.__since = since
        self.__until = until
        self.__api_version = api_version if api_version else self.__default_api_version

    @property
    def url(self):
        url = self.__url
        url = url.substitute(api_version=self.__api_version,
                             business_owner_facebook_id=self.__business_owner_facebook_id,
                             access_token=self.__access_token,
                             since=self.__since,
                             until=self.__until)

        return url
