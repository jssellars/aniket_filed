import typing
from datetime import datetime

from Core.Web.FacebookGraphAPI.GraphAPI.GraphAPIClientBase import GraphAPIClientBase
from Core.Web.FacebookGraphAPI.GraphAPI.GraphAPIClientConfig import GraphAPIClientBaseConfig
from FacebookAccounts.Infrastructure.Domain.AdAccountAmountSpentModel import AdAccountAmountSpentModel
from FacebookAccounts.Infrastructure.GraphAPIMappings.GraphAPIAdAccountSpentMapping import \
    GraphAPIAdAccountSpentMapping
from FacebookAccounts.Infrastructure.GraphAPIRequests.GraphAPIRequestAdAccountSpent import \
    GraphAPIRequestAdAccountSpent


class GraphAPIAdAccountSpentHandler:
    @classmethod
    def handle(cls, request, config, fixtures):
        permanent_token = fixtures.business_owner_repository.get_permanent_token(request.user_id)

        ad_accounts_amount_spent = []

        response_mapper = GraphAPIAdAccountSpentMapping(AdAccountAmountSpentModel)

        for account_detail in request.ad_accounts_details:
            from_date = cls.__convert_datetime(account_detail.from_date)
            to_date = cls.__convert_datetime(account_detail.to_date)
            response = cls.get_account_spent_base(config,
                                                  permanent_token=permanent_token,
                                                  business_owner_facebook_id=request.user_id,
                                                  account_id=account_detail.facebook_id,
                                                  from_date=from_date,
                                                  to_date=to_date)
            if isinstance(response, list) and len(response) == 1:
                response = response[0]

            mapped_response = response_mapper.load(response)
            ad_accounts_amount_spent.append(mapped_response)

        return ad_accounts_amount_spent, []

    @classmethod
    def get_account_spent_base(cls,
                               config,
                               permanent_token: typing.AnyStr = None,
                               business_owner_facebook_id: typing.AnyStr = None,
                               account_id: typing.AnyStr = None,
                               from_date: typing.AnyStr = None,
                               to_date: typing.AnyStr = None):
        account_id = account_id.split("_")[1]
        api_config = GraphAPIClientBaseConfig()
        api_config.request = GraphAPIRequestAdAccountSpent(api_version=config.facebook.api_version,
                                                       access_token=permanent_token,
                                                       business_owner_facebook_id=business_owner_facebook_id,
                                                       account_id=account_id,
                                                       since=from_date,
                                                       until=to_date)

        graph_api_client = GraphAPIClientBase(business_owner_permanent_token=permanent_token, config=api_config)
        response, _ = graph_api_client.call_facebook()

        return response

    @staticmethod
    def __convert_datetime(input_date):
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
                raise Exception(f"Invalid datetime format: {input_date} || {repr(e)}")
        elif isinstance(input_date, str):
            return input_date

        return date.strftime(__DEFAULT_DATETIME_FORMAT__)
