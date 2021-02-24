import pytest
import json


class TestTargetingSearchLanguages:
    @pytest.fixture(scope="session")
    def response(self, client, config):
        url = f"/api/v1/targeting-search/languages"
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

    def test_name_is_non_empty_string(self, response_json):
        for response in response_json:
            assert "name" in response
            name = response.get("name")
            assert isinstance(name, str)
            assert len(name) > 0

    def test_key_is_positive_int(self, response_json):
        for response in response_json:
            assert "key" in response
            key = response.get("key")
            assert isinstance(key, int)
            assert key > 0
