import json
from enum import Enum

import pytest

from Core.test_config import PIXEL_ID


class PixelInsightsField(Enum):
    BREAKDOWN = "breakdown"
    COUNT = "count"
    TIMESTAMP = "timestamp"
    VALUE = "value"


class TestPixelInsights:

    post_data = {
        "facebookId": PIXEL_ID,
        "facebookName": "",
        "breakdown": "browser_type",
        "startTime": "2021-02-27",
        "endTime": "2021-03-05",
        "level": "pixel",
    }

    @pytest.fixture(scope="session")
    def response(self, client, config):
        url = f"/api/v1/pixel/insights"
        return client.post(url, json=self.post_data, headers=config["headers"])

    @pytest.fixture(scope="session")
    def response_json(self, response):
        data = response.data.decode("UTF-8")
        return json.loads(data)

    def test_status_code_200(self, response):
        assert response.status_code == 200

    def test_return_type_is_list(self, response_json):
        assert isinstance(response_json, list)

    def test_breakdown_is_non_empty_string(self, response_json):
        for response in response_json:
            breakdown = response.get(PixelInsightsField.BREAKDOWN.value)
            assert isinstance(breakdown, str)
            assert len(breakdown) > 0

    def test_count_is_positive_int(self, response_json):
        for response in response_json:
            count = response.get(PixelInsightsField.COUNT.value)
            assert isinstance(count, int)
            assert count > 0

    def test_timestamp_is_non_empty_string(self, response_json):
        for response in response_json:
            timestamp = response.get(PixelInsightsField.TIMESTAMP.value)
            assert isinstance(timestamp, str)
            assert len(timestamp) > 0

    def test_value_is_non_empty_string(self, response_json):
        for response in response_json:
            value = response.get(PixelInsightsField.VALUE.value)
            assert isinstance(value, str)
            assert len(value) > 0
