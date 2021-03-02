import json

import pytest

from Core.test_config import ACCOUNT_ID


class TestGetNumberOfPages:
    post_data = {"adAccountId": ACCOUNT_ID, "pageSize": 25}

    @pytest.fixture(scope="session")
    def response(self, client, config):
        url = f"/api/v1/recommendations-number-of-pages"
        return client.post(url, json=self.post_data, headers=config["headers"])

    @pytest.fixture(scope="session")
    def response_json(self, response):
        data = response.data.decode("UTF-8")
        return json.loads(data)

    def test_status_code_200(self, response):
        assert response.status_code == 200

    def test_return_type_is_dict_with_len_1(self, response_json):
        assert isinstance(response_json, dict)
        assert len(response_json) == 1

    def test_number_of_pages_is_positive_int(self, response_json):
        assert "numberOfPages" in response_json
        number_of_pages = response_json["numberOfPages"]
        assert isinstance(number_of_pages, int)
        assert number_of_pages >= 0
