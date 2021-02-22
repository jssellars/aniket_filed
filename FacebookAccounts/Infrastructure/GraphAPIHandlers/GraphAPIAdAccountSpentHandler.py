import typing
from datetime import datetime

from facebook_business.adobjects.adaccount import AdAccount

from Core.Web.FacebookGraphAPI.GraphAPI.GraphAPISdkBase import GraphAPISdkBase
from Core.Web.FacebookGraphAPI.GraphAPIDomain.FacebookMiscFields import FacebookMiscFields
from Core.Web.FacebookGraphAPI.Models.FieldsMetadata import FieldsMetadata
from FacebookAccounts.Infrastructure.Domain.AdAccountAmountSpentModel import AdAccountAmountSpentModel
from FacebookAccounts.Infrastructure.GraphAPIMappings.GraphAPIAdAccountSpentMapping import GraphAPIAdAccountSpentMapping


class GraphAPIAdAccountSpentHandler:
    @classmethod
    def handle(cls, request, config, fixtures):
        permanent_token = fixtures.business_owner_repository.get_permanent_token(request.business_owner_facebook_id)
        ad_accounts_amount_spent = []
        _ = GraphAPISdkBase(config.facebook, permanent_token)

        response_mapper = GraphAPIAdAccountSpentMapping(AdAccountAmountSpentModel)

        for account_id in request.ad_account_ids:
            for date in request.dates:
                response = cls.get_account_spent_base(
                    account_id=account_id,
                    from_date=date.isoformat(),
                    to_date=date.isoformat(),
                )
                if isinstance(response, list) and len(response) == 1:
                    response = response[0]

                if not response:
                    response = dict(ad_account_id=account_id, amount_spent=0)

                mapped_response = response_mapper.load(response)
                mapped_response.date = date.isoformat()
                ad_accounts_amount_spent.append(mapped_response)

        return ad_accounts_amount_spent, []

    @classmethod
    def get_account_spent_base(
        cls,
        account_id: typing.AnyStr = None,
        from_date: typing.AnyStr = None,
        to_date: typing.AnyStr = None,
    ):

        fields = [FieldsMetadata.account_id.name, FieldsMetadata.currency.name, FacebookMiscFields.business]
        filtered_insights = f"insights.time_range({{'since':'{from_date}','until': '{to_date}'}})"
        fields.append(filtered_insights)

        ad_account = AdAccount(f'act_{account_id}')

        response = ad_account.api_get(fields=fields)

        return response.export_all_data()

    @staticmethod
    def __convert_datetime(input_date):
        __MINIMUM_DATETIME_LENGTH__ = 10
        __DEFAULT_DATETIME_FORMAT__ = "%Y-%m-%d"
        __INCOMING_DATETIME_FORMAT__ = "%Y-%m-%dT%H:%M:%S+00:00"
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
