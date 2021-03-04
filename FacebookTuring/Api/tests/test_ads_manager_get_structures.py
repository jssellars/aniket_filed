import json
from enum import Enum

import pytest


class AdsManagerGetStructuresField(Enum):
    DISPLAY_NAME = "displayName"
    KEY = "key"


class TestAdsManagerGetStructures:
    @pytest.fixture(scope="session", params=["campaigns", "adsets", "ads"])
    def response(self, client, config, request):
        url = f"/api/v1/ads-manager/{request.param}/{config['account_id']}"
        return client.get(url, headers=config["headers"])

    @pytest.fixture(scope="session")
    def response_json(self, response):
        data = response.data.decode("UTF-8")
        return json.loads(data)

    def test_status_code_200(self, response):
        assert response.status_code == 200

    def test_return_type_is_list(self, response_json):
        assert isinstance(response_json, list)

    def test_data_in_list_is_dict_with_len_2(self, response_json):
        for response in response_json:
            assert isinstance(response, dict)
            assert len(response) == 2

    def test_key_is_non_empty_string(self, response_json):
        for response in response_json:
            assert AdsManagerGetStructuresField.KEY.value in response
            key = response.get(AdsManagerGetStructuresField.KEY.value)
            assert isinstance(key, str)
            assert len(key) > 0

    def test_name_is_non_empty_string(self, response_json):
        for response in response_json:
            assert AdsManagerGetStructuresField.DISPLAY_NAME.value in response
            display_name = response.get(AdsManagerGetStructuresField.DISPLAY_NAME.value)
            assert isinstance(display_name, str)
            assert len(display_name) > 0
