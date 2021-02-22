import urllib.parse as urlparse
from time import sleep
from urllib.parse import parse_qs
from typing import Dict, List, Optional, Any, Tuple

from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.adobjects.adreportrun import AdReportRun
import json

from facebook_business.api import Cursor

from Core.Dexter.Infrastructure.Domain.LevelEnums import LevelIdKeyEnum
from Core.Tools.QueryBuilder.QueryBuilderLogicalOperator import AgGridFacebookOperator
from Core.Web.FacebookGraphAPI.GraphAPIMappings.LevelMapping import Level


def get_sdk_structures(ad_account_id: str, level: Level, fields: List[str], params: Dict = None) -> Optional[Cursor]:
    ad_account = AdAccount(ad_account_id)

    if level == Level.CAMPAIGN:
        return ad_account.get_campaigns(fields=fields, params=params)
    elif level == Level.ADSET:
        return ad_account.get_ad_sets(fields=fields, params=params)
    elif level == Level.AD:
        return ad_account.get_ads(fields=fields, params=params)

    return None


def get_sdk_insights_page(
        ad_account_id: str, fields: List[str], parameters: Dict, level: Level
) -> Tuple[Optional[List], Optional[Dict], Optional[str]]:
    ad_account = AdAccount(ad_account_id)

    if level == Level.AD and not are_structures_filtered(parameters["filtering"]):
        insights_report = ad_account.get_insights_async(fields=fields, params=parameters)
        insights_report.api_get()

        while insights_report[AdReportRun.Field.async_status] != "Job Completed":
            sleep(1)
            insights_report.api_get()

        insights = insights_report.get_insights(params=parameters)

    else:
        insights = ad_account.get_insights(fields=fields, params=parameters)

    if not insights:
        return None, None, None

    summary = insights.summary() if parameters["default_summary"] else None

    # iterate like this to avoid swapping page on the iterator
    insights_response = []
    for i in range(0, len(insights)):
        insights_response.append(insights[i])

    next_page_cursor = get_next_page_cursor(insights)

    return insights_response, next_page_cursor, json.loads(summary[10:])


def create_facebook_filter(field: str, operator: AgGridFacebookOperator, value: Any) -> Dict:
    return {"field": field, "operator": operator.name, "value": value}


def get_next_page_cursor(cursor: Cursor) -> Optional[str]:
    cursor.params["default_summary"] = True

    if cursor.load_next_page():
        parsed = urlparse.urlparse(cursor._path)
        after_token = parse_qs(parsed.query).get("after")
        if after_token:
            return after_token[0]

    return None


def are_structures_filtered(filtering: List) -> bool:
    filters = json.loads(filtering)
    for current_filter in filters:
        if current_filter["field"].replace(".", "_") in [key.value for key in LevelIdKeyEnum]:
            return True

    return False
