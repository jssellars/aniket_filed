import json
from enum import Enum

import pytest

from Core.test_config import ACCOUNT_ID


class GetRecommendationField(Enum):
    TIME_INTERVAL = "timeInterval"
    CHANNEL = "channel"
    PRIORITY = "priority"
    BUSINESS_OWNER_ID = "businessOwnerId"
    STRUCTURE_ID = "structureId"
    STRUCTURE_NAME = "structureName"
    LEVEL = "level"
    METRICS = "metrics"
    DISPLAY_NAME = "displayName"
    NAME = "name"
    BREAKDOWN = "breakdown"
    ANALYSIS = "analysis"
    TITLE = "title"
    SUBTEXT = "subText"
    QUOTE = "quote"
    AD_ACCOUNT_ID = "adAccountId"
    RECOMMENDATION_ID = "recommendationId"
    IS_APPLICABLE = "isApplicable"
    RECOMMENDATIONS = "recommendations"


class TestGetRecommendation:
    post_data = {"adAccountId": ACCOUNT_ID, "pageSize": 100, "pageNumber": 1}

    channel_list = ["facebook"]
    priority_list = ["High", "Medium", "Low"]
    level_list = ["campaign", "adset", "ad"]

    @pytest.fixture(scope="session")
    def response(self, client, config):
        url = f"/api/v1/get-recommendations"
        return client.post(url, json=self.post_data, headers=config["headers"])

    @pytest.fixture(scope="session")
    def response_json(self, response):
        data = response.data.decode("UTF-8")
        return json.loads(data)

    def test_status_code_200(self, response):
        assert response.status_code == 200

    def test_return_type_is_dict(self, response_json):
        assert isinstance(response_json, dict)

    def test_data_in_dict_is_list(self, response_json):
        assert GetRecommendationField.RECOMMENDATIONS.value in response_json
        recommendations = response_json[GetRecommendationField.RECOMMENDATIONS.value]
        assert isinstance(recommendations, list)

    @pytest.fixture(scope="session")
    def recommendations(self, response_json):
        recommendations = response_json[GetRecommendationField.RECOMMENDATIONS.value]
        return recommendations

    def test_data_in_list_is_non_empty_dict(self, recommendations):
        for response in recommendations:
            assert isinstance(response, dict)
            assert len(response) == 16

    def test_time_interval_is_positive_int(self, recommendations):
        for response in recommendations:
            assert GetRecommendationField.TIME_INTERVAL.value in response
            time_interval = response[GetRecommendationField.TIME_INTERVAL.value]
            assert isinstance(time_interval, int)
            assert time_interval >= 0

    def test_channel_is_non_empty_string(self, recommendations):
        for response in recommendations:
            assert GetRecommendationField.CHANNEL.value in response
            channel = response[GetRecommendationField.CHANNEL.value]
            assert isinstance(channel, str)
            assert channel in self.channel_list

    def test_priority_is_non_empty_string(self, recommendations):
        for response in recommendations:
            assert GetRecommendationField.PRIORITY.value in response
            priority = response[GetRecommendationField.PRIORITY.value]
            assert isinstance(priority, str)
            assert priority in self.priority_list

    def test_business_owner_id_is_numeric_string(self, recommendations):
        for response in recommendations:
            assert GetRecommendationField.BUSINESS_OWNER_ID.value in response
            business_owner_id = response[GetRecommendationField.BUSINESS_OWNER_ID.value]
            assert isinstance(business_owner_id, str)
            assert len(business_owner_id) > 0
            assert business_owner_id.isnumeric()

    def test_structure_id_is_numeric_string(self, recommendations):
        for response in recommendations:
            assert GetRecommendationField.STRUCTURE_ID.value in response
            structure_id = response[GetRecommendationField.STRUCTURE_ID.value]
            assert isinstance(structure_id, str)
            assert len(structure_id) > 0
            assert structure_id.isnumeric()

    def test_structure_name_is_non_empty_string(self, recommendations):
        for response in recommendations:
            assert GetRecommendationField.STRUCTURE_NAME.value in response
            structure_name = response[GetRecommendationField.STRUCTURE_NAME.value]
            assert isinstance(structure_name, str)
            assert len(structure_name) > 0

    def test_level_is_non_empty_string(self, recommendations):
        for response in recommendations:
            assert GetRecommendationField.LEVEL.value in response
            level = response[GetRecommendationField.LEVEL.value]
            assert isinstance(level, str)
            assert level in self.level_list

    def test_metrics_is_list_with_len_1(self, recommendations):
        for response in recommendations:
            assert GetRecommendationField.METRICS.value in response
            metrics = response[GetRecommendationField.METRICS.value]
            assert isinstance(metrics, list)
            assert len(metrics) == 1

    def test_metrics_data_in_list_is_dict_with_len_2(self, recommendations):
        for response in recommendations:
            for data in response[GetRecommendationField.METRICS.value]:
                assert isinstance(data, dict)
                assert len(data) == 2

    def test_metrics_display_name_is_non_empty_string(self, recommendations):
        for response in recommendations:
            metrics = response[GetRecommendationField.METRICS.value][0]
            assert GetRecommendationField.DISPLAY_NAME.value in metrics
            display_name = metrics[GetRecommendationField.DISPLAY_NAME.value]
            assert isinstance(display_name, str)
            assert len(display_name) > 0

    def test_metrics_name_is_non_empty_string(self, recommendations):
        for response in recommendations:
            metrics = response[GetRecommendationField.METRICS.value][0]
            assert GetRecommendationField.NAME.value in metrics
            name = metrics[GetRecommendationField.NAME.value]
            assert isinstance(name, str)
            assert len(name) > 0

    def test_breakdowns_is_dict_with_len_2(self, recommendations):
        for response in recommendations:
            assert GetRecommendationField.BREAKDOWN.value in response
            breakdowns = response[GetRecommendationField.BREAKDOWN.value]
            assert isinstance(breakdowns, dict)
            assert len(breakdowns) == 2

    def test_breakdown_display_name_is_non_empty_string(self, recommendations):
        for response in recommendations:
            assert GetRecommendationField.DISPLAY_NAME.value in response[GetRecommendationField.BREAKDOWN.value]
            display_name = response[GetRecommendationField.BREAKDOWN.value][GetRecommendationField.DISPLAY_NAME.value]
            assert isinstance(display_name, str)
            assert len(display_name) > 0

    def test_breakdown_name_is_non_empty_string(self, recommendations):
        for response in recommendations:
            assert GetRecommendationField.NAME.value in response[GetRecommendationField.BREAKDOWN.value]
            name = response[GetRecommendationField.BREAKDOWN.value][GetRecommendationField.NAME.value]
            assert isinstance(name, str)
            assert len(name) > 0

    def test_analysis_is_non_empty_string(self, recommendations):
        for response in recommendations:
            assert GetRecommendationField.ANALYSIS.value in response
            analysis = response[GetRecommendationField.ANALYSIS.value]
            assert isinstance(analysis, str)
            assert len(analysis) > 0

    def test_title_is_non_empty_string(self, recommendations):
        for response in recommendations:
            assert GetRecommendationField.TITLE.value in response
            title = response[GetRecommendationField.TITLE.value]
            assert isinstance(title, str)
            assert len(title) > 0

    def test_subtext_is_non_empty_string(self, recommendations):
        for response in recommendations:
            assert GetRecommendationField.SUBTEXT.value in response
            subtext = response[GetRecommendationField.SUBTEXT.value]
            assert isinstance(subtext, str)
            assert len(subtext) > 0

    def test_quote_is_non_empty_string(self, recommendations):
        for response in recommendations:
            assert GetRecommendationField.QUOTE.value in response
            quote = response[GetRecommendationField.QUOTE.value]
            assert isinstance(quote, str)
            assert len(quote) > 0

    def test_ad_account_id_is_non_empty_string(self, recommendations):
        for response in recommendations:
            assert GetRecommendationField.AD_ACCOUNT_ID.value in response
            ad_account_id = response[GetRecommendationField.AD_ACCOUNT_ID.value]
            assert isinstance(ad_account_id, str)
            assert len(ad_account_id) > 0

    def test_recommendation_id_is_non_empty_string(self, recommendations):
        for response in recommendations:
            assert GetRecommendationField.RECOMMENDATION_ID.value in response
            recommendation_id = response[GetRecommendationField.RECOMMENDATION_ID.value]
            assert isinstance(recommendation_id, str)
            assert len(recommendation_id) > 0

    def test_is_applicable_is_bool(self, recommendations):
        for response in recommendations:
            assert GetRecommendationField.IS_APPLICABLE.value in response
            is_applicable = response[GetRecommendationField.IS_APPLICABLE.value]
            assert isinstance(is_applicable, bool)
