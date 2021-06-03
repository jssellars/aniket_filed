import logging
import typing
from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from functools import reduce
from typing import Dict, List

from Core.constants import DEFAULT_DATETIME
from Core.facebook.sdk_adapter.ad_objects.content_delivery_report import Placement
from Core.facebook.sdk_adapter.validations import PLACEMENT_X_OBJECTIVE
from Core.Tools.Misc.AgGridConstants import PositiveEffectTrendDirection, Trend
from Core.Tools.QueryBuilder.QueryBuilder import AgGridInsightsRequest, AgGridTrendRequest, QueryBuilderRequestMapper
from Core.Tools.QueryBuilder.QueryBuilderFacebookRequestParser import QueryBuilderFacebookRequestParser
from Core.Web.FacebookGraphAPI.GraphAPIMappings.LevelMapping import Level
from Core.Web.FacebookGraphAPI.Models.FieldsMetadata import FieldsMetadata
from FacebookTuring.Api.startup import config
from FacebookTuring.Infrastructure.Domain.FiledFacebookInsightsTableEnum import FiledFacebookInsightsTableEnum
from FacebookTuring.Infrastructure.GraphAPIHandlers.GraphAPIInsightsHandler import GraphAPIInsightsHandler
from FacebookTuring.Infrastructure.PersistenceLayer.TuringMongoRepository import TuringMongoRepository

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
    FieldsMetadata.campaign_name.name,
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


class AdsManagerInsightsCommandHandler(ABC):
    def __init__(self):
        self.query = QueryBuilderFacebookRequestParser()

    @abstractmethod
    def handle(self, query_json: Dict = None, business_owner_id: str = None, level: str = None):
        pass

    @abstractmethod
    def map_query(self, query_json: typing.Dict = None, level: typing.AnyStr = None, has_breakdowns: bool = True):
        pass


class AdsManagerInsightsReports(AdsManagerInsightsCommandHandler):
    def handle(
            self, query_json: typing.Dict = None, business_owner_id: typing.AnyStr = None, level: typing.AnyStr = None
    ) -> typing.List[typing.Dict]:
        self.map_query(query_json=query_json, has_breakdowns=True)

        # Get insights from the facebook graph api.
        response = GraphAPIInsightsHandler.get_insights_base(
            ad_account_id=self.query.facebook_id,
            fields=self.query.fields,
            parameters=self.query.parameters,
            requested_fields=self.query.requested_columns,
            level=self.query.level,
        )

        # If age_gender breakdown is requested only then.
        if self.query.breakdowns in [['age', 'gender'], ['gender', 'age']]:
            # Remove all the Null values.
            response_without_null = []
            for each_response in response:
                if each_response["cost_per_result"] is not None:
                    response_without_null.append(each_response)

            # Compute Average value of each breakdown.
            response_with_average = []
            all_age_gender = []

            # Grab all the age_gender breakdowns available.
            for each_response in response_without_null:
                if each_response["age_gender"] not in all_age_gender:
                    all_age_gender.append(each_response["age_gender"])

            # Find age_gender in all responses.
            for age_gender in all_age_gender:
                total_cost_per_result = []
                for each_response in response_without_null:
                    if age_gender == each_response["age_gender"]:
                        total_cost_per_result.append(each_response["cost_per_result"])
                    else:
                        continue

                # Compute Cost per result average.
                try:
                    cost_per_result_average = sum(total_cost_per_result) / len(total_cost_per_result)
                    cost_per_result_average = round(cost_per_result_average, 4)
                except ZeroDivisionError:
                    logger.debug("Failed to Calculate Cost Per Result Average")

                # Add each response average.
                each_response_average = {
                    "adset_id": each_response["adset_id"],
                    "adset_name": each_response["adset_name"],
                    "age_gender": age_gender,
                    "cost_per_result": cost_per_result_average,
                    "date_start": None
                }
                response_with_average.append(each_response_average)

            return response_with_average

        return response

    def map_query(self, query_json: typing.Dict = None, level: typing.AnyStr = None, has_breakdowns: bool = True):
        query_builder_request = QueryBuilderRequestMapper(query_json, FiledFacebookInsightsTableEnum)
        self.query.parse(query_builder_request, parse_breakdowns=has_breakdowns)


class AdsManagerInsightsAgGridInsights(AdsManagerInsightsCommandHandler):
    def handle(self, query_json: Dict = None, business_owner_id: str = None, level: str = None) -> Dict:
        self.map_query(query_json=query_json, level=level, has_breakdowns=True)

        return GraphAPIInsightsHandler.get_ag_grid_insights(
            config,
            level=level,
            query=self.query,
        )

    def map_query(self, query_json: typing.Dict = None, level: typing.AnyStr = None, has_breakdowns: bool = True):
        query_builder_request = AgGridInsightsRequest(query_builder_request=query_json)
        self.query.parse_ag_grid_insights_query(query_builder_request, level, parse_breakdowns=has_breakdowns)


class AdsManagerInsightsAgGridTrend(AdsManagerInsightsCommandHandler):
    def handle(
            self, query_json: typing.Dict = None, business_owner_id: typing.AnyStr = None, level: typing.AnyStr = None
    ) -> Dict:
        self.map_query(query_json=query_json, level=level, has_breakdowns=True)

        requested_columns = self.query.requested_columns
        if len(requested_columns) > 1:
            logger.exception("The ag grid trend endpoint should receive only one column.")
            raise Exception("The ag grid trend endpoint should receive only one column.")

        summary = self.get_summary(level, requested_columns)
        past_period_summary = self.get_past_period_summary(level, requested_columns)

        response = AdsManagerInsightsAgGridTrend.get_response(summary, past_period_summary, requested_columns)
        return response

    def map_query(self, query_json: typing.Dict = None, level: typing.AnyStr = None, has_breakdowns: bool = True):
        query_builder_request = AgGridTrendRequest(query_json)
        self.query.parse_ag_grid_trend_query(query_builder_request, level, parse_breakdowns=has_breakdowns)

    def get_summary(self, level: typing.AnyStr = None, requested_columns: List = None) -> List:
        _, _, summary = GraphAPIInsightsHandler.get_insights_page(
            level=level,
            ad_account_id=self.query.facebook_id,
            fields=self.query.fields,
            parameters=self.query.parameters,
            requested_fields=requested_columns,
        )

        return summary

    def get_past_period_summary(self, level: typing.AnyStr = None, requested_columns: List = None) -> List:
        since_date = datetime.strptime(self.query.time_range["since"], DEFAULT_DATETIME)
        until_date = datetime.strptime(self.query.time_range["until"], DEFAULT_DATETIME)
        time_interval_in_days = (until_date - since_date).days + 1

        self.query.time_range["since"] = (since_date - timedelta(days=time_interval_in_days)).date().isoformat()
        self.query.time_range["until"] = (until_date - timedelta(days=time_interval_in_days)).date().isoformat()

        _, _, past_period_summary = GraphAPIInsightsHandler.get_insights_page(
            level=level,
            ad_account_id=self.query.facebook_id,
            fields=self.query.fields,
            parameters=self.query.parameters,
            requested_fields=requested_columns,
        )

        return past_period_summary

    @staticmethod
    def get_response(result: List = None, past_period_result: List = None, requested_columns: List = None) -> Dict:
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


class AdsManagerInsightsAgGridPopup(AdsManagerInsightsCommandHandler):
    def handle(self, query_json: Dict = None, business_owner_id: str = None, level: str = None) -> Dict:
        popup_fields = AdsManagerInsightsAgGridPopup.get_popup_fields(level, query_json)
        query_json["agColumns"] = ",".join(popup_fields)
        self.map_query(query_json=query_json, level=level, has_breakdowns=True)

        insight_response, next_page_cursor, summary = GraphAPIInsightsHandler.get_insights_page(
            ad_account_id=self.query.facebook_id,
            fields=self.query.fields,
            parameters=self.query.parameters,
            requested_fields=self.query.requested_columns,
            level=level,
        )

        return {"nextPageCursor": next_page_cursor, "data": insight_response, "summary": summary}

    def map_query(self, query_json: typing.Dict = None, level: typing.AnyStr = None, has_breakdowns: bool = True):
        query_builder_request = AgGridInsightsRequest(query_builder_request=query_json)
        self.query.parse_ag_grid_insights_query(query_builder_request, level, parse_breakdowns=has_breakdowns)

    @staticmethod
    def get_popup_fields(query_json: typing.Dict = None, level: typing.AnyStr = None) -> List:
        popup_fields = []

        if level == Level.CAMPAIGN.value:
            placements = query_json.get("placements")
            if placements:
                validation_keys = [placement["platformKey"] for placement in placements]
                campaign_ids = AdsManagerInsightsAgGridPopup.get_valid_campaign_ids(validation_keys, query_json)
                query_json["filterModel"].update(
                    {"campaign_id": {"filter": campaign_ids, "filterType": "campaign_id", "type": "inValues"}}
                )
        else:
            popup_fields.extend([*BASE_POPUP_FIELDS, FieldsMetadata.adset_name.name])

        return popup_fields

    @staticmethod
    def get_valid_campaign_ids(validation_keys: List, query_json: Dict) -> List:

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
