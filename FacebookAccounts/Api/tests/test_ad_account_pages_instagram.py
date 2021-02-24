import pytest
import json


class TestAdAccountPagesInstagram:

    @pytest.fixture(scope="session")
    def response(self, client, config):
        # The page id is hard coded in the url. Replace later with sandbox id
        url = f"/api/v1/page-instagram-account/1133228890105750"
        return client.get(url, headers=config['headers'])

    @pytest.fixture(scope="session")
    def response_json(self, response):
        data = response.data.decode("UTF-8")
        return json.loads(data)

    def test_status_code_200(self, response):
        assert response.status_code == 200

    def test_return_type_is_list(self, response_json):
        assert isinstance(response_json, list)

    def test_data_in_list_is_dict_with_len_two(self, response_json):
        for data in response_json:
            assert isinstance(data, dict)
            assert len(data) == 2

    def test_name_param_is_non_empty_string(self, response_json):
        for data in response_json:
            assert "username" in data
            name = data.get("username")
            assert isinstance(name, str)
            assert len(name) > 0

    def test_facebook_id_param_is_non_empty_numeric_string(self, response_json):
        for data in response_json:
            assert "id" in data
            facebook_id = data.get("id")
            assert isinstance(facebook_id, str)
            assert len(facebook_id) > 0
            assert facebook_id.isnumeric()
