# todo: this handler needs refactoring after we introduce the generic table on the accounts page
# todo: amount_spent might need to be divided by 100. check with FB
import copy
import typing
from datetime import datetime

from Core.Web.BusinessOwnerRepository.BusinessOwnerRepository import BusinessOwnerRepository
from Core.Web.FacebookGraphAPI.GraphAPI.GraphAPIClientBase import GraphAPIClientBase
from Core.Web.FacebookGraphAPI.GraphAPI.GraphAPIClientConfig import GraphAPIClientBaseConfig
from Core.Web.FacebookGraphAPI.Tools import Tools
from Potter.FacebookAccounts.Infrastructure.GraphAPIRequests.GraphAPIRequestInsights import GraphAPIRequestInsights


class GraphAPIAdAccountInsightsHandler:

    @classmethod
    def handle(cls, request: typing.Any, startup: typing.Any) -> typing.List[typing.Dict]:
        # get permanent token
        permanent_token = BusinessOwnerRepository(startup.session).get_permanent_token(request.business_owner_facebook_id)

        from_date = cls.__convert_datetime(request.from_date)
        to_date = cls.__convert_datetime(request.to_date)

        response = cls.get_account_insights_base(permanent_token=permanent_token,
                                                 business_owner_facebook_id=request.business_owner_facebook_id,
                                                 from_date=from_date,
                                                 to_date=to_date,
                                                 startup=startup)

        return response

    @classmethod
    def get_account_insights_base(cls,
                                  permanent_token: typing.AnyStr = None,
                                  business_owner_facebook_id: typing.AnyStr = None,
                                  from_date: typing.AnyStr = None,
                                  to_date: typing.AnyStr = None,
                                  startup: typing.Any = None) -> typing.List[typing.Dict]:
        config = GraphAPIClientBaseConfig()
        config.request = GraphAPIRequestInsights(api_version=startup.facebook_config.api_version,
                                                 access_token=permanent_token,
                                                 business_owner_facebook_id=business_owner_facebook_id,
                                                 since=from_date,
                                                 until=to_date)

        graph_api_client = GraphAPIClientBase(business_owner_permanent_token=permanent_token, config=config)
        response, _ = graph_api_client.call_facebook()

        return cls.__map_response(response, business_owner_facebook_id, permanent_token)

    @classmethod
    def __map_response(cls,
                       response: typing.List[typing.Any] = None,
                       business_owner_facebook_id: typing.AnyStr = None,
                       permanent_token: typing.AnyStr = None) -> typing.List[typing.Dict]:
        for index, entry in enumerate(response):
            if not isinstance(entry, dict):
                entry = Tools.convert_to_json(entry)

            # map number of campaigns
            # entry = cls.__map_number_of_campaigns(entry, business_owner_facebook_id, permanent_token)

            # map business
            entry = cls.__map_business(entry)

            # map account_status
            entry = cls.__map_account_status(entry)

            # map conversions
            entry = cls.__map_conversions(entry)

            # map cost per conversion
            entry = cls.__map_cost_per_conversion(entry)

            # map simple insights
            entry = cls.__map_simple_insights(entry)

            entry["account_name"] = entry.pop("name")
            entry["ad_account_id"] = entry.pop("id")
            entry["amount_spent"] = float(entry.pop("amount_spent"))

            if "insights" in entry.keys():
                del entry["insights"]

            response[index] = copy.deepcopy(entry)

        return response

    @classmethod
    def __map_simple_insights(cls, response: typing.Dict) -> typing.Dict:
        if "insights" not in response.keys():
            return response
        else:
            insights = response["insights"]["data"][0]

        insight_keys = ["cpc", "cpm", "cpp", "ctr", "unique_clicks", "unique_ctr", "clicks", "impressions"]

        for insight_key in insight_keys:
            if insight_key in insights.keys():
                response[insight_key] = float(insights[insight_key])
            else:
                response[insight_key] = None

        return response

    # todo: implement this if reaaaally is critical
    # @classmethod
    # def __map_number_of_campaigns(cls,
    #                               response: typing.Dict,
    #                               business_owner_facebook_id: typing.AnyStr,
    #                               permanent_token: typing.AnyStr) -> typing.Dict:
    #     url = cls.__build_get_campaigns_url(business_owner_facebook_id, permanent_token)
    #     campaigns = HTTPRequestBase.loop_pages(response, url)
    #     response["number_of_campaigns"] = len([c for c in campaigns if c["effective_status"] == "ACTIVE"])
    #     return response

    # @classmethod
    # def __build_get_campaigns_url(cls, business_owner_facebook_id, permanent_token):
    #     return ""

    @classmethod
    def __map_conversions(cls, response: typing.Dict) -> typing.Dict:
        response["conversions"] = None
        if "insights" not in response.keys():
            return response
        else:
            insights = response["insights"]

        if "data" not in insights.keys():
            return response
        else:
            insights = insights["data"][0]

        if "actions" not in insights.keys():
            return response
        else:
            actions = insights["actions"]

        # todo: discuss with Chase how to define these metrics better
        response["conversions"] = sum([float(entry["value"]) for entry in list(filter(lambda x: x["action_type"].find("omni") > -1, actions)) if entry["value"]])

        return response

    @classmethod
    def __map_cost_per_conversion(cls, response: typing.Dict) -> typing.Dict:
        try:
            response["cost_per_conversion"] = float(response["amount_spent"]) / response["conversions"]
        except Exception as e:
            response["cost_per_conversion"] = None

        return response

    @classmethod
    def __map_business(cls, response: typing.Dict) -> typing.Dict:
        if "business" in response.keys():
            business = response.pop("business")
            response["business_name"] = business["name"]
            response["business_id"] = business["id"]

        return response

    @classmethod
    def __map_account_status(cls, response: typing.Dict) -> typing.Dict:
        facebook_account_status = {
            '1': 'ACTIVE',
            '2': 'DISABLED',
            '3': 'UNSETTLED',
            '7': 'PENDING RISK REVIEW',
            '8': 'PENDING SETTLEMENT',
            '9': 'IN GRACE PERIOD',
            '100': 'PENDING CLOSURE',
            '101': 'CLOSED',
            '201': 'ANY ACTIVE',
            '202': 'ANY CLOSED'
        }

        if "account_status" in response.keys():
            response["account_status"] = facebook_account_status[str(response["account_status"])]
        else:
            response["account_status"] = "UNKNOWN"

        return response

    @classmethod
    def __load_all_pages_facebook_response(cls, response: typing.Dict) -> typing.List[typing.Dict]:
        return [response]

    @staticmethod
    def __convert_datetime(input_date) -> typing.AnyStr:
        __MINIMUM_DATETIME_LENGTH__ = 10
        __DEFAULT_DATETIME_FORMAT__ = '%Y-%m-%d'
        __INCOMING_DATETIME_FORMAT__ = '%Y-%m-%dT%H:%M:%S+00:00'
        __ISO_DATETIME_FORMAT__ = "%Y-%m-%dT%H:%M:%S"

        date = input_date.split(".")[0]
        if len(date) != __MINIMUM_DATETIME_LENGTH__ and isinstance(input_date, datetime):
            try:
                date = datetime.strptime(date, __INCOMING_DATETIME_FORMAT__)
            except ValueError:
                date = datetime.strptime(date, __ISO_DATETIME_FORMAT__)
            except Exception as e:
                raise Exception(f"Invalid datetime format: {input_date}. Error: {str(e)}")
        elif isinstance(input_date, str):
            return input_date

        return date.strftime(__DEFAULT_DATETIME_FORMAT__)
