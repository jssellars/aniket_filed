import pytest
import json
from enum import Enum


class TargetingSearchInterestsSearchField(Enum):
    ID = "id"
    NAME = "name"
    AUDIENCE_SIZE = "audienceSize"
    PATH = "path"
    TOPIC = "topic"
    TYPE = "type"
    DISAMBIGUATION_CATEGORY = "disambiguationCategory"


class TestTargetingSearchInterestsSearch:
    @pytest.fixture(scope="session", params=["romania"])
    def response(self, client, config, request):
        url = f"/api/v1/targeting-search/interests/search/{request.param}"
        return client.get(url, headers=config["headers"])

    @pytest.fixture(scope="session")
    def response_json(self, response):
        data = response.data.decode("UTF-8")
        return json.loads(data)

    def test_status_code_200(self, response):
        assert response.status_code == 200

    def test_return_type_is_list(self, response_json):
        assert isinstance(response_json, list)

    def test_data_in_list_is_non_empty_dict(self, response_json):
        for response in response_json:
            assert isinstance(response, dict)
            assert len(response) > 0

    def test_id_is_non_empty_numeric_string(self, response_json):
        for response in response_json:
            assert TargetingSearchInterestsSearchField.ID.value in response
            _id = response.get(TargetingSearchInterestsSearchField.ID.value)
            assert isinstance(_id, str)
            assert len(_id) > 0
            assert _id.isnumeric()

    def test_name_is_non_empty_string(self, response_json):
        for response in response_json:
            assert TargetingSearchInterestsSearchField.NAME.value in response
            name = response.get(TargetingSearchInterestsSearchField.NAME.value)
            assert isinstance(name, str)
            assert len(name) > 0

    def test_audience_size_is_positive_string(self, response_json):
        for response in response_json:
            assert TargetingSearchInterestsSearchField.AUDIENCE_SIZE.value in response
            audience_size = response.get(
                TargetingSearchInterestsSearchField.AUDIENCE_SIZE.value
            )
            assert isinstance(audience_size, int)
            assert audience_size > 0

    def test_path_is_non_empty_list(self, response_json):
        for response in response_json:
            assert TargetingSearchInterestsSearchField.PATH.value in response
            path = response.get(TargetingSearchInterestsSearchField.PATH.value)
            assert isinstance(path, list)
            assert len(path) > 0

    def test_data_in_path_is_string(self, response_json):
        for response in response_json:
            path = response.get(TargetingSearchInterestsSearchField.PATH.value)
            for item in path:
                assert isinstance(item, str)
                assert len(item) > 0

    def test_topic_is_non_empty_string(self, response_json):
        for response in response_json:
            topic = response.get(TargetingSearchInterestsSearchField.TOPIC.value)
            if topic:
                assert isinstance(topic, str)
                assert len(topic) > 0

    def test_type_is_non_empty_string(self, response_json):
        for response in response_json:
            assert TargetingSearchInterestsSearchField.TYPE.value in response
            _type = response.get(TargetingSearchInterestsSearchField.TYPE.value)
            assert isinstance(_type, str)
            assert _type == "interests"

    def test_disambiguation_category_is_non_empty_string(self, response_json):
        for response in response_json:
            disambiguation_category = response.get(
                TargetingSearchInterestsSearchField.DISAMBIGUATION_CATEGORY.value
            )
            if disambiguation_category:
                assert isinstance(disambiguation_category, str)
                assert len(disambiguation_category) > 0
