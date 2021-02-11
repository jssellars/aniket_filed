import typing
from typing import Any, Dict, List
from facebook_business.adobjects.user import User
from Core.Metadata.Columns.ViewColumns.ViewColumn import ViewColumn
from Core.Web.FacebookGraphAPI.GraphAPI.AccountStatus import AccountStatus
from Core.Web.FacebookGraphAPI.GraphAPI.GraphAPISdkBase import GraphAPISdkBase
from Core.Web.FacebookGraphAPI.GraphAPIDomain.GraphAPIInsightsFields import GraphAPIInsightsFields
from Core.Web.FacebookGraphAPI.Models.FieldsMetadata import FieldsMetadata
from FacebookAccounts.Api.dtos import accounts_ag_grid_view

import logging

logger = logging.getLogger(__name__)


INSIGHTS_KEY = "insights"
DATA_KEY = "data"


def handle_accounts_insights(request: Any, config: Any, fixtures: Any, ) -> List[Dict]:
    permanent_token = fixtures.business_owner_repository.get_permanent_token(request.business_owner_facebook_id)

    response = get_account_insights_base(
        permanent_token=permanent_token,
        business_owner_facebook_id=request.business_owner_facebook_id,
        from_date=request.from_date,
        to_date=request.to_date,
        config=config,
    )

    return response


def get_account_insights_base(
    permanent_token: typing.AnyStr,
    business_owner_facebook_id: typing.AnyStr,
    from_date: typing.AnyStr,
    to_date: typing.AnyStr,
    config: Any,
) -> typing.List[typing.Dict]:

    account_fields = get_facebook_fields(accounts_ag_grid_view.account_structure_columns)
    insights_fields = get_facebook_fields(accounts_ag_grid_view.account_insight_columns)

    _ = GraphAPISdkBase(config.facebook, permanent_token)

    insight_string = f"insights.time_range({{'since':'{from_date}','until':'{to_date}'}}){{{','.join(insights_fields)}}}"
    account_fields.append(insight_string)

    business = User(business_owner_facebook_id)
    response = business.get_ad_accounts(fields=account_fields)

    return _map_response(response)


def get_facebook_fields(view_fields: List[ViewColumn]) -> List[str]:
    facebook_fields = set()
    for column in view_fields:
        for facebook_field in column.primary_value.facebook_fields:
            facebook_fields.add(facebook_field)

    return list(facebook_fields)


def _map_response(response: List[Any] = None) -> typing.List[Dict]:
    result = []
    for entry in response:
        entry_result = {}
        for column in accounts_ag_grid_view.account_structure_columns:
            try:
                # Business id is nested inside of a dict even if it is an account structure info...
                if GraphAPIInsightsFields.business in entry:
                    if column.primary_value.name == FieldsMetadata.business_id.name:
                        entry_result.update({column.primary_value.name: entry["business"]["id"]})
                        continue

                    elif column.primary_value.name == FieldsMetadata.business_manager.name:
                        entry_result.update({column.primary_value.name: entry["business"]["name"]})
                        continue

                mapped_entry = column.primary_value.mapper.map(entry, column.primary_value)[0]
                if FieldsMetadata.account_status.name in mapped_entry:
                    mapped_entry[FieldsMetadata.account_status.name] = AccountStatus(
                        mapped_entry[FieldsMetadata.account_status.name]
                    ).name

                if FieldsMetadata.account_id.name in mapped_entry:
                    mapped_entry[FieldsMetadata.account_id.name] = f"act_{mapped_entry[FieldsMetadata.account_id.name]}"

                entry_result.update(mapped_entry)
            except Exception as e:
                logger.exception(f"Failed to map the {column.primary_value.name} field || {repr(e)}")

        if INSIGHTS_KEY not in entry and entry_result:
            result.append(entry_result)
            continue

        # Since the insights are at the account level, there is only one entry in the dict
        insights = entry[INSIGHTS_KEY][DATA_KEY][0]

        for column in accounts_ag_grid_view.account_insight_columns:
            try:
                entry_result.update(column.primary_value.mapper.map(insights, column.primary_value)[0])
            except Exception as e:
                logger.exception(f"Failed to map the {column.primary_value.name} field || {repr(e)}")

        if entry_result:
            result.append(entry_result)

    return result
