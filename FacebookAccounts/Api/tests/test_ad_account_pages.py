import pytest
import json


class TestAdAccountPages:

    @pytest.fixture(scope="session")
    def response(self, client, config):
        url = f"/api/v1/pages/{config['account_id']}"
        return client.get(url, headers=config['headers'])

    @pytest.fixture(scope="session")
    def response_json(self, response):
        data = response.data.decode("UTF-8")
        return json.loads(data)

    def test_status_code_200(self, response):
        assert response.status_code == 200

    def test_return_type_is_list(self, response):
        data = response.data.decode("UTF-8")
        assert isinstance(json.loads(data), list)

    def test_return_data_not_empty(self, response_json):
        assert len(response_json) > 0

    def test_data_in_list_is_dict(self, response_json):
        for response in response_json:
            assert isinstance(response, dict)

    def test_dict_in_list_has_length_two(self, response_json):
        for response in response_json:
            assert len(response) == 2

    def test_facebook_id_param_is_non_empty_numeric_string(self, response_json):
        for response in response_json:
            facebook_id = response.get("facebookId", None)
            assert len(facebook_id) > 0
            assert isinstance(facebook_id, str)
            assert facebook_id.isnumeric()

    def test_name_param_is_non_empty_string(self, response_json):
        for response in response_json:
            name = response.get("name", None)
            assert len(name) > 0
            assert isinstance(name, str)

