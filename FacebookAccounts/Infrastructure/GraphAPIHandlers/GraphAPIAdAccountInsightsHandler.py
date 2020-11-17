import copy
import typing
from datetime import datetime
from typing import Any, Dict, List

from Core.Metadata.Columns.ViewColumns.ViewColumn import ViewColumn
from Core.Tools.Logger.LoggerMessageBase import LoggerMessageBase, LoggerMessageTypeEnum
from Core.Web.BusinessOwnerRepository.BusinessOwnerRepository import BusinessOwnerRepository
from Core.Web.FacebookGraphAPI.GraphAPI.GraphAPIClientBase import GraphAPIClientBase
from Core.Web.FacebookGraphAPI.GraphAPI.GraphAPIClientConfig import GraphAPIClientBaseConfig
from Core.Web.FacebookGraphAPI.GraphAPI.AccountStatus import AccountStatus
from Core.Web.FacebookGraphAPI.GraphAPIDomain.GraphAPIInsightsFields import GraphAPIInsightsFields
from Core.Web.FacebookGraphAPI.Models.FieldsMetadata import FieldsMetadata
from Core.Web.FacebookGraphAPI.Tools import Tools
from FacebookAccounts.Api.Dtos.AccountAgGridViewsDto import accounts_ag_grid_view
from FacebookAccounts.Api.Startup import logger
from FacebookAccounts.Infrastructure.GraphAPIRequests.GraphAPIRequestInsights import (
    GraphAPIAccountInsights,
    GraphAPIRequestInsights,
)

INSIGHTS_KEY = "insights"
DATA_KEY = "data"


class GraphAPIAdAccountInsightsHandler:
    @classmethod
    def handle(cls, request: typing.Any, startup: typing.Any) -> typing.List[typing.Dict]:
        # get permanent token
        permanent_token = BusinessOwnerRepository(startup.session).get_permanent_token(
            request.business_owner_facebook_id
        )

        from_date = cls.__convert_datetime(request.from_date)
        to_date = cls.__convert_datetime(request.to_date)

        response = cls.get_account_insights_base(
            permanent_token=permanent_token,
            business_owner_facebook_id=request.business_owner_facebook_id,
            from_date=from_date,
            to_date=to_date,
            startup=startup,
        )

        return response

    @classmethod
    def get_account_insights_base(
        cls,
        permanent_token: typing.AnyStr = None,
        business_owner_facebook_id: typing.AnyStr = None,
        from_date: typing.AnyStr = None,
        to_date: typing.AnyStr = None,
        startup: typing.Any = None,
    ) -> typing.List[typing.Dict]:
        config = GraphAPIClientBaseConfig()
        config.request = GraphAPIRequestInsights(
            api_version=startup.facebook_config.api_version,
            access_token=permanent_token,
            business_owner_facebook_id=business_owner_facebook_id,
            since=from_date,
            until=to_date,
        )

        graph_api_client = GraphAPIClientBase(business_owner_permanent_token=permanent_token, config=config)
        response, _ = graph_api_client.call_facebook()
        if isinstance(response, Exception):
            raise response

        return cls.__map_response(response)

    @classmethod
    def __map_response(cls, response: typing.List[typing.Any] = None) -> typing.List[typing.Dict]:
        for index, entry in enumerate(response):
            if not isinstance(entry, dict):
                entry = Tools.convert_to_json(entry)

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
            entry["amount_spent"] = float(entry.pop("amount_spent")) / 100

            if INSIGHTS_KEY in entry.keys():
                del entry[INSIGHTS_KEY]

            response[index] = copy.deepcopy(entry)

        return response

    @classmethod
    def __map_simple_insights(cls, response: typing.Dict) -> typing.Dict:
        if INSIGHTS_KEY not in response.keys():
            return response
        else:
            insights = response[INSIGHTS_KEY][DATA_KEY][0]

        insight_keys = ["cpc", "cpm", "cpp", "ctr", "unique_clicks", "unique_ctr", "clicks", "impressions"]

        for insight_key in insight_keys:
            if insight_key in insights.keys():
                response[insight_key] = float(insights[insight_key])
            else:
                response[insight_key] = None

        return response

    @classmethod
    def __map_conversions(cls, response: typing.Dict) -> typing.Dict:
        response["conversions"] = None
        if INSIGHTS_KEY not in response.keys():
            return response
        else:
            insights = response[INSIGHTS_KEY]

        if DATA_KEY not in insights.keys():
            return response
        else:
            insights = insights[DATA_KEY][0]

        if "actions" not in insights.keys():
            return response
        else:
            actions = insights["actions"]

        response["conversions"] = sum(
            [
                float(entry["value"])
                for entry in list(filter(lambda x: x["action_type"].find("omni") > -1, actions))
                if entry["value"]
            ]
        )

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

        if "account_status" in response.keys():
            response["account_status"] = AccountStatus(response["account_status"]).name
        else:
            response["account_status"] = "UNKNOWN"

        return response

    @classmethod
    def __load_all_pages_facebook_response(cls, response: typing.Dict) -> typing.List[typing.Dict]:
        return [response]

    @staticmethod
    def __convert_datetime(input_date) -> typing.AnyStr:
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
                raise Exception(f"Invalid datetime format: {input_date}. Error: {str(e)}")
        elif isinstance(input_date, str):
            return input_date

        return date.strftime(__DEFAULT_DATETIME_FORMAT__)


def handle_accounts_insights(request: Any, startup: Any) -> List[Dict]:
    # get permanent token
    permanent_token = BusinessOwnerRepository(startup.session).get_permanent_token(request.business_owner_facebook_id)

    response = get_account_insights_base(
        permanent_token=permanent_token,
        business_owner_facebook_id=request.business_owner_facebook_id,
        from_date=request.from_date,
        to_date=request.to_date,
        startup=startup,
    )

    return response


def get_account_insights_base(
    permanent_token: typing.AnyStr = None,
    business_owner_facebook_id: typing.AnyStr = None,
    from_date: typing.AnyStr = None,
    to_date: typing.AnyStr = None,
    startup: typing.Any = None,
) -> typing.List[typing.Dict]:

    config = GraphAPIClientBaseConfig()
    account_fields = get_facebook_fields(accounts_ag_grid_view.account_structure_columns)
    insights_fields = get_facebook_fields(accounts_ag_grid_view.account_insight_columns)

    config.request = GraphAPIAccountInsights(
        api_version=startup.facebook_config.api_version,
        access_token=permanent_token,
        business_owner_facebook_id=business_owner_facebook_id,
        since=from_date,
        until=to_date,
        account_fields=",".join(account_fields),
        insights_fields=",".join(insights_fields),
    )

    graph_api_client = GraphAPIClientBase(business_owner_permanent_token=permanent_token, config=config)
    response, _ = graph_api_client.call_facebook()
    if isinstance(response, Exception):
        raise response

    return map_response(response)


def get_facebook_fields(view_fields: List[ViewColumn]) -> List[str]:
    facebook_fields = set()
    for column in view_fields:
        for facebook_field in column.primary_value.facebook_fields:
            facebook_fields.add(facebook_field)

    return list(facebook_fields)


def map_response(response: List[Any] = None) -> typing.List[Dict]:
    result = []
    for entry in response:
        entry_result = {}
        for column in accounts_ag_grid_view.account_structure_columns:
            try:
                # Business id is nested inside of a dict even if it is an account structure info...
                if (
                    column.primary_value.name == FieldsMetadata.business_id.name
                    and GraphAPIInsightsFields.business in entry
                ):
                    entry_result.update({column.primary_value.name: entry["business"]["id"]})
                    continue

                mapped_entry = column.primary_value.mapper.map(entry, column.primary_value)[0]
                if FieldsMetadata.account_status.name in mapped_entry:
                    mapped_entry[FieldsMetadata.account_status.name] = AccountStatus(
                        mapped_entry[FieldsMetadata.account_status.name]
                    ).name

                entry_result.update(mapped_entry)
            except Exception as e:
                log = LoggerMessageBase(
                    mtype=LoggerMessageTypeEnum.ERROR,
                    name="FieldMappingException",
                    description=f"Failed to map the {column.primary_value.name} field",
                )
                logger.logger.exception(log.to_dict())

        if INSIGHTS_KEY not in entry and entry_result:
            result.append(entry_result)
            continue

        # Since the insights are at the account level, there is only one entry in the dict
        insights = entry[INSIGHTS_KEY][DATA_KEY][0]

        for column in accounts_ag_grid_view.account_insight_columns:
            try:
                entry_result.update(column.primary_value.mapper.map(insights, column.primary_value)[0])
            except Exception as e:
                log = LoggerMessageBase(
                    mtype=LoggerMessageTypeEnum.ERROR,
                    name="FieldMappingException",
                    description=f"Failed to map the {column.primary_value.name} field",
                )
                logger.logger.exception(log.to_dict())

        if entry_result:
            result.append(entry_result)

    return result
