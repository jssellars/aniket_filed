import json
from enum import Enum

import pytest


class AdsManagerReportsBreakdownField(Enum):
    ACTION = "action"
    DELIVERY = "delivery"
    TIME = "time"
    COLUMN_NAME = "columnName"
    DISPLAY_NAME = "displayName"
    ID = "id"


class TestAdsManagerReportsBreakdown:
    @pytest.fixture(scope="session")
    def response(self, client, config):
        url = f"/api/v1/get-breakdowns"
        return client.get(url, headers=config["headers"])

    @pytest.fixture(scope="session")
    def response_json(self, response):
        data = response.data.decode("UTF-8")
        return json.loads(data)

    def test_status_code_200(self, response):
        assert response.status_code == 200

    def test_return_type_is_dict_of_len_3(self, response_json):
        assert isinstance(response_json, dict)
        assert len(response_json) == 3

    def test_action_is_non_empty_list(self, response_json):
        action_data = response_json.get(AdsManagerReportsBreakdownField.ACTION.value)
        assert isinstance(action_data, list)
        assert len(action_data) > 0

    def test_delivery_is_non_empty_list(self, response_json):
        delivery_data = response_json.get(AdsManagerReportsBreakdownField.DELIVERY.value)
        assert isinstance(delivery_data, list)
        assert len(delivery_data) > 0

    def test_time_is_non_empty_list(self, response_json):
        time_data = response_json.get(AdsManagerReportsBreakdownField.TIME.value)
        assert isinstance(time_data, list)
        assert len(time_data) > 0

    @pytest.fixture(scope="session")
    def all_data(self, response_json):
        data = (
            response_json.get(AdsManagerReportsBreakdownField.ACTION.value)
            + response_json.get(AdsManagerReportsBreakdownField.DELIVERY.value)
            + response_json.get(AdsManagerReportsBreakdownField.TIME.value)
        )
        return data

    def test_column_name_is_non_empty_string(self, all_data):
        for response in all_data:
            column_name = response.get(AdsManagerReportsBreakdownField.COLUMN_NAME.value)
            assert isinstance(column_name, str)
            assert len(column_name) > 0

    def test_display_name_is_non_empty_string(self, all_data):
        for response in all_data:
            display_name = response.get(AdsManagerReportsBreakdownField.DISPLAY_NAME.value)
            assert isinstance(display_name, str)
            assert len(display_name) > 0

    def test_id_is_int(self, all_data):
        for response in all_data:
            _id = response.get(AdsManagerReportsBreakdownField.ID.value)
            assert isinstance(_id, int)
