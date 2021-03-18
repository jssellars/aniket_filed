import json

import pytest

from Core.test_config import ACCOUNT_ID


class TestAccountsAgGridTrend:

    post_data = {
        "filterModel": {},
        "agColumns": "cpm",
        "timeRange": {"since": "2021-02-17", "until": "2021-02-23"},
        "facebookAccountId": ACCOUNT_ID,
    }

    @pytest.fixture(scope="session")
    def response(self, client, config):
        url = f"/api/v1/accounts/ag-grid-insights-trend/"
        return client.post(url, json=self.post_data, headers=config["headers"])

    @pytest.fixture(scope="session")
    def response_json(self, response):
        data = response.data.decode("UTF-8")
        return json.loads(data)

    def test_status_code_200(self, response):
        assert response.status_code == 200

    def test_return_type_is_dict(self, response):
        data = response.data.decode("UTF-8")
        assert isinstance(json.loads(data), dict)

    def test_cpm_is_positive_float(self, response_json):
        assert "cpm" in response_json
        cpm = response_json.get("cpm")
        if cpm is not None:
            assert isinstance(cpm, float)
            assert cpm >= 0

    def test_percentage_difference_is_float(self, response_json):
        assert "percentage_difference" in response_json
        percentage_difference = response_json.get("percentage_difference")
        if percentage_difference is not None:
            assert isinstance(percentage_difference, float)

    def test_trend_is_non_empty_string(self, response_json):
        assert "trend" in response_json
        trend = response_json.get("trend")
        assert isinstance(trend, str)
        assert len(trend) > 0
