import functools
import json
import operator
import urllib.parse as urlparse
from dataclasses import asdict
from typing import Any, Dict, List, Optional, Tuple
from urllib.parse import parse_qs

from bson import BSON
from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.api import Cursor
from facebook_business.exceptions import FacebookUnavailablePropertyException

from Core.Dexter.Infrastructure.Domain.LevelEnums import LevelEnum, LevelIdKeyEnum
from Core.Tools.QueryBuilder.QueryBuilderLogicalOperator import AgGridFacebookOperator
from Core.Web.FacebookGraphAPI.GraphAPIDomain.FacebookMiscFields import FacebookMiscFields, FacebookParametersStrings
from Core.Web.FacebookGraphAPI.GraphAPIDomain.GraphAPIInsightsFields import GraphAPIInsightsFields
from Core.Web.FacebookGraphAPI.GraphAPIMappings.GraphAPIInsightsMapper import GraphAPIInsightsMapper
from Core.Web.FacebookGraphAPI.GraphAPIMappings.LevelMapping import Level, LevelToFacebookIdKeyMapping
from Core.Web.FacebookGraphAPI.GraphAPIMappings.StructureMapping import StructureFields, StructureMapping
from Core.Web.FacebookGraphAPI.Models.Field import Field, FieldType
from Core.Web.FacebookGraphAPI.Models.FieldsMetadata import FieldsMetadata

LEVEL_TO_STRUCTURE_FIELDS = {
    Level.CAMPAIGN.value: [
        FieldsMetadata.account_name,
        FieldsMetadata.account_id,
        FieldsMetadata.campaign_name,
        FieldsMetadata.campaign_id,
    ],
    Level.ADSET.value: [
        FieldsMetadata.account_name,
        FieldsMetadata.account_id,
        FieldsMetadata.campaign_id,
        FieldsMetadata.campaign_name,
        FieldsMetadata.adset_name,
        FieldsMetadata.adset_id,
    ],
    Level.AD.value: [
        FieldsMetadata.account_name,
        FieldsMetadata.account_id,
        FieldsMetadata.campaign_id,
        FieldsMetadata.campaign_name,
        FieldsMetadata.adset_id,
        FieldsMetadata.adset_name,
        FieldsMetadata.ad_name,
        FieldsMetadata.ad_id,
    ],
}


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

    structure_ids, next_page_cursor = get_structure_ids_and_page_cursor_for_page(level, parameters, ad_account)

    insights = ad_account.get_insights(fields=fields, params=parameters)

    try:
        summary = insights.summary() if parameters["default_summary"] else None
    except FacebookUnavailablePropertyException:
        summary = {}

    if summary:
        summary = json.loads(summary[10:])

    # iterate like this to avoid swapping page on the iterator
    insights_response = []
    for i in range(0, len(insights)):
        insights_response.append(insights[i])

    return insights_response, next_page_cursor, summary


def get_structure_ids_and_page_cursor_for_page(
    level: Level, parameters: Dict, ad_account: AdAccount
) -> Tuple[Optional[List[str]], Optional[str]]:
    structure_key = LevelIdKeyEnum[level.value.upper()].value

    insights = ad_account.get_insights(fields=[structure_key], params=parameters)

    if not insights:
        return None, None

    structure_ids = []
    for i in range(0, len(insights)):
        structure_ids.append(insights[i][structure_key])

    next_page_cursor = get_next_page_cursor(insights)

    if level != Level.ACCOUNT:
        parameters[FacebookParametersStrings.filtering] = [
            create_facebook_filter(structure_key.replace("_", "."), AgGridFacebookOperator.IN, structure_ids)
        ]

    # Return the next cursor for the structure ids data, not for the insights
    parameters.pop("after", None)

    return structure_ids, next_page_cursor


def create_facebook_filter(field: str, operator: AgGridFacebookOperator, value: Any) -> Dict:
    return {"field": field, "operator": operator.name, "value": value}


def get_next_page_cursor(cursor: Cursor) -> Optional[str]:
    if cursor._finished_iteration:
        return None

    parsed = urlparse.urlparse(cursor._path)
    after_token = parse_qs(parsed.query).get("after")
    if after_token:
        return after_token[0]

    return None


def are_structures_filtered(filtering: List) -> bool:
    for current_filter in filtering:
        if current_filter["field"].replace(".", "_") in [key.value for key in LevelIdKeyEnum]:
            return True

    return False


def add_results_to_response(level: str, response: List, account_id: str):
    if not response:
        return

    structure_key = LevelToFacebookIdKeyMapping.ADSET.value
    if level == Level.CAMPAIGN.value or level == Level.ADSET.value:
        structure_key = LevelToFacebookIdKeyMapping.get_enum_by_name(level.upper()).value
    elif level == Level.AD.value:
        structure_key = LevelToFacebookIdKeyMapping.get_enum_by_name(Level.ADSET.value.upper()).value
    structure_ids = list({x[structure_key] for x in response if structure_key in x})

    params = {
        FacebookParametersStrings.filtering: [
            json.dumps(
                create_facebook_filter(structure_key.replace("_", "."), AgGridFacebookOperator.IN, structure_ids)
            )
        ]
    }
    fields = [GraphAPIInsightsFields.promoted_object, structure_key, GraphAPIInsightsFields.optimization_goal]
    structure_results = AdAccount(account_id).get_ad_sets(fields=fields, params=params)

    mapped_structures = []
    for structure in structure_results:
        structure = structure.export_all_data()
        structure["adset_id"] = structure.pop("id")

        promoted_event = structure.pop(GraphAPIInsightsFields.promoted_object, None)
        if promoted_event:
            if "pixel_id" in promoted_event:
                structure[GraphAPIInsightsFields.custom_event_type] = promoted_event.get(
                    GraphAPIInsightsFields.custom_event_type, None
                )
        mapped_structures.append(structure)

    __join_insights_and_structure_results(
        structure_key=structure_key, insight_response=response, structure_results=mapped_structures
    )


def __join_insights_and_structure_results(
    structure_key: str = None,
    insight_response: List = None,
    structure_results: List = None,
) -> List:
    for insight in insight_response:
        possible_objective = []
        for structure in structure_results:
            if insight[structure_key] == structure[structure_key]:
                if (
                    GraphAPIInsightsFields.custom_event_type in structure
                    and structure[GraphAPIInsightsFields.custom_event_type]
                ):
                    if structure[GraphAPIInsightsFields.custom_event_type] not in possible_objective:
                        possible_objective.append(structure[GraphAPIInsightsFields.custom_event_type])
                elif (
                    GraphAPIInsightsFields.optimization_goal in structure
                    and structure[GraphAPIInsightsFields.optimization_goal]
                ):
                    if structure[GraphAPIInsightsFields.optimization_goal] not in possible_objective:
                        possible_objective.append(structure[GraphAPIInsightsFields.optimization_goal])
                if len(possible_objective) > 1:
                    insight.update({FieldsMetadata.result_type.name: "multiple_conversion_types"})
                    break
                insight.update(structure)
    return insight_response


def get_dexter_insights(ad_account_id: str, level: Level, breakdown: Field, fields: List[str], parameters: Dict):
    ad_account = AdAccount(ad_account_id)

    # TODO: change how fields param is constructed to avoid using this requested_fb_fields
    fields.extend([x.name for x in LEVEL_TO_STRUCTURE_FIELDS[level.value]])

    if breakdown != FieldsMetadata.breakdown_none:
        fields.append(breakdown.name)

    insights = ad_account.get_insights(fields=get_insights_metrics(fields), params=parameters)

    insights = [insight.export_all_data() for insight in insights]

    results_requested = any(
        [FieldsMetadata.results.name == x or FieldsMetadata.cost_per_result.name == x for x in fields]
    )

    if results_requested:
        add_results_to_response(level.value, insights, ad_account_id)
    insights_response = (
        GraphAPIInsightsMapper().map(requested_fields=get_fieldsmetadata_from_str_list(fields), response=insights)
        if insights
        else []
    )

    for entry in insights_response:
        if breakdown.name not in entry:
            entry.update({"breakdown": breakdown.name})

    return insights_response


def get_insights_metrics(requested_fields: List[str]):
    fb_fields = []
    for field in requested_fields:
        entry = getattr(FieldsMetadata, field, None)

        if not entry:
            continue

        if entry.field_type == FieldType.INSIGHT or entry.field_type == FieldType.ACTION_INSIGHT:
            fb_fields.append(entry.facebook_fields)

    fields = functools.reduce(operator.iconcat, fb_fields, [])
    return list(set(fields))


def get_fieldsmetadata_from_str_list(required_fields: List[str]):
    fields_metadata_list = []
    for field in required_fields:
        entry = getattr(FieldsMetadata, field, None)

        if entry:
            fields_metadata_list.append(entry)

    return fields_metadata_list


def get_and_map_structures(ad_account_id: str, level: LevelEnum, filtering: Optional[Dict]) -> Optional[List]:
    sdk_structures = get_sdk_structures(
        ad_account_id,
        Level[level.value.upper()],
        fields=StructureFields.get(level.value).get_structure_fields(),
        params={FacebookParametersStrings.filtering: [filtering]},
    )

    structures = []

    for structure in sdk_structures:
        mapping = StructureMapping.get(level.value)
        updated_structure = mapping.load(structure.export_all_data())
        updated_structure = asdict(updated_structure)
        # TODO: Remove the BSON encoding (legacy from MongoDB)
        updated_structure[FacebookMiscFields.details] = BSON.decode(updated_structure.get(FacebookMiscFields.details))
        structures.append(updated_structure)

    return structures
