import logging
import typing
from datetime import datetime, timedelta
from functools import reduce
from typing import Dict, List

from Core.constants import DEFAULT_DATETIME
from Core.facebook.sdk_adapter.ad_objects.content_delivery_report import \
    Placement
from Core.facebook.sdk_adapter.validations import PLACEMENT_X_OBJECTIVE
from Core.Tools.Misc.AgGridConstants import PositiveEffectTrendDirection, Trend
from Core.Tools.QueryBuilder.QueryBuilder import (AgGridInsightsRequest,
                                                  AgGridTrendRequest,
                                                  QueryBuilderRequestMapper)
from Core.Tools.QueryBuilder.QueryBuilderFacebookRequestParser import \
    QueryBuilderFacebookRequestParser
from Core.Web.FacebookGraphAPI.GraphAPIMappings.LevelMapping import Level
from Core.Web.FacebookGraphAPI.Models.FieldsMetadata import FieldsMetadata
from FacebookTuring.Api.Commands.AdsManagerInsightsCommand import \
    AdsManagerInsightsCommandEnum
from FacebookTuring.Api.startup import config, fixtures
from FacebookTuring.Infrastructure.Domain.FiledFacebookInsightsTableEnum import \
    FiledFacebookInsightsTableEnum
from FacebookTuring.Infrastructure.GraphAPIHandlers.GraphAPIInsightsHandler import \
    GraphAPIInsightsHandler
from FacebookTuring.Infrastructure.PersistenceLayer.TuringMongoRepository import \
    TuringMongoRepository

logger = logging.getLogger(__name__)

PERCENTAGE_DIFFERENCE_KEY = "percentage_difference"
TREND_KEY = "trend"
BASE_POPUP_FIELDS = [
    FieldsMetadata.impressions.name,
    FieldsMetadata.reach.name,
    FieldsMetadata.unique_link_clicks.name,
    FieldsMetadata.ctr_all.name,
    FieldsMetadata.cpc_all.name,
    FieldsMetadata.campaign_id.name,
    FieldsMetadata.adset_id.name,
]
# TODO: Discuss with FE on structure of placements in request for ag_grid_popup
DEFAULT_PLACEMENT_POSITIONS = {
    "FACEBOOK": [
        Placement.FACEBOOK_FEED,
        Placement.FACEBOOK_STORIES,
    ],
    "INSTAGRAM": [
        Placement.INSTAGRAM_FEED,
        Placement.INSTAGRAM_STORIES,
    ],
    "AUDIENCE_NETWORK": [
        Placement.AUDIENCE_NETWORK_NATIVE_BANNER_AND_INTERSTITIAL,
    ],
}


class AdsManagerInsightsCommandHandler:

    @classmethod
    def handle(cls,
               handler_type: AdsManagerInsightsCommandEnum = None,
               query_json: typing.Dict = None,
               business_owner_id: typing.AnyStr = None,
               level: typing.AnyStr = None) -> typing.List[typing.Dict]:
        handlers = {
            AdsManagerInsightsCommandEnum.INSIGHTS: cls.get_insights,
            AdsManagerInsightsCommandEnum.INSIGHTS_WITH_TOTALS: cls.get_insights_with_totals,
            AdsManagerInsightsCommandEnum.REPORTS: cls.get_reports_insights,
            AdsManagerInsightsCommandEnum.AG_GRID_INSIGHTS: cls.get_ag_grid_insights,
            AdsManagerInsightsCommandEnum.AG_GRID_INSIGHTS_TREND: cls.get_ag_grid_trend,
            AdsManagerInsightsCommandEnum.AG_GRID_ADD_AN_ADSET_AD_PARENT: cls.get_ag_grid_popup
        }
        handler = handlers.get(handler_type, None)
        if handler is None:
            raise ValueError('Invalid insights handler: %s' % handler_type.value)

        return handler(query_json=query_json, business_owner_id=business_owner_id, level=level)

    @classmethod
    def map_query(cls, query: typing.Dict = None, has_breakdowns: bool = True) -> QueryBuilderFacebookRequestParser:
        query_builder_request = QueryBuilderRequestMapper(query, FiledFacebookInsightsTableEnum)
        query = QueryBuilderFacebookRequestParser()
        query.parse(query_builder_request, parse_breakdowns=has_breakdowns)
        return query

    @classmethod
    def map_ag_grid_insights_query(cls, query: typing.Dict = None,
                                   level: typing.AnyStr = None,
                                   has_breakdowns: bool = True) -> QueryBuilderFacebookRequestParser:
        query_builder_request = AgGridInsightsRequest(query_builder_request=query)
        query = QueryBuilderFacebookRequestParser()
        query.parse_ag_grid_insights_query(query_builder_request, level, parse_breakdowns=has_breakdowns)
        return query

    @classmethod
    def map_ag_grid_trend_query(cls, query: typing.Dict = None,
                                level: typing.AnyStr = None,
                                has_breakdowns: bool = True) -> QueryBuilderFacebookRequestParser:
        query_builder_request = AgGridTrendRequest(query)
        query = QueryBuilderFacebookRequestParser()
        query.parse_ag_grid_trend_query(query_builder_request, level, parse_breakdowns=has_breakdowns)
        return query

    @classmethod
    def get_insights(cls,
                     query_json: typing.Dict = None,
                     business_owner_id: typing.AnyStr = None,
                     level: typing.AnyStr = None) -> List[Dict]:
        permanent_token = (
            fixtures.business_owner_repository.get_permanent_token(business_owner_id)
        )
        query = cls.map_query(query_json, has_breakdowns=True)
        response = GraphAPIInsightsHandler.get_insights(
            config,
            permanent_token=permanent_token,
            level=query.level,
            ad_account_id=query.facebook_id,
            fields=query.fields,
            parameters=query.parameters,
            structure_fields=query.structure_fields,
            requested_fields=query.requested_columns,
            filter_params=query.filtering
        )
        return response

    @classmethod
    def get_insights_with_totals(cls,
                                 query_json: typing.Dict = None,
                                 business_owner_id: typing.AnyStr = None,
                                 level: typing.AnyStr = None) -> typing.Dict:
        permanent_token = fixtures.business_owner_repository.get_permanent_token(business_owner_id)
        query = cls.map_query(query_json, has_breakdowns=True)
        response = GraphAPIInsightsHandler.get_insights_with_totals(
            config,
            permanent_token=permanent_token,
            level=query.level,
            ad_account_id=query.facebook_id,
            fields=query.fields,
            parameters=query.parameters,
            structure_fields=query.structure_fields,
            requested_fields=query.requested_columns,
            filter_params=query.filtering
        )
        return response

    @classmethod
    def get_ag_grid_insights(cls,
                             query_json: Dict = None,
                             business_owner_id: str = None,
                             level: str = None) -> Dict:
        permanent_token = fixtures.business_owner_repository.get_permanent_token(business_owner_id)
        query = cls.map_ag_grid_insights_query(query_json, level, has_breakdowns=True)

        return GraphAPIInsightsHandler.get_ag_grid_insights(
            config,
            permanent_token=permanent_token,
            level=level,
            query=query,
        )

    @classmethod
    def get_ag_grid_popup(cls,
                          query_json: Dict = None,
                          business_owner_id: str = None,
                          level: str = None) -> Dict:

        permanent_token = fixtures.business_owner_repository.get_permanent_token(business_owner_id)
        popup_fields = []

        if level == Level.CAMPAIGN.value:
            popup_fields.extend([*BASE_POPUP_FIELDS, FieldsMetadata.campaign_name.name])
            placements = query_json.get("placements")
            if placements:
                validation_keys = [placement["platformKey"] for placement in placements]
                campaign_ids = cls.get_valid_campaign_ids(validation_keys, query_json)
                query_json['filterModel'].update({
                    "campaign_id": {
                        "filter": campaign_ids,
                        "filterType": "campaign_id",
                        "type": "inValues"
                    }
                })
        else:
            popup_fields.extend([*BASE_POPUP_FIELDS, FieldsMetadata.adset_name.name])

        query_json['agColumns'] = ",".join(popup_fields)
        query = cls.map_ag_grid_insights_query(query_json, level, has_breakdowns=True)

        insight_response, next_page_cursor, summary = GraphAPIInsightsHandler.get_insights_page(
            config,
            permanent_token=permanent_token,
            ad_account_id=query.facebook_id,
            fields=query.fields,
            parameters=query.parameters,
            requested_fields=query.requested_columns,
            add_totals=True,
            next_page_cursor=query.next_page_cursor,
            level=level,
            page_size=query.page_size,
        )

        return {"nextPageCursor": next_page_cursor, "data": insight_response, "summary": summary}

    @classmethod
    def get_ag_grid_trend(cls,
                          query_json: typing.Dict = None,
                          business_owner_id: typing.AnyStr = None,
                          level: typing.AnyStr = None) -> Dict:

        permanent_token = fixtures.business_owner_repository.get_permanent_token(business_owner_id)
        query = cls.map_ag_grid_trend_query(query_json, level, has_breakdowns=True)

        requested_columns = query.requested_columns
        if len(requested_columns) > 1:
            logger.exception("The ag grid trend endpoint should receive only one column.")
            raise Exception("The ag grid trend endpoint should receive only one column.")

        _, _, result = GraphAPIInsightsHandler.get_insights_page(
            config,
            permanent_token=permanent_token,
            level=level,
            ad_account_id=query.facebook_id,
            fields=query.fields,
            parameters=query.parameters,
            add_totals=True,
            requested_fields=requested_columns,
            next_page_cursor=query.next_page_cursor,
            page_size=1,
        )

        since_date = datetime.strptime(query.time_range["since"], DEFAULT_DATETIME)
        until_date = datetime.strptime(query.time_range["until"], DEFAULT_DATETIME)
        time_interval_in_days = (until_date - since_date).days + 1

        query.time_range["since"] = (since_date - timedelta(days=time_interval_in_days)).date().isoformat()
        query.time_range["until"] = (until_date - timedelta(days=time_interval_in_days)).date().isoformat()

        _, _, past_period_result = GraphAPIInsightsHandler.get_insights_page(
            config,
            permanent_token=permanent_token,
            level=level,
            ad_account_id=query.facebook_id,
            fields=query.fields,
            parameters=query.parameters,
            add_totals=True,
            requested_fields=requested_columns,
            next_page_cursor=query.next_page_cursor,
            page_size=1,
        )

        required_metric = requested_columns[0].name
        positive_effect_trend_direction = requested_columns[0].positive_effect_trend_direction

        # TODO think of a way to redefine the contract and make some fields optional
        if not result or not result[0] or not result[0].get(required_metric):
            return {required_metric: None, PERCENTAGE_DIFFERENCE_KEY: None, TREND_KEY: Trend.UNDEFINED.name}

        metric_result = result[0][required_metric]

        if not past_period_result or not past_period_result[0] or not past_period_result[0].get(required_metric):
            return {required_metric: metric_result, PERCENTAGE_DIFFERENCE_KEY: None, TREND_KEY: Trend.UNDEFINED.name}

        previous_period_metric_result = past_period_result[0][required_metric]
        percentage_difference = (metric_result / previous_period_metric_result - 1) * 100

        trend = Trend.NEGATIVE.name if positive_effect_trend_direction else Trend.UNDEFINED.name
        if percentage_difference < 0 and positive_effect_trend_direction == PositiveEffectTrendDirection.DECREASING:
            trend = Trend.POSITIVE.name
        elif percentage_difference > 0 and positive_effect_trend_direction == PositiveEffectTrendDirection.INCREASING:
            trend = Trend.POSITIVE.name

        return {required_metric: metric_result, PERCENTAGE_DIFFERENCE_KEY: percentage_difference, TREND_KEY: trend}

    @classmethod
    def get_reports_insights(
            cls,
            query_json: typing.Dict = None,
            business_owner_id: typing.AnyStr = None,
            level: typing.AnyStr = None
    ) -> typing.List[typing.Dict]:
        permanent_token = fixtures.business_owner_repository.get_permanent_token(business_owner_id)
        query = cls.map_query(query_json, has_breakdowns=True)
        response = GraphAPIInsightsHandler.get_reports_insights(
            config,
            permanent_token=permanent_token,
            ad_account_id=query.facebook_id,
            fields=query.fields,
            parameters=query.parameters,
            requested_fields=query.requested_columns,
            level=query.level
        )
        return response

    @classmethod
    def get_valid_campaign_ids(cls,
                               validation_keys: List,
                               query_json: Dict) -> List:

        mapped_keys = []
        for validation_key in validation_keys:
            if validation_key in DEFAULT_PLACEMENT_POSITIONS:
                mapped_keys.extend(DEFAULT_PLACEMENT_POSITIONS[validation_key])

        valid_objectives = [val for key, val in PLACEMENT_X_OBJECTIVE.items() if key in mapped_keys]
        common_objectives = reduce(set.intersection, valid_objectives)
        common_objectives = [objective.value.name_sdk for objective in common_objectives]

        repository = TuringMongoRepository(
            config=config.mongo,
            database_name=config.mongo.structures_database_name,
        )

        query_result = repository.get_campaigns_by_objectives(common_objectives, query_json["facebookAccountId"][4:])
        campaign_ids = [result["campaign_id"] for result in query_result]

        return campaign_ids
